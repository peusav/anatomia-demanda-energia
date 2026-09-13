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
| Roteiro — Carga Atendida por MMGD (ciclo 2024–2028) | https://www.ons.org.br/SCPCB/Paginas/cicloestudos/2024-2028/Roteiro_Carga_Atendida_por_MMGD.pdf | PDF | — | 13/09/2026 | Insumos da estimativa de MMGD (ANEEL, INPE, ONS) |
| Programa de dados abertos da AWS — ONS | https://registry.opendata.aws/ons-opendata-portal/ | Registro | — | 13/09/2026 | Origem dos arquivos no S3 |

## EPE — Empresa de Pesquisa Energética (expansão futura, ainda não usada)

| Título | URL | Tipo | Acesso | Uso previsto |
|---|---|---|---|---|
| Nota Técnica EPE DEA-SEE 009/2023 — Aprimoramento na metodologia de estimação da geração de micro e minigeradores fotovoltaicos distribuídos | https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-789/Aprimoramento%20na%20Metodologia%20de%20Estima%C3%A7%C3%A3o%20da%20Gera%C3%A7%C3%A3o%20de%20Microgeradores%20e%20Minigeradores%20Fotovoltaicos%20Distribu%C3%ADdos%20rev%201.pdf | PDF | 13/09/2026 (localizada, não lida) | Contexto sobre MMGD, se um achado exigir |
| Consumo Mensal de Energia Elétrica por Classe | https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/consumo-de-energia-eletrica | Página | pendente | Camada territorial (consumo por UF/região/classe) |
| Anuário Estatístico de Energia Elétrica | https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/anuario-estatistico-de-energia-eletrica | Página | pendente | Mapeamento subsistema × UF; consumo per capita |

## Fontes secundárias (não oficiais — usadas apenas como pista)

| Título | URL | Acesso | O que indica | Status |
|---|---|---|---|---|
| Sistema Interligado Nacional — Wikipédia | https://pt.wikipedia.org/wiki/Sistema_Interligado_Nacional | 13/09/2026 | Composição dos subsistemas por UF: Maranhão no Norte; Acre e Rondônia no Sudeste/Centro-Oeste | **Pendente de confirmação oficial** antes de qualquer uso |

## Pendências de pesquisa

- Fonte oficial para a composição dos subsistemas por UF (candidatas: Anuário EPE; Mapas do SIN no site do ONS).
- Nota técnica do ONS sobre a estimativa de MMGD (citada como disponível no SINtegre, portal de acesso restrito).
- Confirmação documental de que a série é publicada em hora padrão sem horário de verão (verificado empiricamente; não encontrado em texto oficial).
