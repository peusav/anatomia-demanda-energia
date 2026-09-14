# Bloco 11 — Hipóteses a partir de material especializado

> Escrito à mão em 14/09/2026, a partir de notas técnicas do ONS/EPE/CCEE e de literatura sobre curvas de carga. Cada hipótese traz a fonte, o que os blocos anteriores já mostram, o que faltaria para decidir e o que muda no produto. Nada aqui é conclusão: é o mapa do que a literatura diz que deveria aparecer nos dados — e do que apareceu.

## Fontes consultadas

| Documento | Instituição | O que traz para o projeto |
|---|---|---|
| NT EPE-DEA-SEE-001/2025 · ONS DPL 0013/2025 · CCEE 02434/2025 — *Previsão de carga para o Planejamento Anual da Operação Energética 2025–2029* | EPE, ONS, CCEE | Leitura oficial de 2024 (calor, renda, classes), projeção por subsistema, **geração de MMGD por subsistema em MWmed**, método de perfis típicos, premissa de Roraima |
| NT ONS DPL 0119/2024 · EPE-DEA-SEE-009/24 — *Projeção de carga global de demanda máxima considerando os efeitos da Portaria Normativa nº 50/2022* | ONS, EPE, CCEE | Migração de consumidores ao mercado livre e seu efeito na **demanda máxima noturna** |
| IT-EPE-DEA-SEE-001/2021 — *Metodologia para criação de séries horárias de geração distribuída fotovoltaica por subsistema* | EPE | Como se estima o perfil horário da MMGD (o que o ONS soma à carga desde 2023) |
| Literatura da "curva do pato" (CAISO; artigos brasileiros sobre GD fotovoltaica) | diversos | Vocabulário e mecanismo: carga líquida, barriga do meio-dia, rampa da noite |

Referências completas em [../fontes.md](../fontes.md).

## H5 — A migração ao mercado livre está aumentando a demanda noturna

**O que a literatura diz.** A Portaria Normativa MME nº 50/2022 permitiu, a partir de janeiro de 2024, que consumidores do grupo A com demanda abaixo de 500 kW migrassem ao Ambiente de Contratação Livre. O ONS, a EPE e a CCEE escreveram uma nota técnica só para estimar "possíveis incrementos na demanda máxima, especialmente no período noturno": no mercado regulado esses consumidores pagam tarifa horossazonal, com ponta cara entre ~18h e 21h, e evitam consumir nesse horário; no mercado livre esse sinal desaparece. A nota projeta o efeito com curvas de adoção (Bass) e perfis típicos por distribuidora.

**O que os dados mostram.** A noite (18–21h) ganhou peso exatamente a partir de 2024, sob regime homogêneo: no SIN, de +8,6% (2024) para +10,7% (2025) e +12,0% (2026 YTD) em relação à média do dia. Em MW absolutos, nos dias úteis de 1º/jan–11/set: a noite do SE subiu de 50,4 para 51,7 GW enquanto o meio do dia **caiu** de 49,6 para 47,9 GW; no NE, noite +8% e meio-dia parado. O desconto de domingo também encolheu desde 2024 no SE e no Sul.

**O que não dá para separar.** O mesmo período tem a expansão da MMGD (que reduz o meio-dia e, por normalização, "sobe" a noite) e o calor de 2024–2025. A migração ao ACL é uma terceira força na mesma direção — e a única das três que age *só* sobre a noite de dias úteis. Um teste possível: se H5 é relevante, o ganho da noite deve ser maior em dias úteis do que em fins de semana (tarifa de ponta não vale em sábados e domingos) e maior no SE/S (onde está a maior parte dos consumidores do grupo A) do que no N.

**Para o produto.** A frase "a noite cresce" tem pelo menos três causas plausíveis; o texto do dashboard não deve atribuir a uma só.

## H6 — Calor mais renda: a climatização está reescrevendo o verão

