# 03 — Metodologia

Regras que valem para toda análise e todo visual do projeto. Cada seção diz o que é **definição oficial**, o que é **verificação nossa** e o que é **decisão nossa**.

## 1. O que é cada observação da fato

**Definição oficial** (dicionário de dados do ONS, v1.2, 06/04/2026): `val_cargaenergiahomwmed` é o "Valor da Carga de Energia, em MWmed"; `din_instante` é a "Data de referência"; nulo não é permitido, zero é permitido, negativo não é permitido.

**Verificação nossa** ([05-qualidade.md](05-qualidade.md)):

- cada linha é a carga média (MWmed) de um subsistema durante uma hora cheia, identificada pelo instante de início (`2025-03-10 15:00:00` = 15h00–15h59);
- os carimbos de hora seguem a **hora oficial de Brasília** em todos os subsistemas — inclusive Norte e Nordeste, que nunca adotaram horário de verão. Nas janelas de horário de verão (01/01–18/02/2017; 15/10/2017–17/02/2018; 04/11/2018–16/02/2019, último do país) a série está em UTC−2 e no restante em UTC−3: nesses trechos as horas aparecem deslocadas +1h, e a hora 0 do dia de início (15/10/2017, 04/11/2018) não existe nos arquivos (verificado pelo horário da rampa noturna do NE, que "muda" de 18h→19h para 17h→18h na semana da transição). O ONS publicou 24 registros também no dia da transição, então a irregularidade não aparece na contagem de horas. Tratamento: essas janelas ficam fora de qualquer análise horária (A8, A8b, A8c em `anomalias.csv`); médias diárias e mensais não são afetadas;
- a média dos 24 valores horários coincide (erro ~1e-12) com a Carga de Energia Diária do ONS para todos os anos completos de 2018 em diante (em 2017, quatro dias do SE divergem até 1,9% — revisões em momentos diferentes). **A curva horária e a base diária são a mesma série**, portanto a metodologia documentada para a diária vale integralmente para a horária.

**Leitura para a persona:** "quanta potência, em média, o sistema precisou entregar a essa parte do país durante essa hora".

## 2. Os três regimes metodológicos

O ONS mudou o que entra na conta da carga duas vezes dentro da janela do projeto.

**Definição oficial** (descrição do dataset Carga de Energia Diária, ONS Dados Abertos, consultada em 13/09/2026):

> "Até fevereiro/2021, os dados representam a carga atendida por usinas despachadas e/ou programadas pelo ONS, com base em dados recebidos pelo Sistema de Supervisão e Controle do ONS. Entre março/2021 e abril/23, os dados representam a carga atendida por usinas despachadas e/ou programadas pelo ONS, com base em dados recebidos pelo Sistema de Supervisão e Controle do ONS, mais a previsão de geração de usinas não despachadas pelo ONS. A partir de 29/04/2023, além dos dados anteriormente considerados, passou a ser incorporado o valor estimado da micro e minigeração distribuída (MMGD), com base em dados meteorológicos previstos."

A data exata do primeiro marco aparece no Boletim Diário da Operação do ONS: "a partir de 02/03/2021, passou a ser considerado o conceito de carga global".

| Era | Vigência | O que a carga inclui | Rótulo no projeto |
|---|---|---|---|
| 1 | 01/01/2017 → 01/03/2021 | Geração das usinas despachadas/programadas pelo ONS (medida pela supervisão) | `Supervisão ONS` |
| 2 | 02/03/2021 → 28/04/2023 | Era 1 **+** previsão de geração das usinas não despachadas | `Carga global` |
| 3 | 29/04/2023 → hoje | Era 2 **+** estimativa da MMGD (a partir de previsão meteorológica) | `Carga global + MMGD` |

**Interpretação nossa:** cada marco *adiciona* uma parcela que antes não era contada. A série tende a subir em degraus nessas datas por razão de medição, não de demanda. A parcela adicionada em 2023 tem forte perfil intradiário (solar: zero à noite, máxima ao meio-dia), então ela altera não só o nível, mas o **formato** da curva.

**Decisões nossas:**

1. As datas 02/03/2021 e 29/04/2023 aparecem como marcos em todo gráfico histórico e a coluna/medida `RegimeMetodologico` fica disponível no modelo.
2. Não se produz afirmação do tipo "a demanda cresceu X% entre 2019 e 2025". A forma aceitável é: "a carga registrada aumentou X% no período, que atravessa duas mudanças de metodologia".
3. Comparações quantitativas de nível e formato usam o **núcleo comparável 2024–2025**.
4. O histórico 2017–2023 serve para estrutura, sazonalidade e rupturas — sempre com o regime identificado.

