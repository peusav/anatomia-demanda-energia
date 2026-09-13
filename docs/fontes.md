# Fontes

Toda fonte consultada, com o que foi extraído dela. Onde a informação é definição oficial, o texto está citado verbatim nos documentos que a usam. Data de acesso no formato dd/mm/aaaa.

## ONS — Operador Nacional do Sistema Elétrico

| Título | URL | Tipo | Publicação / atualização | Acesso | Uso |
|---|---|---|---|---|---|
| Curva de Carga Horária (conjunto de dados) | https://dados.ons.org.br/dataset/curva-carga | Dataset + metadados CKAN | Atualizado 13/09/2026 15:01 UTC; arquivos históricos reprocessados em 09/10/2025 | 13/09/2026 | Fato do projeto; descrição, frequência, licença, aviso de consistência |
| Dicionário de Dados — Curva de Carga Horária, v1.2 | https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/curva-carga-ho/DicionarioDados_CurvaCarga.pdf | PDF | 06/04/2026 (v1.0 em 10/03/2022; v1.1 em 02/05/2023) | 13/09/2026 | Definição das colunas; regras de nulo/zero/negativo; explicação da troca de `nom_subsistema` |
| Carga de Energia Diária (conjunto de dados) | https://dados.ons.org.br/dataset/carga-energia | Dataset + metadados CKAN | Atualizado 13/09/2026 15:01 UTC | 13/09/2026 | Texto oficial dos três regimes metodológicos; base de reconciliação |
| Dicionário de Dados — Carga de Energia Diária | https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/carga_energia_di/DicionarioDados_Carga_Energia_Diaria.pdf | PDF | 16/08/2021 | 13/09/2026 | Colunas da base diária (`val_cargaenergiamwmed`) |
| O que é o SIN | https://www.ons.org.br/paginas/sobre-o-sin/o-que-e-o-sin | Página institucional | — | 13/09/2026 | Definição do SIN e dos quatro subsistemas |
| Boletim Diário da Operação, 01/08/2023 | https://sdro.ons.org.br/SDRO/DIARIO/2023_08_01/index.htm | Boletim | 01/08/2023 | 13/09/2026 | Data exata do marco de carga global (02/03/2021) e da MMGD (29/04/2023) |
| Boletim Diário da Operação, 15/08/2023 — Principais Ocorrências no SIN | https://sdro.ons.org.br/SDRO/DIARIO/2023_08_15/HTML/18_PrincipaisOcorrenciasSIN.html | Boletim | 15/08/2023 | 13/09/2026 | Apagão de 15/08/2023: cargas interrompidas por submercado; **composição dos subsistemas por estado** |
| Ocorrência no SIN em 15 de agosto de 2023 | https://www.ons.org.br/Paginas/Noticias/Ocorr%C3%AAncia-no-SIN-em-15-de-agosto-de-2023.aspx | Notícia institucional | 08/2023 | 13/09/2026 | Causa do apagão (LT Quixadá–Fortaleza II) |
| Boletins Diários da Operação de 22/12/2021, 08/11/2024 e 09/11/2024 | https://sdro.ons.org.br/SDRO/DIARIO/{AAAA_MM_DD}/HTML/18_PrincipaisOcorrenciasSIN.html | Boletim | — | 13/09/2026 | "Sem ocorrências significativas" nas datas dos picos isolados A3 e A4 |
| Sistema Interligado Nacional registra quarto recorde de demanda instantânea em 2025 — MME | https://www.gov.br/mme/pt-br/assuntos/noticias/sistema-interligado-nacional-registra-quarto-recorde-de-demanda-instantanea-de-energia-em-2025 | Notícia institucional | 02/2025 | 13/09/2026 | Recordes de fevereiro/2025 (106.532 MW em 26/02 às 14h27) — valida o máximo da série |
| Incêndio em subestação provoca apagão na madrugada em todas as regiões — Agência Brasil | https://agenciabrasil.ebc.com.br/geral/noticia/2025-10/incendio-em-subestacao-provoca-apagao-na-madrugada-em-todas-regioes | Notícia (EBC) | 14/10/2025 | 13/09/2026 | Apagão de 14/10/2025: causa, cargas interrompidas por subsistema, recomposição |
| Roteiro — Carga Atendida por MMGD (ciclo 2024–2028) | https://www.ons.org.br/SCPCB/Paginas/cicloestudos/2024-2028/Roteiro_Carga_Atendida_por_MMGD.pdf | PDF | — | 13/09/2026 | Insumos da estimativa de MMGD (ANEEL, INPE, ONS) |
| Programa de dados abertos da AWS — ONS | https://registry.opendata.aws/ons-opendata-portal/ | Registro | — | 13/09/2026 | Origem dos arquivos no S3 |

