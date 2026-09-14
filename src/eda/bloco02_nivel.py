"""
Bloco 2 da exploração — Nível.

Quanto o sistema demanda, como evoluiu e onde a carga está concentrada.
Gera docs/eda/img/02_*.png e as tabelas de docs/eda/02-nivel.md.

Uso: python src\\eda\\bloco02_nivel.py
"""

from __future__ import annotations

import statistics as st
from collections import defaultdict
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from comum import (COR, MARCOS, PROJECT_ROOT, ROTULO, SUBSISTEMAS, TEXTO_2, carregar_anomalias,
                   carregar_dim, carregar_fato, estilo, horas_excluidas, marcar_marcos, md_table,
                   media_diaria, salvar)

DOC_PATH = PROJECT_ROOT / "docs" / "eda" / "02-nivel.md"
ANOS_COMPLETOS = list(range(2017, 2026))
TODOS = ["SIN"] + SUBSISTEMAS


def main() -> None:
    estilo()
    serie = carregar_fato()
    dim = carregar_dim()
    excluidas = horas_excluidas(carregar_anomalias(), escopo="diario")
    ultimo = max(serie["SIN"]).date()
    corte = (ultimo.month, ultimo.day)

    diaria = {s: media_diaria(serie[s]) for s in TODOS}

    # ---------- médias anuais, mensais, YTD ----------
    anual = {s: {y: st.mean(v for d, v in diaria[s].items() if d.year == y) for y in ANOS_COMPLETOS} for s in TODOS}
    ytd = {s: {y: st.mean(v for d, v in diaria[s].items() if d.year == y and (d.month, d.day) <= corte)
               for y in (2024, 2025, 2026)} for s in TODOS}
    mensal = {s: defaultdict(list) for s in TODOS}
    for s in TODOS:
        for d, v in diaria[s].items():
            mensal[s][(d.year, d.month)].append(v)
        mensal[s] = {k: st.mean(v) for k, v in mensal[s].items()}

    # ---------- gráfico 1: média mensal por subsistema, com marcos ----------
    fig, axes = plt.subplots(5, 1, figsize=(11, 13), sharex=True)
    for ax, s in zip(axes, TODOS):
        xs = [date(y, m, 15) for (y, m) in sorted(mensal[s])]
        ys = [mensal[s][(x.year, x.month)] / 1000 for x in xs]
        ax.plot(xs, ys, color=COR[s])
        ax.set_title(f"{ROTULO[s]} — carga média mensal (GWmed)")
        ax.set_ylim(min(ys) * 0.9, max(ys) * 1.12)
        ax.text(xs[-1], ys[-1], f" {ys[-1]:.1f}", color=COR[s], va="center", fontsize=9, fontweight="bold")
        marcar_marcos(ax)
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axes[-1].set_xlabel("2026 vai até " + ultimo.strftime("%d/%m"))
    fig.suptitle("Carga média mensal, 2017–2026 — escalas independentes; linhas tracejadas = mudanças de metodologia do ONS",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "02_media_mensal_subsistemas.png")

    # ---------- gráfico 2: YTD 2024 × 2025 × 2026 (mesmo intervalo) ----------
    fig, axes = plt.subplots(1, 5, figsize=(13, 4), gridspec_kw={"width_ratios": [1.4, 1, 1, 1, 1]})
    for ax, s in zip(axes, TODOS):
        anos = [2024, 2025, 2026]
        vals = [ytd[s][y] / 1000 for y in anos]
        bars = ax.bar([str(y) for y in anos], vals, color=[COR[s]] * 3, width=0.6)
        bars[-1].set_alpha(0.55)
        for b, v, y in zip(bars, vals, anos):
            ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.1f}", ha="center", va="bottom", fontsize=9)
        var25 = ytd[s][2025] / ytd[s][2024] - 1
        var26 = ytd[s][2026] / ytd[s][2025] - 1
        ax.set_title(f"{ROTULO[s]}\n25/24 {var25:+.1%} · 26/25 {var26:+.1%}", fontsize=10)
        ax.set_ylim(0, max(vals) * 1.18)
        ax.grid(axis="x", visible=False)
        ax.set_yticks([])
    fig.suptitle(f"Carga média de 1º/jan a {ultimo:%d/%m} em cada ano (GWmed) — 2026 é parcial, por isso comparado só no mesmo intervalo",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "02_ytd_2024_2025_2026.png")

    # ---------- gráfico 3: participação dos subsistemas por ano ----------
    part = {s: {y: anual[s][y] / anual["SIN"][y] for y in ANOS_COMPLETOS} for s in SUBSISTEMAS}
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for s in SUBSISTEMAS:
        ys = [100 * part[s][y] for y in ANOS_COMPLETOS]
        ax.plot(ANOS_COMPLETOS, ys, color=COR[s], marker="o", markersize=5)
        ax.text(ANOS_COMPLETOS[-1] + 0.1, ys[-1], f"{ROTULO[s]} {ys[-1]:.1f}%", color=COR[s], va="center", fontsize=9)
    ax.set_xlim(2016.7, 2027)
    ax.set_xticks(ANOS_COMPLETOS)
    ax.set_ylabel("% da carga do SIN")
    ax.set_title("Participação de cada subsistema na carga anual do SIN, 2017–2025")
    fig.tight_layout()
    salvar(fig, "02_participacao_subsistemas.png")

    # ---------- gráfico 4: máximo e mínimo horário por ano (excluindo artefatos) ----------
    extremos = {s: {} for s in TODOS}
    for s in TODOS:
        for y in ANOS_COMPLETOS + [2026]:
            horas = [(t, v) for t, v in serie[s].items() if t.year == y and (s == "SIN" or (s, t) not in excluidas)]
            if s == "SIN":
                horas = [(t, v) for t, v in horas if not any((x, t) in excluidas for x in SUBSISTEMAS)]
            tmax = max(horas, key=lambda kv: kv[1])
            tmin = min(horas, key=lambda kv: kv[1])
            extremos[s][y] = (tmax, tmin, st.mean(v for _, v in horas))
    fig, axes = plt.subplots(1, 5, figsize=(13, 4.2), gridspec_kw={"width_ratios": [1.4, 1, 1, 1, 1]})
    for ax, s in zip(axes, TODOS):
        anos = ANOS_COMPLETOS + [2026]
        for i, y in enumerate(anos):
            (tmax, vmax), (tmin, vmin), med = extremos[s][y]
            ax.plot([i, i], [vmin / 1000, vmax / 1000], color=COR[s], linewidth=3, solid_capstyle="round",
                    alpha=0.5 if y == 2026 else 1)
            ax.plot(i, med / 1000, marker="_", color="black", markersize=10, markeredgewidth=1.5)
        ax.set_xticks(range(len(anos)))
        ax.set_xticklabels([str(y)[2:] for y in anos], fontsize=8)
        ax.set_title(ROTULO[s], fontsize=10)
        ax.grid(axis="x", visible=False)
        if s == "SIN":
            ax.set_ylabel("GWmed")
    fig.suptitle("Faixa entre a menor e a maior hora de cada ano (traço preto = média do ano); artefatos de dado excluídos; 2026 parcial",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "02_extremos_por_ano.png")

    # ---------- tabelas ----------
    t_anual = md_table(
        ["Ano"] + [ROTULO[s] for s in TODOS] + ["Regime"],
        [[y] + [f"{anual[s][y] / 1000:.2f}" for s in TODOS] +
         ["Supervisão ONS" if y < 2021 else "misto" if y in (2021, 2023) else "Carga global" if y == 2022 else "Carga global + MMGD"]
         for y in ANOS_COMPLETOS],
    )
    t_var = md_table(
        ["Variação"] + [ROTULO[s] for s in TODOS],
        [[f"{y}/{y - 1}"] + [f"{anual[s][y] / anual[s][y - 1] - 1:+.1%}" for s in TODOS] for y in ANOS_COMPLETOS[1:]] +
        [["**2025/2019 (atravessa 2 marcos)**"] + [f"**{anual[s][2025] / anual[s][2019] - 1:+.1%}**" for s in TODOS],
         ["**2019/2017 (mesmo regime)**"] + [f"**{anual[s][2019] / anual[s][2017] - 1:+.1%}**" for s in TODOS]],
    )
    t_ytd = md_table(
        [f"1º/jan–{ultimo:%d/%m}"] + [ROTULO[s] for s in TODOS],
        [[str(y)] + [f"{ytd[s][y] / 1000:.2f}" for s in TODOS] for y in (2024, 2025, 2026)] +
        [["2025/2024"] + [f"{ytd[s][2025] / ytd[s][2024] - 1:+.1%}" for s in TODOS],
         ["2026/2025"] + [f"{ytd[s][2026] / ytd[s][2025] - 1:+.1%}" for s in TODOS]],
    )
    t_part = md_table(
        ["Ano"] + [ROTULO[s] for s in SUBSISTEMAS],
        [[y] + [f"{100 * part[s][y]:.1f}%" for s in SUBSISTEMAS] for y in ANOS_COMPLETOS],
    )
    t_ext = md_table(
        ["Subsistema", "Maior hora da série", "Quando", "Menor hora da série", "Quando", "Razão máx/mín"],
        [[ROTULO[s],
          f"{max(extremos[s][y][0][1] for y in extremos[s]) / 1000:.2f} GW",
          max((extremos[s][y][0] for y in extremos[s]), key=lambda kv: kv[1])[0].strftime("%d/%m/%Y %Hh"),
          f"{min(extremos[s][y][1][1] for y in extremos[s]) / 1000:.2f} GW",
          min((extremos[s][y][1] for y in extremos[s]), key=lambda kv: kv[1])[0].strftime("%d/%m/%Y %Hh"),
          f"{max(extremos[s][y][0][1] for y in extremos[s]) / min(extremos[s][y][1][1] for y in extremos[s]):.2f}×"]
         for s in TODOS],
    )

    # meses de maior e menor carga (média 2024-2025) por subsistema
    t_meses = []
    for s in TODOS:
        mm = {m: st.mean(mensal[s][(y, m)] for y in (2024, 2025)) for m in range(1, 13)}
        hi = max(mm, key=mm.get)
        lo = min(mm, key=mm.get)
        t_meses.append([ROTULO[s], f"{hi:02d} ({mm[hi] / 1000:.1f} GW)", f"{lo:02d} ({mm[lo] / 1000:.1f} GW)", f"{mm[hi] / mm[lo] - 1:+.1%}"])
    t_meses = md_table(["Subsistema", "Mês de maior carga", "Mês de menor carga", "Diferença"], t_meses)

    doc = f"""# Bloco 2 — Nível

> Gerado por `src/eda/bloco02_nivel.py` sobre a extração de {ultimo:%d/%m/%Y}. Tabelas e gráficos são reproduzíveis; a interpretação ao final é do analista e está datada.

Pergunta do bloco: **quanto** o sistema demanda, como isso evoluiu e onde a carga está concentrada. Unidade: GWmed (média de potência). Artefatos de dado (`data/reference/anomalias.csv`, tratamento `excluir`) ficam fora dos extremos; nas médias, seu efeito é desprezível.

## 1. Evolução mensal

![Carga média mensal por subsistema](img/02_media_mensal_subsistemas.png)

## 2. Média anual (anos completos)

{t_anual}

Variação ano a ano:

{t_var}

## 3. Comparação de períodos equivalentes (YTD)

O último dia disponível de 2026 é {ultimo:%d/%m}. A tabela compara 1º/jan–{ultimo:%d/%m} nos três anos do regime atual.

{t_ytd}

![YTD 2024, 2025 e 2026](img/02_ytd_2024_2025_2026.png)

## 4. Onde a carga está concentrada

{t_part}

![Participação dos subsistemas](img/02_participacao_subsistemas.png)

## 5. Extremos

{t_ext}

![Faixa entre mínimo e máximo horário por ano](img/02_extremos_por_ano.png)

## 6. Meses de maior e menor carga (média 2024–2025)

{t_meses}

## 7. Leitura (analista, 13/09/2026; revisada após a ampliação para 2017)

**Quanto.** No regime atual, o SIN demanda cerca de **80 GWmed** em média — 44 no Sudeste/Centro-Oeste, 14 no Sul, 13 no Nordeste e 8 no Norte. O pico horário absoluto foi de 106 GW em 26/02/2025, numa onda de calor; a menor hora foi de 40 GW, num domingo de maio de 2020, em plena pandemia. O sistema opera, portanto, numa faixa de **2,6×** entre a hora mais leve e a mais pesada da série.

**Como evoluiu — a leitura ingênua e a correta.** A carga registrada do SIN subiu **+23% entre 2019 e 2025**. Mas os três maiores saltos anuais coincidem com o que não é demanda: 2021 (+8%) mistura recuperação pós-COVID com a entrada da "carga global"; 2023 (+7%) e 2024 (+7%) são a entrada da MMGD estimada em abril/2023 e seu primeiro ano cheio. Quando se compara **sob a mesma metodologia** — 2025 contra 2024, e o YTD de 2026 contra o de 2025 — o SIN cresce **+0,8% e +1,0%**. E o mesmo se vê no regime original: de 2017 a 2019, também sem mudança de metodologia, o SIN cresceu +3,0% em dois anos (~1,5% ao ano) — o mesmo ritmo. A história defensável não é "a demanda explodiu"; é "a carga *registrada* saltou por mudanças de medição, e a demanda sob regime homogêneo cresce devagar".

**Onde — e quem cresce.** O Sudeste/Centro-Oeste concentra 56% da carga, mas perde participação todo ano (57,5% → 55,6%). No regime atual ele está **estável ou em leve queda** (−0,5% em 2025; −0,4% no YTD 2026). Quem cresce é o **Norte**: +6% ao ano em 2025 e 2026, passando de 8,5% para 10,4% do SIN — o único subsistema cujo crescimento se mantém forte *dentro* do regime homogêneo. Nordeste e Sul crescem +2 a +3% ao ano. Hipótese para o bloco 10: o que está por trás do Norte (carga industrial no Pará, expansão em Manaus, interligações novas) e se a estabilidade do SE reflete MMGD *dentro* da estimativa do ONS ou saturação real.

**Sazonalidade em primeira leitura.** Os subsistemas têm calendários diferentes: SE e S atingem o máximo em **fevereiro** e o mínimo em **junho/julho** (verão = ar-condicionado); o NE tem máximo em **novembro** e mínimo em julho; o N tem máximo em **setembro** (estação seca e quente) e mínimo em **janeiro** (chuvas). A amplitude sazonal vai de **13% no NE a 28% no S** — o Sul é o subsistema mais sensível ao clima, o que os extremos confirmam: sua razão máx/mín é 3,95×, contra 2,34× no NE. O bloco 3 aprofunda.

**Os picos crescem mais que a base.** No gráfico de extremos, o mínimo anual de cada subsistema é quase estável (S: 6–7 GW todos os anos), enquanto o máximo sobe (S: 18,7 → 22,7 GW). A faixa se alarga por cima — consistente com demanda de climatização em dias quentes, e relevante para o bloco 6 (amplitude).

**Ressalva.** O mínimo do Norte (2,97 GW, 19/04/2020) cai no mês sinalizado como não explicado (A2); não foi excluído porque o tratamento é `sinalizar`, mas não deve ser citado como "menor demanda real" sem essa nota.

**O que leva para o produto.** (1) A tabela YTD e a variação sob regime homogêneo são o KPI de nível correto — não a variação 2019→2025. (2) O gráfico de participação conta a história "o Norte cresce, o SE perde peso". (3) Os marcos metodológicos precisam estar em qualquer série histórica de nível.
"""
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(doc, encoding="utf-8")
    print(f"  documento: {DOC_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
