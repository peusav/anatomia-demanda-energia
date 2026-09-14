"""
Blocos 7 e 8 da exploração — Curvas normalizadas; mudança histórica.

Bloco 7: compara as três normalizações candidatas (pela média do dia, pelo
pico do dia, min-max) sobre as mesmas curvas e fixa a escolha.
Bloco 8: como o formato do dia mudou de 2019 a 2026 — hora do pico, meio do
dia, noite, amplitude e convergência entre subsistemas — com os marcos
metodológicos visíveis.

Gera docs/eda/img/07_*.png, 08_*.png e docs/eda/07-08-normalizacao-mudanca.md.

Uso: python src\\eda\\bloco07_08_normalizacao_mudanca.py
"""

from __future__ import annotations

import statistics as st

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb

from bloco04_intradiario import media_perfis, metricas, normalizar, perfis_diarios, tipo_dia
from bloco05_06_subsistemas_amplitude import rms
from comum import (COR, PROJECT_ROOT, ROTULO, SUBSISTEMAS, TEXTO_2, carregar_anomalias, carregar_dim,
                   carregar_fato, estilo, horas_excluidas, md_table, salvar)

DOC_PATH = PROJECT_ROOT / "docs" / "eda" / "07-08-normalizacao-mudanca.md"
TODOS = ["SIN"] + SUBSISTEMAS
ANOS = [2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026]  # 2020 fora (D04); 2026 parcial
REGIME = {2017: "Supervisão", 2018: "Supervisão", 2019: "Supervisão", 2021: "misto", 2022: "Global", 2023: "misto", 2024: "Global+MMGD", 2025: "Global+MMGD", 2026: "Global+MMGD (YTD)"}
PARES = [("SE", "S"), ("NE", "N"), ("SE", "NE"), ("S", "N")]


def tons(cor_hex: str, n: int) -> list:
    """n tons da mesma cor, do claro ao escuro (rampa ordinal)."""
    r, g, b = to_rgb(cor_hex)
    cmap = LinearSegmentedColormap.from_list("t", [(0.75 + 0.25 * r, 0.75 + 0.25 * g, 0.75 + 0.25 * b), (r, g, b), (0.45 * r, 0.45 * g, 0.45 * b)])
    return [cmap(i / max(n - 1, 1)) for i in range(n)]


def norm_pico(p):
    m = max(p)
    return [x / m for x in p]


def norm_minmax(p):
    lo, hi = min(p), max(p)
    return [(x - lo) / (hi - lo) for x in p]


