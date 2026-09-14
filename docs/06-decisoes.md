# 06 — Decisões analíticas

Registro curto das decisões que não são dedutíveis do código. Formato: contexto → decisão → consequência. Novas decisões entram no fim, com data.

## D01 — Curva de Carga Horária como única fato

**Contexto.** O ONS publica carga em três bases: horária, diária e no balanço de energia (com geração e intercâmbio).
**Decisão.** Usar só a horária. A diária serve para validar; o balanço fica fora.
**Consequência.** O produto consegue falar de formato (quando), que é sua tese. Verificou-se depois que a diária é a média exata da horária, então nada se perde. Geração e oferta não entram, mantendo o escopo em demanda.

## D02 — Janela 2019–2026

**Contexto.** O ONS tem histórico desde 2000.
**Decisão.** Começar em 2019 (um ano pré-pandemia como âncora) e ir até o ano corrente.
**Consequência.** A janela atravessa COVID e duas mudanças metodológicas — rica para padrões e rupturas, inadequada para "crescimento acumulado". Exige as janelas de D03.

## D03 — Três janelas: histórico, núcleo comparável, YTD

**Contexto.** Definição de carga mudou em 02/03/2021 e 29/04/2023; 2026 é parcial.
**Decisão.** 2019–2025 para estrutura e rupturas; 2024–2025 para comparações rigorosas; 2026 só YTD contra o mesmo intervalo.
**Consequência.** Todo visual histórico carrega os marcos; nenhum KPI compara 2026 com ano cheio.

## D04 — Curvas típicas por tipo de dia

**Contexto.** Dia útil, sábado, domingo e feriado têm formatos distintos.
**Decisão.** Nunca calcular "dia médio" misturando tipos; segmentar por `TipoDia`.
**Consequência.** Toda curva típica é qualificada ("dia útil de 2025 no SE").

## D05 — Normalização principal pela média do dia

**Contexto.** Três candidatas avaliadas em [03-metodologia.md](03-metodologia.md) §6.
**Decisão (preliminar).** carga(h) ÷ média do dia como principal; ÷ pico como complementar; min-max descartada.
**Consequência.** Formato e amplitude relativa ficam comparáveis entre subsistemas e anos. Revisar após a exploração.

## D06 — `id_subsistema` como chave; rótulo único para SE

**Contexto.** `nom_subsistema` muda de `SUDESTE` para `SUDESTE/CENTRO-OESTE` em 2026 (dicionário v1.2).
**Decisão.** Relacionamentos e filtros usam o código; o rótulo de exibição é "Sudeste/Centro-Oeste" para todo o período.
**Consequência.** O Sudeste não se parte em duas séries no Power BI.

## D07 — EPE/IBGE só depois, e só se ajudar

**Contexto.** Há interesse em relacionar carga com população/consumo por UF. Subsistema do ONS não coincide com região do IBGE.
**Decisão.** Nenhuma camada territorial antes de concluir a exploração do ONS. Se entrar, a EPE fornece consumo (não carga) e a compatibilidade subsistema × UF precisa de fonte oficial.
**Consequência.** Evita dois projetos paralelos e evita a divisão ingênua "população da região NE ÷ carga do subsistema NE".

## D08 — Sem base meteorológica na primeira versão

**Contexto.** Temperatura explica parte das anomalias.
**Decisão.** Não incorporar. Consultar clima como contexto pontual quando uma anomalia exigir.
**Consequência.** Anomalias são descritas, não explicadas causalmente.

## D09 — Dados brutos versionados

**Contexto.** O ONS revisa dados após publicação; o portal pode mudar.
**Decisão.** Versionar `data/raw/*.parquet` (≈3,7 MB), o manifest e o consolidado (≈2,8 MB).
**Consequência.** Qualquer pessoa reproduz exatamente a análise da data de extração, mesmo que o ONS revise os arquivos.

## D10 — Tratamento das anomalias horárias (13/09/2026)