**O que a literatura diz.** A nota de previsão de carga descreve 2024 como "excepcionalmente quente", com El Niño no primeiro semestre e ondas de calor, e afirma que "as boas condições do mercado de trabalho […] ao favorecer o aumento da posse e do uso de equipamentos elétricos, acabam por reforçar o efeito da temperatura sobre o consumo, principalmente devido à climatização de ambientes". Consumo residencial +9,7% e comercial +7,4% até outubro de 2024. A EPE projeta o residencial crescendo 3,6% ao ano até 2029, acima do total.

**O que os dados mostram.** É a explicação que costura os blocos 2, 3 e 6: os máximos anuais sobem enquanto os mínimos não (bloco 2); a amplitude sazonal do SE e do Sul depende de quão quente foi o verão, e 2025 foi o ano mais sazonal da série (bloco 3); os dias mais pesados são os mais planos, porque o ar-condicionado enche a tarde (bloco 6). O Norte ficando mais sazonal (bloco 3) é o mesmo fenômeno chegando a uma região onde a carga era industrial e plana.

**O que faltaria.** Temperatura por subsistema (INMET) para separar "mais calor" de "mais aparelhos". A EPE faz isso com modelos de carga × temperatura; o projeto decidiu não fazer (D08).

**Para o produto.** Sustenta a frase-síntese do bloco 6 — *o verão estressa o nível; o inverno estressa o formato* — e explica por que os recordes de carga se concentram em fevereiro.

## H7 — Norte e Nordeste crescem pela baixa tensão

**O que a literatura diz.** "Entre os subsistemas, observa-se um crescimento mais alto no Norte e no Nordeste. […] Também no Nordeste, o desempenho no período possui relação com o consumo da baixa tensão, enquanto o consumo industrial deve crescer menos que a média do SIN." Ou seja: quem puxa N e NE é o consumidor residencial e comercial pequeno, não a indústria.

**O que os dados mostram.** O Norte é o subsistema que mais cresce sob regime homogêneo (+6% ao ano, bloco 2) e o que mais mudou de sazonalidade (bloco 3); ambos são compatíveis com residencial + climatização crescendo sobre uma base industrial estável. Mas a base industrial continua visível: o domingo do Norte cai só 8% (bloco 3) e o dia é o mais plano do país (bloco 4).

**O que faltaria.** Consumo por classe e por UF (EPE, Consumo Mensal), o passo natural da camada territorial. É a primeira vez que um achado do ONS pede a EPE — e o que o projeto disse que esperaria antes de abri-la.

## H8 — Roraima interligado desde fevereiro de 2026

**O que a literatura diz.** A nota de 2025 adota como premissa "interligação de Roraima ao subsistema Norte em fevereiro/2026", com impacto "sobretudo no consumo na baixa tensão".

**O que os dados mostram.** Nada visível: a média mensal do Norte em fevereiro e março de 2026 fica +5,4% e +4,4% sobre 2025, *abaixo* do crescimento de janeiro (+7,2%) e muito abaixo do de agosto–setembro (+9 a +10%). Roraima (~300 MW, ~3,5% do Norte) ou ainda não está na série, ou entrou de forma gradual, ou a premissa não se realizou. Registrado em [../fontes.md](../fontes.md) como pendência; não afeta nenhuma conclusão.

## H9 — A "curva do pato" chegou ao Nordeste pelo lado da carga

**O que a literatura diz.** A curva do pato (CAISO, 2013) descreve a *carga líquida* — demanda menos geração solar e eólica — com a barriga no meio do dia e o pescoço na rampa da noite. No Brasil, a discussão concentra-se no Nordeste, onde a geração eólica e solar centralizada já é cortada em momentos de excesso e a complementaridade (vento à noite, sol de dia) é o que sustenta o sistema.

