"""file_bridge_automation.py – Automação de cópia/cola guiada por planilha
----------------------------------------------------------------------
Este script torna um computador “ponte” entre múltiplos caminhos de origem e
 destino listados em uma planilha (CSV ou XLSX) com **duas colunas** obrigatórias
: COPIAR (origem) e COLAR (destino).

Fluxo de cada linha:
1. Abre caminho **COPIAR** via Win+R.
   • Se o valor apontar para um arquivo → `explorer.exe /select,"arquivo"`.
   • Se apontar para pasta          → `explorer "pasta"` e depois Ctrl+A.
2. Copia (Ctrl+C).
3. Abre caminho **COLAR** via Win+R (`explorer "destino"`).
4. Cola (Ctrl+V).
5. Fecha as janelas abertas.

O script detecta‑e‑preenche pop‑ups de credenciais (Credenciais de Rede / UAC)
com USERNAME e PASSWORD fornecidos pelo diálogo ou `.env`.

Dependências:
```
pip install pyautogui pygetwindow python-dotenv pandas openpyxl
```
"""

import os
import time
import csv
from pathlib import Path

import pyautogui as pg
import pygetwindow as gw
from dotenv import load_dotenv
import pandas as pd

import tkinter as tk
from tkinter import simpledialog

# ------------- Configurações globais -------------
pg.PAUSE = 0.15
pg.FAILSAFE = True
load_dotenv()

def is_file_path(path: str) -> bool:
    return Path(path).suffix != ""

# ------------- Diálogos de entrada -------------
root = tk.Tk(); root.withdraw()

sheet_path = simpledialog.askstring(
    title="Planilha de caminhos",
    prompt="Informe o caminho da planilha (.csv ou .xlsx) com colunas COPIAR e COLAR:",
    initialvalue=os.getenv("SHEET_PATH", "")
)

user_input = simpledialog.askstring(
    title="Usuário (opcional)",
    prompt="Usuário para Credenciais de Rede/UAC:",
    initialvalue=os.getenv("USERNAME", "")
)

pass_input = simpledialog.askstring(
    title="Senha (opcional)",
    prompt="Senha correspondente:",
    show="*",
    initialvalue=os.getenv("PASSWORD", "")
)
root.destroy()

USERNAME = user_input or os.getenv("USERNAME", "")
PASSWORD = pass_input or os.getenv("PASSWORD", "")

if not sheet_path:
    raise FileNotFoundError("Caminho da planilha não fornecido.")

# ----------- Carrega a planilha -----------
if sheet_path.lower().endswith(".csv"):
    df = pd.read_csv(sheet_path, dtype=str)
else:
    df = pd.read_excel(sheet_path, dtype=str)

required_cols = {"COPIAR", "COLAR"}
if not required_cols.issubset(df.columns.str.upper()):
    raise ValueError("Planilha deve ter colunas COPIAR e COLAR.")

# Normaliza nomes das colunas para maiúsculo
    df.columns = [str(c).upper() for c in df.columns]
    required_cols = {"COPIAR", "COLAR"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError("Planilha deve ter colunas COPIAR e COLAR.")
    df = df.dropna(subset=["COPIAR", "COLAR"]).reset_index(drop=True)

# ----------- Funções de automação -----------

def login_popup():
    if not USERNAME or not PASSWORD:
        return
    titles = [
        "Segurança do Windows", "Windows Security", "Credenciais de Rede",
        "Network Credentials", "Controle de Conta de Usuário", "User Account Control"
    ]
    for _ in range(60):  # ~9 s
        for t in titles:
            wins = gw.getWindowsWithTitle(t)
            if wins:
                pg.write(USERNAME)
                pg.press("tab")
                pg.write(PASSWORD)
                pg.press("enter")
                time.sleep(1.5)
                return
        time.sleep(0.15)


def open_run_command(cmd: str):
    pg.hotkey("winleft", "r")
    time.sleep(0.4)
    pg.write(cmd, interval=0.02)
    pg.press("enter")
    time.sleep(2)
    return gw.getActiveWindow()


def open_path(path: str):
    if is_file_path(path):
        cmd = f'explorer.exe /select,"{path}"'
        win = open_run_command(cmd)
    else:
        cmd = f'explorer "{path}"'
        win = open_run_command(cmd)
        pg.hotkey("ctrl", "a")  # seleciona tudo se for pasta
    login_popup()
    return win


def copy_selection():
    pg.hotkey("ctrl", "c")
    time.sleep(0.5)


def paste_in_folder():
    pg.hotkey("ctrl", "v")
    time.sleep(5)


def close_window(win):
    win.activate()
    pg.hotkey("alt", "f4")
    time.sleep(0.3)

# ------------- Loop principal -------------

def main():
    for idx, row in df.iterrows():
        src = row["COPIAR"].strip()
        dst = row["COLAR"].strip()
        if not src or not dst:
            continue
        print(f"[{idx+1}/{len(df)}] Copiando de {src} para {dst}…")

        # Abre origem e copia
        win_src = open_path(src)
        copy_selection()

        # Abre destino e cola
        win_dst = open_path(dst)
        paste_in_folder()

        # Fecha janelas
        close_window(win_dst)
        close_window(win_src)

    print("✔️ Todos os caminhos processados com sucesso.")


if __name__ == "__main__":
    main()
