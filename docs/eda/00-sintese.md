# Síntese da exploração — o que estrutura o dashboard

> 14/09/2026. Fecha os blocos 1–11 (2017–2026, extração de 11/09/2026). Serve de briefing para a modelagem no Power BI: os padrões que sustentam o produto, os visuais que os mostram, as medidas que cada visual exige e o que fica de fora.

## A tese, agora com evidência

> Mais importante do que saber quanto de energia o Brasil demanda é entender quando essa demanda acontece, onde ela se concentra e como seu formato vem mudando.

A exploração confirmou a tese e a deixou mais específica: **o nível quase não muda sob a mesma metodologia (~1,5% ao ano), mas o formato do dia está girando — menos meio-dia, mais noite — e cada subsistema tem seu próprio calendário.**

## Cinco padrões fortes

| # | Padrão | Evidência | Bloco |
|---|---|---|---|
| **P1** | **O crescimento aparente é medição.** A carga registrada subiu 23% de 2019 a 2025, mas os três maiores saltos coincidem com a pós-COVID e os dois marcos do ONS. Sob regime homogêneo: +1,5% ao ano em 2017–2019 e +0,8 a +1,0% em 2024–2026 | Variação anual com marcos; YTD 2024 × 2025 × 2026 | 2 |
| **P2** | **Quatro calendários, não um.** SE e Sul: pico em fevereiro, vale em junho–julho. Nordeste: novembro. Norte: setembro–outubro, o inverso do país. O SIN esconde isso porque é 56% Sudeste | Índice sazonal mensal por subsistema | 3 |
| **P3** | **Dois formatos de dia.** SE e Sul têm madrugada profunda e pico às 19h; NE e Norte são quase planos, com pico às 21–22h (NE) e 14h (N). Fator de carga de 0,87 no Sul a 0,94 no Norte | Curvas normalizadas sobrepostas; matriz de distância | 4, 5 |
| **P4** | **O verão estressa o nível; o inverno estressa o formato.** No verão o ar-condicionado enche a tarde: pico às 14h, dia plano, recordes de carga. No inverno a tarde cai e a noite vira pico isolado — amplitude de 50% no Sul. Dias mais pesados são dias mais planos (r = −0,75 no SE) | Heatmap hora × mês; scatter nível × amplitude | 4, 6 |
| **P5** | **O dia está girando da tarde para a noite.** Meio do dia do SIN: +9,5–9,9% (2017–2019) → +3,7% (2026); noite: +9% → +12%. No Nordeste o meio-dia já está abaixo da média e o pico à tarde passou de 85% para 0% dos dias úteis. Continua sob regime homogêneo (~1,7 p.p./ano). Acompanha a geração distribuída (r = −0,92 no NE); não é o mercado livre (domingo gira igual) | Formato por ano; indicadores por ano; MMGD × meio-dia | 8, 10, 11 |

Dois achados de apoio que merecem uma linha no produto: **o Norte cresce +6% ao ano e ficou sazonal** (blocos 2, 3); **três apagões nacionais e a greve dos caminhoneiros são visíveis na série** (bloco 7 de anomalias) — bons "eventos" para anotar nos gráficos históricos.

## As três camadas, com visuais e medidas

### Camada 1 — A demanda brasileira em perspectiva (P1, P2)

| Visual | Origem | Medidas necessárias |
|---|---|---|
| Carga média mensal por subsistema, pequenos múltiplos, com os marcos 02/03/2021 e 29/04/2023 desenhados | `02_media_mensal_subsistemas` | Carga média (MWmed) por mês; marcos como linhas de referência |
| KPI de nível: YTD 2026 × 2025 × 2024 no mesmo intervalo, com a variação sob regime homogêneo — **não** a variação 2019→2025 | `02_ytd_2024_2025_2026` | Carga média YTD com data de corte = último dia disponível; variação % |
| Participação de cada subsistema por ano | `02_participacao_subsistemas` | Carga média por subsistema ÷ SIN |
| Índice sazonal mensal por subsistema (mês ÷ média do ano) | `03_indice_mensal` | Média mensal ÷ média anual, por subsistema |

Texto de apoio: uma frase sobre os três regimes (o que mudou em 2021 e 2023) e uma sobre a regra YTD.

