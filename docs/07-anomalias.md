# 07 — Anomalias investigadas

Registro de cada sinal apontado pelo diagnóstico de qualidade ([05-qualidade.md](05-qualidade.md), seção 5: saltos hora a hora acima de 25%), com o que os dados mostram, o que as fontes externas dizem e a classificação adotada. Investigação feita em 13/09/2026 sobre a extração do mesmo dia.

Classificações possíveis: **evento real documentado** · **evento real não documentado** · **provável artefato de dado** · **falso positivo** (comportamento normal capturado pelo limiar).

## Resumo

| # | Subsistema | Quando | O que se vê | Classificação | Tratamento |
|---|---|---|---|---|---|
| A1 | N, NE (e SE, S) | 15/08/2023, 08h–14h | N cai de 6,8 para 1,4 GW; NE de 11,4 para 7,4 GW | **Evento real documentado** — apagão nacional | Excluir o dia das curvas típicas; manter no histórico com anotação |
| A2 | N | Abril/2020 (10 saltos) | Perfil horário errático em fins de semana e feriados; variação média hora a hora 7,0% contra 2,2% normal | **Não explicado** — o nível é COVID, a oscilação não | 2020 já está fora das curvas típicas; sinalizar |
| A3 | N | 08/11/2024, 23h | Queda de 1,5 GW por uma hora, retorno imediato | **Provável artefato de dado** — ONS não registra ocorrência | Manter; irrelevante em agregações |
| A4 | NE | 22/12/2021, 14h | Pico isolado de +3,2 GW em uma hora, sem rastro nas vizinhas | **Provável artefato de dado** — ONS não registra ocorrência | Manter; irrelevante em agregações |
| A5 | S | 7 domingos (2020–2026), 17h–18h | Salto de +25 a +29% entre 17h e 18h | **Falso positivo** — rampa noturna normal de domingo de inverno | Nada a fazer; refinar o limiar do diagnóstico |

## A1 — Apagão de 15 de agosto de 2023

**Dados.** No Norte a carga cai de 6.822 MWmed às 08h para 1.364 às 09h (−80%) e só recupera o nível normal às 14h. No Nordeste, de 11,4 GW às 07h para 7,4 GW às 09h. Sudeste/Centro-Oeste e Sul mostram um degrau menor às 08h (SE 39,6 → 38,5 GW, contra 42,5 na terça anterior). É o menor valor do Norte em toda a série.

**Fonte oficial.** Boletim Diário da Operação do ONS de 15/08/2023, seção "Principais Ocorrências no SIN":

> "No submercado Nordeste ocorreu o desligamento parcial dos estados de Alagoas, Bahia, Ceará, Paraíba, Pernambuco, Rio Grande do Norte e Sergipe e do Piauí. Neste submercado ocorreu a interrupção de aproximadamente 5.138 MW de cargas. No submercado Norte ocorreu o desligamento total dos estados do Amapá, Amazonas, Maranhão, Pará e Tocantins. O estado de Roraima permaneceu atendido de forma isolada do SIN. Neste submercado ocorreu a interrupção de aproximadamente 6.803 MW de cargas. No submercado Sudeste/Centro-Oeste todos os estados foram parcialmente afetados pela perturbação por atuação do Esquema Regional de Alívio de Cargas - ERAC. Ressalta-se que nos estados do Acre e de Rondônia houve interrupção total das cargas […]. Neste submercado ocorreu a interrupção de aproximadamente 5.289 MW de cargas. No submercado Sul […] a interrupção foi de aproximadamente 1.670 MW de cargas. A redução total de cargas no SIN atingiu um montante aproximado de 18.900 MW, correspondendo a 27% da carga total do SIN naquele momento […]. O SIN foi 100% recomposto às 14h49."

