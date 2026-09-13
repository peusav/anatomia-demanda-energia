# 01 — O projeto

## Em uma frase

**Mais importante do que saber quanto de energia o Brasil demanda é entender quando essa demanda acontece, onde ela se concentra e como seu formato vem mudando ao longo do tempo.**

## O que é

Projeto de portfólio em análise e visualização de dados, com entrega principal em Power BI, sobre a **carga** do sistema elétrico brasileiro — a demanda que o Sistema Interligado Nacional (SIN) precisa atender, hora a hora, em cada um dos seus quatro subsistemas.

Não é um estudo do setor elétrico. É uma leitura estruturada de um único fenômeno — o formato da demanda no tempo — feita com dados públicos e oficiais do ONS.

## Pergunta central

> Como o padrão da demanda de energia elétrica brasileira varia ao longo do tempo e entre subsistemas, e como seu formato vem mudando?

A pergunta combina quatro dimensões: **nível**, **tempo**, **geografia** e **mudança histórica**.

## Persona

Uma pessoa analítica, não especialista no setor elétrico, que quer compreender rapidamente como a demanda elétrica brasileira funciona e como ela mudou. O produto não pressupõe conhecimento de SIN, subsistema, MWmed ou curva de carga; os conceitos indispensáveis são explicados de forma breve (ver [02-dominio-e-glossario.md](02-dominio-e-glossario.md)).

## Famílias de perguntas

As perguntas abaixo são hipóteses de exploração, não uma narrativa a ser forçada sobre os dados. O produto final deve responder às que os dados sustentarem.

| Família | Perguntas |
|---|---|
| **Quanto?** | Qual é o nível da carga? Como evolui no tempo? Onde está concentrada? Quais períodos têm maiores e menores níveis? |
| **Quando?** | Como a carga se distribui pelas 24 horas? Como muda entre dias úteis, sábados, domingos e feriados? Como varia entre meses? Em que horários aparecem pico e vale? |
| **Onde?** | Como Norte, Nordeste, Sul e Sudeste/Centro-Oeste diferem? Diferem só em escala ou também em formato? Quais têm maior amplitude intradiária? |
| **Como mudou?** | O horário do pico mudou? A diferença entre pico e vale mudou? O perfil intradiário mudou? Os subsistemas estão convergindo? O fim de semana mudou? |
| **O que foge do padrão?** | Há dias ou períodos atípicos? Sazonalidade explica? É ruptura metodológica? É choque externo? |

## Escopo

**Núcleo: carga + tempo + subsistema.**

Dentro do escopo inicial:

- evolução da carga no tempo;
- sazonalidade intradiária, semanal e anual;
- diferenças entre os quatro subsistemas do SIN;
- dias úteis × fins de semana × feriados;
- perfil horário, pico, vale e amplitude;
- curvas absolutas e normalizadas;
- evolução histórica do formato;
- identificação descritiva de padrões, rupturas e eventos atípicos;
- documentação das mudanças metodológicas da série.

Fora do escopo inicial: previsão de demanda; geração por fonte; balanço oferta × demanda; preço e PLD; tarifas e contratos; mercado livre × regulado; hidrologia e reservatórios; despacho; transmissão e intercâmbios; operação de usinas; causalidade econômica; explicação abrangente do setor.

## Fontes

- **Núcleo:** ONS — [Curva de Carga Horária](https://dados.ons.org.br/dataset/curva-carga). Única fato do produto.
- **Validação:** ONS — [Carga de Energia Diária](https://dados.ons.org.br/dataset/carga-energia). É a mesma série agregada por dia (verificado em [05-qualidade.md](05-qualidade.md)).
- **Não usado:** ONS — Balanço de Energia nos Subsistemas. Traria geração e intercâmbio, deslocando o foco de demanda para oferta.
- **Expansão possível, não iniciada:** EPE (consumo por UF/classe) e IBGE (população), apenas se um achado do ONS exigir contextualização territorial. Ver [06-decisoes.md](06-decisoes.md).

Detalhes, URLs e datas de acesso em [fontes.md](fontes.md).

## Janelas temporais

| Janela | Período | Finalidade |
|---|---|---|
| Histórico estendido | 2019–2025 | Estrutura, padrões, sazonalidade, rupturas e evolução do formato — com os marcos metodológicos explicitados |
| Núcleo comparável | 2024–2025 | Dois anos completos sob a metodologia atual. Referência para comparações quantitativas mais rigorosas |
| Atual | 2026 YTD | Somente por períodos equivalentes: mesmo intervalo de datas em 2024 e 2025 |

Por que não uma série homogênea: a definição de "carga" mudou em 02/03/2021 e em 29/04/2023. Ver [03-metodologia.md](03-metodologia.md).

## Contexto histórico da janela (para investigação, não como explicação)

| Ano | Contexto |
|---|---|
| 2019 | Referência pré-pandemia |
| 2020 | Choque da COVID-19 — período extraordinário, não define "normal" |
| 2021 | Recuperação + mudança metodológica (carga global) |
| 2022 | Normalização |
| 2023 | Transição: incorporação da MMGD estimada a partir de 29/04 |
| 2024–2025 | Período recente mais comparável |
| 2026 | Ano corrente, parcial |

## Arquitetura conceitual do produto

Três camadas, que não precisam virar três páginas:

1. **A demanda brasileira em perspectiva** — quanto o sistema demanda, como evoluiu, onde se concentra, com os marcos metodológicos visíveis.
2. **Anatomia de um dia** — como a carga se distribui pelas 24 horas, por subsistema e tipo de dia. Assinatura visual do projeto.
3. **Como o perfil mudou** — curvas normalizadas, evolução do horário do pico e da amplitude, aproximação ou afastamento entre subsistemas.

Uma camada de anomalias só existirá se a exploração revelar achados fortes.

## Princípios analíticos

1. Começar por perguntas, não por gráficos.
2. Entender a variável antes de compará-la — a definição da carga é parte do produto.
3. Separar histórico amplo de período homogêneo.
4. Comparar períodos equivalentes (YTD com a mesma data de corte).
5. Não confundir nível com formato.
6. Controlar o calendário (dia da semana, feriados, eventos móveis).
7. Tratar 2020 como excepcional.
8. Distinguir tendência, sazonalidade e evento.
9. Não atribuir causalidade sem evidência.
10. Explicitar limitações.
11. Deixar a exploração refinar o produto.
12. Priorizar clareza e parcimônia: poucos visuais fortes.
13. Manter o produto acessível à persona.
14. Preservar rastreabilidade: fontes, datas de extração, transformações.

## Entrega inicial esperada

- Dashboard em Power BI com uma ou duas páginas e quatro ou cinco visuais centrais.
- Notas metodológicas sobre 2021, 2023, 2020 e 2026 YTD.
- Esta documentação.
