import pytest
import pandas as pd
from schema_inference.infer import ColumnTypeInferer
from schema_inference.enums import ColumnType

# Asumimos que en el directorio tests/data/ están los CSV de prueba y manifest.csv
MANIFEST_PATH = "test/data/test_csvs/manifest.csv"
DATA_DIR = "test/data/test_csvs/"

@pytest.fixture(scope="module")
def inferer():
    return ColumnTypeInferer()

@pytest.fixture(scope="module")
def manifest():
    df = pd.read_csv(MANIFEST_PATH)
    # El manifest debe tener columnas: filename, column_name, expected_type
    assert set(["filename", "column_name", "expected_type"]).issubset(df.columns)
    return df

@pytest.mark.parametrize("row", [
    pytest.param(r, id=f"{r['filename']}:{r['column_name']}")
    for _, r in pd.read_csv(MANIFEST_PATH).iterrows()
])
def test_infer_column_type(inferer, manifest, row):
    filename = row['filename']
    column = row['column_name']
    expected_type = row['expected_type']

    df = pd.read_csv(f"{DATA_DIR}{filename}")
    assert column in df.columns, f"Columna '{column}' no encontrada en {filename}"

    inferred = inferer.infer(df[column]).value
    assert inferred == expected_type, (
        f"Para {filename}/{column}: se esperaba '{expected_type}', pero se obtuvo '{inferred}'"
    )
