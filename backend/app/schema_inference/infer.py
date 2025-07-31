from typing import Any
import pandas as pd
import numpy as np
from dateutil.parser import parse

from .config import (
    BOOLEAN_TOKENS,
    CURRENCY_SYMBOLS,
    CURRENCY_CODE_PATTERN,
    PERCENTAGE_SYMBOL,
    DATE_PARSE_THRESHOLD,
    DATE_YMD_PATTERN,
    DATE_DMY_PATTERN,
    SAMPLE_SIZE,
)
from .enums import ColumnType
from .exceptions import InferenceError
from .utils import default_logger as logger, is_high_cardinality

class ColumnTypeInferer:
    """
    Clase para inferir tipos de datos ampliados de una columna de pandas.
    """

    def __init__(
        self,
        sample_size: int = SAMPLE_SIZE,
        boolean_tokens: set[str] = BOOLEAN_TOKENS,
        currency_symbols: set[str] = CURRENCY_SYMBOLS,
        date_threshold: float = DATE_PARSE_THRESHOLD,
    ):
        self.sample_size = sample_size
        self.boolean_tokens = boolean_tokens
        self.currency_symbols = currency_symbols
        self.date_threshold = date_threshold

    def infer(self, series: pd.Series) -> ColumnType:
        """
        Orden de inferencia:
        1) BOOLEAN
        2) PERCENTAGE
        3) CURRENCY
        4) INTEGER
        5) FLOAT
        6) TIMESTAMP
        7) DATE
        8) ID
        9) STRING
        """
        try:
            non_null = series.dropna()
            sample = non_null.sample(
                n=min(len(non_null), self.sample_size),
                random_state=0
            )
        except Exception as e:
            logger.error("Error al muestrear datos: %s", e)
            raise InferenceError(e)

        values = sample.astype(str).values
        total = len(series)
        unique_count = series.nunique(dropna=True)

        # 1) BOOLEAN
        if len(set(values)) == 2 and set(values).issubset(self.boolean_tokens):
            logger.info("%s -> BOOLEAN", series.name)
            return ColumnType.BOOLEAN

        # 2) PERCENTAGE
        if all(v.endswith(PERCENTAGE_SYMBOL) for v in values):
            try:
                stripped = [v.strip(PERCENTAGE_SYMBOL) for v in values]
                pd.to_numeric(stripped, errors='raise')
                logger.info("%s -> PERCENTAGE", series.name)
                return ColumnType.PERCENTAGE
            except Exception:
                pass

        # 3) CURRENCY
        def is_currency(v: str) -> bool:
            # símbolo al inicio o final, o código ISO
            return (
                any(sym in v for sym in self.currency_symbols) or
                bool(CURRENCY_CODE_PATTERN.search(v))
            )
        if all(is_currency(v) for v in values):
            try:
                raw = [v.strip().lstrip(''.join(self.currency_symbols)).strip() for v in values]
                pd.to_numeric(raw, errors='raise')
                logger.info("%s -> CURRENCY", series.name)
                return ColumnType.CURRENCY
            except Exception:
                pass

        # 4) INTEGER
        try:
            numeric = pd.to_numeric(values, errors='raise')
            if numeric.dtype.kind == 'i' or np.allclose(numeric, numeric.astype(int)):
                logger.info("%s -> INTEGER", series.name)
                return ColumnType.INTEGER
        except Exception:
            pass

        # 5) FLOAT
        try:
            numeric = pd.to_numeric(values, errors='raise')
            if numeric.dtype.kind == 'f':
                logger.info("%s -> FLOAT", series.name)
                return ColumnType.FLOAT
        except Exception:
            pass

        # 6) TIMESTAMP (datetime con hora)
        parsed_count = 0
        for v in values:
            try:
                dt = parse(v, fuzzy=False)
                if dt.hour or dt.minute or dt.second:
                    parsed_count += 1
            except:
                break
        if parsed_count >= len(values) * self.date_threshold:
            logger.info("%s -> TIMESTAMP", series.name)
            return ColumnType.TIMESTAMP

        # 7) DATE (sin hora)
        if all(DATE_YMD_PATTERN.match(v) for v in values) or all(DATE_DMY_PATTERN.match(v) for v in values):
            logger.info("%s -> DATE (formato específico)", series.name)
            return ColumnType.DATE
        parsed=0
        for v in values:
            try:
                dt = parse(v, fuzzy=False)
                if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
                    parsed += 1
            except:
                break
        if parsed >= len(values) * self.date_threshold:
            logger.info("%s -> DATE", series.name)
            return ColumnType.DATE

        # 8) ID (alta cardinalidad)
        if is_high_cardinality(unique_count, total):
            logger.info("%s -> ID", series.name)
            return ColumnType.ID

        # 9) STRING
        logger.info("%s -> STRING", series.name)
        return ColumnType.STRING