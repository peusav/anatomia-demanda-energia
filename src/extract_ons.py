from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import requests


# ============================================================
# CONFIGURAÇÃO
# ============================================================

START_YEAR = 2017
END_YEAR = 2026

BASE_URL = (
    "https://ons-aws-prod-opendata.s3.amazonaws.com/"
    "dataset/curva-carga-ho/CURVA_CARGA_{year}.parquet"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
MANIFEST_PATH = RAW_DIR / "manifest.csv"

CHUNK_SIZE = 1024 * 1024  # 1 MB
TIMEOUT = 120


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def calculate_sha256(file_path: Path) -> str:
    """Calcula o hash SHA-256 de um arquivo."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def download_file(url: str, destination: Path) -> None:
    """
    Baixa um arquivo utilizando streaming.

    O download é inicialmente salvo em um arquivo temporário
    para evitar deixar um arquivo incompleto na pasta raw.
    """
    temp_path = destination.with_suffix(destination.suffix + ".tmp")

    try:
        with requests.get(url, stream=True, timeout=TIMEOUT) as response:
            response.raise_for_status()

            with temp_path.open("wb") as file:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        file.write(chunk)

        temp_path.replace(destination)

    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def append_manifest(
    year: int,
    filename: str,
    url: str,
    size_bytes: int,
    sha256: str,
) -> None:
    """Registra os metadados da extração."""

    file_exists = MANIFEST_PATH.exists()

    with MANIFEST_PATH.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "extraction_timestamp_utc",
                "year",
                "filename",
                "source_url",
                "size_bytes",
                "sha256",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "extraction_timestamp_utc": datetime.now(
                    timezone.utc
                ).isoformat(),
                "year": year,
                "filename": filename,
                "source_url": url,
                "size_bytes": size_bytes,
                "sha256": sha256,
            }
        )


# ============================================================
# EXTRAÇÃO
# ============================================================

def extract_year(year: int) -> None:
    """Baixa e registra o arquivo de um determinado ano."""

    url = BASE_URL.format(year=year)
    filename = f"CURVA_CARGA_{year}.parquet"
    destination = RAW_DIR / filename

    print(f"\n[{year}] {url}")

    # Guarda o hash anterior para identificar revisões do ONS
    previous_hash = None

    if destination.exists():
        previous_hash = calculate_sha256(destination)

    download_file(url, destination)

    current_hash = calculate_sha256(destination)
    size_bytes = destination.stat().st_size

    if previous_hash is None:
        status = "NOVO"
    elif previous_hash == current_hash:
        status = "SEM ALTERAÇÃO"
    else:
        status = "ATUALIZADO PELO ONS"

    append_manifest(
        year=year,
        filename=filename,
        url=url,
        size_bytes=size_bytes,
        sha256=current_hash,
    )

    print(
        f"[{year}] {status} | "
        f"{size_bytes / (1024 ** 2):.2f} MB | "
        f"SHA256: {current_hash[:12]}..."
    )


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("Extração da Curva de Carga Horária - ONS")
    print(f"Período: {START_YEAR}-{END_YEAR}")
    print(f"Destino: {RAW_DIR}")

    errors = []

    for year in range(START_YEAR, END_YEAR + 1):
        try:
            extract_year(year)

        except requests.HTTPError as error:
            print(f"[{year}] ERRO HTTP: {error}")
            errors.append(year)

        except requests.RequestException as error:
            print(f"[{year}] ERRO DE CONEXÃO: {error}")
            errors.append(year)

    print("\nExtração concluída.")

    if errors:
        print(f"Anos com erro: {errors}")


if __name__ == "__main__":
    main()