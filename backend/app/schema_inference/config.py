from typing import Set
import re

# Tokens considerados booleanos
BOOLEAN_TOKENS: Set[str] = {"0", "1", "True", "False", "true", "false", "Sí", "No", "si", "no"}

# Símbolos de moneda
CURRENCY_SYMBOLS: Set[str] = {"$", "€", "£", "¥"}
# Parcial: también aceptamos códigos ISO delante o detrás (p.ej. USD 100)
CURRENCY_CODE_PATTERN = re.compile(r"\b([A-Z]{3})\b")

# Símbolo de porcentaje
PERCENTAGE_SYMBOL: str = "%"

# Umbral mínimo de parseo de fechas en muestras
DATE_PARSE_THRESHOLD: float = 0.8
# Ratios de formatos de fecha exactos
DATE_YMD_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_DMY_PATTERN = re.compile(r"^\d{2}/\d{2}/\d{4}$")

# Tamaño de la muestra para inferencia
SAMPLE_SIZE: int = 100