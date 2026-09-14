"""
Blocos 5 e 6 da exploração — Diferenças entre subsistemas; pico, vale e amplitude.

Bloco 5: os subsistemas diferem só em escala ou também em formato? Quais têm
maior amplitude intradiária?
Bloco 6: pico, vale, amplitude relativa e fator de carga como séries diárias
(2024–2026), sua distribuição e sua relação com o nível do dia.

Gera docs/eda/img/05_*.png, 06_*.png e docs/eda/05-06-subsistemas-amplitude.md.

Uso: python src\\eda\\bloco05_06_subsistemas_amplitude.py
"""

from __future__ import annotations

import statistics as st
from collections import defaultdict
from datetime import date, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from bloco04_intradiario import media_perfis, metricas, normalizar, perfis_diarios, tipo_dia
from comum import (COR, PROJECT_ROOT, ROTULO, SUBSISTEMAS, TEXTO_2, carregar_anomalias, carregar_dim,
                   carregar_fato, estilo, horas_excluidas, md_table, salvar)

DOC_PATH = PROJECT_ROOT / "docs" / "eda" / "05-06-subsistemas-amplitude.md"
TODOS = ["SIN"] + SUBSISTEMAS
NUCLEO = (2024, 2025)
TIPOS = ["Dia útil", "Sábado", "Domingo"]
ESTACOES = ["Verão", "Outono", "Inverno", "Primavera"]
COR_ESTACAO = {"Verão": "#eb6834", "Outono": "#eda100", "Inverno": "#2a78d6", "Primavera": "#1baf7a"}


def percentil(xs: list[float], q: float) -> float:
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    i = int(k)
    return xs[i] + (xs[min(i + 1, len(xs) - 1)] - xs[i]) * (k - i)


def rms(a: list[float], b: list[float]) -> float:
    return (sum((x - y) ** 2 for x, y in zip(a, b)) / len(a)) ** 0.5


def media_movel(serie: dict[date, float], janela: int = 7) -> tuple[list[date], list[float]]:
    dias = sorted(serie)
    xs, ys = [], []
    for i in range(janela - 1, len(dias)):
        bloco = dias[i - janela + 1:i + 1]
        if (bloco[-1] - bloco[0]).days == janela - 1:  # sem buracos
            xs.append(bloco[-1])
            ys.append(st.mean(serie[d] for d in bloco))
    return xs, ys


