# 04 — Dados e pipeline

## Fluxo

```
ONS Dados Abertos (S3, um parquet por ano)
        │  src/extract_ons.py — download em streaming, SHA-256, manifest.csv
        ▼
data/raw/CURVA_CARGA_{ano}.parquet          ← cópia fiel do ONS, versionada
        │  src/consolidate.py — unifica tipos entre anos e concatena
        ▼
data/consolidated/CURVA_CARGA_2017_2026.parquet   ← fato (versionada)
        │  src/quality_check.py — gera docs/05-qualidade.md
        ▼
powerbi/ (PBIP)  ← fato_curva_carga + dim_datas
```

`data/reference/anomalias.csv` é a tabela de anomalias, eventos e datas de calendário que afetam curvas típicas e extremos, mantida à mão a partir de [07-anomalias.md](07-anomalias.md) (dicionário das colunas lá).

`data/consolidated/dim_datas.parquet` é a dimensão de calendário (2017–2026), versionada, gerada por `build_dim_datas.py` a partir do intervalo de anos; todos os campos são calculados a partir da data:

| Grupo | Colunas | Convenção |
|---|---|---|
| Hierarquia | `Ano`, `Semestre`, `Trimestre`, `MesNumero`, `MesNome`, `MesAbrev`, `AnoMes`, `AnoMesOrdem`, `DiaMes`, `DiaAno` | — |
| Semana | `SemanaAno`, `AnoSemana` | ISO 8601 (segunda a domingo; 01/01/2021 é `2020-W53`) |
| Dia da semana | `DiaSemanaNumero` (1 = segunda … 7 = domingo), `DiaSemana`, `DiaSemanaAbrev`, `FimDeSemana` | — |
| Feriados | `Feriado` (Sim/Não), `NomeFeriado` | Feriados nacionais por lei; Consciência Negra a partir de 2024; Paixão de Cristo pela Páscoa |
| Pontos facultativos | `PontoFacultativo` | Carnaval (segunda e terça), Quarta-feira de Cinzas, Corpus Christi |
| Vésperas e recesso | `Vespera`, `Recesso` | `Vespera`: `Natal` (24/12), `Ano-Novo` (31/12), `-`. `Recesso`: Sim de 24/12 a 02/01 |
| Tipo de dia | `TipoDia` (Dia útil / Sábado / Domingo / Feriado), `DiaUtil` | Carnaval e Corpus Christi contam como `Feriado`; Quarta-feira de Cinzas é dia útil |
| Estação | `EstacaoAno`, `AnoBissexto` | Datas fixas do hemisfério sul |
| Metodologia | `RegimeMetodologico` | `Supervisão ONS` até 01/03/2021; `Carga global` até 28/04/2023; `Carga global + MMGD` depois |

Curvas típicas devem segmentar por `TipoDia` e, para dias úteis, excluir `Recesso = "Sim"` (24/12 a 02/01 se comportam como sábado — ver [07-anomalias.md](07-anomalias.md)).

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

## Dicionário da fato `CURVA_CARGA_2017_2026.parquet`

| Coluna | Tipo | Descrição oficial (ONS) | Observações nossas |
|---|---|---|---|
| `id_subsistema` | string | Código do Subsistema | `N`, `NE`, `S`, `SE`. **Chave** para subsistema |
| `nom_subsistema` | string | Nome do Subsistema | `NORTE`, `NORDESTE`, `SUL`, `SUDESTE` (até 2025) / `SUDESTE/CENTRO-OESTE` (2026+). Não usar como chave |
| `din_instante` | timestamp | Data de referência | Início da hora, hora padrão de Brasília, sem horário de verão. Um registro por hora cheia |
| `val_cargaenergiahomwmed` | double | Valor da Carga de Energia, em MWmed | Potência média demandada na hora. Numericamente igual à energia da hora em MWh. O dicionário não permite nulo, mas a hora inexistente do início do horário de verão (15/10/2017, 04/11/2018) vem vazia e é gravada como nulo (7 registros) |

Volume: 339.936 linhas (4 subsistemas × 84.984 horas) de 01/01/2017 00h a 11/09/2026 23h na extração de 13/09/2026. O número atualizado está sempre em [05-qualidade.md](05-qualidade.md).

## Transformações aplicadas

Apenas uma, em `consolidate.py`:

- **Unificação de tipo.** `val_cargaenergiahomwmed` vem como *string* nos arquivos de 2017 a 2024 e como *double* em 2025 e 2026. O consolidado converte tudo para `float64`; strings vazias viram nulo. Qualquer outra combinação de tipos entre anos interrompe o script com erro explícito, para que a decisão seja consciente.

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
- Regime metodológico: já disponível em `dim_datas[RegimeMetodologico]`.
- Rótulo único de subsistema derivado de `id_subsistema` — **ainda não existe**.
- Tabela `anomalias` importada de `data/reference/anomalias.csv`, relacionada à fato por data e subsistema, usada pelas medidas de curva típica e de máximos — **ainda não importada**.

O arquivo PBIP atual aponta para o caminho absoluto do consolidado na máquina do autor; ao clonar, ajuste a fonte no Power Query.

## Como reproduzir

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\extract_ons.py        # baixa data/raw (2017-2026)
python src\consolidate.py        # gera data/consolidated/CURVA_CARGA_2017_2026.parquet
python src\quality_check.py      # gera docs/05-qualidade.md (baixa a base diária para reconciliar)
```

Problemas comuns de instalação (PATH, certificados SSL corporativos) estão no [README](../README.md).
