# Anatomia da Demanda de Energia Elétrica Brasileira

Projeto de portfólio em análise e visualização de dados sobre a demanda elétrica brasileira, com entrega principal em Power BI.

Este README explica só o essencial para rodar os scripts de extração e consolidação de dados.

## Início rápido

Se você já tem Python instalado, no PowerShell, dentro da pasta do projeto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\extract_ons.py
python src\consolidate.py
```

Ao final, o dataset consolidado estará em `data\consolidated\CURVA_CARGA_{ano_inicial}_{ano_final}.parquet`. Se algo der errado, veja o passo a passo detalhado e a seção [Problemas comuns](#problemas-comuns) abaixo.

## Estrutura do projeto

```
.
├── data/
│   ├── raw/            # dados baixados do ONS, um arquivo por ano (não versionado)
│   └── consolidated/
│       ├── CURVA_CARGA_{ano_inicial}_{ano_final}.parquet   # não versionado
│       └── dim_datas.parquet   # dimensão de calendário, versionada
├── powerbi/             # arquivos do painel Power BI
├── src/
│   ├── extract_ons.py   # baixa a curva de carga horária do ONS (2019-2026)
│   └── consolidate.py   # une os parquets de data/raw em um único arquivo
└── requirements.txt
```

`data/consolidated/dim_datas.parquet` é a dimensão de datas (calendário) usada no modelo do Power BI — campos como ano, mês, trimestre, dia da semana, feriado, tipo de dia, estação do ano etc., cobrindo 2019-2026. Ela já vem pronta no repositório; o processo que a gera não faz parte deste projeto público.

## Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/) instalado (marque a opção "Add python.exe to PATH" no instalador do Windows).
- Conexão com a internet (o script baixa arquivos do ONS).

Para conferir se o Python está instalado, abra o PowerShell e rode:

```powershell
python --version
```

## Passo a passo

**1. Abra o PowerShell na pasta do projeto.**

**2. Crie o ambiente virtual** (isso cria uma pasta `.venv` isolada, só precisa fazer uma vez):

```powershell
python -m venv .venv
```

**3. Ative o ambiente virtual:**

```powershell
.venv\Scripts\Activate.ps1
```

O prompt do terminal deve passar a mostrar `(.venv)` no início da linha, indicando que está ativo.

> Se aparecer um erro de política de execução de scripts, rode primeiro:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**4. Instale as dependências do projeto:**

```powershell
python -m pip install -r requirements.txt
```

**5. Rode o script de extração:**

```powershell
python src\extract_ons.py
```

Os arquivos baixados vão aparecer em `data\raw`, junto com um `manifest.csv` que registra data da extração, tamanho e hash de cada arquivo.

**6. Rode o script de consolidação:**

```powershell
python src\consolidate.py
```

Ele une todos os arquivos de `data\raw` em um único arquivo em `data\consolidated\CURVA_CARGA_{ano_inicial}_{ano_final}.parquet`, já normalizando eventuais mudanças de tipo de coluna que o ONS tenha feito entre os anos.

**7. Quando terminar, para sair do ambiente virtual:**

```powershell
deactivate
```

Nas próximas vezes, não é preciso repetir o passo 2 (criar o venv) nem o 4 (instalar dependências) — só ativar (passo 3) e rodar os scripts (passos 5 e 6).

## Problemas comuns

- **`python` não é reconhecido como comando**: o Python não está no PATH. Reinstale marcando "Add python.exe to PATH", ou use o caminho completo do executável.
- **Erro de certificado SSL ao instalar dependências** (`CERTIFICATE_VERIFY_FAILED`): geralmente causado por antivírus/proxy corporativo que o Python não reconhece. Rode a instalação com:
  ```powershell
  python -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
  ```
- **Erro de certificado SSL ao rodar `extract_ons.py`** (mesmo erro `CERTIFICATE_VERIFY_FAILED`, mas ao baixar do ONS): o `requirements.txt` já inclui o pacote `pip-system-certs`, que resolve isso automaticamente fazendo o Python confiar nos mesmos certificados que o Windows confia — se ainda assim ocorrer, confirme que ele foi instalado (`pip show pip-system-certs`).
