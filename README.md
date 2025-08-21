# 🤖 Transfer Automation - Automação de Transferência de Arquivos

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-WebCash--inc-black.svg?style=for-the-badge&logo=github)](https://github.com/WebCash-inc)
[![Documentation](https://img.shields.io/badge/Docs-Online-brightgreen?style=for-the-badge)](https://webcash-inc.github.io/transfer-automation/)

## 🎯 Visão Geral

O **Transfer Automation** é uma ferramenta avançada de automação que permite transferir arquivos e pastas automaticamente usando uma planilha como guia de instruções. O sistema simula interações humanas com a interface gráfica do Windows, executando operações de copiar e colar de forma inteligente e autônoma.

### 🌟 Principais Funcionalidades

- **🔄 Automação Completa**: Executa transferências baseadas em planilhas Excel/CSV
- **🖱️ Simulação de UI**: Imita ações de mouse e teclado humanas
- **🛡️ Tratamento de Diálogos**: Lida automaticamente com pop-ups do sistema
- **📊 Logging Detalhado**: Registro completo de todas as operações
- **🌐 Suporte à Rede**: Autenticação automática em unidades de rede
- **📈 Relatórios Inteligentes**: Resumos de execução e estatísticas

## 🎥 Demonstração

[![Demonstração Transfer Automation](https://img.youtube.com/vi/wk62Oqq6JTs/0.jpg)](https://www.youtube.com/watch?v=wk62Oqq6JTs)

> 📺 **Assista ao vídeo**: [Managed File Transfer Automation Isn't as Complex as You Think](https://www.youtube.com/watch?v=wk62Oqq6JTs)

## 🏗️ Arquitetura do Sistema

O projeto é estruturado em 6 componentes principais:

```
📦 Transfer Automation
├── 🎹 Interactive User Input          # Interface de entrada de dados
├── 🎼 Transfer Workflow Orchestrator  # Gerenciamento do fluxo principal
├── 📊 Spreadsheet Data Manager       # Manipulação de planilhas
├── 🤖 UI Automation Engine           # Automação da interface gráfica
├── 🪟 Windows Dialog Handler         # Tratamento de pop-ups
└── 📝 Operational Logging & Reporting # Sistema de logs e relatórios
```

## 📋 Pré-requisitos

### Sistema Operacional
- **Windows 10/11** (obrigatório para automação de UI)

### Python
```bash
Python 3.8+ (recomendado 3.10+)
```

### Dependências Principais
- `pandas` - Manipulação de planilhas
- `openpyxl` - Suporte a arquivos Excel
- `pyautogui` - Automação de interface gráfica
- `pygetwindow` - Gerenciamento de janelas
- `tkinter` - Interface gráfica (incluído no Python)

## 🚀 Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/WebCash-inc/TRANSFER_AUTOMATION.git
cd TRANSFER_AUTOMATION
```

### 2. Crie um Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac (se aplicável para desenvolvimento)
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Estrutura de Arquivos
```
TRANSFER_AUTOMATION/
├── main.py                    # Script principal
├── requirements.txt           # Dependências Python
├── README.md                 # Este arquivo
├── SECURITY.md              # Políticas de segurança
├── transfer_log.txt         # Arquivo de log gerado
├── users_transfer.xlsx      # Planilha de exemplo/template
└── documentation/           # Documentação completa
    ├── index.html          # Documentação web
    ├── style.css          # Estilos da documentação
    ├── script.js          # Scripts da documentação
    └── img/               # Imagens da documentação
        └── logo_webcash.png
```

## 📊 Preparação da Planilha

### Formato Obrigatório
Sua planilha deve conter as seguintes colunas:

| COPIAR | COLAR | STATUS |
|--------|-------|--------|
| C:\Origem\arquivo.txt | D:\Destino\ | |
| \\Servidor\pasta\ | C:\Local\backup\ | OK |
| E:\Dados\importante.xlsx | \\Rede\compartilhado\ | |

### Colunas Obrigatórias
- **COPIAR**: Caminho completo do arquivo/pasta de origem
- **COLAR**: Caminho completo da pasta de destino
- **STATUS**: Coluna de controle (preenchida automaticamente)

### Formatos Suportados
- `.xlsx` (Excel)
- `.csv` (Valores Separados por Vírgula)

## ▶️ Como Executar

### 1. Execução Básica
```bash
python main.py
```

### 2. Fluxo de Execução
1. **📁 Seleção da Planilha**: Janela pop-up solicitará o caminho
2. **🔐 Credenciais** (opcional): Usuário e senha para redes
3. **🚀 Processamento**: Automação executa as transferências
4. **📊 Relatório**: Resumo final com estatísticas

### 3. Exemplo de Execução
```bash
C:\TRANSFER_AUTOMATION> python main.py

# Pop-ups aparecerão solicitando:
# 1. Caminho da planilha: C:\dados\minhas_transferencias.xlsx
# 2. Usuário de rede: meu_usuario (opcional)
# 3. Senha de rede: ********* (opcional)

# Execução automática iniciará...
```

## 🛠️ Configurações Avançadas

### Configurações de Segurança
No início do `main.py`:
```python
import pyautogui

# Configurações de segurança
pyautogui.PAUSE = 0.15      # Pausa entre ações
pyautogui.FAILSAFE = True   # Mover mouse para canto = parada de emergência
```

### Personalização de Timeouts
```python
# Ajustar tempos de espera conforme necessário
time.sleep(2)  # Aguardar abertura de janelas
time.sleep(4)  # Aguardar conclusão de operações
```

## 📝 Sistema de Logs

### Localização dos Logs
Os logs são salvos automaticamente como `transfer_log.txt` na mesma pasta da planilha.

### Exemplo de Log
```
2025-01-20 14:30:15 - [1/5] Copiando C:\Documentos\relatorio.pdf → D:\Backup\
2025-01-20 14:30:28 - [SKIP] Linha 2 já OK – pulando...
2025-01-20 14:30:30 - [3/5] Copiando \\Servidor\dados\ → C:\Local\
2025-01-20 14:30:45 - Resumo: 3 processadas, 1 puladas, 0 erro(s) | Concluído em 30.2 segundos
```

## 🔧 Tratamento de Erros

### Diálogos Suportados
- **"Substituir ou Ignorar Arquivos"**: Automático (substitui)
- **"Segurança do Windows"**: Login automático com credenciais
- **"Credenciais de Rede"**: Autenticação transparente

### Estados de STATUS
- **Vazio**: Aguardando processamento
- **OK**: Transferência concluída com sucesso
- **ERRO**: Falha na transferência (verifique logs)

## ⚠️ Limitações e Considerações

### Limitações Técnicas
- **Windows Only**: Funciona apenas em sistemas Windows
- **Interface Gráfica**: Requer ambiente desktop (não funciona via SSH)
- **Resolução de Tela**: Pode necessitar ajustes em resoluções diferentes

### Boas Práticas
- **Teste Pequeno**: Execute primeiro com poucos arquivos
- **Backup**: Sempre mantenha backup dos dados originais
- **Monitoramento**: Acompanhe os logs durante execução
- **Rede Estável**: Certifique-se de conectividade estável

## 🐛 Solução de Problemas

### Problemas Comuns

#### 1. "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas openpyxl
```

#### 2. Automação não funciona
- Verifique se está executando em ambiente desktop
- Certifique-se de que não há outras janelas interferindo
- Teste com `pyautogui.PAUSE = 1.0` (mais lento, mais estável)

#### 3. Falha em diálogos de rede
- Verifique credenciais de usuário e senha
- Teste acesso manual às pastas de rede primeiro
- Confirme que usuário tem permissões adequadas

### Modo Debug
Para debugging, adicione prints adicionais:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um **Pull Request**

### Diretrizes
- Mantenha o código limpo e documentado
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Siga as convenções de código Python (PEP 8)

## 📄 Licença

Este projeto é distribuído sob a Licença MIT. Veja o arquivo [LICENSE]() para mais detalhes.

## 📚 Documentação Completa

Para documentação detalhada de cada componente:

🌐 **[Acesse a documentação completa online](https://transferautomation.netlify.app/)**

### Capítulos Disponíveis
- **Capítulo 1**: Interactive User Input
- **Capítulo 2**: Transfer Workflow Orchestrator  
- **Capítulo 3**: Spreadsheet Data Manager
- **Capítulo 4**: UI Automation Engine
- **Capítulo 5**: Windows Dialog Handler
- **Capítulo 6**: Operational Logging & Reporting

## 👥 Equipe

Desenvolvido por **WebCash-inc**

- 🌐 GitHub: [@WebCash-inc](https://github.com/WebCash-inc)
- 📧 Suporte: Abra uma issue no GitHub
- 📖 Documentação: Consulte os arquivos em `documentation/`

## 🔄 Histórico de Versões

- **v1.0.0** - Versão inicial com funcionalidades básicas
- **v1.1.0** - Melhorias no tratamento de diálogos
- **v1.2.0** - Sistema de logging aprimorado
- **v1.3.0** - Documentação completa e interface web

## 🆘 Suporte

### Canais de Suporte
- **Issues GitHub**: Para bugs e solicitações de recursos
- **Discussões**: Para dúvidas gerais e compartilhamento de experiências
- **Documentação**: Consulte primeiro a documentação completa

### FAQ Rápido

**P: Funciona no Linux/Mac?**
R: Não, apenas Windows devido à automação de UI específica.

**P: Posso pausar a execução?**
R: Sim, mova o mouse para qualquer canto da tela (FAILSAFE ativo).

**P: Como processar milhares de arquivos?**
R: Execute em lotes menores e monitore o sistema regularmente.

---

⭐ **Se este projeto foi útil, deixe uma estrela no repositório!**

📢 **Compartilhe com sua equipe e ajude a automatizar mais processos!**