### Camada 2 — Anatomia de um dia (P3, P4) — assinatura visual

| Visual | Origem | Medidas necessárias |
|---|---|---|
| **Curvas típicas normalizadas dos quatro subsistemas sobrepostas** (dia útil; alternável para sábado/domingo) | `04_formato_normalizado_subsistemas` | Média por hora de (carga ÷ média do dia) sobre os dias do tipo, 2024–2025, excluindo `anomalias` (`excluir`) e `Recesso` |
| Heatmap hora × mês do dia útil, com a hora do pico marcada | `04_heatmap_hora_mes` | Mesma medida, por mês |
| Cartões de pico, vale, amplitude e fator de carga por subsistema × tipo de dia | tabela do bloco 4 | Pico, vale, hora do pico, amplitude ÷ média, fator de carga |
| Scatter nível × amplitude por estação (SE e Sul) — sustenta a frase "verão × inverno" | `06_nivel_vs_amplitude` | Média e amplitude relativa por dia |

Regras: nunca "hora média do pico" (não existe — é 14h no verão e 19h no inverno); curvas típicas sempre por `TipoDia`; dia útil exclui `Recesso`.

### Camada 3 — Como o perfil mudou (P5)

| Visual | Origem | Medidas necessárias |
|---|---|---|
| Dia útil típico por ano, rampa de cor clara → escura, um painel por subsistema | `08_formato_por_ano` | Curva normalizada por ano (2020 omitido; horário de verão excluído) |
| Meio do dia (12–15h) e noite (18–21h) por ano, com os marcos; versão YTD sob regime homogêneo como KPI | `08_indicadores_por_ano` | Média de (hora ÷ média do dia) nas faixas, por ano |
| "Pico à tarde × à noite", por ano e por estação | `08_periodo_do_pico_por_ano`, `04_periodo_do_pico_por_estacao` | % de dias úteis com hora do pico em 12–17h vs 18–23h |
| MMGD × meio do dia (visual de apoio, único com dado externo) | `10_mmgd_vs_meio_do_dia` | `mmgd_por_subsistema` ÷ carga média do ano |

Texto de apoio: "curva do pato da carga" para o NE; "um em cada doze MWh do NE vem do telhado" (EPE); as causas visíveis (MMGD, climatização) e a plausível (mercado livre), sem atribuir a uma só.

### O que fica de fora da primeira versão

- Página de anomalias (D-camada opcional): os eventos entram como **anotações** nos gráficos históricos, não como página.
- Camada EPE/UF/população: a única pergunta que a pede (H7, Norte e Nordeste pela baixa tensão) não muda nenhum visual acima. Fica como expansão.
- Temperatura (INMET): decidido não incorporar (D08); o texto usa "climatização" como leitura, não como medida.

## O que o modelo precisa ter

1. `fato_curva_carga` (2017–2026) relacionada a `dim_datas` por data e a uma **dimensão de hora** (0–23; rótulo; período: madrugada 0–5, manhã 6–11, tarde 12–17, noite 18–23) — a única tabela de calendário ainda não criada.
2. `anomalias` (de `data/reference/anomalias.csv`) relacionada por data + subsistema, com `tratamento`; medidas de curva típica e de máximo filtram `excluir`.
3. `mmgd_por_subsistema` (de `data/reference/mmgd_por_subsistema.csv`) para o visual de apoio da Camada 3.
4. Rótulo único "Sudeste/Centro-Oeste" (chave `id_subsistema`); linha "SIN" como soma dos quatro.
5. Medidas de base: carga média; carga por hora ÷ média do dia; pico, vale, hora do pico, amplitude ÷ média, fator de carga; YTD com data de corte dinâmica; participação; índice sazonal.
6. Marcos metodológicos e regime (`dim_datas[RegimeMetodologico]`) disponíveis a todo visual histórico.

## Decisões pendentes que a síntese fecha

- **Dimensão de hora:** criar como tabela de referência versionada (`data/reference/dim_horas.csv`), no mesmo padrão da tabela de anomalias — pequena, à mão, documentada.
- **Camada EPE:** não abrir na primeira versão.
- **Ordem de construção:** modelo e medidas → Camada 2 (assinatura) → Camada 3 → Camada 1 → textos e notas metodológicas.