**Contexto.** O diagnóstico sinalizou 25 saltos hora a hora acima de 25%. Investigação em [07-anomalias.md](07-anomalias.md).
**Decisão.** 15/08/2023 (apagão nacional, documentado pelo ONS) sai de todas as curvas típicas e recebe anotação nos gráficos históricos. Abril/2020 no Norte fica sinalizado como "não explicado" (já excluído das típicas por D04). Os pontos isolados de 22/12/2021 (NE) e 08/11/2024 (N) são mantidos como prováveis artefatos. Os domingos do Sul são comportamento normal e não recebem tratamento.
**Consequência.** Uma tabela `anomalias` (data, subsistema, classificação) entra no modelo para excluir/anotar; o `quality_check.py` passa a comparar saltos com o mesmo horário de semanas vizinhas.

## D11 — Tabela de anomalias fora do Power BI (13/09/2026)

**Contexto.** A varredura ampla ([07-anomalias.md](07-anomalias.md), parte 2) produziu 37 registros entre artefatos, eventos, clima e calendário.
**Decisão.** Manter em `data/reference/anomalias.csv`, versionado e mantido à mão, e importar no Power BI — não criar como tabela "Inserir dados" nem como coluna da fato.
**Consequência.** A mesma lista serve à exploração em Python e ao dashboard; o histórico de mudanças fica no git; a fato continua cópia fiel do ONS. Medidas de máximo/recorde devem excluir `tratamento = excluir`.

## D12 — Dimensão de datas calculada, não transcrita (13/09/2026)

**Contexto.** A revisão completa da `dim_datas` encontrou 27 divergências de feriado herdadas da planilha (Independência em 07/07 em 2024–2026; Carnaval só na terça, errado em 2019 e ausente em 2026; Corpus Christi só em 2023) e duas convenções de semana misturadas.
**Decisão.** O gerador passa a calcular feriados nacionais e móveis a partir da data (Páscoa pelo algoritmo de Meeus), usa ISO 8601 para semana, e acrescenta `PontoFacultativo`, `Vespera`, `DiaUtil` e `RegimeMetodologico`. A planilha fornece apenas a lista de datas.
**Consequência.** Efeitos de calendário saem da tabela de anomalias; curvas típicas usam `TipoDia` e `Vespera`; o regime metodológico vem da dimensão, não de medida.

## D13 — Normalização pela média do dia confirmada (13/09/2026)

**Contexto.** D05 era preliminar; o bloco 7 comparou as três candidatas sobre as mesmas curvas.
**Decisão.** Normalização principal = carga(h) ÷ média do dia. Pelo pico fica como medida complementar; min-max descartada (apaga a amplitude).
**Consequência.** Todas as curvas normalizadas do produto usam a mesma definição; a leitura é "% acima/abaixo da média do dia".

## D14 — Série ampliada para 2017–2026 (13/09/2026)

**Contexto.** O bloco 8 mostrou uma virada de formato entre 2019 e 2021 grande demais para repousar num único ano pré-pandemia, cujo verão tinha só 25 dias válidos após excluir o horário de verão.
**Decisão.** Estender a extração para 2017 (três anos sob "Supervisão ONS": 2017, 2018, 2019). O histórico estendido passa a ser 2017–2025; o núcleo comparável (2024–2025) e a regra YTD não mudam.
**Consequência.** Duas janelas a mais de horário de verão excluídas das curvas horárias (A8b, A8c); a hora inexistente do início do horário de verão entra como nulo no consolidado; a dimensão de datas é gerada para 2017–2026 a partir do próprio intervalo, sem depender da planilha; o consolidado passa a se chamar `CURVA_CARGA_2017_2026.parquet`.

## Pendentes (a decidir na exploração)

- Abrir a camada EPE (consumo por classe e UF) para decidir H7 (Norte e Nordeste crescem pela baixa tensão)? É o primeiro achado do ONS que pede a EPE; decidir na síntese.


- ~~Tratamento dos saltos hora a hora~~ → resolvido em D10.
- Confirmar a normalização principal (D05).
- Se a dimensão de hora entra como tabela própria (0–23, rótulo, período do dia) — o regime metodológico já está na `dim_datas`.