**Pendência:** o ONS menciona nota técnica sobre a estimativa de MMGD no portal SINtegre (acesso restrito). Não localizada em fonte aberta. O [Roteiro de Carga Atendida por MMGD](https://www.ons.org.br/SCPCB/Paginas/cicloestudos/2024-2028/Roteiro_Carga_Atendida_por_MMGD.pdf) descreve os insumos (potência instalada da ANEEL, irradiação do INPE, fator de capacidade do ONS).

## 3. Janelas e comparação YTD

| Janela | Uso |
|---|---|
| 2017–2025 | Contexto, padrões, rupturas, evolução do formato (2017–2019 sob a metodologia original) |
| 2024–2025 | Comparações quantitativas rigorosas |
| 2026 YTD | Somente contra o mesmo intervalo de datas dos anos anteriores |

**Regra YTD:** se o último dia disponível de 2026 é D, toda comparação com 2024 e 2025 usa 01/01 → D daqueles anos. Nunca comparar média ou total parcial de 2026 com ano completo. O relatório de qualidade informa D a cada extração.

## 4. Calendário e "dia típico"

**Decisões nossas:**

- Curvas típicas são calculadas **por tipo de dia** (dia útil, sábado, domingo, feriado) e nunca misturam os quatro numa média única.
- Feriados nacionais contam como "feriado" mesmo caindo em fim de semana; Carnaval (segunda e terça) e Corpus Christi contam como feriado; Quarta-feira de Cinzas é dia útil.
- Vésperas de Natal e de Ano-Novo (`dim_datas[Vespera]`) ficam fora das curvas típicas de dia útil: caem 16–24% e se comportam como sábado.
- As janelas de horário de verão (2017–2019) ficam fora das curvas horárias (ver §1).
- Ao comparar meses entre anos, lembrar que Carnaval e Páscoa mudam de data e que a quantidade de fins de semana varia.
- 2020 não entra na definição de "típico" para o histórico; é analisado à parte.
- Dias sinalizados como anômalos pelo diagnóstico de qualidade (saltos hora a hora) são investigados antes de entrar em curva típica; a decisão de excluir ou manter é registrada em [06-decisoes.md](06-decisoes.md).

## 5. Métricas derivadas

Definidas sobre um dia × subsistema (ou sobre o SIN, somando os quatro):

| Métrica | Definição | Unidade |
|---|---|---|
| Carga média | média das 24 horas | MWmed |
| Energia do dia | soma das 24 horas | MWh |
| Pico | máximo horário | MWmed |
| Vale | mínimo horário | MWmed |
| Hora do pico / do vale | hora em que ocorrem | h |
| Amplitude absoluta | pico − vale | MWmed |
| Amplitude relativa | (pico − vale) ÷ carga média | adimensional |
| Fator de carga | carga média ÷ pico | adimensional (0–1) |

Para o SIN, pico e vale são calculados sobre a **soma horária** dos subsistemas (não a soma dos picos, que ocorrem em horas diferentes).

## 6. Curvas normalizadas

O projeto separa **nível** (quanto) de **formato** (quando). Para comparar formato entre subsistemas de tamanhos muito diferentes (SE ≈ 6× N) e entre anos com metodologias diferentes, usa curvas normalizadas.

Três candidatas, cada uma respondendo a uma pergunta diferente:

| Normalização | Fórmula | O que preserva | Limitação |
|---|---|---|---|
| **Pela média do dia** | carga(h) ÷ média do dia | Formato e amplitude relativa; valor 1,0 = "hora média" | Sensível a dias atípicos; ainda carrega o efeito intradiário da MMGD |
| **Pelo pico do dia** | carga(h) ÷ pico do dia | "Quão cheio está o sistema" em cada hora; 1,0 = pico | Esconde diferenças de amplitude quando o pico é agudo |
| **Min-max** | (carga(h) − vale) ÷ (pico − vale) | Só o formato, 0 = vale, 1 = pico | Perde nível e amplitude; duas curvas com amplitude muito diferente ficam idênticas |

**Decisão nossa (preliminar, a confirmar na exploração):** a normalização **pela média do dia** é a principal — é a mais legível para a persona ("às 19h a demanda está 14% acima da média do dia") e preserva a amplitude. A **pelo pico** entra como complementar quando a pergunta for sobre o pico. Min-max não será usada.

A normalização reduz o efeito de escala, mas **não elimina a quebra metodológica**: a MMGD altera o formato, não só o nível. Os marcos continuam visíveis em gráficos normalizados.

## 7. Revisões do ONS

**Definição oficial:** "Os dados disponibilizados fazem parte de um processo de consistência recorrente e, portanto, podem ser atualizados após a sua publicação."

**Verificação nossa:** já ocorreu dentro do projeto. A extração de 22/08/2026 diverge da base diária publicada em 13/09/2026 em dias de maio e junho de 2026 (até 2,9% no NE em 30/05). Anos completos não divergiram.

**Decisões nossas:**

- a data de extração (do `manifest.csv`) aparece no dashboard;
- o `extract_ons.py` detecta arquivos alterados pelo hash e registra no manifest;
- antes de qualquer entrega, rodar extração + consolidação + `quality_check.py` e revisar a seção de reconciliação.

## 8. Clima, economia e causalidade

O projeto não incorpora base meteorológica nem econômica. Quando uma anomalia exigir contexto, o clima pode ser consultado como fonte externa, e a redação deve distinguir tendência, sazonalidade, evento e possível efeito climático — sem apresentar causalidade como comprovada.
