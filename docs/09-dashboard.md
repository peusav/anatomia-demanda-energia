# 09 — Plano do dashboard

Planejamento das páginas, visuais e textos, a partir da [síntese da exploração](eda/00-sintese.md) e do [modelo](08-modelo-powerbi.md). Escopo do projeto: uma página principal forte, uma de aprofundamento, quatro ou cinco visuais centrais.

## Princípios de desenho

1. **Um visual, uma pergunta.** Título = o assunto; subtítulo = a pergunta que o visual responde mais a unidade de leitura ("O formato do dia em cada subsistema" / "Como a carga se distribui pelas 24 horas? Cada ponto é a hora em relação à média do próprio dia"). O **insight não vai no título**: um visual com filtros muda de resposta a cada clique, e um título-afirmação fica errado assim que o filtro muda. Insights ficam em caixas de texto fixas (que não reagem a filtros) ou na página "Sobre". Explicações necessárias para ler o visual (normalização, exclusões) vão num ícone ⓘ com dica de ferramenta.
2. **A persona não é do setor.** Unidades explicadas uma vez (GWmed = "potência média"); nenhum jargão sem tooltip; os marcos metodológicos aparecem como linhas com rótulo, não como nota de rodapé.
3. **Cor segue a entidade.** Uma cor fixa por subsistema (as da exploração: SE azul, Sul verde-água, NE laranja, Norte amarelo; SIN cinza), em todas as páginas. Tipo de dia e estação têm as suas.
4. **Nunca "hora média do pico".** Hora do pico só em dia único ou curva típica; ao longo do tempo, "% de dias com pico à tarde/à noite".
5. **Nível sempre com o regime.** Todo gráfico que atravessa 2021 ou 2023 mostra os dois marcos.
6. **Filtros comuns no topo**: Subsistema (botões, com "SIN" = todos), Ano, Tipo de dia. Sem filtro de hora nem de mês: as páginas já os usam como eixo.

## Estrutura: duas páginas e uma de apoio

| Página | Camada | Pergunta | Papel |
|---|---|---|---|
| **1 · Anatomia de um dia** | 2 | Como a carga se distribui pelas 24 horas, e isso muda com a estação? | Página principal e assinatura visual |
| **2 · Como o perfil mudou** | 3 + 1 | O Brasil demanda energia do mesmo jeito de 2017? Quanto cresceu de fato? | Aprofundamento: história e nível |
| **Sobre os dados** | — | O que é carga, o que mudou em 2021 e 2023, como ler | Página de apoio (botão "?" nas duas anteriores), sem visuais de dados |

## Página 1 — Anatomia de um dia (1280 × 720)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Título · subtítulo (tese em uma linha)      [Subsistema ▢▢▢▢] [Ano] [?]  │
├────────────────────────────────────┬─────────────────────────────────────┤
│ V1  O dia típico dos quatro        │ V2  Quando é o pico? Depende do mês │
│     subsistemas (curvas            │     (heatmap hora × mês, dia útil,  │
│     normalizadas sobrepostas,      │     traço na hora do pico de cada   │
│     dia útil; botões: sáb/dom)     │     mês)                            │
│                                    │                                     │
├─────────┬─────────┬────────┬───────┼─────────────────────────────────────┤
│ Pico    │ Vale    │ Amplit.│ Fator │ V3  Dias mais pesados são mais      │
│ 19h     │ 4h      │ ÷ média│ carga │     planos (dispersão nível ×       │
│ 51,6 GW │ 37,4 GW │ 31%    │ 0,89  │     amplitude, cor = estação)       │
└─────────┴─────────┴────────┴───────┴─────────────────────────────────────┘
```

| # | Visual | Campos | Medidas | Filtros do visual |
|---|---|---|---|---|
| V1 | Linhas, 4 séries (uma por subsistema), eixo `dim_horas[HoraRotulo]`. Título "O formato do dia em cada subsistema"; subtítulo "Como a carga se distribui pelas 24 horas? Cada ponto é a hora em relação à média do próprio dia (0% = média)"; ⓘ com a explicação da normalização e das exclusões; linha de referência em 0 rotulada "média do dia"; sem títulos de eixo; sem rótulos na ponta das linhas (a legenda identifica) | legenda `dim_subsistemas[Subsistema]` | `Índice Horário` | `TipoDia` pelo botão (Dia útil padrão; Sábado; Domingo); `Recesso = Não`; anos do núcleo por padrão (2024–2025), obedece ao filtro de ano |
| V2 | Matriz com formatação condicional (heatmap) — linhas `dim_horas[HoraRotulo]`, colunas `dim_datas[MesAbrev]` | | `Índice Horário` (escala azul, −25% a +25%) | `TipoDia = Dia útil`, `Recesso = Não`; reage ao filtro de subsistema |
| Cartões | 4 cartões | | `Hora do Pico`, `Pico Horário`, `Vale Horário`, `Amplitude ÷ Média`, `Fator de Carga` — calculados sobre a **curva típica** (contexto do V1) | os mesmos do V1 |
| V3 | Dispersão — x `Carga Média Válida` por dia, y `Amplitude ÷ Média`, detalhe `dim_datas[Data]`, legenda `EstacaoAno` | | | `TipoDia = Dia útil`, `Recesso = Não`; mostra o subsistema selecionado (com "SIN", mostra o SIN) |

Caixa de texto fixa da página (não reage a filtros) com o insight do dia útil: *"No dia útil, o pico é às 14h no Norte, 19h no Sudeste e no Sul, 21h no Nordeste — quatro rotinas no mesmo país."* Sem atribuir causa (indústria × residencial): a curva de carga mostra o horário, não quem consome; a leitura por tipo de consumidor é a hipótese H7, que exigiria dados da EPE.

Texto do ⓘ do V1: *"Para cada dia, dividimos a carga de cada hora pela média daquele dia. Isso tira o efeito de tamanho — o Sudeste é seis vezes o Norte, mas aqui os dois cabem na mesma escala e o que sobra é o formato. Dias com falhas de dado, apagões, horário de verão e o recesso de fim de ano ficam fora."*

Os cartões leem a curva típica, não a série: medidas da pasta **Curva típica** (`Hora do Pico da Curva Típica`, `Pico da Curva Típica (MWmed)`, `Vale da Curva Típica (MWmed)`, `Amplitude da Curva Típica ÷ Média`, `Fator de Carga da Curva Típica`), já no modelo.

## Página 2 — Como o perfil mudou

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Título                                       [Subsistema ▢▢▢▢]     [?]   │
├────────────────────────────────────┬─────────────────────────────────────┤
│ V4  O dia está girando: menos      │ V5  Meio do dia cai, noite sobe     │
│     meio-dia, mais noite           │     (duas linhas por subsistema:    │
│     (dia útil típico por ano,      │     Meio do Dia ÷ Média e Noite ÷   │
│     rampa clara→escura, 2017→2026, │     Média, por ano, com os marcos)  │
│     2020 omitido)                  │                                     │
├────────────────────────────────────┼─────────────────────────────────────┤
│ V6  Quanto cresceu de fato         │ V7  % de dias úteis com pico à      │
│     (carga média mensal 2017–2026  │     tarde × à noite, por ano,       │
│     com os marcos; cartão YTD:     │     verão e inverno separados       │
│     2026 vs 2025 no mesmo período) │     (colunas 100%)                  │
└────────────────────────────────────┴─────────────────────────────────────┘
```

