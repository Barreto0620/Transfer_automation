"""file_bridge_automation.py – Automação ponte guiada por planilha
----------------------------------------------------------------
► Planilha (CSV ou XLSX) com colunas **COPIAR**, **COLAR**, opcional **STATUS**.
► Pula linhas já marcadas **OK** e prossegue.
► Copia/cola via teclado, aceita “Substituir” e atualiza STATUS.
► Mostra resumo em mensagem pop‑up **e** grava em arquivo *transfer_log.txt* no mesmo diretório da planilha.
► Fecha Explorers somente após concluir tudo.

Dependências
```
pip install pyautogui pygetwindow python-dotenv pandas openpyxl
```
"""

import os
import sys
import time
from pathlib import Path
import logging

import pyautogui as pg
import pygetwindow as gw
from dotenv import load_dotenv
import pandas as pd

import tkinter as tk
from tkinter import simpledialog, messagebox

# ------------- Configurações globais -------------
pg.PAUSE = 0.15
pg.FAILSAFE = True
load_dotenv()

# ---------------- Utilitários -------------------

def is_file(path: str) -> bool:
    return Path(path).suffix != ""


def login_popup(username: str, password: str):
    if not username or not password:
        return
    titles = [
        "Segurança do Windows", "Windows Security", "Credenciais de Rede",
        "Network Credentials", "Controle de Conta de Usuário", "User Account Control",
    ]
    for _ in range(60):
        for t in titles:
            if gw.getWindowsWithTitle(t):
                pg.write(username)
                pg.press("tab")
                pg.write(password)
                pg.press("enter")
                time.sleep(1.5)
                return
        time.sleep(0.15)


def run_command(cmd: str):
    pg.hotkey("winleft", "r")
    time.sleep(0.4)
    pg.write(cmd, interval=0.02)
    pg.press("enter")
    time.sleep(2)
    return gw.getActiveWindow()


def open_path(path: str, username: str, password: str):
    if is_file(path):
        win = run_command(f'explorer.exe /select,"{path}"')
    else:
        win = run_command(f'explorer "{path}"')
        pg.hotkey("ctrl", "a")
    login_popup(username, password)
    return win


def copy_selection(is_folder: bool):
    if is_folder:
        pg.hotkey("ctrl", "a")
    pg.hotkey("ctrl", "c")
    time.sleep(0.5)


def handle_replace_dialog():
    titles = ["Substituir ou Ignorar Arquivos", "Replace or Skip Files"]
    for _ in range(50):
        for t in titles:
            if gw.getWindowsWithTitle(t):
                pg.press("enter")
                time.sleep(0.5)
                return
        time.sleep(0.15)


def paste_in_folder():
    pg.hotkey("ctrl", "v")
    time.sleep(0.5)
    handle_replace_dialog()
    time.sleep(4)


def close_window(win):
    try:
        win.activate()
        pg.hotkey("alt", "f4")
        time.sleep(0.3)
    except Exception:
        pass

# ------------- Diálogos de entrada -------------
# ------------- Diálogos de entrada -------------
root = tk.Tk(); root.withdraw()

sheet_path = simpledialog.askstring(
    title="Planilha de caminhos",
    prompt="Informe o caminho da planilha (.csv ou .xlsx):",
    initialvalue=os.getenv("SHEET_PATH", "")
)
sheet_path = sheet_path.strip('"') if sheet_path else None  # <-- LINHA CRUCIAL

username = simpledialog.askstring(
    title="Usuário (opcional)",
    prompt="Usuário para Credenciais de Rede/UAC:",
    initialvalue=os.getenv("USERNAME", "")
)

password = simpledialog.askstring(
    title="Senha (opcional)",
    prompt="Senha correspondente:",
    show="*",
    initialvalue=os.getenv("PASSWORD", "")
)
root.destroy()

# ------------- Logging -------------
log_file = Path(sheet_path).with_name("transfer_log.txt")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)
console = logging.getLogger()
console.addHandler(logging.StreamHandler(sys.stdout))

# ------------- Carrega planilha -------------
if sheet_path.lower().endswith(".csv"):
    df = pd.read_csv(sheet_path, dtype=str)
    def write_back(frame):
        frame.to_csv(sheet_path, index=False)
else:
    df = pd.read_excel(sheet_path, dtype=str, engine="openpyxl")
    def write_back(frame):
        frame.to_excel(sheet_path, index=False, engine="openpyxl")

# Normaliza colunas
df.columns = [str(c).upper() for c in df.columns]
if "STATUS" not in df.columns:
    df["STATUS"] = ""

required = {"COPIAR", "COLAR"}
if not required.issubset(set(df.columns)):
    sys.exit("❌ Planilha precisa das colunas COPIAR e COLAR.")

df = df.dropna(subset=["COPIAR", "COLAR"]).reset_index(drop=True)

# ------------- Loop principal -------------
start = time.perf_counter()
processed = skipped = errors = 0
explorer_windows = []

def remember(win):
    if win not in explorer_windows:
        explorer_windows.append(win)

for i, row in df.iterrows():
    status_now = str(row.get("STATUS", "")).strip().upper()
    if status_now == "OK":
        logging.info(f"[SKIP] Linha {i+1} já OK – pulando…")
        skipped += 1
        continue

    src = row["COPIAR"].strip()
    dst = row["COLAR"].strip()
    try:
        logging.info(f"[{i+1}/{len(df)}] Copiando {src} → {dst}")
        win_src = open_path(src, username, password); remember(win_src)
        copy_selection(not is_file(src))
        win_dst = open_path(dst, username, password); remember(win_dst)
        paste_in_folder()
        df.at[i, "STATUS"] = "OK"
        processed += 1
    except Exception as e:
        logging.error(f"Linha {i+1} erro: {e}")
        df.at[i, "STATUS"] = "ERRO"
        errors += 1

# ------------- Salva e encerra -------------
write_back(df)

for w in reversed(explorer_windows):
    close_window(w)

elapsed = time.perf_counter() - start
summary = (
    f"\n" +
    f"Resumo: {processed} processadas, {skipped} puladas, {errors} erro(s).\n" +
    f"Concluído em {elapsed:.1f} segundos. Planilha e log atualizados."
)
logging.info(summary.replace("\n", " | "))  # em uma linha no arquivo
print(summary)

# Pop‑up de conclusão
messagebox.showinfo("Transferência concluída", summary)

if __name__ == "__main__":
    pass
