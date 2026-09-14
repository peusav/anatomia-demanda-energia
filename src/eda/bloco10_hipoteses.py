"""
Bloco 10 da exploração — Hipóteses que pedem dados externos.

Testa a hipótese principal (o vale solar do meio-dia acompanha a expansão
da micro e minigeração distribuída) com o cadastro de GD da ANEEL,
agregado por subsistema em data/reference/mmgd_por_subsistema.csv.
Gera docs/eda/img/10_*.png e docs/eda/10-hipoteses.md.

Uso: python src\\eda\\bloco10_hipoteses.py
"""

from __future__ import annotations

import csv
import statistics as st

import matplotlib.pyplot as plt

from bloco04_intradiario import media_perfis, metricas, normalizar, perfis_diarios, tipo_dia
from comum import (COR, PROJECT_ROOT, ROTULO, SUBSISTEMAS, TEXTO_2, carregar_anomalias, carregar_dim,
                   carregar_fato, estilo, horas_excluidas, md_table, media_diaria, salvar)

DOC_PATH = PROJECT_ROOT / "docs" / "eda" / "10-hipoteses.md"
MMGD_PATH = PROJECT_ROOT / "data" / "reference" / "mmgd_por_subsistema.csv"
ANOS = [2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026]


def main() -> None:
    estilo()
    serie = carregar_fato()
    dim = carregar_dim()
    excluidas = horas_excluidas(carregar_anomalias(), escopo="horario")
    ultimo = max(serie["SIN"]).date()

    # MMGD acumulada por subsistema e ano (MW)
    mmgd = {}
    with MMGD_PATH.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            mmgd[(r["id_subsistema"], int(r["ate"][:4]))] = float(r["mmgd_mw"])

    perfis = {s: perfis_diarios(serie, dim, excluidas, s) for s in SUBSISTEMAS}
    diaria = {s: media_diaria(serie[s]) for s in SUBSISTEMAS}

    pontos = {s: [] for s in SUBSISTEMAS}
    for s in SUBSISTEMAS:
        for y in ANOS:
            ps = [p for d, p in perfis[s].items() if d.year == y and tipo_dia(dim, d) == "Dia útil"]
            normas = [normalizar(p) for p in ps]
            meio = st.mean(st.mean(n[12:16]) for n in normas)
            noite = st.mean(st.mean(n[18:22]) for n in normas)
            tarde = sum(12 <= metricas(p)["hora_pico"] <= 17 for p in ps) / len(ps)
            carga = st.mean(v for d, v in diaria[s].items() if d.year == y)
            razao = mmgd[(s, y)] / carga  # MW de MMGD por MW de carga média
            pontos[s].append({"ano": y, "razao": razao, "meio": meio, "noite": noite, "tarde": tarde, "carga": carga, "mmgd": mmgd[(s, y)]})

    # gráfico: meio do dia × MMGD ÷ carga média, um traço por subsistema, anos anotados
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax, chave, titulo in ((axes[0], "meio", "Meio do dia (12–15h) em relação à média do dia"),
                              (axes[1], "tarde", "Dias úteis com pico à tarde (12–17h)")):
        for s in SUBSISTEMAS:
            xs = [100 * p["razao"] for p in pontos[s]]
            ys = [100 * (p[chave] - 1) if chave == "meio" else 100 * p[chave] for p in pontos[s]]
            ax.plot(xs, ys, color=COR[s], marker="o", markersize=4, label=ROTULO[s])
            for p, x, y in zip(pontos[s], xs, ys):
                if p["ano"] in (2017, 2021, 2024, 2026):
                    ax.text(x, y, f" {str(p['ano'])[2:]}", color=COR[s], fontsize=7, va="center")
        ax.set_xlabel("MMGD instalada ÷ carga média do subsistema (%)")
        ax.set_title(titulo, fontsize=10)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("%")
    axes[0].axhline(0, color=TEXTO_2, linewidth=0.8)
    axes[0].legend(fontsize=8, loc="upper right")
    fig.suptitle("Quanto mais geração distribuída, menos meio-dia: cada ponto é um ano (2017–2026), cada traço um subsistema; 2020 omitido",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "10_mmgd_vs_meio_do_dia.png")

    # tabela
    linhas = []
    for s in SUBSISTEMAS:
        for p in pontos[s]:
            linhas.append([ROTULO[s], p["ano"], f"{p['mmgd'] / 1000:.1f}", f"{p['carga'] / 1000:.1f}", f"{100 * p['razao']:.0f}%",
                           f"{100 * (p['meio'] - 1):+.1f}%", f"{100 * (p['noite'] - 1):+.1f}%", f"{100 * p['tarde']:.0f}%"])
    t_mmgd = md_table(["Subsistema", "Ano", "MMGD acumulada (GW)", "Carga média (GW)", "MMGD ÷ carga", "Meio do dia", "Noite", "Pico à tarde"], linhas)

    # correlação por subsistema (razão × meio do dia), anos sob regime homogêneo e todos
    linhas = []
    for s in SUBSISTEMAS:
        xs = [p["razao"] for p in pontos[s]]
        ys = [p["meio"] for p in pontos[s]]
        mx, my = st.mean(xs), st.mean(ys)
        r = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
        # inclinação: p.p. de meio-dia por 10 p.p. de MMGD/carga
        b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        linhas.append([ROTULO[s], f"{r:+.2f}", f"{100 * b * 0.10:+.1f} p.p."])
    t_corr = md_table(["Subsistema", "Correlação MMGD÷carga × meio do dia (2017–2026)", "Efeito por +10 p.p. de MMGD÷carga"], linhas)

    doc = f"""# Bloco 10 — Hipóteses que pedem dados externos

> Gerado por `src/eda/bloco10_hipoteses.py` sobre a extração de {ultimo:%d/%m/%Y}. A agregação da ANEEL está em `data/reference/mmgd_por_subsistema.csv`; a interpretação ao final é do analista e está datada.

Os blocos 2–8 deixaram quatro hipóteses que os dados do ONS sozinhos não decidem. Este bloco testa a principal com dados abertos da ANEEL e registra o estado das outras.

## H1 — O vale solar do meio-dia acompanha a micro e minigeração distribuída

**Dado externo.** Cadastro de empreendimentos de geração distribuída da ANEEL (4,6 milhões de unidades em 13/09/2026), agregado por subsistema usando a composição por estado confirmada em [07-anomalias.md](../07-anomalias.md), com a potência acumulada até o fim de cada ano (data de atualização cadastral como proxy da conexão). 99% da potência é fotovoltaica.

![MMGD × meio do dia](img/10_mmgd_vs_meio_do_dia.png)

{t_mmgd}

{t_corr}

## H2 — O que cresce no Norte

Sem dado externo conclusivo. O ONS projeta o Norte como o subsistema de maior crescimento percentual (cerca de +11% na revisão de 2026) e atribui a alta geral da carga a recuperação econômica, setores eletrointensivos (data centers, agronegócio, mineração) e migração para o mercado livre — sem detalhar o Norte. A interligação de Roraima ao SIN não aparece como degrau na série. Fica como hipótese aberta; a camada EPE (consumo por UF e classe) é o caminho natural para decidi-la, se o produto vier a precisar.

## H3 — Sazonalidade do Norte e do Nordeste é temperatura

Não testada: exigiria séries do INMET por estação meteorológica e um mapeamento para subsistemas. O padrão (Norte com máximo em setembro–outubro, na estação seca) é consistente com a hipótese, mas o projeto decidiu não incorporar base meteorológica na primeira versão (D08).

## H4 — Quanto de 2020 é COVID e quanto é clima

Não separável com os dados disponíveis; 2020 continua tratado como ano excepcional (D04).

## Leitura (analista, 14/09/2026)

**H1 se sustenta — com uma ressalva honesta.** A geração distribuída saiu de praticamente zero em 2017 para **26 GW no SE, 13 GW no Sul, 10 GW no NE e 4 GW no Norte** em agosto de 2026; em relação à carga média, o Sul chega a 93% e o Nordeste a 74%. E o meio do dia cai junto: correlação de **−0,92 no Nordeste**, −0,71 no SE, −0,73 no Sul. A cada 10 p.p. a mais de MMGD ÷ carga, o meio do dia perde 0,6 a 1,1 p.p. em relação à média do dia. A ressalva: as duas séries crescem no tempo, então parte da correlação é trivial. O que a torna convincente é a comparação *entre* subsistemas — o Nordeste, com o dia mais plano do país (amplitude 19%), é onde a mesma dose de MMGD move mais o formato, a ponto de virar o pico da tarde para a noite; e é onde a inclinação é a maior (−1,1 p.p.).

**O Norte é a exceção que informa.** Tem MMGD ÷ carga comparável ao SE (47% contra 55% em 2025), mas seu meio do dia quase não se moveu (+4,6% em 2017, +4,1% em 2025; correlação −0,17). Leitura: no Norte o meio do dia é sustentado por climatização na estação seca e por carga industrial contínua, que crescem junto com a MMGD e a compensam. Formato é o resultado de uma soma, não de um fator.

**O degrau de 2024 aparece nos quatro.** Em todos os subsistemas o ponto de 2024 fica acima da tendência — é o ano em que o ONS passou a *somar* a estimativa de MMGD à carga publicada — e em 2025 e 2026 a queda retoma. Ou seja, a estimativa oficial devolve parte do meio-dia, mas não toda: ou a estimativa é conservadora, ou há outros fatores diurnos (eficiência, mudança de hábitos, tarifa branca) além da MMGD. É a fronteira do que os dados públicos permitem dizer.

**O que leva para o produto.** O gráfico "MMGD × meio do dia" é o único do projeto que usa um dado fora do ONS, e é o que fecha a história da Camada 3: *o dia girou da tarde para a noite, e a geração distribuída é a explicação mais forte disponível*. Entra como visual de apoio, com a ressalva de correlação explícita no texto.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    print(f"  documento: {DOC_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
