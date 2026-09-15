# 08 — Modelo semântico (Power BI)

O modelo vive em `powerbi/anatomia-demanda-energia.SemanticModel/definition/` no formato TMDL (texto), editável no repositório e no Power BI Desktop. Esta página descreve o que ele contém e como validá-lo depois de editar o TMDL à mão.

## Parâmetro

`CaminhoProjeto` — pasta raiz do repositório, com barra final. Todas as fontes são `CaminhoProjeto & "data\..."`. Ao clonar em outra máquina, basta trocar o valor (Transformar dados → Gerenciar parâmetros).

## Tabelas

| Tabela | Fonte | Papel | Linhas |
|---|---|---|---|
| `fato_curva_carga` | `data/consolidated/CURVA_CARGA_2017_2026.parquet` | Fato horária. Além das 4 colunas do ONS, ganha no Power Query `Data`, `Hora`, `AnomaliaId` e `Tratamento` (junção com `anomalias_horas`). As 7 horas nulas do horário de verão são removidas | ~340 mil |
| `dim_datas` | `data/consolidated/dim_datas.parquet` | Calendário 2017–2026 com `TipoDia`, `Recesso`, `RegimeMetodologico` etc. ([04-dados.md](04-dados.md)) | 3.652 |
| `dim_horas` | `data/reference/dim_horas.csv` | Hora 0–23, rótulo, período do dia (madrugada, manhã, tarde, noite) | 24 |
| `dim_subsistemas` | `data/reference/dim_subsistemas.csv` | Código, rótulo único ("Sudeste/Centro-Oeste"), ordem | 4 |
| `anomalias` | `data/reference/anomalias.csv` | Eventos e anomalias para anotações; não relacionada | 41 |
| `anomalias_horas` (oculta) | derivada de `anomalias` | Expansão subsistema × dia × hora, com `excluir` prevalecendo quando há sobreposição; usada só para classificar a fato | ~30 mil |
| `mmgd_por_subsistema` | `data/reference/mmgd_por_subsistema.csv` | Potência instalada de MMGD por subsistema e ano (ANEEL) | 40 |
| `_Medidas` | vazia | Só medidas | 0 |

A fato continua cópia fiel do ONS: as colunas adicionais são derivadas no Power Query, não no parquet (D09, D11).

## Relacionamentos

```
dim_datas[Data] 1 ──< fato_curva_carga[Data]
dim_horas[Hora] 1 ──< fato_curva_carga[Hora]
dim_subsistemas[id_subsistema] 1 ──< fato_curva_carga[id_subsistema]
dim_subsistemas[id_subsistema] 1 ──< mmgd_por_subsistema[id_subsistema]
```

As tabelas de data automáticas do Power BI estão desligadas (`__PBI_TimeIntelligenceEnabled = 0`): toda inteligência de tempo passa pela `dim_datas`.

## Medidas

Pasta **Nível**

| Medida | Definição | Observação |
|---|---|---|
| Carga Média (MWmed) | média, sobre as horas do contexto, da soma da carga dos subsistemas selecionados | com todos os subsistemas = SIN; com um = o subsistema |
| Energia (MWh) | soma das horas | 1 MWmed horário = 1 MWh |
| Carga Média Válida (MWmed) | Carga Média sem horas `Tratamento = "excluir"` | base para pico, vale e curvas típicas |
| Participação no SIN | Carga Média ÷ Carga Média sem filtro de subsistema | |

Pasta **YTD**

| Medida | Definição |
|---|---|
| Data de Corte | último dia com dados na série |
| Carga Média YTD (MWmed) | 1º/jan até o dia e mês da Data de Corte, no ano do contexto |
| Variação YTD vs ano anterior | (YTD ano − YTD ano−1) ÷ YTD ano−1 |

Pasta **Sazonalidade**

| Medida | Definição |
|---|---|
| Índice Sazonal Mensal | Carga Média do mês ÷ Carga Média do ano − 1 |
| Tipo de Dia ÷ Dia Útil | Carga Média do tipo ÷ Carga Média dos dias úteis fora do recesso − 1 |

