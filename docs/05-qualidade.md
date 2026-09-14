# Diagnóstico de qualidade — Curva de Carga Horária

> Gerado automaticamente por `src/quality_check.py` em 13/09/2026 21:13. Não edite à mão; rode o script novamente após uma nova extração.

## Resumo

| Item | Valor |
|---|---|
| Arquivo | `data/consolidated/CURVA_CARGA_2017_2026.parquet` |
| Última extração (manifest, UTC) | 2026-09-14T00:07:50.229766+00:00 |
| Registros | 339.936 |
| Período | 01/01/2017 00h → 11/09/2026 23h |
| Último dia com dados | 11/09/2026 (corte para comparações YTD) |
| Duplicidades (subsistema, instante) | 0 |
| Dias com quantidade de horas ≠ 24 | 0 |
| Valores nulos / negativos / zero | 7 / 0 / 1 |

## 1. Cobertura por ano e subsistema

| Ano | Esperado (dias×24) | N | NE | S | SE | Situação |
|---|---|---|---|---|---|---|
| 2017 | 8760 | 8760 | 8760 | 8760 | 8760 | completo |
| 2018 | 8760 | 8760 | 8760 | 8760 | 8760 | completo |
| 2019 | 8760 | 8760 | 8760 | 8760 | 8760 | completo |
| 2020 | 8784 | 8784 | 8784 | 8784 | 8784 | completo |
| 2021 | 8760 | 8760 | 8760 | 8760 | 8760 | completo |
| 2022 | 8760 | 8760 | 8760 | 8760 | 8760 | completo |
| 2023 | 8760 | 8760 | 8760 | 8760 | 8760 | completo |
| 2024 | 8784 | 8784 | 8784 | 8784 | 8784 | completo |
| 2025 | 8760 | 8760 | 8760 | 8760 | 8760 | completo |
| 2026 | 8760 | 6096 | 6096 | 6096 | 6096 | parcial |

## 2. Continuidade horária

| Subsistema | Primeiro | Último | Registros | Fora da hora cheia | Gaps/saltos | Exemplos |
|---|---|---|---|---|---|---|
| N | 2017-01-01 00h | 2026-09-11 23h | 84984 | 0 | 0 | - |
| NE | 2017-01-01 00h | 2026-09-11 23h | 84984 | 0 | 0 | - |
| S | 2017-01-01 00h | 2026-09-11 23h | 84984 | 0 | 0 | - |
| SE | 2017-01-01 00h | 2026-09-11 23h | 84984 | 0 | 0 | - |

## 3. Horas por dia

Distribuição de registros por (subsistema, dia): 24 horas → 14164 dias.

Nenhum dia irregular. Atenção: a contagem não revela o horário de verão — os carimbos seguem a hora oficial de Brasília, e 01/01–16/02/2019 está em UTC−2 (ver docs/03-metodologia.md §1 e A8 em anomalias.csv).

## 4. Faixas de valor (MWmed)

| Subsistema | Mínimo | P1 | Mediana | P99 | Máximo |
|---|---|---|---|---|---|
| N | 842 | 4503 | 6112 | 9607 | 11196 |
| NE | 665 | 8246 | 11427 | 15323 | 18157 |
| S | 0 | 7096 | 12227 | 18740 | 22737 |
| SE | 21658 | 25982 | 39750 | 54927 | 62150 |

Duplicidades: 0

Nulos em: N 2017-10-15 00h, NE 2017-10-15 00h, S 2017-10-15 00h, SE 2017-10-15 00h, N 2018-11-04 00h, NE 2018-11-04 00h, SE 2018-11-04 00h. Zeros em: S 2018-11-04 00h. Nulos e zeros nas horas 0 de 15/10/2017 e 04/11/2018 correspondem à hora inexistente do início do horário de verão — ver A8/A9 em `anomalias.csv`.

## 5. Saltos hora a hora

Variações abruptas entre horas consecutivas que excedem a variação habitual do mesmo horário e dia da semana nas semanas vizinhas. Não são necessariamente erro — podem ser eventos operacionais reais — mas merecem investigação antes de compor curvas típicas. Cada uma está classificada em `07-anomalias.md`.

| Subsistema | Saltos > 25% além do habitual | Meses (quantidade) | Maior salto |
|---|---|---|---|
| N | 21 | 2018-03 (3), 2018-10 (1), 2020-04 (10), 2023-08 (6), 2024-11 (1) | 2018-03-21 17h: 842 → 2800 (+233%; habitual -4%) |
| NE | 10 | 2018-03 (6), 2018-08 (3), 2021-12 (1) | 2018-08-26 00h: 3321 → 9803 (+195%; habitual -3%) |
| S | 4 | 2018-06 (1), 2018-11 (1), 2025-08 (1), 2026-05 (1) | 2018-11-04 00h: 8631 → 0 (-100%; habitual -8%) |
| SE | 0 | - | - |

## 6. Grafias de subsistema

O dicionário de dados do ONS (v1.2, 06/04/2026) informa que o nome abreviado do subsistema foi substituído pela descrição completa. Use `id_subsistema` como chave e um rótulo único no modelo.

| id_subsistema | nom_subsistema | De | Até |
|---|---|---|---|
| N | NORTE | 2017-01-01 | 2026-09-11 |
| NE | NORDESTE | 2017-01-01 | 2026-09-11 |
| S | SUL | 2017-01-01 | 2026-09-11 |
| SE | SUDESTE | 2017-01-01 | 2025-12-31 |
| SE | SUDESTE/CENTRO-OESTE | 2026-01-01 | 2026-09-11 |

## 7. Sinais em torno dos marcos metodológicos

Média diária do SIN (soma dos quatro subsistemas) nos dias vizinhos a cada mudança de definição da carga. Um degrau visível aqui indica efeito de medição, não de demanda.

**02/03/2021 — Carga global: passa a incluir previsão de geração de usinas não despachadas**

| Data | Dia | SIN (MWmed) |  |
|---|---|---|---|
| 2021-02-27 | Sáb | 65877 |  |
| 2021-02-28 | Dom | 60035 |  |
| 2021-03-01 | Seg | 69699 |  |
| 2021-03-02 | Ter | 72986 |  ◀ marco |
| 2021-03-03 | Qua | 74408 |  |
| 2021-03-04 | Qui | 74485 |  |
| 2021-03-05 | Sex | 73573 |  |

**29/04/2023 — Passa a incorporar estimativa de MMGD (micro e minigeração distribuída)**

| Data | Dia | SIN (MWmed) |  |
|---|---|---|---|
| 2023-04-26 | Qua | 72621 |  |
| 2023-04-27 | Qui | 73881 |  |
| 2023-04-28 | Sex | 72889 |  |
| 2023-04-29 | Sáb | 68158 |  ◀ marco |
| 2023-04-30 | Dom | 62116 |  |
| 2023-05-01 | Seg | 62227 |  |
| 2023-05-02 | Ter | 73025 |  |

## 8. Reconciliação com a Carga de Energia Diária (ONS)

_Pulado (`--sem-diaria`)._
