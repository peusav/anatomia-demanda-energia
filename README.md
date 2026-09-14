# Anatomia da Demanda de Energia Elétrica Brasileira

> Mais importante do que saber **quanto** de energia o Brasil demanda é entender **quando** essa demanda acontece, **onde** ela se concentra e **como seu formato vem mudando**.

Projeto de portfólio em análise e visualização de dados, com entrega em Power BI, construído sobre a curva de carga horária do ONS (2017–2026) para os quatro subsistemas do Sistema Interligado Nacional.

## A pergunta

**Como o padrão da demanda de energia elétrica brasileira varia ao longo do tempo e entre subsistemas, e como seu formato vem mudando?**

O produto não é um painel de níveis de carga. É uma leitura do *formato* da demanda: como ela se distribui pelas 24 horas, como isso difere entre Norte, Nordeste, Sul e Sudeste/Centro-Oeste, e como mudou nos últimos anos — com as quebras metodológicas da série tratadas como parte da análise, não como nota de rodapé.

## Os dados em uma frase

Cada linha é a **carga média em MWmed** de um **subsistema** durante **uma hora**: 4 subsistemas × 24 horas × todos os dias desde 01/01/2017. Fonte única: [Curva de Carga Horária — ONS Dados Abertos](https://dados.ons.org.br/dataset/curva-carga), licença CC-BY.

Três cuidados que valem para qualquer número deste projeto:

- **Carga não é consumo.** É a demanda vista pelo sistema, não a energia faturada aos consumidores.
- **A definição de carga mudou** em 02/03/2021 (carga global) e em 29/04/2023 (inclusão da MMGD estimada). Comparações absolutas que atravessam essas datas exigem cautela; 2024–2025 é o núcleo comparável.
- **2026 é parcial.** Só se compara com o mesmo intervalo de datas dos anos anteriores.

## Documentação

| Documento | O que responde |
|---|---|
| [docs/01-projeto.md](docs/01-projeto.md) | Por que o projeto existe, perguntas, escopo, persona, janelas, princípios |
| [docs/02-dominio-e-glossario.md](docs/02-dominio-e-glossario.md) | SIN, subsistema, carga × consumo, MW/MWmed/MWh, curva, pico, vale, MMGD |
| [docs/03-metodologia.md](docs/03-metodologia.md) | Regimes metodológicos (texto oficial), YTD, dia típico, métricas, normalização, revisões |
| [docs/04-dados.md](docs/04-dados.md) | Pipeline, dicionário da fato, transformações, rastreabilidade |
| [docs/05-qualidade.md](docs/05-qualidade.md) | Diagnóstico de qualidade gerado pelo script (cobertura, gaps, anomalias, reconciliação) |
| [docs/06-decisoes.md](docs/06-decisoes.md) | Decisões analíticas e pendências |
| [docs/07-anomalias.md](docs/07-anomalias.md) | Cada anomalia sinalizada: dados, fontes externas, classificação e tratamento |
| [docs/fontes.md](docs/fontes.md) | Todas as fontes, com URL, instituição e data de acesso |
| [docs/eda/00-sintese.md](docs/eda/00-sintese.md) | Os cinco padrões que estruturam o dashboard, visuais por camada e medidas necessárias |
| [docs/eda/](docs/eda/) | Análise exploratória por bloco, com gráficos gerados por `src/eda/` |

## Estado atual

- [x] Extração e consolidação reproduzíveis, com manifest e hash
- [x] Diagnóstico de qualidade (339.936 registros, sem gaps, reconciliado com a base diária do ONS)
- [x] Camada conceitual e metodológica documentada
- [x] Anomalias e eventos investigados contra fontes externas (`data/reference/anomalias.csv`)
- [x] Dimensão de datas revisada: feriados calculados, pontos facultativos, vésperas e regime metodológico
- [x] Análise exploratória 2017–2026 — [síntese](docs/eda/00-sintese.md); blocos: [2 nível](docs/eda/02-nivel.md), [3 sazonalidade](docs/eda/03-sazonalidade.md), [4 ciclo intradiário](docs/eda/04-intradiario.md), [5–6 subsistemas e amplitude](docs/eda/05-06-subsistemas-amplitude.md), [7–8 normalização e mudança histórica](docs/eda/07-08-normalizacao-mudanca.md), [10 hipóteses externas](docs/eda/10-hipoteses.md), [11 hipóteses da literatura](docs/eda/11-hipoteses-literatura.md)
- [ ] Modelo e dashboard em Power BI
- [ ] Principais achados

## Estrutura

```
.
├── data/
│   ├── raw/             # parquets do ONS, um por ano + manifest.csv (versionados)
│   └── consolidated/    # CURVA_CARGA_2017_2026.parquet e dim_datas.parquet (versionados)
├── docs/                # documentação conceitual e metodológica
├── powerbi/             # projeto Power BI (PBIP)
├── src/
│   ├── extract_ons.py   # baixa a curva de carga horária do ONS
│   ├── consolidate.py   # une os anos em um único parquet
│   ├── quality_check.py # gera docs/05-qualidade.md
│   └── eda/             # scripts da análise exploratória, um por bloco
└── requirements.txt
```

## Como rodar

Requer [Python 3.11+](https://www.python.org/downloads/) e internet. No PowerShell, dentro da pasta do projeto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\extract_ons.py
python src\consolidate.py
python src\quality_check.py
```

Ao final, a fato estará em `data\consolidated\CURVA_CARGA_2017_2026.parquet` e o relatório de qualidade em `docs\05-qualidade.md`. O projeto Power BI em `powerbi\` aponta para a fato por caminho absoluto — ajuste a fonte no Power Query após clonar.

<details>
<summary>Problemas comuns</summary>

- **`python` não é reconhecido**: o Python não está no PATH. Reinstale marcando "Add python.exe to PATH".
- **Erro de política de execução ao ativar o venv**: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- **`CERTIFICATE_VERIFY_FAILED` ao instalar dependências** (antivírus/proxy corporativo):
  `python -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org`
- **`CERTIFICATE_VERIFY_FAILED` ao baixar do ONS**: o `requirements.txt` inclui `pip-system-certs`, que faz o Python confiar nos certificados do Windows. Confirme com `pip show pip-system-certs`.

</details>

## Licença dos dados

Dados do ONS sob [Creative Commons Atribuição (CC-BY)](http://opendefinition.org/od/2.1/pt-br). Os arquivos em `data/raw` são cópias fiéis; a única alteração no consolidado é a unificação do tipo numérico entre anos, descrita em [docs/04-dados.md](docs/04-dados.md).