def main() -> None:
    estilo()
    serie = carregar_fato()
    dim = carregar_dim()
    excluidas = horas_excluidas(carregar_anomalias(), escopo="horario")
    ultimo = max(serie["SIN"]).date()

    perfis = {s: perfis_diarios(serie, dim, excluidas, s) for s in TODOS}
    nucleo = {s: {d: p for d, p in perfis[s].items() if d.year in NUCLEO} for s in TODOS}
    recente = {s: {d: p for d, p in perfis[s].items() if d.year >= 2024} for s in TODOS}

    # métricas diárias
    diarias = {s: {d: metricas(p) for d, p in recente[s].items()} for s in TODOS}

    # ================= BLOCO 5 =================
    # 5a. distância de formato entre curvas típicas normalizadas (dia útil, núcleo)
    tipico_norm = {}
    for s in TODOS:
        ps = [normalizar(p) for d, p in nucleo[s].items() if tipo_dia(dim, d) == "Dia útil"]
        tipico_norm[s] = media_perfis(ps)
    dist = {(a, b): 100 * rms(tipico_norm[a], tipico_norm[b]) for a in SUBSISTEMAS for b in SUBSISTEMAS}

    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    n = len(SUBSISTEMAS)
    mx = max(dist.values())
    for i, a in enumerate(SUBSISTEMAS):
        for j, b in enumerate(SUBSISTEMAS):
            v = dist[(a, b)]
            cor = plt.cm.Blues(0.15 + 0.7 * v / mx) if v else "white"
            ax.add_patch(plt.Rectangle((j, n - 1 - i), 1, 1, color=cor, ec="white", lw=2))
            ax.text(j + 0.5, n - 1 - i + 0.5, f"{v:.1f}" if v else "—", ha="center", va="center", fontsize=10,
                    color="white" if v > 0.6 * mx else "#0b0b0b")
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks([k + 0.5 for k in range(n)])
    ax.set_xticklabels([ROTULO[s].split("/")[0] for s in SUBSISTEMAS], fontsize=9)
    ax.set_yticks([k + 0.5 for k in range(n)])
    ax.set_yticklabels([ROTULO[s].split("/")[0] for s in reversed(SUBSISTEMAS)], fontsize=9)
    ax.grid(False)
    ax.set_title("Distância entre formatos de dia útil\n(desvio médio hora a hora, em % da média do dia)")
    fig.tight_layout()
    salvar(fig, "05_distancia_entre_formatos.png")

    # 5b. distribuição da amplitude relativa diária por subsistema e tipo de dia (p10–p90, mediana)
    amp_dist = {s: {} for s in TODOS}
    for s in TODOS:
        for t in TIPOS:
            xs = [m["amplitude_rel"] for d, m in diarias[s].items() if d.year in NUCLEO and tipo_dia(dim, d) == t]
            amp_dist[s][t] = (percentil(xs, 0.1), percentil(xs, 0.5), percentil(xs, 0.9))
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, t in zip(axes, TIPOS):
        for i, s in enumerate(SUBSISTEMAS):
            p10, p50, p90 = (100 * v for v in amp_dist[s][t])
            ax.plot([i, i], [p10, p90], color=COR[s], linewidth=6, alpha=0.35, solid_capstyle="round")
            ax.plot(i, p50, "o", color=COR[s], markersize=8)
            ax.text(i + 0.18, p50, f"{p50:.0f}%", color=COR[s], va="center", fontsize=9)
        ax.set_xticks(range(len(SUBSISTEMAS)))
        ax.set_xticklabels([ROTULO[s].split("/")[0] for s in SUBSISTEMAS], fontsize=9)
        ax.set_xlim(-0.5, len(SUBSISTEMAS) - 0.3)
        ax.set_title(t)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("amplitude do dia ÷ média do dia (%)")
    fig.suptitle("Amplitude intradiária de cada dia, 2024–2025 — ponto = mediana; faixa = do 10º ao 90º percentil",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "05_amplitude_distribuicao.png")

    # ================= BLOCO 6 =================
    # 6a. série diária da amplitude relativa (média móvel de 7 dias), 2024–2026
    fig, axes = plt.subplots(5, 1, figsize=(11, 11), sharex=True)
    for ax, s in zip(axes, TODOS):
        xs, ys = media_movel({d: 100 * m["amplitude_rel"] for d, m in diarias[s].items()})
        ax.plot(xs, ys, color=COR[s])
        ax.set_title(f"{ROTULO[s]} — amplitude do dia ÷ média do dia, média móvel de 7 dias (%)")
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
        for y in (2024, 2025, 2026):
            for e, m0, m1 in (("Verão", 1, 3), ("Inverno", 6, 9)):
                ax.axvspan(date(y, m0, 1), date(y, m1, 1) + timedelta(days=30), color=COR_ESTACAO[e], alpha=0.06, lw=0)
    fig.suptitle("Como a amplitude intradiária varia ao longo do ano (faixas: verão em laranja, inverno em azul) — todos os tipos de dia",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "06_amplitude_serie_diaria.png")

    # 6b. nível do dia × amplitude (dia útil, núcleo), por estação — SE e S
    fig, axes = plt.subplots(1, 4, figsize=(15, 4), sharey=False)
    for ax, s in zip(axes, SUBSISTEMAS):
        for e in ESTACOES:
            pts = [(m["media"] / 1000, 100 * m["amplitude_rel"]) for d, m in diarias[s].items()
                   if d.year in NUCLEO and tipo_dia(dim, d) == "Dia útil" and dim[d]["EstacaoAno"] == e]
            ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=12, color=COR_ESTACAO[e], alpha=0.7, label=e, edgecolors="white", linewidths=0.4)
        ax.set_title(ROTULO[s], fontsize=10)
        ax.set_xlabel("carga média do dia (GW)")
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("amplitude ÷ média (%)")
    axes[0].legend(fontsize=8, loc="upper right")
    fig.suptitle("Dias mais pesados são dias mais planos? Dias úteis de 2024–2025, um ponto por dia", x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "06_nivel_vs_amplitude.png")

    # ---------- tabelas ----------
    t_dist = md_table([""] + [ROTULO[s].split("/")[0] for s in SUBSISTEMAS],
                      [[ROTULO[a].split("/")[0]] + [f"{dist[(a, b)]:.1f}" if a != b else "—" for b in SUBSISTEMAS] for a in SUBSISTEMAS])

    # escala × formato: o que explica a diferença de cada subsistema para o SIN?
    linhas = []
    for s in SUBSISTEMAS:
        escala = st.mean(m["media"] for d, m in diarias[s].items() if d.year in NUCLEO) / st.mean(m["media"] for d, m in diarias["SIN"].items() if d.year in NUCLEO)
        linhas.append([ROTULO[s], f"{100 * escala:.0f}%", f"{100 * rms(tipico_norm[s], tipico_norm['SIN']):.1f}",
                       f"{metricas(tipico_norm[s])['hora_pico']}h vs {metricas(tipico_norm['SIN'])['hora_pico']}h",
                       f"{100 * metricas(tipico_norm[s])['amplitude_rel']:.0f}% vs {100 * metricas(tipico_norm['SIN'])['amplitude_rel']:.0f}%"])
    t_escala = md_table(["Subsistema", "Escala (÷ SIN)", "Distância de formato para o SIN", "Hora do pico (dia útil)", "Amplitude ÷ média"], linhas)

    linhas = []
    for s in TODOS:
        for t in TIPOS:
            p10, p50, p90 = amp_dist[s][t]
            fc = [m["fator_carga"] for d, m in diarias[s].items() if d.year in NUCLEO and tipo_dia(dim, d) == t]
            linhas.append([ROTULO[s], t, f"{100 * p10:.0f}%", f"{100 * p50:.0f}%", f"{100 * p90:.0f}%", f"{percentil(fc, 0.5):.2f}"])
    t_amp = md_table(["Subsistema", "Tipo de dia", "Amplitude p10", "Mediana", "p90", "Fator de carga (mediana)"], linhas)

    linhas = []
    for s in TODOS:
        for e in ESTACOES:
            ms = [m for d, m in diarias[s].items() if d.year in NUCLEO and tipo_dia(dim, d) == "Dia útil" and dim[d]["EstacaoAno"] == e]
            horas = [m["hora_pico"] for m in ms]
            moda = max(set(horas), key=horas.count)
            linhas.append([ROTULO[s], e, f"{100 * st.median(m['amplitude_rel'] for m in ms):.0f}%", f"{st.median(m['fator_carga'] for m in ms):.2f}",
                           f"{moda}h ({100 * horas.count(moda) / len(horas):.0f}% dos dias)", f"{st.median(m['pico'] for m in ms) / 1000:.1f}", f"{st.median(m['vale'] for m in ms) / 1000:.1f}"])
    t_est = md_table(["Subsistema", "Estação (dia útil)", "Amplitude mediana", "Fator de carga", "Hora do pico mais frequente", "Pico mediano (GW)", "Vale mediano (GW)"], linhas)

    # correlação nível × amplitude por subsistema (dia útil, núcleo)
    linhas = []
    for s in TODOS:
        pts = [(m["media"], m["amplitude_rel"]) for d, m in diarias[s].items() if d.year in NUCLEO and tipo_dia(dim, d) == "Dia útil"]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        mx, my = st.mean(xs), st.mean(ys)
        r = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
        top = sorted(pts, key=lambda p: -p[0])[:25]
        bot = sorted(pts, key=lambda p: p[0])[:25]
        linhas.append([ROTULO[s], f"{r:+.2f}", f"{100 * st.mean(p[1] for p in top):.0f}%", f"{100 * st.mean(p[1] for p in bot):.0f}%"])
    t_corr = md_table(["Subsistema", "Correlação nível × amplitude", "Amplitude nos 25 dias mais pesados", "Amplitude nos 25 dias mais leves"], linhas)

    doc = f"""# Blocos 5 e 6 — Diferenças entre subsistemas; pico, vale e amplitude

> Gerado por `src/eda/bloco05_06_subsistemas_amplitude.py` sobre a extração de {ultimo:%d/%m/%Y}. Tabelas e gráficos são reproduzíveis; a interpretação ao final é do analista e está datada.

Perguntas: os subsistemas diferem só em **escala** ou também em **formato**? Quais têm maior amplitude intradiária? Como pico, vale e amplitude se comportam dia a dia? Definições em [03-metodologia.md](../03-metodologia.md) §5: amplitude relativa = (pico − vale) ÷ média do dia; fator de carga = média ÷ pico. Janela: 2024–2025 para distribuições; 2024–2026 para séries. Exclusões como no bloco 4.

## Bloco 5 — Escala ou formato?

![Distância entre formatos](img/05_distancia_entre_formatos.png)

Desvio médio hora a hora entre as curvas típicas normalizadas de dia útil (em pontos percentuais da média do dia):

{t_dist}

Cada subsistema em relação ao SIN:

{t_escala}

### Quem tem a maior amplitude intradiária?

![Distribuição da amplitude](img/05_amplitude_distribuicao.png)

{t_amp}

## Bloco 6 — Pico, vale e amplitude ao longo do tempo

![Série da amplitude](img/06_amplitude_serie_diaria.png)

{t_est}

### Dias mais pesados são dias mais planos?

![Nível × amplitude](img/06_nivel_vs_amplitude.png)

{t_corr}

## Leitura (analista, 13/09/2026)

**Escala e formato são coisas diferentes — e os subsistemas se agrupam em pares.** A distância entre as curvas típicas normalizadas mostra dois grupos claros: **Sudeste e Sul** (desvio de 3,9 p.p. entre si) e **Nordeste e Norte** (3,0 p.p.). Entre os grupos a distância é de 7 a 12 p.p. — o Sul e o Norte são os dois formatos mais diferentes do país (12,3). O SIN é praticamente o Sudeste (distância 1,5): tudo o que o Brasil agregado "mostra" sobre o formato do dia é o formato do Sudeste, com 56% da escala. Responder "quanto do Nordeste é escala e quanto é formato": ele tem 17% do tamanho do SIN e um formato que difere em 5,8 p.p. hora a hora, com o pico duas horas mais tarde (21h) e amplitude 30% menor (19% contra 27%).

**Quem tem a maior amplitude é o Sul, por larga margem.** A amplitude mediana de um dia útil é **44%** da média no Sul, 32% no SE, 19% no NE e **18%** no Norte. A faixa entre o 10º e o 90º percentil também é maior no Sul (35–55%): o Sul não só tem o dia mais "pontudo", como tem os dias mais variados entre si. O domingo do Sul chega a 45% (fator de carga 0,78) — a rampa noturna de domingo que o diagnóstico de qualidade sinalizava como "anomalia" é a característica mais marcante do subsistema. O Norte é o oposto: sábado com amplitude de 14% e fator de carga 0,94 — um dia quase reto.

**A amplitude tem estação: cresce no inverno em SE e S, não muda em NE e N.** Na série diária (média móvel de 7 dias) o SE oscila entre ~28% no verão e ~38% no inverno; o Sul entre ~38% e ~50%. No Nordeste e no Norte a linha é plana o ano inteiro (19% ± 2). A hora do pico mais frequente confirma o bloco 4 com granularidade diária: no SE, 14h em 52% dos dias de verão e 18h em 79% dos de inverno.

**Dias mais pesados são dias mais planos — o achado central destes blocos.** No SE a correlação entre a carga média do dia e sua amplitude relativa é **−0,75**; no Sul, −0,58; no SIN, −0,71. Os 25 dias úteis mais pesados do SE têm amplitude de 28%; os 25 mais leves, 41%. A leitura: o que faz um dia ser pesado é o ar-condicionado, que liga de manhã e só desliga à noite — ele enche a tarde e o começo da noite, e o dia fica alto e plano. O que faz um dia ser leve é a ausência de climatização — sobra o pico noturno de iluminação e chuveiro sobre uma tarde baixa. No Nordeste (+0,04) e no Norte (+0,21) a relação não existe ou se inverte de leve: a climatização ali é carga de base, presente todo dia, e não diferencia dias.

**Implicação para a leitura do sistema.** "Pico" e "amplitude" contam histórias opostas: os dias de pico recorde (fevereiro/2025) são dias de amplitude *baixa*. Um dashboard que mostrasse só o pico diria "o sistema está mais estressado no verão"; um que mostrasse só a amplitude diria "no inverno". Os dois são verdade, e o produto precisa dizer isso: **o verão estressa o nível; o inverno estressa o formato.**

**O que leva para o produto.** (1) O scatter nível × amplitude, colorido por estação, é o gráfico que resume os blocos 4–6 numa imagem e sustenta a frase acima. (2) A matriz de distância justifica tratar SE/S e NE/N como pares na narrativa. (3) A distribuição de amplitude por subsistema e tipo de dia é a tabela de referência das medidas de formato.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    print(f"  documento: {DOC_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
