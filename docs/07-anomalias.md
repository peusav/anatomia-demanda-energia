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
