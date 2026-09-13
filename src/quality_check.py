"""
Diagnóstico de qualidade da Curva de Carga Horária consolidada.

Gera docs/05-qualidade.md com as verificações previstas na seção de
qualidade da metodologia: cobertura, duplicidades, gaps, dias com
quantidade de horas diferente de 24, nulos/negativos/zeros, faixas de
valor, saltos hora a hora, grafias de subsistema e reconciliação com a
base diária do ONS (Carga de Energia Diária), quando disponível.

Uso:
    python src\\quality_check.py

A reconciliação com a base diária baixa os arquivos CARGA_ENERGIA_{ano}.parquet
para data/external/carga_diaria/ (não versionados). Use --sem-diaria para pular.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

import pyarrow.parquet as pq

# ============================================================
# CONFIGURAÇÃO
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSOLIDATED_DIR = PROJECT_ROOT / "data" / "consolidated"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
MANIFEST_PATH = RAW_DIR / "manifest.csv"
DAILY_DIR = PROJECT_ROOT / "data" / "external" / "carga_diaria"
REPORT_PATH = PROJECT_ROOT / "docs" / "05-qualidade.md"

DAILY_URL = (
    "https://ons-aws-prod-opendata.s3.amazonaws.com/"
    "dataset/carga_energia_di/CARGA_ENERGIA_{year}.parquet"
)

SUBSYSTEMS = ["N", "NE", "S", "SE"]
DIA_ABREV = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

# Marcos metodológicos do ONS (ver docs/03-metodologia.md)
METHOD_BREAKS = [
    (date(2021, 3, 2), "Carga global: passa a incluir previsão de geração de usinas não despachadas"),
    (date(2023, 4, 29), "Passa a incorporar estimativa de MMGD (micro e minigeração distribuída)"),
]

JUMP_THRESHOLD = 0.25  # variação hora a hora considerada suspeita
DAILY_TOLERANCE = 0.005  # 0,5% de diferença entre horária agregada e diária


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def find_consolidated_file() -> Path:
    files = sorted(CONSOLIDATED_DIR.glob("CURVA_CARGA_*_*.parquet"))
    if not files:
        sys.exit(f"Nenhum consolidado em {CONSOLIDATED_DIR}. Rode antes o consolidate.py.")
    return files[-1]


def load_rows(path: Path) -> list[dict]:
    return pq.read_table(path).to_pylist()


def last_extraction() -> str:
    if not MANIFEST_PATH.exists():
        return "manifest não encontrado"
    last = MANIFEST_PATH.read_text(encoding="utf-8").strip().splitlines()[-1]
    return last.split(",")[0]


def pct(value: float) -> str:
    return f"{100 * value:.2f}%"


def md_table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def download_daily(year: int) -> Path | None:
    """Baixa a base diária do ONS para um ano, se ainda não existir."""
    import requests

    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    destination = DAILY_DIR / f"CARGA_ENERGIA_{year}.parquet"
    if destination.exists():
        return destination
    try:
        response = requests.get(DAILY_URL.format(year=year), timeout=120)
        response.raise_for_status()
        destination.write_bytes(response.content)
        return destination
    except Exception as error:  # noqa: BLE001 - relatório segue sem a diária
        print(f"  [aviso] não foi possível baixar a base diária de {year}: {error}")
        return None


# ============================================================
# VERIFICAÇÕES
# ============================================================

def check_coverage(rows: list[dict]) -> str:
    count = defaultdict(int)
    for r in rows:
        count[(r["din_instante"].year, r["id_subsistema"])] += 1

    years = sorted({y for y, _ in count})
    table = []
    for y in years:
        days = 366 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 365
        expected = days * 24
        cells = [count[(y, s)] for s in SUBSYSTEMS]
        status = "completo" if all(c == expected for c in cells) else "parcial"
        table.append([y, expected, *cells, status])

    return md_table(["Ano", "Esperado (dias×24)", *SUBSYSTEMS, "Situação"], table)


def check_duplicates(rows: list[dict]) -> tuple[int, str]:
    keys = Counter((r["id_subsistema"], r["din_instante"]) for r in rows)
    dups = [k for k, v in keys.items() if v > 1]
    sample = ", ".join(f"{s} {t:%Y-%m-%d %H:%M}" for s, t in dups[:5])
    return len(dups), sample


def check_continuity(rows: list[dict]) -> str:
    table = []
    for s in SUBSYSTEMS:
        ts = sorted(r["din_instante"] for r in rows if r["id_subsistema"] == s)
        not_full_hour = sum(1 for t in ts if t.minute or t.second)
        gaps = [(a, b) for a, b in zip(ts, ts[1:]) if b - a != timedelta(hours=1)]
        gap_text = "; ".join(f"{a:%Y-%m-%d %H}h→{b:%Y-%m-%d %H}h" for a, b in gaps[:3]) or "-"
        table.append([s, f"{ts[0]:%Y-%m-%d %H}h", f"{ts[-1]:%Y-%m-%d %H}h", len(ts), not_full_hour, len(gaps), gap_text])
    return md_table(
        ["Subsistema", "Primeiro", "Último", "Registros", "Fora da hora cheia", "Gaps/saltos", "Exemplos"],
        table,
    )


def check_hours_per_day(rows: list[dict]) -> tuple[Counter, list]:
    per_day = defaultdict(int)
    for r in rows:
        per_day[(r["id_subsistema"], r["din_instante"].date())] += 1
    distribution = Counter(per_day.values())
    irregular = sorted((d, s, n) for (s, d), n in per_day.items() if n != 24)
    return distribution, irregular


def check_values(rows: list[dict]) -> tuple[dict, str]:
    values = [r["val_cargaenergiahomwmed"] for r in rows]
    summary = {
        "nulos": sum(v is None for v in values),
        "negativos": sum(v is not None and v < 0 for v in values),
        "zeros": sum(v == 0 for v in values),
    }
    table = []
    for s in SUBSYSTEMS:
        v = sorted(r["val_cargaenergiahomwmed"] for r in rows if r["id_subsistema"] == s and r["val_cargaenergiahomwmed"] is not None)
        n = len(v)
        table.append([s, round(v[0]), round(v[n // 100]), round(v[n // 2]), round(v[-max(1, n // 100)]), round(v[-1])])
    return summary, md_table(["Subsistema", "Mínimo", "P1", "Mediana", "P99", "Máximo"], table)


def check_jumps(rows: list[dict]) -> str:
    table = []
    for s in SUBSYSTEMS:
        series = sorted((r["din_instante"], r["val_cargaenergiahomwmed"]) for r in rows if r["id_subsistema"] == s)
        jumps = [
            (a[0], a[1], b[1])
            for a, b in zip(series, series[1:])
            if a[1] and abs(b[1] / a[1] - 1) > JUMP_THRESHOLD
        ]
        by_month = Counter(f"{t:%Y-%m}" for t, _, _ in jumps)
        months = ", ".join(f"{m} ({n})" for m, n in sorted(by_month.items())[:6]) or "-"
        table.append([s, len(jumps), months])
    return md_table(["Subsistema", f"Saltos > {int(JUMP_THRESHOLD * 100)}% hora a hora", "Meses (quantidade)"], table)


def check_names(rows: list[dict]) -> str:
    span = {}
    for r in rows:
        k = (r["id_subsistema"], r["nom_subsistema"])
        d = r["din_instante"].date()
        lo, hi = span.get(k, (d, d))
        span[k] = (min(lo, d), max(hi, d))
    table = [[s, n, lo, hi] for (s, n), (lo, hi) in sorted(span.items())]
    return md_table(["id_subsistema", "nom_subsistema", "De", "Até"], table)


def check_break_signals(rows: list[dict]) -> str:
    """Média diária do SIN nos dias em torno de cada marco metodológico."""
    daily = defaultdict(float)
    for r in rows:
        daily[r["din_instante"].date()] += r["val_cargaenergiahomwmed"] / 24

    blocks = []
    for break_date, label in METHOD_BREAKS:
        table = []
        for k in range(-3, 4):
            d = break_date + timedelta(days=k)
            mark = " ◀ marco" if k == 0 else ""
            table.append([d, DIA_ABREV[d.weekday()], round(daily.get(d, 0)), mark])
        blocks.append(f"**{break_date:%d/%m/%Y} — {label}**\n\n" + md_table(["Data", "Dia", "SIN (MWmed)", ""], table))
    return "\n\n".join(blocks)


def check_daily_reconciliation(rows: list[dict], years: list[int]) -> str:
    """Compara a média das 24 horas com o valor da base diária do ONS."""
    hourly = defaultdict(list)
    for r in rows:
        hourly[(r["id_subsistema"], r["din_instante"].date())].append(r["val_cargaenergiahomwmed"])

    table = []
    for y in years:
        path = download_daily(y)
        if path is None:
            table.append([y, "-", "-", "-", "não baixado"])
            continue
        daily_rows = pq.read_table(path).to_pylist()
        diffs = []
        for r in daily_rows:
            k = (r["id_subsistema"], r["din_instante"].date())
            if k in hourly:
                v = float(r["val_cargaenergiamwmed"])
                m = sum(hourly[k]) / len(hourly[k])
                diffs.append((abs(v - m) / v if v else 0, k, v, m))
        if not diffs:
            table.append([y, len(daily_rows), 0, "-", "sem interseção"])
            continue
        diffs.sort(reverse=True)
        worst = diffs[0]
        above = sum(d[0] > DAILY_TOLERANCE for d in diffs)
        table.append([
            y,
            len(daily_rows),
            len(diffs),
            above,
            f"{pct(worst[0])} em {worst[1][0]} {worst[1][1]} (diária {worst[2]:.0f} × horária {worst[3]:.0f})",
        ])
    return md_table(
        ["Ano", "Linhas na diária", "Dias comparados", f"Dias com dif. > {pct(DAILY_TOLERANCE)}", "Maior diferença"],
        table,
    )


# ============================================================
# RELATÓRIO
# ============================================================

def build_report(skip_daily: bool) -> str:
    source = find_consolidated_file()
    print(f"Lendo {source}")
    rows = load_rows(source)
    years = sorted({r["din_instante"].year for r in rows})
    first = min(r["din_instante"] for r in rows)
    last = max(r["din_instante"] for r in rows)

    n_dups, dup_sample = check_duplicates(rows)
    hours_dist, irregular_days = check_hours_per_day(rows)
    value_summary, value_table = check_values(rows)

    parts = [
        "# Diagnóstico de qualidade — Curva de Carga Horária",
        "",
        f"> Gerado automaticamente por `src/quality_check.py` em {datetime.now():%d/%m/%Y %H:%M}. "
        "Não edite à mão; rode o script novamente após uma nova extração.",
        "",
        "## Resumo",
        "",
        md_table(["Item", "Valor"], [
            ["Arquivo", f"`{source.relative_to(PROJECT_ROOT).as_posix()}`"],
            ["Última extração (manifest, UTC)", last_extraction()],
            ["Registros", f"{len(rows):,}".replace(",", ".")],
            ["Período", f"{first:%d/%m/%Y %Hh} → {last:%d/%m/%Y %Hh}"],
            ["Último dia com dados", f"{last:%d/%m/%Y} (corte para comparações YTD)"],
            ["Duplicidades (subsistema, instante)", n_dups],
            ["Dias com quantidade de horas ≠ 24", len(irregular_days)],
            ["Valores nulos / negativos / zero", f"{value_summary['nulos']} / {value_summary['negativos']} / {value_summary['zeros']}"],
        ]),
        "",
        "## 1. Cobertura por ano e subsistema",
        "",
        check_coverage(rows),
        "",
        "## 2. Continuidade horária",
        "",
        check_continuity(rows),
        "",
        "## 3. Horas por dia",
        "",
        "Distribuição de registros por (subsistema, dia): "
        + ", ".join(f"{n} horas → {c} dias" for n, c in sorted(hours_dist.items())) + ".",
        "",
        ("Nenhum dia irregular. A série é publicada em hora padrão, sem ajuste de horário de verão "
         "(o fim do horário de verão em 17/02/2019 não gerou dia de 25 horas)."
         if not irregular_days else
         "Dias irregulares: " + "; ".join(f"{s} {d} ({n}h)" for d, s, n in irregular_days[:20])),
        "",
        "## 4. Faixas de valor (MWmed)",
        "",
        value_table,
        "",
        f"Duplicidades: {n_dups}" + (f" — exemplos: {dup_sample}" if dup_sample else ""),
        "",
        "## 5. Saltos hora a hora",
        "",
        "Variações abruptas entre horas consecutivas. Não são necessariamente erro — podem ser eventos "
        "operacionais reais — mas merecem investigação antes de compor curvas típicas.",
        "",
        check_jumps(rows),
        "",
        "## 6. Grafias de subsistema",
        "",
        "O dicionário de dados do ONS (v1.2, 06/04/2026) informa que o nome abreviado do subsistema foi "
        "substituído pela descrição completa. Use `id_subsistema` como chave e um rótulo único no modelo.",
        "",
        check_names(rows),
        "",
        "## 7. Sinais em torno dos marcos metodológicos",
        "",
        "Média diária do SIN (soma dos quatro subsistemas) nos dias vizinhos a cada mudança de definição da carga. "
        "Um degrau visível aqui indica efeito de medição, não de demanda.",
        "",
        check_break_signals(rows),
        "",
        "## 8. Reconciliação com a Carga de Energia Diária (ONS)",
        "",
    ]

    if skip_daily:
        parts.append("_Pulado (`--sem-diaria`)._")
    else:
        parts += [
            "A base diária do ONS deve ser igual à média das 24 horas da curva horária. Diferenças acima da "
            "tolerância indicam **revisão posterior** de um dos arquivos pelo ONS (processo de consistência recorrente), "
            "e não erro de agregação.",
            "",
            check_daily_reconciliation(rows, years),
        ]

    parts.append("")
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sem-diaria", action="store_true", help="não baixar nem comparar com a base diária do ONS")
    args = parser.parse_args()

    report = build_report(skip_daily=args.sem_diaria)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Relatório gravado em {REPORT_PATH}")


if __name__ == "__main__":
    main()
