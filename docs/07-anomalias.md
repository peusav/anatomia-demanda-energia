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
| A8 | todos | 01/01–16/02/2019 | Horas deslocadas +1h (hora oficial de Brasília em UTC−2) | **Convenção horária** — horário de verão | Excluir das curvas horárias; médias diárias intactas |

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

## A8 — Horário de verão em janeiro–fevereiro de 2019

**Dados.** Nenhum dia tem 23 ou 25 registros, o que levou à conclusão inicial de que a série estava em hora padrão. O teste correto é outro: comparar o horário da rampa noturna antes e depois de 17/02/2019, último fim de horário de verão. No Nordeste — que **não** adotava horário de verão — o salto de ~1,5 GW da noite acontece entre 18h e 19h nos sábados 09/02 e 16/02 e entre 17h e 18h em 23/02. O comportamento não mudou; o rótulo mudou.

**Interpretação.** O ONS carimba todos os subsistemas na hora oficial de Brasília, que era UTC−2 até 16/02/2019 e UTC−3 desde então. Os 47 dias de 01/01 a 16/02/2019 têm as horas deslocadas +1h em relação ao restante da série, nos quatro subsistemas. No dia da transição o ONS publicou 24 valores, então não há hora duplicada visível.

**Tratamento.** `excluir` de curvas horárias, hora do pico e do vale. Médias diárias, mensais e anuais não são afetadas (somar 24 horas dá o mesmo resultado). Se a série for ampliada para antes de 2019, cada janela de horário de verão (outubro–fevereiro) precisará da mesma regra. Contexto: o horário de verão foi extinto pelo Decreto 9.772/2019 porque o pico do SIN deixou de ser no início da noite, o que o bloco 8 da exploração documenta.

## Parte 3 — Anos de 2017 e 2018 (ampliação da série, 13/09/2026)

A série foi ampliada para 2017–2026 (decisão D14). O diagnóstico de qualidade sobre os dois anos novos trouxe:

| # | Subsistema | Quando | O que se vê | Classificação | Tratamento |
|---|---|---|---|---|---|
| A8b, A8c | todos | 01/01–18/02/2017 e 15/10/2017–17/02/2018 | Janelas de horário de verão (mesma convenção de A8). A hora 0 de 15/10/2017 e de 04/11/2018 **não existe** nos arquivos (vazia) — confirmação direta de que os carimbos seguem a hora oficial | **Convenção horária** | Excluir das curvas horárias |
| A9 | S | 04/11/2018, 0h | Valor **zero** na hora inexistente (os outros subsistemas trazem vazio) | Artefato | Excluir |
| A10 | N, NE (e todos) | 21/03/2018, 15h–21h | N cai de 5,1 para 0,8 GW; NE de 10,7 para 0,7 GW às 16h; recomposição até 21h | **Evento real documentado** — apagão de 21/03/2018 | Excluir das curvas típicas |
| A11 | NE | 25/08/2018, dia inteiro | Carga de 2,5 a 5,9 GW o dia todo (habitual: 10–12 GW); volta ao normal à 0h de 26/08 | **Provável artefato** | Excluir |
| A12 | N | 18/10/2018, 21h | Queda isolada de 1,5 GW por uma hora | **Provável artefato** | Excluir |
| — | S | 23 e 30/07/2017, 17/06/2018 | Rampa noturna de domingo de inverno | Falso positivo (A5) | Nada |

