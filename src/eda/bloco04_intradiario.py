"""
Bloco 4 da exploração — Ciclo intradiário.

Como a carga se distribui pelas 24 horas: o "dia típico" de cada subsistema
por tipo de dia e por estação, no núcleo comparável 2024–2025.
Gera docs/eda/img/04_*.png e docs/eda/04-intradiario.md.

Uso: python src\\eda\\bloco04_intradiario.py
"""

from __future__ import annotations

import statistics as st
from collections import defaultdict
from datetime import date, datetime, time

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from comum import (COR, PROJECT_ROOT, ROTULO, SUBSISTEMAS, TEXTO_2, carregar_anomalias, carregar_dim,
                   carregar_fato, estilo, horas_excluidas, md_table, salvar)

DOC_PATH = PROJECT_ROOT / "docs" / "eda" / "04-intradiario.md"
TODOS = ["SIN"] + SUBSISTEMAS
NUCLEO = (2024, 2025)
TIPOS = ["Dia útil", "Sábado", "Domingo", "Feriado"]
COR_TIPO = {"Dia útil": "#2a78d6", "Sábado": "#1baf7a", "Domingo": "#eb6834", "Feriado": "#4a3aa7"}
ESTACOES = ["Verão", "Outono", "Inverno", "Primavera"]
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
RAMPA = LinearSegmentedColormap.from_list("azul", ["#f4f8fd", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])


def perfis_diarios(serie, dim, excluidas, s):
    """{data: [24 valores]} apenas para dias completos e não excluídos."""
    dias = defaultdict(dict)
    for t, v in serie[s].items():
        if s == "SIN":
            if any((x, t) in excluidas for x in SUBSISTEMAS):
                continue
        elif (s, t) in excluidas:
            continue
        dias[t.date()][t.hour] = v
    return {d: [h[k] for k in range(24)] for d, h in dias.items() if len(h) == 24}


def tipo_dia(dim, d: date) -> str | None:
    r = dim[d]
    if r["TipoDia"] == "Dia útil" and r["Recesso"] == "Sim":
        return None  # recesso de fim de ano (24/12–02/01) fica fora de qualquer curva típica
    return r["TipoDia"]


def media_perfis(perfis: list[list[float]]) -> list[float]:
    return [st.mean(p[h] for p in perfis) for h in range(24)]


def normalizar(p: list[float]) -> list[float]:
    m = st.mean(p)
    return [x / m for x in p]


def metricas(p: list[float]) -> dict:
    pico, vale = max(p), min(p)
    media = st.mean(p)
    return {
        "hora_pico": p.index(pico), "hora_vale": p.index(vale),
        "pico": pico, "vale": vale, "media": media,
        "amplitude_rel": (pico - vale) / media, "fator_carga": media / pico,
    }