Pasta **Formato**

| Medida | Definição | Regra de uso |
|---|---|---|
| Pico Horário / Vale Horário (MWmed) | maior / menor hora do contexto, sem `excluir` | o falso recorde do NE (08/02/2024) fica fora |
| Hora do Pico | hora (0–23) do Pico Horário | só para um dia ou uma curva típica; **nunca como média anual** |
| Amplitude ÷ Média | (pico − vale) ÷ Carga Média Válida | |
| Fator de Carga | Carga Média Válida ÷ Pico | |
| Índice Horário | para cada dia, carga da hora ÷ média do dia; média entre os dias do contexto; −1 | a curva típica normalizada (D13). Dias com qualquer hora `excluir` ficam fora; no SIN, exige os quatro subsistemas completos |
| Meio do Dia (12–15h) ÷ Média · Noite (18–21h) ÷ Média | Índice Horário restrito à faixa | indicadores da rotação do dia (bloco 8) |
| % Dias com Pico à Tarde / à Noite | parcela dos dias do contexto com Hora do Pico em 12–17h / 18–23h | substitui "hora média do pico" |

Pasta **Curva típica** (cartões da Página 1 — leem a curva típica do contexto, não a série)

| Medida | Definição |
|---|---|
| Pico / Vale da Curva Típica ÷ Média | máximo / mínimo de `Índice Horário` sobre as 24 horas |
| Hora do Pico / do Vale da Curva Típica | hora em que ocorrem |
| Amplitude da Curva Típica ÷ Média | pico − vale (fração da média do dia) |
| Fator de Carga da Curva Típica | 1 ÷ (1 + pico) |
| Média do Dia Típico (MWmed) | Carga Média Válida sem filtro de hora |
| Pico / Vale da Curva Típica (MWmed) | (1 + índice) × Média do Dia Típico |

Pasta **MMGD**: MMGD Instalada (MW); MMGD ÷ Carga Média. Pasta **Marcos**: Marco Carga Global (02/03/2021) e Marco MMGD (29/04/2023), para linhas de referência.

## Regras que as medidas já aplicam

- Curvas típicas (`Índice Horário`) usam apenas horas válidas e dias completos; o visual deve filtrar `TipoDia` e, para dia útil, `Recesso = "Não"`.
- Máximos ignoram artefatos (`Tratamento = "excluir"`).
- YTD compara sempre o mesmo intervalo de datas.
- Rótulo do subsistema vem de `dim_subsistemas[Subsistema]`, nunca de `nom_subsistema` (removida no Power Query).

## Como validar depois de editar o TMDL

1. Abrir `powerbi/anatomia-demanda-energia.pbip` no Power BI Desktop (versão com suporte a PBIP/TMDL) e **Atualizar**. Se o Desktop reclamar de um arquivo TMDL, a linha e o arquivo aparecem na mensagem.
2. Conferir em *Exibição de modelo* os quatro relacionamentos e que não existem tabelas `LocalDateTable_*`.
3. Verificação de números, com uma tabela simples:
   - Carga Média (MWmed) em 2025, todos os subsistemas: **79.6xx** (bloco 2: 79,61 GW).
   - Pico Horário em 2025, todos: **106.149** (26/02/2025 14h); Nordeste em 2024: **≤ 16.9xx** (o 18.157 de 08/02 deve estar fora).
   - Índice Horário, dia útil de 2024–2025, `Recesso = Não`, hora 19, Sudeste/Centro-Oeste: **≈ +13%** (bloco 4).
   - Carga Média YTD em 2026 vs 2025, todos: **+1,0%** (bloco 2, com Data de Corte = 11/09/2026 na extração atual).
4. Salvar no Desktop: ele acrescenta `lineageTag` e reorganiza os arquivos; o diff no git deve ser só isso.

## O que ainda não está no modelo

- Páginas e visuais (o relatório tem uma página vazia).
- Anotações de eventos nos gráficos históricos (a tabela `anomalias` está carregada para isso).
- Textos e notas metodológicas.