def main() -> None:
    estilo()
    serie = carregar_fato()
    dim = carregar_dim()
    excluidas = horas_excluidas(carregar_anomalias(), escopo="horario")
    ultimo = max(serie["SIN"]).date()
    corte = (ultimo.month, ultimo.day)

    perfis = {s: perfis_diarios(serie, dim, excluidas, s) for s in TODOS}
    uteis = {s: {d: p for d, p in perfis[s].items() if tipo_dia(dim, d) == "Dia útil"} for s in TODOS}

    # ================= BLOCO 7 =================
    nucleo = {s: [p for d, p in uteis[s].items() if d.year in (2024, 2025)] for s in SUBSISTEMAS}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    for ax, (nome, f, unidade) in zip(axes, (("Pela média do dia", normalizar, "hora ÷ média do dia"),
                                            ("Pelo pico do dia", norm_pico, "hora ÷ pico do dia"),
                                            ("Min-max", norm_minmax, "(hora − vale) ÷ (pico − vale)"))):
        for s in SUBSISTEMAS:
            curva = media_perfis([f(p) for p in nucleo[s]])
            ax.plot(range(24), curva, color=COR[s], label=ROTULO[s])
        ax.set_title(nome)
        ax.set_ylabel(unidade)
        ax.set_xticks(range(0, 24, 4))
        ax.grid(axis="x", visible=False)
    axes[0].legend(fontsize=8, loc="lower right")
    fig.suptitle("As mesmas quatro curvas (dia útil, 2024–2025) sob as três normalizações candidatas", x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "07_normalizacoes.png")

    linhas = []
    for s in SUBSISTEMAS:
        c_media = media_perfis([normalizar(p) for p in nucleo[s]])
        c_pico = media_perfis([norm_pico(p) for p in nucleo[s]])
        c_mm = media_perfis([norm_minmax(p) for p in nucleo[s]])
        linhas.append([ROTULO[s], f"{max(c_media) - min(c_media):.2f}", f"{1 - min(c_pico):.2f}", f"{max(c_mm) - min(c_mm):.2f}",
                       f"{c_media[3]:.2f} / {c_pico[3]:.2f} / {c_mm[3]:.2f}"])
    t_norm = md_table(["Subsistema", "Amplitude (÷ média)", "Amplitude (÷ pico)", "Amplitude (min-max)", "Valor às 3h (média / pico / min-max)"], linhas)

    # ================= BLOCO 8 =================
    # curvas típicas normalizadas de dia útil por ano (2026 só até o corte, e os outros anos idem para comparabilidade YTD)
    def amostra(s, y, ytd=False):
        return [p for d, p in uteis[s].items() if d.year == y and (not ytd or (d.month, d.day) <= corte)]

    tipico_ano = {s: {y: media_perfis([normalizar(p) for p in amostra(s, y)]) for y in ANOS} for s in TODOS}
    tipico_ano_ytd = {s: {y: media_perfis([normalizar(p) for p in amostra(s, y, ytd=True)]) for y in ANOS} for s in TODOS}

    # gráfico 1: formato por ano, rampa ordinal
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.4), sharey=True)
    for ax, s in zip(axes, SUBSISTEMAS):
        cores = tons(COR[s], len(ANOS))
        for y, c in zip(ANOS, cores):
            ys = [100 * (v - 1) for v in tipico_ano[s][y]]
            ax.plot(range(24), ys, color=c, linewidth=2.2 if y in (2017, 2025) else 1.3, label=str(y) + (" YTD" if y == 2026 else ""))
        ax.axhline(0, color=TEXTO_2, linewidth=0.8)
        ax.set_title(ROTULO[s], fontsize=10)
        ax.set_xticks(range(0, 24, 4))
        ax.grid(axis="x", visible=False)
        if s == "SE":
            ax.legend(fontsize=7, loc="lower right", ncol=2)
    axes[0].set_ylabel("% em relação à média do dia")
    fig.suptitle("Dia útil típico de cada ano, normalizado (claro = 2017 … escuro = 2026); 2020 omitido", x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "08_formato_por_ano.png")

    # indicadores por ano: meio do dia (12–15h), noite (18–21h), amplitude mediana, fator de carga
    ind = {s: {} for s in TODOS}
    for s in TODOS:
        for y in ANOS:
            ps = amostra(s, y)
            normas = [normalizar(p) for p in ps]
            ind[s][y] = {
                "meio_dia": st.mean(st.mean(n[12:16]) for n in normas),
                "noite": st.mean(st.mean(n[18:22]) for n in normas),
                "madrugada": st.mean(st.mean(n[1:5]) for n in normas),
                "amplitude": st.median(metricas(p)["amplitude_rel"] for p in ps),
                "fator": st.median(metricas(p)["fator_carga"] for p in ps),
                "pico_tarde": sum(12 <= metricas(p)["hora_pico"] <= 17 for p in ps) / len(ps),
                "pico_noite": sum(18 <= metricas(p)["hora_pico"] <= 23 for p in ps) / len(ps),
                "n": len(ps),
            }
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    for ax, (chave, titulo, fmt) in zip(axes, (("meio_dia", "Meio do dia (12–15h) em relação à média do dia", 100),
                                              ("noite", "Noite (18–21h) em relação à média do dia", 100),
                                              ("amplitude", "Amplitude mediana do dia útil (÷ média)", 100))):
        for s in SUBSISTEMAS:
            ys = [fmt * (ind[s][y][chave] - (1 if chave != "amplitude" else 0)) for y in ANOS]
            ax.plot(ANOS, ys, color=COR[s], marker="o", markersize=4)
            ax.text(ANOS[-1] + 0.15, ys[-1], ROTULO[s].split("/")[0], color=COR[s], fontsize=8, va="center")
        for x in (2021, 2023):
            ax.axvline(x - 0.5 if x == 2021 else x - 0.67, color=TEXTO_2, linewidth=1, linestyle=(0, (4, 3)))
        ax.set_title(titulo, fontsize=10)
        ax.set_xticks(ANOS)
        ax.set_xticklabels([str(y)[2:] + ("*" if y == 2026 else "") for y in ANOS])
        ax.set_xlim(2016.5, 2027.3)
        ax.grid(axis="x", visible=False)
        if chave != "amplitude":
            ax.axhline(0, color=TEXTO_2, linewidth=0.8)
    axes[0].set_ylabel("%")
    fig.suptitle("Indicadores de formato por ano, dias úteis (tracejado = marcos metodológicos 02/03/2021 e 29/04/2023; * = 2026 parcial; 2020 omitido)",
                 x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "08_indicadores_por_ano.png")

    # período do pico por ano
    fig, axes = plt.subplots(1, 5, figsize=(16, 3.8), sharey=True, gridspec_kw={"width_ratios": [1.3, 1, 1, 1, 1]})
    for ax, s in zip(axes, TODOS):
        tarde = [100 * ind[s][y]["pico_tarde"] for y in ANOS]
        noite = [100 * ind[s][y]["pico_noite"] for y in ANOS]
        outro = [100 - a - b for a, b in zip(tarde, noite)]
        xs = range(len(ANOS))
        ax.bar(xs, outro, color="#c3c2b7", width=0.65, label="Outro horário", edgecolor="white")
        ax.bar(xs, tarde, bottom=outro, color="#eda100", width=0.65, label="Tarde 12–17h", edgecolor="white")
        ax.bar(xs, noite, bottom=[o + t for o, t in zip(outro, tarde)], color="#4a3aa7", width=0.65, label="Noite 18–23h", edgecolor="white")
        for i, (o, t, n) in enumerate(zip(outro, tarde, noite)):
            if t >= 12:
                ax.text(i, o + t / 2, f"{t:.0f}", ha="center", va="center", fontsize=7, color="white")
            if n >= 12:
                ax.text(i, o + t + n / 2, f"{n:.0f}", ha="center", va="center", fontsize=7, color="white")
        ax.set_xticks(list(xs))
        ax.set_xticklabels([str(y)[2:] + ("*" if y == 2026 else "") for y in ANOS], fontsize=8)
        ax.set_title(ROTULO[s], fontsize=10)
        ax.grid(axis="x", visible=False)
        if s == "SIN":
            ax.set_ylabel("% dos dias úteis")
            ax.legend(fontsize=7, loc="lower left")
    fig.suptitle("Em que período do dia ocorre o pico? Dias úteis por ano (* = 2026 parcial; 2020 omitido)", x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    salvar(fig, "08_periodo_do_pico_por_ano.png")

    # convergência: distância entre pares por ano
    conv = {par: {y: 100 * rms(tipico_ano[a][y], tipico_ano[b][y]) for y in ANOS} for par in PARES for a, b in [par]}
    fig, ax = plt.subplots(figsize=(9, 4.4))
    estilos = ["-", "-", "--", "--"]
    for (a, b), ls in zip(PARES, estilos):
        ys = [conv[(a, b)][y] for y in ANOS]
        cor = COR[a] if ls == "-" else TEXTO_2
        ax.plot(ANOS, ys, color=cor, linestyle=ls, marker="o", markersize=4, alpha=1 if ls == "-" else 0.7)
        ax.text(ANOS[-1] + 0.15, ys[-1], f"{ROTULO[a].split('/')[0]} × {ROTULO[b].split('/')[0]}", color=cor, fontsize=8, va="center")
    for x in (2021, 2023):
        ax.axvline(x - 0.5 if x == 2021 else x - 0.67, color=TEXTO_2, linewidth=1, linestyle=(0, (4, 3)))
    ax.set_xticks(ANOS)
    ax.set_xticklabels([str(y)[2:] + ("*" if y == 2026 else "") for y in ANOS])
    ax.set_xlim(2016.5, 2027.6)
    ax.set_ylabel("distância de formato (p.p. da média do dia)")
    ax.set_title("Os subsistemas estão convergindo? Distância entre curvas típicas de dia útil, por ano")
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    salvar(fig, "08_convergencia_subsistemas.png")

    # por estação: hora do pico em verão e inverno, 2019 vs 2025
    def por_estacao(s, y, e):
        ps = [p for d, p in uteis[s].items() if d.year == y and dim[d]["EstacaoAno"] == e]
        if len(ps) < 10:
            return None
        normas = [normalizar(p) for p in ps]
        return {
            "n": len(ps),
            "pico_tarde": sum(12 <= metricas(p)["hora_pico"] <= 17 for p in ps) / len(ps),
            "meio_dia": st.mean(st.mean(n[12:16]) for n in normas),
            "noite": st.mean(st.mean(n[18:22]) for n in normas),
            "amplitude": st.median(metricas(p)["amplitude_rel"] for p in ps),
        }

    # ---------- tabelas ----------
    t_ind = md_table(
        ["Subsistema", "Ano", "Regime", "Dias", "Meio do dia 12–15h", "Noite 18–21h", "Madrugada 1–4h", "Amplitude mediana", "Fator de carga", "Pico à tarde", "Pico à noite"],
        [[ROTULO[s], y, REGIME[y], ind[s][y]["n"], f"{100 * (ind[s][y]['meio_dia'] - 1):+.1f}%", f"{100 * (ind[s][y]['noite'] - 1):+.1f}%",
          f"{100 * (ind[s][y]['madrugada'] - 1):+.1f}%", f"{100 * ind[s][y]['amplitude']:.0f}%", f"{ind[s][y]['fator']:.2f}",
          f"{100 * ind[s][y]['pico_tarde']:.0f}%", f"{100 * ind[s][y]['pico_noite']:.0f}%"] for s in TODOS for y in ANOS],
    )
    linhas = []
    for s in TODOS:
        for e in ("Verão", "Inverno"):
            for y in (2017, 2019, 2022, 2025):
                r = por_estacao(s, y, e)
                if r:
                    linhas.append([ROTULO[s], e, y, r["n"], f"{100 * r['pico_tarde']:.0f}%", f"{100 * (r['meio_dia'] - 1):+.1f}%", f"{100 * (r['noite'] - 1):+.1f}%", f"{100 * r['amplitude']:.0f}%"])
    t_est = md_table(["Subsistema", "Estação", "Ano", "Dias", "Pico à tarde", "Meio do dia 12–15h", "Noite 18–21h", "Amplitude mediana"], linhas)
    t_conv = md_table(["Par"] + [str(y) + ("*" if y == 2026 else "") for y in ANOS],
                      [[f"{ROTULO[a].split('/')[0]} × {ROTULO[b].split('/')[0]}"] + [f"{conv[(a, b)][y]:.1f}" for y in ANOS] for a, b in PARES])
    # YTD: 2024 × 2025 × 2026 mesmo intervalo
    linhas = []
    for s in TODOS:
        for y in (2024, 2025, 2026):
            c = tipico_ano_ytd[s][y]
            m = metricas(c)
            linhas.append([ROTULO[s], y, f"{100 * (st.mean(c[12:16]) - 1):+.1f}%", f"{100 * (st.mean(c[18:22]) - 1):+.1f}%", f"{m['hora_pico']}h", f"{100 * m['amplitude_rel']:.0f}%"])
    t_ytd = md_table([f"1º/jan–{ultimo:%d/%m}", "Ano", "Meio do dia", "Noite", "Hora do pico (curva típica)", "Amplitude"], linhas)

    doc = f"""# Blocos 7 e 8 — Curvas normalizadas; mudança histórica

> Gerado por `src/eda/bloco07_08_normalizacao_mudanca.py` sobre a extração de {ultimo:%d/%m/%Y}. Tabelas e gráficos são reproduzíveis; a interpretação ao final é do analista e está datada.

## Bloco 7 — Qual normalização?

As três candidatas de [03-metodologia.md](../03-metodologia.md) §6, aplicadas às mesmas curvas típicas de dia útil (2024–2025):

![Normalizações](img/07_normalizacoes.png)

{t_norm}

## Bloco 8 — Como o formato mudou, 2017 → 2026

Dias úteis; 2020 omitido (D04); janelas de horário de verão excluídas (A8, 2017–2019); dias com horas excluídas em `anomalias.csv` fora. Regimes: 2017–2019 = Supervisão ONS; 2021 e 2023 = anos mistos; 2022 = Carga global; 2024–2026 = Carga global + MMGD. **Toda diferença que atravessa 2021 ou 2023 mistura mudança de demanda com mudança de medição.**

![Formato por ano](img/08_formato_por_ano.png)

![Indicadores por ano](img/08_indicadores_por_ano.png)

![Período do pico por ano](img/08_periodo_do_pico_por_ano.png)

{t_ind}

### Verão e inverno separados: 2017 × 2019 × 2022 × 2025

{t_est}

### Mesmo intervalo de datas: 2024 × 2025 × 2026 (1º/jan–{ultimo:%d/%m})

{t_ytd}

### Os subsistemas estão convergindo?

![Convergência](img/08_convergencia_subsistemas.png)

{t_conv}

## Leitura (analista, 13/09/2026)

### Bloco 7 — a normalização pela média do dia fica confirmada

As três candidatas contam a mesma história de formato, mas com legibilidade diferente. **Min-max** apaga a informação de amplitude: as quatro curvas ficam com amplitude ≈ 0,9 e o Norte, que é o subsistema mais plano do país, parece tão "pontudo" quanto o Sul. **Pelo pico** preserva a amplitude, mas comprime tudo abaixo de 1,0 e reduz a separação visual (às 3h, NE 0,86 e N 0,89 — quase indistinguíveis). **Pela média** mantém a amplitude, separa bem as curvas e tem a leitura mais natural para a persona ("às 19h a carga está 13% acima da média do dia"). A decisão preliminar D05 passa a definitiva (D13); a normalização pelo pico fica como medida complementar para perguntas sobre o pico.

### Bloco 8 — o dia está girando: menos meio-dia, mais noite (leitura revisada após a ampliação para 2017)

**O achado central.** Em todos os subsistemas o meio do dia (12–15h) perdeu peso relativo e a noite (18–21h) ganhou. No SIN, o meio do dia esteve estável em **+9,5 a +9,9%** acima da média nos três anos do regime original (2017, 2018, 2019) e está **+3,7%** em 2026; a noite foi de +8,9% para +12,0%. No Nordeste a virada é completa: o meio do dia era +6,4% em 2019 e está **−2,6%** em 2026 — **abaixo da média do dia** — enquanto a noite dobrou (+3,6% → +9,3%). A amplitude quase não mudou (SE 36% → 34–35%; NE 24% → 21%); o que mudou foi *onde* a carga está no dia. O formato não achatou nem se alongou: **girou**, da tarde para a noite.

**A virada acontece sob regime homogêneo — não é só efeito de medição.** A comparação mais limpa é a YTD 2024 × 2025 × 2026 no mesmo intervalo de datas, toda sob "Carga global + MMGD": o meio do dia cai de +7,2% para +5,3% e +3,7% no SIN; no NE, de +2,9% para −0,5% e −2,6%; a noite sobe em todos. Cerca de **1,7 p.p. por ano** de rotação no SIN, sem nenhuma mudança de metodologia no caminho. A sequência anual completa mostra um detalhe que confirma a leitura: em 2024, primeiro ano cheio com a MMGD *somada* à carga, o meio do dia **sobe** em relação a 2023 (SIN +5,9% → +7,4%) — exatamente o que se espera quando se passa a contar uma geração diurna que antes era invisível — e depois **volta a cair** em 2025 e 2026. Ou seja: a estimativa de MMGD do ONS devolve parte do meio-dia, mas a rotação continua por baixo dela.

**A hora do pico virou uma questão de estação — e o inverno perdeu a tarde por completo.** Em 2017–2019 o pico do SIN ocorria à tarde em 44–58% dos dias úteis e no inverno em 15–25% deles; desde 2022 o inverno tem **0%** de picos à tarde em SE, S e NE. No verão a tarde ainda vence quando faz calor (84% em 2019, 75% em 2025, 52% no verão ameno de 2022). O resultado anual, por isso, oscila com o clima (51% à tarde em 2024, ano quente; 23% em 2025) e não deve ser lido como tendência sozinho — a tendência está nas estações separadas.

**O Nordeste é onde a história é mais forte.** Em 2017, 2018 e 2019, 82–92% dos dias úteis do NE tinham pico à tarde, no verão *e* no inverno (63–70% mesmo no inverno). Desde 2021, **0%**: o NE virou um sistema de pico noturno em todas as estações. O meio do dia do NE, que era a parte mais alta do dia, hoje está abaixo da média. É o subsistema com a maior penetração relativa de geração solar distribuída e o resultado é o "vale solar" clássico: a rede vê cada vez menos demanda quando o sol está alto.

**Os subsistemas não estão convergindo.** A distância SE × NE foi de 6,7 p.p. em 2017 para 8,1 em 2026; Sul × Norte segue em 12–14. Os dois pares internos (SE × S; NE × N) ficaram estáveis ou se aproximaram de leve. Cada região está mudando à sua maneira e as diferenças de formato aumentam.

**Um detalhe do Sul.** A curva de 2017–2019 tinha um degrau de almoço às 12h (queda de ~5 p.p.) que hoje é um vale de ~10 p.p. — mesmo fenômeno solar somado ao horário de almoço industrial.

**2019 era típico — a ampliação para 2017 confirmou.** Nos três anos do regime original os indicadores de formato são quase idênticos entre si (meio do dia do SIN +9,9 / +9,6 / +9,5%; NE com pico à tarde em 82 / 92 / 85% dos dias; distância SE × NE 6,7 / 6,9 / 7,1) e o desconto de domingo não se move. Ou seja: o "antes" é um patamar estável de três anos, não um ponto isolado, e a virada que aparece entre 2019 e 2021 é uma ruptura de fato — parte medição (carga global), parte real (o vale solar continua sob regime homogêneo em 2024–2026). A Camada 3 do produto pode comparar "2017–2019" com "2024–2026" sem depender de um ano só.

**O que leva para o produto.** (1) O gráfico de formato por ano (rampa clara → escura) é a imagem da Camada 3 "como o perfil mudou". (2) As séries de meio-dia e noite por ano, com os marcos, são o KPI de mudança — e a comparação YTD sob regime homogêneo é a versão defensável. (3) "Pico à tarde vs à noite, por estação" substitui qualquer "hora média do pico". (4) O NE merece destaque próprio: é a região onde a demanda mais mudou de formato.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    print(f"  documento: {DOC_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