| # | Visual | Campos | Medidas | Filtros |
|---|---|---|---|---|
| V4 | Linhas, uma por ano, eixo `HoraRotulo`, legenda `dim_datas[Ano]` com paleta ordinal da cor do subsistema | | `Índice Horário` | `TipoDia = Dia útil`, `Recesso = Não`, `Ano <> 2020`; um subsistema por vez (com "SIN", mostra o SIN) |
| V5 | Linhas, eixo `Ano`, duas séries | | `Meio do Dia (12–15h) ÷ Média`, `Noite (18–21h) ÷ Média` | idem; linhas de referência em 2021 e 2023 |
| V6 | Linhas, eixo `AnoMes`, uma por subsistema | | `Carga Média (MWmed)`; linhas de referência `Marco Carga Global` e `Marco MMGD`; cartão `Variação YTD vs ano anterior` para 2026 | — |
| V7 | Colunas 100% empilhadas, eixo `Ano`, pequenos múltiplos por `EstacaoAno` (Verão, Inverno) | | `% Dias com Pico à Tarde`, `% Dias com Pico à Noite` | `TipoDia = Dia útil`, `Ano <> 2020` |

Anotações de eventos (apagões de 2018, 2023, 2025; greve de 2018; COVID) entram no V6 como marcadores de dados ou tooltip, lendo `anomalias` — segunda iteração, não a primeira.

## Página "Sobre os dados"

Texto curto, sem gráfico: o que é carga (e por que não é consumo); MWmed; os quatro subsistemas e que não são regiões do IBGE; os três regimes (02/03/2021, 29/04/2023) e a regra "2024–2025 é o núcleo comparável, 2026 é parcial"; o que foi excluído (apagões, artefatos, horário de verão, recesso) e onde está a lista; fonte e data da extração (`Data de Corte`). Conteúdo vem de [02](02-dominio-e-glossario.md) e [03](03-metodologia.md).

## Ordem de construção

1. Validar o modelo no Desktop com os quatro números de [08-modelo-powerbi.md](08-modelo-powerbi.md).
2. Criar as medidas auxiliares dos cartões (pico/vale/amplitude da curva típica).
3. Página 1: V1 primeiro (é a assinatura; se não convencer, o resto não importa), depois V2, cartões, V3.
4. Página 2: V4 e V5 (a história), depois V6 e V7.
5. Filtros, cores fixas, títulos-resposta, tooltips.
6. Página "Sobre os dados" e botões "?".
7. Anotações de eventos (segunda iteração).

## Decisões tomadas (14/09/2026)

- **"SIN" no filtro de subsistema**: botão explícito que seleciona os quatro.
- **Anos padrão da Página 1**: 2024–2025 (núcleo comparável); o filtro de ano altera.
- **V3 no SIN**: mostra o agregado (um ponto por dia).