**O que os dados mostram.** A série do ONS é *carga*, não carga líquida; a geração centralizada não entra. Mesmo assim o Nordeste já exibe a barriga: o meio do dia está abaixo da média do dia desde 2025 (bloco 8), porque a MMGD — que é abatida da carga antes de o ONS a medir e só parcialmente devolvida pela estimativa — faz o papel do "menos solar" da definição. A nota da EPE dá a escala: MMGD estimada de **1.182 MWmed no NE em 2025**, 8,9% da carga média; como a fotovoltaica concentra sua produção em ~6 horas, isso equivale a 25–30% da carga do meio-dia. É o suficiente para explicar a virada do pico para a noite.

**Para o produto.** É o nome que a persona vai reconhecer. A Camada 3 pode chamar o achado do NE de "curva do pato da carga" — com a nota de que a curva do pato oficial (carga líquida) é ainda mais funda.

## H10 — O método do dia típico coincide com o do ONS/EPE

**O que a literatura diz.** Para projetar a demanda máxima, ONS/EPE/CCEE calculam "perfis típicos de demanda máxima para cada subsistema, sistema e SIN por mês", usando K-means para agrupar dias por similaridade, e projetam a demanda instantânea a partir da integrada por um fator mensal.

**O que os dados mostram.** O projeto chegou ao mesmo lugar por outro caminho: curva típica por subsistema × tipo de dia × mês (bloco 4) e a distinção entre pico horário integrado e instantâneo (bloco 2, recorde de 106.149 MWmed contra 106.532 MW instantâneos).

**Para o produto.** Validação de método. Uma extensão possível — agrupar dias por formato (K-means) em vez de por calendário — fica como ideia, não como pendência.

## H11 — Existe uma "carga global recomposta" que homogeneíza o histórico

**O que a literatura diz.** A nota de 2025 diz que a projeção de demanda usou "a Carga Global recomposta com MMGD no período 2018 a 2022". Ou seja, o ONS e a EPE mantêm uma versão do histórico em que os anos anteriores aos marcos foram *recompostos* na metodologia atual.

**O que isso significa para o projeto.** Essa série resolveria a quebra metodológica que o projeto contorna com as três janelas. Não está no portal de dados abertos. Registrada como pendência de pesquisa: se for publicada, substitui a regra "não comparar através dos marcos" por uma comparação direta.

## H12 — Quanto da carga já é atendida por MMGD, por subsistema

**O que a literatura diz.** Tabela 8 da nota de 2025 (MWmed, geração de MMGD): Norte 450; Nordeste 1.182; Sudeste/CO 3.240; Sul 1.256; SIN 6.128 em 2025, crescendo 9,1% ao ano até 2029, quando atenderá "cerca de 11% do consumo".

**O que os dados mostram.** Em relação à carga média de 2025 (bloco 2): N 5,4%, NE 8,9%, SE 7,3%, S 9,1%, SIN 7,7%. O bloco 10 mediu o mesmo fenômeno pela potência instalada da ANEEL (NE 67%, S 89% da carga média); a EPE converte potência em energia com o fator de capacidade (~11–13%), o que explica a diferença de escala. As duas medidas contam a mesma história e a da EPE é a mais fácil de explicar à persona: **"um em cada doze MWh do Nordeste já vem do telhado".**

## Síntese: o que a literatura acrescentou

1. Uma terceira causa para a noite crescer (mercado livre), além de MMGD e clima — e um teste para separá-la (dias úteis × fins de semana).
2. A confirmação oficial de que 2024 foi um ano de calor e renda, e de que residencial e comercial lideram — o que fecha a leitura dos blocos 2, 3 e 6.
3. A pista de que Norte e Nordeste crescem pela baixa tensão — a primeira demanda concreta por dados da EPE.
4. Uma premissa (Roraima em fev/2026) que os dados não confirmam.
5. O vocabulário "curva do pato" e a escala da MMGD em energia, que tornam o achado do Nordeste narrável.
6. A existência de um histórico recomposto que, se publicado, mudaria a metodologia.