## EPE — Empresa de Pesquisa Energética (expansão futura, ainda não usada)

| Título | URL | Tipo | Acesso | Uso previsto |
|---|---|---|---|---|
| Nota Técnica EPE DEA-SEE 009/2023 — Aprimoramento na metodologia de estimação da geração de micro e minigeradores fotovoltaicos distribuídos | https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-789/Aprimoramento%20na%20Metodologia%20de%20Estima%C3%A7%C3%A3o%20da%20Gera%C3%A7%C3%A3o%20de%20Microgeradores%20e%20Minigeradores%20Fotovoltaicos%20Distribu%C3%ADdos%20rev%201.pdf | PDF | 13/09/2026 (localizada, não lida) | Contexto sobre MMGD, se um achado exigir |
| Consumo Mensal de Energia Elétrica por Classe | https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/consumo-de-energia-eletrica | Página | pendente | Camada territorial (consumo por UF/região/classe) |
| Anuário Estatístico de Energia Elétrica | https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/anuario-estatistico-de-energia-eletrica | Página | pendente | Mapeamento subsistema × UF; consumo per capita |

## Outras fontes (eventos sociais e climáticos)

| Título | URL | Acesso | Uso |
|---|---|---|---|
| Jogos do Brasil na Copa do Mundo 2026 — Olympics.com | https://www.olympics.com/pt/noticias/copa-do-mundo-2026-brasil-locais-datas-jogos-cruzamentos-selecao-brasil | 13/09/2026 | Datas e horários dos jogos (E6–E10) |
| Jogos do Brasil na Copa 2022 | conhecimento público (24/11 16h, 28/11 13h, 02/12 16h, 05/12 16h, 09/12 12h, horário de Brasília) | — | E1–E5 |

## Fontes secundárias (não oficiais — usadas apenas como pista)

| Título | URL | Acesso | O que indica | Status |
|---|---|---|---|---|
| Sistema Interligado Nacional — Wikipédia | https://pt.wikipedia.org/wiki/Sistema_Interligado_Nacional | 13/09/2026 | Composição dos subsistemas por UF | Confirmada pelo Boletim ONS de 15/08/2023 (acima) |
| CMSE avalia impactos da pandemia — MME | http://www.mme.gov.br/todas-as-noticias/-/asset_publisher/pdAS9IcdBICN/content/cmse-avalia-impactos-da-pandemia-do-covid-19-no-setor-eletrico-brasileiro | 13/09/2026 | Queda de ~10% da carga do SIN entre 18/03 e 10/04/2020 | Contexto para A2 (fonte governamental) |
| AM tem a maior queda no consumo de energia no Norte — A Crítica | https://www.acritica.com/manaus/am-tem-a-maior-queda-no-consumo-de-energia-no-norte-durante-isolamento-social-1.43416 | 13/09/2026 | Amazonas com a maior queda do Norte no isolamento | Contexto para A2 (imprensa) |

## Pendências de pesquisa

- ~~Composição dos subsistemas por UF~~ → resolvida pelo Boletim de 15/08/2023. Falta apenas confirmar a data em que Roraima passou a operar interligado ao SIN.
- Boletins diários do ONS de 2020 não estão disponíveis no endereço atual (404); a oscilação horária do Norte em abril/2020 (A2) segue sem explicação oficial.
- Nota técnica do ONS sobre a estimativa de MMGD (citada como disponível no SINtegre, portal de acesso restrito).
- Confirmação documental da convenção de hora do ONS (verificado empiricamente que os carimbos seguem a hora oficial de Brasília, com UTC−2 durante o horário de verão até 16/02/2019; não encontrado em texto oficial).
- Decisão pendente após o bloco 8: ampliar a série para 2017–2018 (exigiria a mesma regra para cada janela de horário de verão).