**A10 — apagão de 21/03/2018.** Às 15h48, abertura indevida de um disjuntor na subestação Xingu (PA), no bipolo de Belo Monte, quando o fluxo era elevado a 4.000 MW; 18.000 MW interrompidos (22,5% do SIN), Norte e Nordeste desligados, 14 estados e ~70 milhões de pessoas afetados ([Agência Brasil](https://agenciabrasil.ebc.com.br/geral/noticia/2018-04/apagao-no-norte-e-nordeste-foi-causado-por-falha-humana-diz-ons); [ONS](https://www.ons.org.br/paginas/noticias/20180506-analiseocorrencianorteenordeste.aspx)). Junto com 15/08/2023 e 14/10/2025, é o terceiro apagão nacional da série — e os três aparecem na base.

**A11 — Nordeste em 25/08/2018.** Não há apagão registrado nessa data (a busca por notícias devolve apenas o evento de 15/08/2023). A base diária do ONS traz o mesmo valor, então não é erro de agregação: é a mesma falha na origem. Os boletins diários do ONS de 2018 não estão mais disponíveis (404). Excluído.

**Reconciliação com a base diária em 2017.** Quatro dias do SE em outubro e novembro de 2017 divergem 0,5–1,9% entre a curva horária e a base diária (por exemplo 07/10: diária 34.837, horária 34.182 MWmed). É o único ano completo em que as duas bases não coincidem exatamente — sinal de que foram revisadas em momentos diferentes. Registrado; sem tratamento (as diferenças são pequenas e 2017 é ano de contexto).

## Parte 4 — Segunda varredura externa (13/09/2026)

Nova lista de eventos externos testada contra a base 2017–2026, com foco nos anos novos e em eventos sociais e climáticos que a primeira varredura não cobriu.

### Eventos que deixam rastro

| Evento | Rastro na base | Registro |
|---|---|---|
| **Greve dos caminhoneiros** (21/05–01/06/2018) | O maior evento não climático da série depois da COVID: carga do SIN **−7% na segunda-feira 21/05, −22% na quinta 31/05** (Sul −29%, SE −23%) em relação a duas semanas antes; volta ao normal em 02–03/06. Doze dias em que o país parou e a rede sentiu — indústria sem insumo, comércio sem estoque | E11, `sinalizar` |
| **Copa do Mundo 2018** — cinco jogos do Brasil | −10 a −21% na hora do jogo no SE (Brasil × Bélgica, 06/07 15h: −21%). O jogo contra o México (02/07, 15h) quase não aparece (−3%) — sem explicação | E12–E16, `sinalizar` |
| **Ciclone-bomba no Sul** (30/06/2020) | 1,9 milhão de consumidores sem energia em SC, RS e PR; Sul −8% em 30/06 e −12% em 01/07 vs semana anterior | E17, `sinalizar` |
| **Temporal em São Paulo** (03/11/2023, apagão de até 6 dias na área da Enel) | SE −5% em 03/11, −10% em 05 e 06/11 vs semana anterior. O sinal se mistura com o feriado de Finados (02/11) e com a onda de calor que veio logo depois (13–17/11) | E18, `sinalizar` |
| **Onda de calor de setembro/2020** (recorde de setembro em SP; 17/09–05/10) | SE +10 a +18% vs semana anterior entre 28/09 e 02/10 | C8, `sinalizar` |
| **Carnaval cancelado pela COVID** | 2021: o Nordeste tratou a segunda e a terça como dias úteis (−2% vs dia útil; em 2019 foram −15/−18%), o SE não (−13%). 2022: o SE e o Sul trabalharam (−2 a −4%; +1 a −6%), o NE folgou parcialmente (−6%). A dimensão de datas marca os dois anos como Feriado — está correta como regra, mas esses quatro dias não são feriados na carga | E19, E20, `sinalizar` |

**Um efeito de calendário novo: o recesso de fim de ano.** A varredura de nível diário de 2017–2018 apontou os dias úteis entre o Natal e o Ano-Novo — 26 a 30/12 — e o 02/01 como "dias úteis atípicos", com −5 a −16% no SE e −5 a −23% no Sul, em todos os anos (o NE quase não sente). Não são feriados nem vésperas; são dias em que boa parte do país está de recesso. A dimensão de datas ganhou a coluna `Recesso` (24/12 a 02/01), que substitui `Vespera` como critério de exclusão das curvas típicas de dia útil.

### Eventos que não deixam rastro (ou deixam rastro ambíguo)

| Evento | Resultado |
|---|---|
| **Crise hídrica 2021** (bandeira de escassez, set/2021–abr/2022) | A carga do SIN em cada mês de 2021–22 fica 1–11% acima do mesmo mês de 2019 — sem sinal de redução por tarifa. Mas 2021 é o ano da "carga global", então qualquer efeito de demanda está escondido pela mudança de medição. Inconclusivo |
| **Eleições** (07 e 28/10/2018; 02 e 30/10/2022, domingos) | ±5% em relação ao domingo anterior, dentro do ruído de um domingo de outubro |
| **Colapso hospitalar de Manaus** (jan/2021) | Norte −4 a −7% em 18–20/01; fraco e sem padrão |
| **Onda de frio de julho/2021** (geada) | Sul +2%; nada |
| **Temporal em SP de 11/10/2024** (Enel, 2 milhões) | SE −2 a −6%, mas 12/10 é feriado; ambíguo |
| **Copa 2018, Brasil × México** | −3% na hora do jogo, contra −10 a −21% nos outros quatro |

### O que muda na tabela

`data/reference/anomalias.csv` passa a ter 41 linhas: 13 de dado, operação e convenção horária (A), 20 de eventos sociais (E), 8 de clima (C); 11 com tratamento `excluir`, 30 `sinalizar`. Efeitos de calendário (feriados, pontos facultativos, recesso) continuam na `dim_datas`.

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

**Atualização (13/09/2026):** a dimensão de datas foi revisada e regenerada — feriados nacionais e móveis passaram a ser calculados a partir da data (Páscoa por algoritmo), e ganhou as colunas `PontoFacultativo`, `Vespera`, `DiaUtil` e `RegimeMetodologico`. Todos os casos acima agora estão corretos na `dim_datas`; as linhas `K` foram retiradas da tabela de anomalias, que fica só com dados, eventos e clima.

### Clima sem documentação (hipóteses)

O Sul responde à temperatura com amplitude que nenhum outro subsistema tem: dezenas de dias com ±15–24% em relação ao mesmo tipo de dia nas semanas vizinhas, quase todos em janeiro–março (calor) ou em frentes frias de outono e primavera. Registrei apenas os casos mais extremos (C3–C7), como hipótese climática, para que a exploração da sazonalidade não os confunda com erro. Exemplo: sábado 09/11/2024 no Sul teve carga diurna de 7,6 GW contra 13–14 GW no sábado anterior — perfil de domingo de inverno, sem ocorrência registrada pelo ONS; provável frente fria após semana quente.

## A tabela `data/reference/anomalias.csv`

| Coluna | Conteúdo |
|---|---|
| `id` | A = anomalia de dado/operação; E = evento social; C = clima |
| `data_inicio`, `data_fim` | Intervalo de datas (inclusive) |
| `hora_inicio`, `hora_fim` | Intervalo de horas (inclusive), vazio = dia inteiro |
| `id_subsistema` | `N`, `NE`, `S`, `SE` ou `*` (todos) |
| `tipo` | `evento_documentado`, `clima_documentado`, `clima_hipotese`, `artefato_provavel`, `nao_explicado`, `convencao_horaria` |
| `tratamento` | `excluir` = fora das curvas típicas e dos extremos; `sinalizar` = entra nos cálculos, com anotação disponível |
| `descricao`, `referencia` | Texto e fonte |

24 linhas em 13/09/2026: 5 `excluir`, 19 `sinalizar`. Efeitos de calendário (feriados, pontos facultativos, vésperas) não ficam aqui — estão na `dim_datas`. A tabela é mantida à mão; toda linha nova precisa de uma entrada neste documento e, quando houver, em [fontes.md](fontes.md).