A causa (abertura da LT 500 kV Quixadá–Fortaleza II às 08h31 e desempenho abaixo do modelado dos controles de tensão de usinas eólicas e fotovoltaicas da região) está na [nota do ONS](https://www.ons.org.br/Paginas/Noticias/Ocorr%C3%AAncia-no-SIN-em-15-de-agosto-de-2023.aspx) e no Relatório de Análise de Perturbação.

**Interpretação nossa.** A carga registrada caiu porque a carga foi *interrompida*, não porque a demanda diminuiu. O dia é atípico por construção e não pode compor nenhuma curva "típica" de terça-feira, de agosto ou de 2023. No histórico, é um marcador útil — e um bom exemplo, para a persona, de que "carga" mede o que o sistema *conseguiu* atender.

**Bônus.** O mesmo boletim é a **fonte oficial** que faltava para a composição dos subsistemas por estado (ver [02-dominio-e-glossario.md](02-dominio-e-glossario.md)).

## A2 — Norte em abril de 2020

**Dados.** Dez saltos acima de 25% concentrados em 10/04 (Sexta-feira Santa), 11 e 12/04 (Páscoa), 19/04, 26/04 (domingos) e 27–28/04. O perfil desses dias é serrilhado: quedas às 07h–10h e às 15h–18h, picos abruptos às 22h. A variação média hora a hora do mês é 7,0%, contra 2,0–2,6% em todos os outros meses de 2019 a 2021 (nos outros subsistemas, abril/2020 fica em 2,4–4,4%). O nível mensal cai 8% em relação a março (5.347 → 4.921 MWmed) e recupera em maio.

**Fontes externas.** O ONS não disponibiliza os boletins diários de 2020 no endereço atual (404). A queda de *nível* é amplamente documentada: entre 18/03 e 10/04/2020 a carga do SIN caiu cerca de 10% com o isolamento social ([CMSE/MME](http://www.mme.gov.br/todas-as-noticias/-/asset_publisher/pdAS9IcdBICN/content/cmse-avalia-impactos-da-pandemia-do-covid-19-no-setor-eletrico-brasileiro)), e o Amazonas teve a maior queda de consumo do Norte no período ([A Crítica](https://www.acritica.com/manaus/am-tem-a-maior-queda-no-consumo-de-energia-no-norte-durante-isolamento-social-1.43416)); Manaus foi o epicentro da crise sanitária em abril. Nenhuma fonte encontrada explica a *oscilação horária*.

**Interpretação nossa (hipótese, não conclusão).** O Norte tem carga pequena e proporcionalmente muito industrial (eletrointensivos no Pará). Em fins de semana e feriados de um mês de demanda residencial e comercial deprimida, variações da carga industrial — ou falhas de telemetria — ficam proporcionalmente grandes. Não é possível distinguir as duas coisas com os dados públicos.

**Tratamento.** 2020 já está fora das curvas típicas por decisão de projeto (D04). O mês fica sinalizado no histórico como "comportamento horário atípico, não explicado".

## A3 — Norte, 08/11/2024 às 23h

**Dados.** 7.373 → 6.906 → 8.810 MWmed. Uma hora ~1,5 GW abaixo da vizinhança; nenhum outro subsistema reage.

**Fonte oficial.** Boletins diários do ONS de 08/11 e 09/11/2024: "não foram verificadas ocorrências significativas com origem na Rede de Operação do SIN, envolvendo interrupção de cargas".

**Classificação.** Provável artefato de dado (ou interrupção fora da rede de operação do ONS, invisível ao boletim). Uma hora em 67 mil; não afeta médias diárias ou mensais. Mantido.

## A4 — Nordeste, 22/12/2021 às 14h

**Dados.** 11.872 → 15.049 → 12.534 MWmed. O SIN também sobe 5 GW nessa hora, então não é transferência entre subsistemas.

**Fonte oficial.** Boletim diário do ONS de 22/12/2021: sem ocorrências significativas.

**Classificação.** Provável artefato de dado. Mantido; sinalizar se algum visual horário de dezembro/2021 for usado.

## A5 — Domingos no Sul, 17h–18h

**Dados.** Sete domingos entre julho/2020 e maio/2026 com salto de +25% a +29% entre 17h e 18h (ou 16h e 17h, conforme a estação). Nos domingos vizinhos o salto é de +20% a +24% — mesmo formato, só um pouco abaixo do limiar.

**Interpretação nossa.** É a rampa noturna normal do Sul: a tarde de domingo é o ponto mais baixo da semana, e o pico da noite (iluminação, chuveiro elétrico, aquecimento no inverno) tem o mesmo nível de qualquer dia. A razão pico/vale é a maior da semana justamente no domingo, e o limiar fixo de 25% captura os domingos mais frios. Não há anomalia; há um padrão — e um achado para a Camada 2 do produto (domingo no Sul tem a rampa mais íngreme do país).

**Tratamento.** Nenhum. O diagnóstico de qualidade passou a comparar cada salto com o mesmo horário do mesmo dia da semana nas quatro semanas vizinhas; com isso, cinco dos sete domingos deixam de ser sinalizados. Os dois restantes (10/08/2025 e 10/05/2026) só aparecem porque os domingos vizinhos foram mais amenos (rampa habitual de +15%) — mesmo padrão, intensidade maior, provavelmente frio. Continuam classificados como falso positivo.

## Composição dos subsistemas confirmada

O boletim de 15/08/2023 lista os estados de cada submercado:

| Subsistema | Estados citados | Observação |
|---|---|---|
| Norte | Amapá, Amazonas, **Maranhão**, Pará, Tocantins | Roraima estava isolado do SIN em 2023 |
| Nordeste | Alagoas, Bahia, Ceará, Paraíba, Pernambuco, Rio Grande do Norte, Sergipe, Piauí | Maranhão **não** está aqui |
| Sudeste/Centro-Oeste | "todos os estados" da região + **Acre e Rondônia** | — |
| Sul | "todos os estados" | — |

Isso confirma, em fonte oficial, que subsistema não é região do IBGE: o Maranhão (7 milhões de habitantes) conta no Norte, e Acre e Rondônia contam no Sudeste/Centro-Oeste.

---

# Parte 2 — Varredura ampla (13/09/2026)

A primeira parte olhou só saltos hora a hora. Esta parte varre a base de quatro outras formas e confronta com uma lista de eventos externos conhecidos. Resultado consolidado em `data/reference/anomalias.csv`.

## Métodos

| Varredura | Como | O que captura |
|---|---|---|
| **Nível diário** | Média do dia ÷ mediana dos dias do mesmo tipo (útil/sáb/dom/feriado) em ±3 semanas; sinaliza desvio ≥ 8% | Feriados não marcados, vésperas, ondas de calor e frio, apagões longos |
| **Formato do dia** | Correlação do perfil normalizado com o perfil típico do mesmo dia da semana em ±4 semanas; sinaliza corr < 0,85 | Dias que se comportam como outro tipo de dia; apagões; artefatos |
| **Degraus** | Média de 28 dias depois ÷ 28 dias antes, semana a semana; sinaliza ≥ 6% | Rupturas de nível (COVID, metodologia, estrutura) |
| **Extremos** | 5 maiores horas e 5 menores dias por subsistema | Recordes verdadeiros e falsos |
| **Eventos externos** | Lista de eventos documentados testada diretamente na base | O que os métodos estatísticos não veem porque o efeito é pequeno ou esperado |

## O que apareceu

### Recordes: um deles é falso

| Subsistema | Maior hora da série | Verificação |
|---|---|---|
| SIN | 106.149 MWmed, 26/02/2025 14h | **Confirmado**: o ONS registrou recorde de demanda instantânea de 106.532 MW às 14h27 desse dia, sexto recorde de fevereiro, atribuído a onda de calor ([MME](https://www.gov.br/mme/pt-br/assuntos/noticias/sistema-interligado-nacional-registra-quarto-recorde-de-demanda-instantanea-de-energia-em-2025)). A média horária é coerentemente menor que o instantâneo |
| SE | 62.150, 18/02/2025 14h | Mesma onda de calor; o anterior era 61.217 em 14/11/2023, também onda de calor documentada |
| S | 22.737, 11/02/2025 14h | Verão 2025 |
| N | 11.196, 03/09/2026 14h | Setembro de 2026; o Norte cresce continuamente na série (7,3 GW em jan/2024 → 9,8 GW em set/2026) |
| NE | **18.157, 08/02/2024 10h** | **Falso.** Hora isolada entre 14,6 e 14,9 GW; 7% acima de qualquer outra hora do NE em oito anos; o SIN salta junto. Mesmo padrão de A4. Registrado como **A6**, tratamento `excluir` — o recorde real do NE é 16.987 MWmed (04/02/2026 22h) |

Lição: **toda medida de "máximo" ou "recorde" precisa excluir as horas classificadas como artefato**, senão o dashboard publica um recorde que não existiu.

### Eventos externos que deixam rastro

| Evento | Rastro na base | Registro |
|---|---|---|
| **Apagão de 14/10/2025, 00h32** (incêndio na SE Bateias, PR; 13 estados; SE 4.800 MW, NE 1.900, S 1.600, N 1.600; recomposição em até 2h30 — [Agência Brasil](https://agenciabrasil.ebc.com.br/geral/noticia/2025-10/incendio-em-subestacao-provoca-apagao-na-madrugada-em-todas-regioes)) | SE às 00h: 39,6 GW contra 45,8 na semana anterior (−13%). Pequeno, porque foi de madrugada e curto | A7, `sinalizar` |
| **Copa do Mundo 2022** — cinco jogos do Brasil | Queda de **−14 a −24%** na hora do jogo, em todos os subsistemas. No Brasil × Suíça (28/11, 13h): S −24%, SE −20%, N −16%, NE −13%. Recuperação na hora seguinte | E1–E5, `sinalizar` |
| **Copa do Mundo 2026** — jogos do Brasil em 13, 19 e 24/06, 29/06 e 05/07 ([datas](https://www.olympics.com/pt/noticias/copa-do-mundo-2026-brasil-locais-datas-jogos-cruzamentos-selecao-brasil)) | Detectados **sem saber as datas**: SE −10/−12% às 21–22h de 19/06; −13/−15% às 19–20h de 24/06; −19/−22% às 14–16h de 29/06 (segunda-feira); −15/−18% às 17–19h de 05/07. Nenhum sinal em 11/07 | E6–E10, `sinalizar` |
| **Onda de calor de novembro/2023** | SE +24% em 13/11 e +20% em 14/11 vs semana anterior; recorde do SE na época | C1, `sinalizar` |
| **Onda de calor de fevereiro/2025** | Sequência de recordes do SIN de 21 a 26/02 | C2, `sinalizar` |
| **COVID-19** | Degrau de −14% no SIN entre a semana de 17/03 e a de 07/04/2020 (S e SE −16 a −19%); os cinco menores dias do SIN em toda a série são domingos de abril e maio de 2020 | Já tratado por D04 (2020 fora das típicas); sem linha própria |

### Eventos externos que **não** deixam rastro

| Evento | Por que não aparece |
|---|---|
| **Apagão do Amapá** (03/11/2020, 22 dias) | O Amapá é ~4% do subsistema Norte; a média diária do N em novembro/2020 fica entre −8% e +15% do mesmo dia de 2019, sem padrão. Invisível na escala do subsistema |
| **Enchentes do Rio Grande do Sul** (maio/2024) | A média do Sul em maio/2024 (12,5 GW) é **maior** que em maio/2023 (12,1) e menor que em maio/2025 (12,9); a primeira quinzena de maio/2024 não destoa de abril. Uma tragédia regional não move um subsistema de três estados quando a temperatura domina |
| **Interligação de Roraima ao SIN** | Nenhum degrau na média mensal do Norte entre 2024 e 2026; o crescimento é contínuo. Ou a carga de Roraima (~300 MW) é pequena demais, ou a integração ainda não está refletida na série. Pendência |

### Calendário: o que o nível diário revelou

O método de nível diário sinalizou como "dia útil atípico" um conjunto de datas que na verdade são feriados ou vésperas — ou seja, dias que **não deveriam entrar em curvas típicas de dia útil**:

- **Vésperas de Natal e de Ano-Novo** caindo em dia útil: −16 a −24% no Sul, −16 a −17% no SE. Dez ocorrências entre 2019 e 2025 (K5–K14). Comportam-se como sábado.
- **Segunda-feira de Carnaval**: 20/02/2023, S −19%; a dimensão de datas marca só a terça.
- **Carnaval 2019** (04–05/03): NE −16/−18%, SE −16%; não marcado.
- **Carnaval 2026** (16–17/02): não marcado.
- **07/09/2026** (Independência, segunda-feira): S −24%, SE −19%, SIN −17%; a dimensão de datas registra a Independência em **07/07** nos anos 2024, 2025 e 2026 (troca de dia e mês).
- **Corpus Christi** só está marcado em 2023 (é ponto facultativo, então a ausência nos outros anos pode ser intencional).

Os fatos acima sobre a `dim_datas` são reportados aqui porque afetam diretamente a definição de "dia típico"; a correção é decisão do autor da dimensão. Enquanto isso, as datas estão na tabela de anomalias com tipo `calendario` e tratamento `excluir`.

### Clima sem documentação (hipóteses)

O Sul responde à temperatura com amplitude que nenhum outro subsistema tem: dezenas de dias com ±15–24% em relação ao mesmo tipo de dia nas semanas vizinhas, quase todos em janeiro–março (calor) ou em frentes frias de outono e primavera. Registrei apenas os casos mais extremos (C3–C7), como hipótese climática, para que a exploração da sazonalidade não os confunda com erro. Exemplo: sábado 09/11/2024 no Sul teve carga diurna de 7,6 GW contra 13–14 GW no sábado anterior — perfil de domingo de inverno, sem ocorrência registrada pelo ONS; provável frente fria após semana quente.

## A tabela `data/reference/anomalias.csv`

| Coluna | Conteúdo |
|---|---|
| `id` | A = anomalia de dado/operação; E = evento social; C = clima; K = calendário |
| `data_inicio`, `data_fim` | Intervalo de datas (inclusive) |
| `hora_inicio`, `hora_fim` | Intervalo de horas (inclusive), vazio = dia inteiro |
| `id_subsistema` | `N`, `NE`, `S`, `SE` ou `*` (todos) |
| `tipo` | `evento_documentado`, `clima_documentado`, `clima_hipotese`, `artefato_provavel`, `nao_explicado`, `calendario` |
| `tratamento` | `excluir` = fora das curvas típicas e dos extremos; `sinalizar` = entra nos cálculos, com anotação disponível |
| `descricao`, `referencia` | Texto e fonte |

37 linhas em 13/09/2026: 18 `excluir`, 19 `sinalizar`. A tabela é mantida à mão; toda linha nova precisa de uma entrada neste documento e, quando houver, em [fontes.md](fontes.md).
