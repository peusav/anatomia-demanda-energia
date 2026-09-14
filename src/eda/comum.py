"""
Utilitários compartilhados pelos scripts de análise exploratória.

Carrega a fato, a dimensão de datas e a tabela de anomalias; define a
paleta (uma cor fixa por subsistema) e o estilo dos gráficos.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pyarrow.parquet as pq

matplotlib.use("Agg")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FATO_PATH = PROJECT_ROOT / "data" / "consolidated" / "CURVA_CARGA_2017_2026.parquet"
DIM_PATH = PROJECT_ROOT / "data" / "consolidated" / "dim_datas.parquet"
ANOMALIAS_PATH = PROJECT_ROOT / "data" / "reference" / "anomalias.csv"
IMG_DIR = PROJECT_ROOT / "docs" / "eda" / "img"

SUBSISTEMAS = ["SE", "S", "NE", "N"]  # ordem de grandeza
ROTULO = {"SE": "Sudeste/Centro-Oeste", "S": "Sul", "NE": "Nordeste", "N": "Norte", "SIN": "SIN"}

# Uma cor fixa por subsistema (paleta categórica validada; slots 1-4) e neutro para o SIN.
COR = {"SE": "#2a78d6", "S": "#1baf7a", "NE": "#eb6834", "N": "#eda100", "SIN": "#52514e"}

MARCOS = [
    (date(2021, 3, 2), "Carga global\n02/03/2021"),
    (date(2023, 4, 29), "+ MMGD\n29/04/2023"),
]

TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
GRADE = "#e6e5e1"


def estilo() -> None:
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": GRADE,
        "axes.grid": True,
        "grid.color": GRADE,
        "grid.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelcolor": TEXTO_2,
        "xtick.color": TEXTO_2,
        "ytick.color": TEXTO_2,
        "text.color": TEXTO,
        "font.size": 10,
        "legend.frameon": False,
        "lines.linewidth": 2,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    })


def carregar_fato() -> dict[str, dict[datetime, float]]:
    """{subsistema: {instante: MWmed}}, mais 'SIN' como soma horária dos quatro."""
    rows = pq.read_table(FATO_PATH).to_pylist()
    serie: dict[str, dict[datetime, float]] = defaultdict(dict)
    for r in rows:
        if r["val_cargaenergiahomwmed"] is not None:  # horas inexistentes do horário de verão
            serie[r["id_subsistema"]][r["din_instante"]] = r["val_cargaenergiahomwmed"]
    sin: dict[datetime, float] = {}
    for t in serie["SE"]:
        if all(t in serie[s] for s in SUBSISTEMAS):
            sin[t] = sum(serie[s][t] for s in SUBSISTEMAS)
    serie["SIN"] = sin
    return serie


def carregar_dim() -> dict[date, dict]:
    return {r["Data"]: r for r in pq.read_table(DIM_PATH).to_pylist()}


def carregar_anomalias() -> list[dict]:
    with ANOMALIAS_PATH.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def horas_excluidas(anomalias: list[dict], escopo: str = "horario") -> set[tuple[str, datetime]]:
    """
    Conjunto (subsistema, instante) com tratamento 'excluir'; '*' expande para os quatro.

    escopo="horario": tudo que tem tratamento 'excluir' (curvas horárias, hora do pico).
    escopo="diario": ignora o tipo 'convencao_horaria' (horário de verão), que desloca
    rótulos de hora mas não altera médias diárias.
    """
    out = set()
    for a in anomalias:
        if a["tratamento"] != "excluir":
            continue
        if escopo == "diario" and a["tipo"] == "convencao_horaria":
            continue
        subs = SUBSISTEMAS if a["id_subsistema"] == "*" else [a["id_subsistema"]]
        d0 = date.fromisoformat(a["data_inicio"])
        d1 = date.fromisoformat(a["data_fim"])
        h0 = int(a["hora_inicio"]) if a["hora_inicio"] else 0
        h1 = int(a["hora_fim"]) if a["hora_fim"] else 23
        d = d0
        while d <= d1:
            for h in range(h0, h1 + 1):
                for s in subs:
                    out.add((s, datetime.combine(d, datetime.min.time()) + timedelta(hours=h)))
            d += timedelta(days=1)
    return out


def media_diaria(serie: dict[datetime, float]) -> dict[date, float]:
    acc: dict[date, list[float]] = defaultdict(list)
    for t, v in serie.items():
        acc[t.date()].append(v)
    return {d: sum(v) / len(v) for d, v in acc.items()}


def marcar_marcos(ax, y_frac: float = 0.97) -> None:
    for d, rotulo in MARCOS:
        ax.axvline(d, color=TEXTO_2, linewidth=1, linestyle=(0, (4, 3)))
        ax.text(d, ax.get_ylim()[0] + y_frac * (ax.get_ylim()[1] - ax.get_ylim()[0]), " " + rotulo,
                fontsize=8, color=TEXTO_2, va="top", ha="left")


def salvar(fig, nome: str) -> Path:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    path = IMG_DIR / nome
    fig.savefig(path)
    plt.close(fig)
    print(f"  gráfico: {path.relative_to(PROJECT_ROOT).as_posix()}")
    return path


def fmt_gw(v: float) -> str:
    return f"{v / 1000:.1f} GW"


def md_table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)
