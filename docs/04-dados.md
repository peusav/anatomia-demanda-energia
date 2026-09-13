# 04 — Dados e pipeline

## Fluxo

```
ONS Dados Abertos (S3, um parquet por ano)
        │  src/extract_ons.py — download em streaming, SHA-256, manifest.csv
        ▼
data/raw/CURVA_CARGA_{ano}.parquet          ← cópia fiel do ONS, versionada
        │  src/consolidate.py — unifica tipos entre anos e concatena
        ▼
data/consolidated/CURVA_CARGA_2019_2026.parquet   ← fato (versionada)
        │  src/quality_check.py — gera docs/05-qualidade.md
        ▼
powerbi/ (PBIP)  ← fato_curva_carga + dim_datas
```

`data/consolidated/dim_datas.parquet` é a dimensão de calendário (2019–2026), pronta e versionada. Cobre ano, semestre, trimestre, mês, semana, dia da semana, fim de semana, feriado e nome do feriado, tipo de dia (Dia útil / Sábado / Domingo / Feriado), estação do ano e ano bissexto.

## Fonte

| | |
|---|---|
| Dataset | Curva de Carga Horária — ONS Dados Abertos |
| Página | https://dados.ons.org.br/dataset/curva-carga |
| Arquivos | `https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/curva-carga-ho/CURVA_CARGA_{ano}.parquet` |
| Formatos disponíveis | CSV, XLSX, Parquet (usamos Parquet) |
| Atualização pelo ONS | Diária, 12h e 19h |
| Licença | CC-BY (atribuição ao ONS; informar alterações) |
| Dicionário oficial | [PDF](https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/curva-carga-ho/DicionarioDados_CurvaCarga.pdf) · [JSON](https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/curva-carga-ho/DicionarioDados_CurvaCarga.json) — v1.2, 06/04/2026 |

## Dicionário da fato `CURVA_CARGA_2019_2026.parquet`

| Coluna | Tipo | Descrição oficial (ONS) | Observações nossas |
|---|---|---|---|
| `id_subsistema` | string | Código do Subsistema | `N`, `NE`, `S`, `SE`. **Chave** para subsistema |
| `nom_subsistema` | string | Nome do Subsistema | `NORTE`, `NORDESTE`, `SUL`, `SUDESTE` (até 2025) / `SUDESTE/CENTRO-OESTE` (2026+). Não usar como chave |
| `din_instante` | timestamp | Data de referência | Início da hora, hora padrão de Brasília, sem horário de verão. Um registro por hora cheia |
| `val_cargaenergiahomwmed` | double | Valor da Carga de Energia, em MWmed | Potência média demandada na hora. Numericamente igual à energia da hora em MWh. Nulo/negativo não permitidos, zero permitido (dicionário) |

Volume: 269.856 linhas (4 subsistemas × 67.464 horas) de 01/01/2019 00h a 11/09/2026 23h na extração de 13/09/2026. O número atualizado está sempre em [05-qualidade.md](05-qualidade.md).

## Transformações aplicadas

Apenas uma, em `consolidate.py`:

- **Unificação de tipo.** `val_cargaenergiahomwmed` vem como *string* nos arquivos de 2019 a 2024 e como *double* em 2025 e 2026. O consolidado converte tudo para `float64`. Qualquer outra combinação de tipos entre anos interrompe o script com erro explícito, para que a decisão seja consciente.

Nada é filtrado, agregado, renomeado ou recalculado. O consolidado é a união fiel dos arquivos do ONS.

## Rastreabilidade

`data/raw/manifest.csv` registra, a cada execução de `extract_ons.py`: timestamp UTC, ano, arquivo, URL, tamanho e SHA-256. Se o hash de um ano mudar entre execuções, o script imprime `ATUALIZADO PELO ONS` — sinal de revisão retroativa (ver [03-metodologia.md](03-metodologia.md), §7).

## Bases auxiliares

| Base | Uso | Onde fica |
|---|---|---|
| Carga de Energia Diária (ONS) | Reconciliação da curva horária no `quality_check.py` | `data/external/carga_diaria/` (baixada sob demanda, não versionada) |

## O que o modelo Power BI espera

- `fato_curva_carga` ← consolidado, com relacionamento para `dim_datas` pela data de `din_instante`.
- Uma pequena dimensão de hora (0–23, rótulo, período do dia, ordem) **ainda não existe** — está prevista após a exploração.
- Coluna ou medida de regime metodológico (`Supervisão ONS` / `Carga global` / `Carga global + MMGD`) derivada de `din_instante` — **ainda não existe**.
- Rótulo único de subsistema derivado de `id_subsistema` — **ainda não existe**.

O arquivo PBIP atual aponta para o caminho absoluto do consolidado na máquina do autor; ao clonar, ajuste a fonte no Power Query.

## Como reproduzir

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\extract_ons.py        # baixa data/raw
python src\consolidate.py        # gera data/consolidated/CURVA_CARGA_2019_2026.parquet
python src\quality_check.py      # gera docs/05-qualidade.md (baixa a base diária para reconciliar)
```

Problemas comuns de instalação (PATH, certificados SSL corporativos) estão no [README](../README.md).
