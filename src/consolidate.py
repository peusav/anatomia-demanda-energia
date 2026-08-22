from __future__ import annotations

import re
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

# ============================================================
# CONFIGURAÇÃO
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
CONSOLIDATED_DIR = PROJECT_ROOT / "data" / "consolidated"

FILENAME_PATTERN = re.compile(r"^CURVA_CARGA_(\d{4})\.parquet$")


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def find_raw_files() -> list[Path]:
    """Localiza e ordena por ano os arquivos brutos disponíveis."""

    files = [
        path
        for path in RAW_DIR.glob("CURVA_CARGA_*.parquet")
        if FILENAME_PATTERN.match(path.name)
    ]

    return sorted(files, key=lambda path: int(FILENAME_PATTERN.match(path.name).group(1)))


def output_filename(files: list[Path]) -> str:
    """Nomeia o arquivo consolidado a partir do intervalo de anos encontrado."""

    years = [int(FILENAME_PATTERN.match(path.name).group(1)) for path in files]
    return f"CURVA_CARGA_{min(years)}_{max(years)}.parquet"


def resolve_field_type(field_name: str, types: set[pa.DataType]) -> pa.DataType:
    """
    Decide o tipo comum de uma coluna quando o ONS mudou seu formato entre anos.

    Caso conhecido: `val_cargaenergiahomwmed` era exportado como string até
    2024 e passou a double a partir de 2025. Quando houver mistura de string
    com um tipo numérico, assume-se que a string é um número em formato
    textual e o alvo vira float64.
    """

    if len(types) == 1:
        return next(iter(types))

    if pa.string() in types and all(
        t == pa.string() or pa.types.is_floating(t) or pa.types.is_integer(t)
        for t in types
    ):
        return pa.float64()

    raise ValueError(
        f"Coluna '{field_name}' tem tipos incompatíveis entre arquivos: {types}. "
        "É preciso decidir manualmente como unificá-la."
    )


def unify_tables(tables: list[pa.Table]) -> list[pa.Table]:
    """Normaliza os tipos de coluna entre todas as tabelas antes de concatenar."""

    field_types: dict[str, set[pa.DataType]] = {}

    for table in tables:
        for field in table.schema:
            field_types.setdefault(field.name, set()).add(field.type)

    target_types = {
        name: resolve_field_type(name, types) for name, types in field_types.items()
    }

    normalized = []

    for table in tables:
        for name, target_type in target_types.items():
            column = table.column(name)
            if column.type != target_type:
                index = table.schema.get_field_index(name)
                table = table.set_column(index, name, pc.cast(column, target_type))
        normalized.append(table)

    return normalized


# ============================================================
# CONSOLIDAÇÃO
# ============================================================

def consolidate() -> None:
    """Une todos os arquivos parquet brutos em um único arquivo consolidado."""

    files = find_raw_files()

    if not files:
        print(f"Nenhum arquivo encontrado em {RAW_DIR}. Rode antes o extract_ons.py.")
        return

    print(f"Consolidando {len(files)} arquivo(s):")

    tables = []

    for path in files:
        print(f"  - {path.name}")
        tables.append(pq.read_table(path))

    tables = unify_tables(tables)
    combined = pa.concat_tables(tables)

    CONSOLIDATED_DIR.mkdir(parents=True, exist_ok=True)
    destination = CONSOLIDATED_DIR / output_filename(files)

    pq.write_table(combined, destination)

    print(
        f"\nConsolidado: {destination} | "
        f"{combined.num_rows} linhas | "
        f"{destination.stat().st_size / (1024 ** 2):.2f} MB"
    )


def main() -> None:
    consolidate()


if __name__ == "__main__":
    main()
