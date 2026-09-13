# Diagnóstico de qualidade — Curva de Carga Horária

> Gerado automaticamente por `src/quality_check.py` em 13/09/2026 17:18. Não edite à mão; rode o script novamente após uma nova extração.

## Resumo

| Item | Valor |
|---|---|
| Arquivo | `data/consolidated/CURVA_CARGA_2019_2026.parquet` |
| Última extração (manifest, UTC) | 2026-09-13T20:17:52.499258+00:00 |
| Registros | 269.856 |
| Período | 01/01/2019 00h → 11/09/2026 23h |
| Último dia com dados | 11/09/2026 (corte para comparações YTD) |
| Duplicidades (subsistema, instante) | 0 |
| Dias com quantidade de horas ≠ 24 | 0 |
| Valores nulos / negativos / zero | 0 / 0 / 0 |

## 1. Cobertura por ano e subsistema

| Ano | Esperado (dias×24) | N | NE | S | SE | Situação |
|---|---|---|---|---|---|---|
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
| N | 2019-01-01 00h | 2026-09-11 23h | 67464 | 0 | 0 | - |
| NE | 2019-01-01 00h | 2026-09-11 23h | 67464 | 0 | 0 | - |
| S | 2019-01-01 00h | 2026-09-11 23h | 67464 | 0 | 0 | - |
| SE | 2019-01-01 00h | 2026-09-11 23h | 67464 | 0 | 0 | - |

## 3. Horas por dia

Distribuição de registros por (subsistema, dia): 24 horas → 11244 dias.

Nenhum dia irregular. A série é publicada em hora padrão, sem ajuste de horário de verão (o fim do horário de verão em 17/02/2019 não gerou dia de 25 horas).

## 4. Faixas de valor (MWmed)

| Subsistema | Mínimo | P1 | Mediana | P99 | Máximo |
|---|---|---|---|---|---|
| N | 1364 | 4637 | 6577 | 9707 | 11196 |
| NE | 7262 | 8382 | 11825 | 15397 | 18157 |
| S | 5756 | 7336 | 12499 | 19015 | 22737 |
| SE | 21658 | 26837 | 40727 | 55400 | 62150 |

Duplicidades: 0

## 5. Saltos hora a hora

Variações abruptas entre horas consecutivas. Não são necessariamente erro — podem ser eventos operacionais reais — mas merecem investigação antes de compor curvas típicas.

| Subsistema | Saltos > 25% hora a hora | Meses (quantidade) |
|---|---|---|
| N | 17 | 2020-04 (10), 2023-08 (6), 2024-11 (1) |
| NE | 1 | 2021-12 (1) |
| S | 7 | 2020-07 (1), 2020-08 (3), 2022-09 (1), 2025-08 (1), 2026-05 (1) |
| SE | 0 | - |

## 6. Grafias de subsistema

O dicionário de dados do ONS (v1.2, 06/04/2026) informa que o nome abreviado do subsistema foi substituído pela descrição completa. Use `id_subsistema` como chave e um rótulo único no modelo.

| id_subsistema | nom_subsistema | De | Até |
|---|---|---|---|
| N | NORTE | 2019-01-01 | 2026-09-11 |
| NE | NORDESTE | 2019-01-01 | 2026-09-11 |
| S | SUL | 2019-01-01 | 2026-09-11 |
| SE | SUDESTE | 2019-01-01 | 2025-12-31 |
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

A base diária do ONS deve ser igual à média das 24 horas da curva horária. Diferenças acima da tolerância indicam **revisão posterior** de um dos arquivos pelo ONS (processo de consistência recorrente), e não erro de agregação.

| Ano | Linhas na diária | Dias comparados | Dias com dif. > 0.50% | Maior diferença |
|---|---|---|---|---|
| 2019 | 1460 | 1460 | 0 | 0.00% em N 2019-04-27 (diária 5320 × horária 5320) |
| 2020 | 1464 | 1464 | 0 | 0.00% em N 2020-04-11 (diária 4864 × horária 4864) |
| 2021 | 1460 | 1460 | 0 | 0.00% em N 2021-01-24 (diária 5375 × horária 5375) |
| 2022 | 1460 | 1460 | 0 | 0.00% em N 2022-01-22 (diária 5745 × horária 5745) |
| 2023 | 1460 | 1460 | 0 | 0.00% em N 2023-04-23 (diária 6393 × horária 6393) |
| 2024 | 1464 | 1464 | 0 | 0.00% em N 2024-03-22 (diária 7337 × horária 7337) |
| 2025 | 1460 | 1460 | 0 | 0.00% em N 2025-02-02 (diária 7130 × horária 7130) |
| 2026 | 1016 | 1016 | 0 | 0.00% em S 2026-04-18 (diária 13285 × horária 13285) |
