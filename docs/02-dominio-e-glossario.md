# 02 — Domínio e glossário

Conceitos necessários para ler o produto, na acepção usada neste projeto. Onde há definição oficial, ela está marcada como tal; o restante é interpretação nossa, escrita para a persona não especialista.

## Sistema Interligado Nacional (SIN)

**Definição oficial (ONS):** "O Sistema Interligado Nacional é constituído por quatro subsistemas: Sul, Sudeste/Centro-Oeste, Nordeste e a maior parte da região Norte." ([O que é o SIN](https://www.ons.org.br/paginas/sobre-o-sin/o-que-e-o-sin))

**No projeto:** é o nível "Brasil". Não existe linha própria para o SIN na base — ele é a soma dos quatro subsistemas.

## Subsistema

Divisão **elétrica** do SIN usada pelo ONS para operar e planejar o sistema. São quatro: Norte (N), Nordeste (NE), Sul (S) e Sudeste/Centro-Oeste (SE).

**Subsistema não é região do IBGE.** A divisão segue a topologia da rede, não a divisão político-administrativa. O Boletim Diário da Operação do ONS de 15/08/2023 (fonte oficial, ver [07-anomalias.md](07-anomalias.md)) lista os estados de cada submercado: o **Maranhão** pertence ao subsistema **Norte** (com Amapá, Amazonas, Pará e Tocantins), e **Acre e Rondônia** pertencem ao **Sudeste/Centro-Oeste**. Roraima operava isolado do SIN em 2023. Qualquer cruzamento com população ou território precisa usar essa composição, não a regional do IBGE.

Na base, o código `SE` teve o nome grafado como `SUDESTE` até 2025 e `SUDESTE/CENTRO-OESTE` a partir de 2026 (o dicionário de dados v1.2 explica a troca). O projeto usa o código como chave e o rótulo "Sudeste/Centro-Oeste" sempre.

## Carga

**Variável principal do projeto.** É a potência que o sistema elétrico precisa atender em determinado momento ou período — a demanda vista pelo operador.

Formalmente, a carga do ONS é a soma da geração das usinas que atendem o subsistema, ajustada pelo intercâmbio com os outros subsistemas. Como o operador não mede cada consumidor, ele mede (ou estima) o que foi *gerado* para atendê-los. Isso tem consequências importantes, descritas em [03-metodologia.md](03-metodologia.md): o que entra nessa soma mudou ao longo do tempo.

Preferir "carga" ou "demanda elétrica". Não dizer "consumo" automaticamente.

## Carga ≠ consumo

| | Carga (ONS) | Consumo (EPE) |
|---|---|---|
| Ponto de vista | Do sistema: o que a rede precisou entregar | Do consumidor: o que foi faturado/medido nas unidades consumidoras |
| Inclui perdas da rede? | Sim | Não |
| Inclui o que o consumidor gera para si (MMGD)? | Não até 28/04/2023; a partir de 29/04/2023, sim, por **estimativa** somada à carga medida | Depende da publicação |
| Granularidade típica | Hora, dia | Mês |
| Recorte | Subsistema | UF, região, classe de consumo |

Os dois estão relacionados, mas não são iguais e não devem ser comparados diretamente. O núcleo deste projeto usa **carga**; uma eventual camada territorial usaria **consumo**.

## MW, MWmed e MWh

- **MW (megawatt)** — potência em um instante. A "vazão da torneira".
- **MWmed (megawatt médio)** — potência média ao longo de um intervalo. É a unidade da base do ONS: cada linha é a potência média demandada durante uma hora.
- **MWh (megawatt-hora)** — energia acumulada ao longo do tempo. A "água acumulada no balde".

Relação: energia = potência média × tempo. Como cada registro da base cobre exatamente uma hora, o valor em MWmed é numericamente igual à energia daquela hora em MWh. Somar 24 valores horários dá a energia do dia em MWh; a média deles dá a carga média do dia em MWmed.

**Não tratar MW/MWmed e MWh como sinônimos.** Um pico de 62.150 MWmed às 15h não é "62 mil MWh".

## Curva de carga

O desenho da carga ao longo do tempo. No projeto, principalmente o desenho das 24 horas de um dia: 00h → 01h → … → 23h. É o coração do produto porque mostra **como** a demanda se distribui, não apenas seu nível médio.

## Pico, vale e amplitude

- **Pico** — maior carga observada no período (no dia, tipicamente).
- **Vale** — menor carga observada.
- **Amplitude** — diferença entre pico e vale. Pode ser absoluta (MWmed) ou relativa (pico ÷ vale, ou amplitude ÷ média).
- **Hora do pico / hora do vale** — em que hora do dia ocorrem.
- **Fator de carga** — carga média ÷ carga de pico. Quanto mais próximo de 1, mais "plana" é a curva.

Essas medidas caracterizam o formato de um dia e permitem comparar dias, subsistemas e anos.

## Ciclo intradiário

O padrão das 24 horas. A pergunta é "como é o perfil típico de um dia?" e, depois, "esse perfil muda entre subsistemas, tipos de dia, meses e anos?".

## Sazonalidade

Padrões que se repetem regularmente. O projeto procura sazonalidade em quatro escalas: **horária** (dentro do dia) → **semanal** (dia útil × sábado × domingo × feriado) → **mensal/estacional** (verão × inverno) → **anual**.

## Mudança estrutural × sazonalidade × evento

Nem toda diferença é tendência. Diante de uma variação, perguntar:

1. É um padrão **recorrente**? → sazonalidade.
2. É uma mudança **persistente**? → possível mudança estrutural (ou metodológica).
3. É um episódio **pontual**? → evento (feriado, clima, perturbação, pandemia).

Temperatura, pandemia, feriados e mudanças de metodologia produzem comportamentos incomuns que não são "crescimento" nem "queda" da demanda.

## Geração, intercâmbio e MMGD (fora do núcleo, mas necessários para entender a carga)

- **Geração** — energia produzida pelas usinas. O ONS classifica as usinas em *despachadas* (o operador decide quando geram), *programadas* e *não despachadas* (geram por conta própria; o ONS só estima).
- **Intercâmbio** — energia trocada entre subsistemas pela rede de transmissão. É o que faz a carga de um subsistema ser diferente da geração dentro dele.
- **MMGD — micro e minigeração distribuída** — geração de pequeno porte instalada junto ao consumidor, majoritariamente solar fotovoltaica em telhados. O consumidor gera parte do que consome; a rede "vê" apenas o restante. Por isso o crescimento da MMGD **reduz a carga medida pela rede no meio do dia** sem que o consumo tenha caído. Desde 29/04/2023 o ONS **soma** uma estimativa da MMGD à carga medida, para que o número publicado represente a demanda total e não apenas a parte atendida pela rede (ver [03-metodologia.md](03-metodologia.md)). Antes dessa data, a MMGD simplesmente não aparecia.

## Modelo mental para qualquer gráfico

1. **Quanto?** — qual é o nível da carga.
2. **Quando?** — em que hora, dia, mês, período.
3. **Onde?** — em que subsistema.
4. **Como mudou?** — o nível ou o formato se alterou ao longo dos anos.
5. **O que foge do padrão?** — há anomalia, ruptura ou evento que merece investigação.