def main() -> None:
    estilo()
    serie = carregar_fato()
    dim = carregar_dim()
    excluidas = horas_excluidas(carregar_anomalias(), escopo="horario")
    ultimo = max(serie["SIN"]).date()

    perfis = {s: perfis_diarios(serie, dim, excluidas, s) for s in TODOS}
    nucleo = {s: {d: p for d, p in perfis[s].items() if d.year in NUCLEO} for s in TODOS}

    # ---------- curvas típicas por tipo de dia (absoluto e normalizado) ----------
    tipico = {s: {} for s in TODOS}       # média dos perfis absolutos
    tipico_norm = {s: {} for s in TODOS}  # média dos perfis normalizados (cada dia pesa igual)
    n_dias = {s: {} for s in TODOS}
    for s in TODOS:
        for t in TIPOS:
            ps = [p for d, p in nucleo[s].items() if tipo_dia(dim, d) == t]
            n_dias[s][t] = len(ps)
            tipico[s][t] = media_perfis(ps)
            tipico_norm[s][t] = media_perfis([normalizar(p) for p in ps])

    # gráfico 1: dia típico absoluto, por subsistema, um traço por tipo de dia
    fig, axes = plt.subplots(1, 5, figsize=(16, 4.2), gridspec_kw={"width_ratios": [1.3, 1, 1, 1, 1]})
    for ax, s in zip(axes, TODOS):
        for t in TIPOS:
            ax.plot(range(24), [v / 1000 for v in tipico[s][t]], color=COR_TIPO[t], label=t, linewidth=2 if t == "Dia útil" else 1.6)
        m = metricas(tipico[s]["Dia útil"])
        ax.plot(m["hora_pico"], m["pico"] / 1000, "o", color=COR_TIPO["Dia útil"], markersize=6)
        ax.text(m["hora_pico"], m["pico"] / 1000, f"  pico {m['hora_pico']}h", fontsize=8, va="bottom", ha="left" if m["hora_pico"] < 18 else "right")
        ax.set_title(ROTULO[s], fontsize=10)
        ax.set_xticks([0, 6, 12, 18, 23])
        ax.set_xticklabels(["0h", "6h", "12h", "18h", "23h"], fontsize=8)
        ax.grid(axis="x", visible=False)
        if s == "SIN":
            ax.set_ylabel("GWmed")
            ax.legend(fontsize=8, loc="lower right")
    fig.suptitle("Dia típico por tipo de dia, 2024–2025 (média das 24 horas de cada dia do tipo; escalas independentes)",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "04_dia_tipico_por_tipo_de_dia.png")

    # gráfico 2: normalizado, subsistemas sobrepostos, dia útil e domingo
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), sharey=True)
    for ax, t in zip(axes, ("Dia útil", "Domingo")):
        for s in SUBSISTEMAS:
            ys = [100 * (v - 1) for v in tipico_norm[s][t]]
            ax.plot(range(24), ys, color=COR[s], label=ROTULO[s])
            ax.text(23.2, ys[-1], ROTULO[s].split("/")[0], color=COR[s], fontsize=8, va="center")
        ax.axhline(0, color=TEXTO_2, linewidth=0.8)
        ax.set_title(f"{t} — cada hora em relação à média do dia")
        ax.set_xticks(range(0, 24, 2))
        ax.set_xlim(0, 25.5)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("% acima/abaixo da média do dia")
    axes[0].legend(fontsize=8, loc="upper left")
    fig.suptitle("Formato do dia, sem o efeito de escala — 2024–2025", x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "04_formato_normalizado_subsistemas.png")

    # ---------- heatmap hora × mês (dia útil, normalizado) ----------
    hm = {s: [[None] * 12 for _ in range(24)] for s in TODOS}
    for s in TODOS:
        for m in range(1, 13):
            ps = [normalizar(p) for d, p in nucleo[s].items() if d.month == m and tipo_dia(dim, d) == "Dia útil"]
            prof = media_perfis(ps)
            for h in range(24):
                hm[s][h][m - 1] = 100 * (prof[h] - 1)
    fig, axes = plt.subplots(1, 5, figsize=(16, 5.2), gridspec_kw={"width_ratios": [1.3, 1, 1, 1, 1, ]})
    vmin, vmax = -25, 25
    for ax, s in zip(axes, TODOS):
        im = ax.imshow(hm[s], aspect="auto", cmap=RAMPA, vmin=vmin, vmax=vmax, origin="lower")
        ax.set_title(ROTULO[s], fontsize=10)
        ax.set_xticks(range(12))
        ax.set_xticklabels([m[0] for m in MESES], fontsize=8)
        ax.set_yticks(range(0, 24, 3))
        ax.set_yticklabels([f"{h}h" for h in range(0, 24, 3)], fontsize=8)
        ax.grid(False)
        # marca a hora do pico de cada mês
        for m in range(12):
            col = [hm[s][h][m] for h in range(24)]
            ax.plot(m, col.index(max(col)), marker="_", color="white", markersize=9, markeredgewidth=2)
    cb = fig.colorbar(im, ax=axes, fraction=0.015, pad=0.01)
    cb.set_label("% em relação à média do dia")
    fig.suptitle("Dia útil por mês — quando a carga está acima da média do dia (traço branco = hora do pico do mês), 2024–2025",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    salvar(fig, "04_heatmap_hora_mes.png")

    # ---------- distribuição da hora do pico por estação (dia útil) ----------
    faixas = [("Madrugada 0–5h", range(0, 6)), ("Manhã 6–11h", range(6, 12)), ("Tarde 12–17h", range(12, 18)), ("Noite 18–23h", range(18, 24))]
    dist = {s: {} for s in TODOS}
    for s in TODOS:
        for e in ESTACOES:
            horas = [p.index(max(p)) for d, p in nucleo[s].items() if tipo_dia(dim, d) == "Dia útil" and dim[d]["EstacaoAno"] == e]
            dist[s][e] = {nome: sum(h in faixa for h in horas) / len(horas) for nome, faixa in faixas}
    fig, axes = plt.subplots(1, 5, figsize=(16, 3.8), sharey=True, gridspec_kw={"width_ratios": [1.3, 1, 1, 1, 1]})
    cores_faixa = ["#c3c2b7", "#86b6ef", "#eda100", "#4a3aa7"]
    for ax, s in zip(axes, TODOS):
        base = [0] * 4
        for (nome, _), cor in zip(faixas, cores_faixa):
            ys = [100 * dist[s][e][nome] for e in ESTACOES]
            ax.bar(range(4), ys, bottom=base, color=cor, width=0.65, label=nome, edgecolor="white", linewidth=1)
            for i, (b, y) in enumerate(zip(base, ys)):
                if y >= 12:
                    ax.text(i, b + y / 2, f"{y:.0f}", ha="center", va="center", fontsize=7, color="white" if cor != "#c3c2b7" else TEXTO_2)
            base = [b + y for b, y in zip(base, ys)]
        ax.set_xticks(range(4))
        ax.set_xticklabels(ESTACOES, fontsize=8)
        ax.set_title(ROTULO[s], fontsize=10)
        ax.grid(axis="x", visible=False)
        if s == "SIN":
            ax.set_ylabel("% dos dias úteis")
            ax.legend(fontsize=7, loc="lower left", ncol=2)
    fig.suptitle("Em que período do dia ocorre o pico? Dias úteis de 2024–2025, por estação", x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "04_periodo_do_pico_por_estacao.png")

    # ---------- tabelas ----------
    linhas = []
    for s in TODOS:
        for t in TIPOS:
            m = metricas(tipico[s][t])
            linhas.append([ROTULO[s], t, n_dias[s][t], f"{m['media'] / 1000:.1f}", f"{m['pico'] / 1000:.1f}", f"{m['hora_pico']}h",
                           f"{m['vale'] / 1000:.1f}", f"{m['hora_vale']}h", f"{100 * m['amplitude_rel']:.0f}%", f"{m['fator_carga']:.2f}"])
    t_tipos = md_table(["Subsistema", "Tipo de dia", "Dias", "Média (GW)", "Pico (GW)", "Hora", "Vale (GW)", "Hora", "Amplitude ÷ média", "Fator de carga"], linhas)

    linhas = []
    for s in TODOS:
        for e in ESTACOES:
            ps = [p for d, p in nucleo[s].items() if tipo_dia(dim, d) == "Dia útil" and dim[d]["EstacaoAno"] == e]
            m = metricas(media_perfis(ps))
            linhas.append([ROTULO[s], e, f"{m['hora_pico']}h", f"{m['hora_vale']}h", f"{100 * m['amplitude_rel']:.0f}%", f"{m['fator_carga']:.2f}",
                           f"{100 * (dist[s][e]['Tarde 12–17h']):.0f}%", f"{100 * (dist[s][e]['Noite 18–23h']):.0f}%"])
    t_estacao = md_table(["Subsistema", "Estação (dia útil)", "Hora do pico", "Hora do vale", "Amplitude ÷ média", "Fator de carga", "Pico à tarde", "Pico à noite"], linhas)

    # perfil normalizado dia útil, tabela de horas-chave
    horas_chave = [3, 6, 9, 12, 15, 18, 19, 21, 23]
    t_norm = md_table(["Dia útil, hora"] + [ROTULO[s] for s in TODOS],
                      [[f"{h}h"] + [f"{100 * (tipico_norm[s]['Dia útil'][h] - 1):+.0f}%" for s in TODOS] for h in horas_chave])

    doc = f"""# Bloco 4 — Ciclo intradiário

> Gerado por `src/eda/bloco04_intradiario.py` sobre a extração de {ultimo:%d/%m/%Y}. Tabelas e gráficos são reproduzíveis; a interpretação ao final é do analista e está datada.

Pergunta do bloco: **como a carga se distribui pelas 24 horas** — o "dia típico" de cada subsistema — e como esse formato muda entre tipos de dia e estações. Janela: núcleo comparável 2024–2025. Dias com horas excluídas em `anomalias.csv` (escopo horário) e dias úteis do recesso de fim de ano (24/12–02/01) ficam fora. "Dia típico" é a média, hora a hora, de todos os dias do tipo; a versão normalizada divide cada dia pela sua própria média antes de tirar a média, para que cada dia pese igual.

## 1. O dia típico por tipo de dia

![Dia típico por tipo de dia](img/04_dia_tipico_por_tipo_de_dia.png)

{t_tipos}

## 2. O formato sem a escala

![Formato normalizado](img/04_formato_normalizado_subsistemas.png)

{t_norm}

## 3. O dia típico muda com a estação?

![Heatmap hora × mês](img/04_heatmap_hora_mes.png)

![Período do pico por estação](img/04_periodo_do_pico_por_estacao.png)

{t_estacao}

## 4. Leitura (analista, 13/09/2026)

**O dia típico do Brasil.** Num dia útil de 2024–2025 o SIN acorda no vale das **4h** (−16% da média), sobe até as 9h, fica num patamar alto a tarde inteira (+8% às 15h) e atinge o pico às **19h** (+11%), quando ainda há carga comercial e a residencial já entrou. A amplitude entre vale e pico é 27% da média; o fator de carga, 0,90 — a hora mais pesada é só 10% acima da média, o que diz que o sistema é relativamente "plano". Sábado e domingo mantêm o pico às 19h, mas perdem a manhã: o vale desliza para 5–6h e a subida matinal some.

**Existem dois formatos de dia no país, não um.** Sudeste/Centro-Oeste e Sul têm o dia "clássico": vale profundo na madrugada (−19% e **−25%** às 3h), rampa da manhã, tarde alta, pico às 19h (+13% e +16%). Nordeste e Norte são quase planos: madrugada só −4 a −6%, mínimo às 6h, amplitude de 17–19% contra 31–40%. E o pico está em outro lugar: no **Nordeste às 21–22h**, tarde da noite; no **Norte às 14h**, com a noite abaixo da média. Fator de carga de 0,92 e 0,94 — o Norte é o subsistema mais plano do Brasil, consistente com a base industrial contínua identificada nos blocos anteriores. Somar tudo no SIN produz o formato do SE, porque o SE é 56% do total.

**O pico muda de lugar com a estação — e isso é a chave do produto.** No verão, o pico do SIN é às **14h** em 82% dos dias úteis; no inverno, é às **18–19h** em 95% deles. No SE e no Sul a explicação é o ar-condicionado: no verão ele enche a tarde e o dia fica *mais plano* (amplitude 27% no SE, 37% no Sul); no inverno, sem climatização diurna, a tarde cai e a noite (iluminação, chuveiro, aquecimento) vira o pico isolado — amplitude 37% no SE e **50% no Sul**, a maior do país. Ou seja: o inverno tem menos carga, mas um dia mais "pontudo". O heatmap mostra isso como duas manchas: uma às 14–15h de novembro a março, outra às 18–19h de abril a setembro. No **Nordeste** o pico é noturno em todas as estações (90–99% dos dias), só desliza de 18h no inverno para 22h no verão. No **Norte** o pico é à tarde (14–15h) em outono, inverno e primavera, mas no verão — a estação chuvosa — migra para as 22h, quando o calor diurno alivia.

**O que isso muda nas perguntas do projeto.** A pergunta "em que horário ocorre o pico?" não tem uma resposta; tem uma por subsistema e por estação. Uma média anual da hora do pico (o que um dashboard ingênuo mostraria) misturaria 14h e 19h e produziria um número que não acontece em nenhum dia. O bloco 8 vai perguntar se essa alternância verão/inverno é nova (efeito do ar-condicionado e da MMGD) ou se 2019 já era assim.

**O que leva para o produto.** (1) O gráfico de formato normalizado com os quatro subsistemas sobrepostos é a **assinatura visual** da "anatomia": mostra em uma imagem que o país tem dois formatos de dia. (2) O heatmap hora × mês é o segundo candidato — resolve "quando é o pico?" sem forçar uma resposta única. (3) A tabela de tipo de dia sustenta as medidas de pico, vale, amplitude e fator de carga com definições explícitas.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    print(f"  documento: {DOC_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
