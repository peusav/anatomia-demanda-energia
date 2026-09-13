"""
Bloco 3 da exploração — Sazonalidade.

Padrões que se repetem: ao longo do ano (mês) e ao longo da semana
(dia útil, sábado, domingo, feriado). Gera docs/eda/img/03_*.png e
docs/eda/03-sazonalidade.md.

Uso: python src\\eda\\bloco03_sazonalidade.py
"""

from __future__ import annotations

import statistics as st
from collections import defaultdict
from datetime import date

import matplotlib.pyplot as plt

from comum import (COR, PROJECT_ROOT, ROTULO, SUBSISTEMAS, TEXTO_2, carregar_anomalias, carregar_dim,
                   carregar_fato, estilo, horas_excluidas, md_table, media_diaria, salvar)

DOC_PATH = PROJECT_ROOT / "docs" / "eda" / "03-sazonalidade.md"
TODOS = ["SIN"] + SUBSISTEMAS
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
NUCLEO = (2024, 2025)
ANOS_COMPLETOS = [2019, 2021, 2022, 2023, 2024, 2025]  # 2020 fora do "típico" (D04)


def main() -> None:
    estilo()
    serie = carregar_fato()
    dim = carregar_dim()
    excluidas = horas_excluidas(carregar_anomalias(), escopo="diario")
    ultimo = max(serie["SIN"]).date()

    # dias a excluir (qualquer hora excluída no subsistema; para o SIN, em qualquer subsistema)
    dias_excluidos = {s: {t.date() for (x, t) in excluidas if x == s} for s in SUBSISTEMAS}
    dias_excluidos["SIN"] = set().union(*dias_excluidos.values())

    diaria = {s: {d: v for d, v in media_diaria(serie[s]).items() if d not in dias_excluidos[s]} for s in TODOS}

    def tipo(d: date) -> str:
        r = dim[d]
        if r["TipoDia"] == "Dia útil" and r["Vespera"] != "-":
            return "Véspera"
        return r["TipoDia"]

    # ---------- índice mensal: média do mês ÷ média do ano ----------
    indice_mensal = {s: {} for s in TODOS}
    for s in TODOS:
        for y in ANOS_COMPLETOS:
            ano = [v for d, v in diaria[s].items() if d.year == y]
            media_ano = st.mean(ano)
            for m in range(1, 13):
                mes = [v for d, v in diaria[s].items() if d.year == y and d.month == m]
                indice_mensal[s][(y, m)] = st.mean(mes) / media_ano

    fig, axes = plt.subplots(1, 5, figsize=(15, 4.2), sharey=True, gridspec_kw={"width_ratios": [1.3, 1, 1, 1, 1]})
    for ax, s in zip(axes, TODOS):
        for y, alpha, lw, ls in ((2019, 0.35, 1.5, "--"), (2022, 0.35, 1.5, ":"), (2024, 0.8, 2, "-"), (2025, 1, 2.4, "-")):
            ys = [100 * (indice_mensal[s][(y, m)] - 1) for m in range(1, 13)]
            ax.plot(range(1, 13), ys, color=COR[s], alpha=alpha, linewidth=lw, linestyle=ls, label=str(y))
        ax.axhline(0, color=TEXTO_2, linewidth=0.8)
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels([m[0] for m in MESES], fontsize=8)
        ax.set_title(ROTULO[s], fontsize=10)
        ax.grid(axis="x", visible=False)
        if s == "SIN":
            ax.set_ylabel("% acima/abaixo da média do ano")
            ax.legend(fontsize=8, loc="lower left", ncol=2)
    fig.suptitle("Índice sazonal mensal — cada mês em relação à média do próprio ano (2019 e 2022 tracejados; 2024 e 2025 cheios)",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "03_indice_mensal.png")

    # ---------- amplitude sazonal por ano ----------
    amp = {s: {y: max(indice_mensal[s][(y, m)] for m in range(1, 13)) - min(indice_mensal[s][(y, m)] for m in range(1, 13))
               for y in ANOS_COMPLETOS} for s in TODOS}
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for s in SUBSISTEMAS:
        ys = [100 * amp[s][y] for y in ANOS_COMPLETOS]
        ax.plot(ANOS_COMPLETOS, ys, color=COR[s], marker="o", markersize=5)
        ax.text(ANOS_COMPLETOS[-1] + 0.1, ys[-1], f"{ROTULO[s]} {ys[-1]:.0f} p.p.", color=COR[s], va="center", fontsize=9)
    ax.set_xlim(2018.7, 2027)
    ax.set_xticks(ANOS_COMPLETOS)
    ax.set_ylabel("mês mais alto − mês mais baixo (p.p. da média anual)")
    ax.set_title("Amplitude sazonal por ano (2020 omitido)")
    fig.tight_layout()
    salvar(fig, "03_amplitude_sazonal_por_ano.png")

    # ---------- índice por tipo de dia (núcleo 2024-2025) ----------
    tipos = ["Dia útil", "Sábado", "Domingo", "Feriado", "Véspera"]
    indice_tipo = {s: {} for s in TODOS}
    indice_dow = {s: {} for s in TODOS}
    for s in TODOS:
        nucleo = {d: v for d, v in diaria[s].items() if d.year in NUCLEO}
        base = st.mean(v for d, v in nucleo.items() if tipo(d) == "Dia útil")
        for t in tipos:
            vals = [v for d, v in nucleo.items() if tipo(d) == t]
            indice_tipo[s][t] = (st.mean(vals) / base, len(vals))
        for i in range(1, 8):
            vals = [v for d, v in nucleo.items() if d.isoweekday() == i and dim[d]["Feriado"] == "Não" and dim[d]["PontoFacultativo"] == "-" and dim[d]["Vespera"] == "-"]
            indice_dow[s][i] = st.mean(vals) / base

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axes[0]
    for s in SUBSISTEMAS:
        ys = [100 * (indice_dow[s][i] - 1) for i in range(1, 8)]
        ax.plot(range(1, 8), ys, color=COR[s], marker="o", markersize=5, label=ROTULO[s])
        ax.text(7.1, ys[-1], f"{ys[-1]:+.0f}%", color=COR[s], va="center", fontsize=9)
    ax.axhline(0, color=TEXTO_2, linewidth=0.8)
    ax.set_xticks(range(1, 8))
    ax.set_xticklabels(DIAS)
    ax.set_xlim(0.7, 7.6)
    ax.set_ylabel("% em relação ao dia útil médio")
    ax.set_title("Dia da semana (sem feriados, pontos facultativos e vésperas), 2024–2025")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(axis="x", visible=False)
    ax = axes[1]
    largura = 0.18
    for k, s in enumerate(SUBSISTEMAS):
        ys = [100 * (indice_tipo[s][t][0] - 1) for t in tipos[1:]]
        xs = [i + (k - 1.5) * largura for i in range(len(ys))]
        ax.bar(xs, ys, width=largura, color=COR[s])
        for x, y in zip(xs, ys):
            ax.text(x, y - 0.6, f"{y:.0f}", ha="center", va="top", fontsize=7, color="white" if abs(y) > 6 else TEXTO_2)
    ax.set_xticks(range(len(tipos) - 1))
    ax.set_xticklabels(tipos[1:])
    ax.axhline(0, color=TEXTO_2, linewidth=0.8)
    ax.set_title("Tipo de dia em relação ao dia útil, 2024–2025")
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    salvar(fig, "03_dia_da_semana_e_tipo_de_dia.png")

    # ---------- evolução do desconto de fim de semana por ano ----------
    dom_por_ano = {s: {} for s in TODOS}
    for s in TODOS:
        for y in ANOS_COMPLETOS:
            ano = {d: v for d, v in diaria[s].items() if d.year == y}
            base = st.mean(v for d, v in ano.items() if tipo(d) == "Dia útil")
            dom_por_ano[s][y] = {t: st.mean(v for d, v in ano.items() if tipo(d) == t) / base for t in ("Sábado", "Domingo")}
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
    for ax, t in zip(axes, ("Sábado", "Domingo")):
        for s in SUBSISTEMAS:
            ys = [100 * (dom_por_ano[s][y][t] - 1) for y in ANOS_COMPLETOS]
            ax.plot(ANOS_COMPLETOS, ys, color=COR[s], marker="o", markersize=4)
            ax.text(ANOS_COMPLETOS[-1] + 0.1, ys[-1], ROTULO[s], color=COR[s], va="center", fontsize=8)
        ax.set_title(f"{t} em relação ao dia útil do mesmo ano")
        ax.set_xticks(ANOS_COMPLETOS)
        ax.set_xlim(2018.7, 2027.2)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("%")
    fig.suptitle("O desconto de fim de semana mudou? (2020 omitido)", x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "03_fim_de_semana_por_ano.png")

    # ---------- sazonalidade × tipo de dia: desconto de domingo por estação (núcleo) ----------
    estacoes = ["Verão", "Outono", "Inverno", "Primavera"]
    dom_estacao = {s: {} for s in TODOS}
    for s in TODOS:
        nucleo = {d: v for d, v in diaria[s].items() if d.year in NUCLEO}
        for e in estacoes:
            base = st.mean(v for d, v in nucleo.items() if tipo(d) == "Dia útil" and dim[d]["EstacaoAno"] == e)
            dom = st.mean(v for d, v in nucleo.items() if tipo(d) == "Domingo" and dim[d]["EstacaoAno"] == e)
            dom_estacao[s][e] = dom / base

    # ---------- tabelas ----------
    t_mensal = md_table(
        ["Mês"] + [ROTULO[s] for s in TODOS],
        [[MESES[m - 1]] + [f"{100 * (st.mean(indice_mensal[s][(y, m)] for y in NUCLEO) - 1):+.1f}%" for s in TODOS] for m in range(1, 13)],
    )
    t_amp = md_table(
        ["Ano"] + [ROTULO[s] for s in TODOS],
        [[y] + [f"{100 * amp[s][y]:.1f}" for s in TODOS] for y in ANOS_COMPLETOS],
    )
    t_tipo = md_table(
        ["Tipo de dia (2024–2025)", "Dias"] + [ROTULO[s] for s in TODOS],
        [[t, indice_tipo["SIN"][t][1]] + [f"{100 * (indice_tipo[s][t][0] - 1):+.1f}%" for s in TODOS] for t in tipos],
    )
    t_dow = md_table(
        ["Dia da semana (2024–2025)"] + [ROTULO[s] for s in TODOS],
        [[DIAS[i - 1]] + [f"{100 * (indice_dow[s][i] - 1):+.1f}%" for s in TODOS] for i in range(1, 8)],
    )
    t_dom_ano = md_table(
        ["Domingo ÷ dia útil"] + [ROTULO[s] for s in TODOS],
        [[y] + [f"{100 * (dom_por_ano[s][y]['Domingo'] - 1):+.1f}%" for s in TODOS] for y in ANOS_COMPLETOS],
    )
    t_dom_est = md_table(
        ["Domingo ÷ dia útil, por estação (2024–2025)"] + [ROTULO[s] for s in TODOS],
        [[e] + [f"{100 * (dom_estacao[s][e] - 1):+.1f}%" for s in TODOS] for e in estacoes],
    )

    doc = f"""# Bloco 3 — Sazonalidade

> Gerado por `src/eda/bloco03_sazonalidade.py` sobre a extração de {ultimo:%d/%m/%Y}. Tabelas e gráficos são reproduzíveis; a interpretação ao final é do analista e está datada.

Pergunta do bloco: quais padrões se **repetem** — ao longo do ano e ao longo da semana — e se eles são os mesmos em cada subsistema. Todos os índices são relativos (mês ÷ média do ano; tipo de dia ÷ dia útil), o que os torna comparáveis entre subsistemas de tamanhos diferentes e entre regimes metodológicos. 2020 fica fora (D04); dias com horas excluídas em `anomalias.csv` ficam fora; vésperas de Natal e Ano-Novo são um tipo de dia à parte.

## 1. Ao longo do ano

![Índice sazonal mensal](img/03_indice_mensal.png)

Índice médio de 2024–2025 (cada mês em relação à média do ano):

{t_mensal}

### A sazonalidade está mudando de intensidade?

![Amplitude sazonal por ano](img/03_amplitude_sazonal_por_ano.png)

{t_amp}

## 2. Ao longo da semana

![Dia da semana e tipo de dia](img/03_dia_da_semana_e_tipo_de_dia.png)

{t_dow}

{t_tipo}

### O desconto de fim de semana mudou ao longo dos anos?

![Fim de semana por ano](img/03_fim_de_semana_por_ano.png)

{t_dom_ano}

### Fim de semana × estação

{t_dom_est}

## 3. Leitura (analista, 13/09/2026)

**Quatro calendários, não um.** "O verão pesa mais" vale para o Sudeste/Centro-Oeste (fevereiro +10%, julho −8%) e sobretudo para o Sul (fevereiro **+18%**, junho −7%, setembro −7%). O Nordeste tem um ciclo suave (novembro +5%, julho −7%), com máximo na primavera. O Norte é o inverso do resto do país: máximo em **setembro–outubro (+8%)**, fim da estação seca, e mínimo em **janeiro–fevereiro (−7%)**, na estação chuvosa — exatamente quando SE e S estão no pico. O SIN (fevereiro +8%, julho −6%) é dominado pelo SE e esconde o Norte. É o argumento mais direto para o produto mostrar subsistemas em vez de só o Brasil.

**A intensidade da sazonalidade varia com o verão, e o Norte ficou mais sazonal.** No SE e no S não há tendência limpa: a amplitude entre o mês mais alto e o mais baixo foi de 23 p.p. em 2019, 14 em 2024 e 24 em 2025 no SE — o que muda é quão quente foi o verão (2025 teve a onda de calor dos recordes; 2024 não). No Sul, 2025 foi o ano mais sazonal da série (30 p.p.). O Nordeste é o mais estável (12–14 p.p., exceto 2023). O achado inesperado é o **Norte**: sua amplitude sazonal passou de 7 p.p. em 2019 para 15–20 p.p. desde 2022. Um subsistema que era quase plano ao longo do ano passou a ter um pico claro em setembro. Hipótese para o bloco 10: crescimento da carga residencial/comercial (climatização) em relação à industrial de base, que não tem estação.

**A semana tem dois formatos — e o Sul tem o fim de semana mais fundo.** De segunda a sexta a carga é plana (segunda −1,5%, o resto ±0,7%). Sábado cai **8%** e domingo **15%** no SIN. Mas a variação entre subsistemas é grande: no **Sul** o domingo cai **22%** e o sábado 13%; no **Norte**, o domingo cai só **8%** e o sábado 4%. Leitura: o Norte tem uma base industrial (eletrointensivos) que não para no fim de semana; o Sul tem carga comercial e industrial que para. Feriado fica entre sábado e domingo (−11%); véspera de Natal e Ano-Novo se comporta como sábado (−8%), menos no Nordeste (−3%).

**O domingo está ficando menos diferente — mas só a partir de 2024.** No SIN o desconto de domingo ficou em −15 a −17% de 2019 a 2023 e caiu para −15% em 2024 e **−14% em 2025**; no SE, de −16,6% para −13,9%; no Sul, de −25% para −21,6%. No NE e no N não mudou. O momento (2024–2025) e a geografia (SE e S, onde há mais MMGD) apontam para a estimativa de MMGD, somada igualmente em qualquer dia, como parte da explicação — a ser separada de crescimento residencial no bloco 8.

**Domingo de verão é menos domingo.** No Sul o desconto de domingo é −20% no verão contra −24% no outono/inverno; no NE, −10% contra −11 a −12%. Climatização residencial funciona no domingo. No SE a diferença é pequena (−14% vs −15%) e no Norte não há.

**O que leva para o produto.** (1) Um pequeno múltiplo do índice mensal por subsistema — o gráfico que diz "o Brasil não tem uma estação de pico, tem quatro". (2) A tabela de tipo de dia justifica, com números, a segmentação das curvas típicas e mostra que o formato da semana também é regional. (3) A tendência do domingo desde 2024 é candidata à Camada 3, condicionada ao bloco 8.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    print(f"  documento: {DOC_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
