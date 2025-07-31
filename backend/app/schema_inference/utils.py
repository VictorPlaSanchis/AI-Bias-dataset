import logging

# Logger configurado para el módulo de inferencia
default_logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
default_logger.addHandler(handler)
default_logger.setLevel(logging.INFO)

def is_high_cardinality(n_unique: int, total: int, threshold: float = 0.8) -> bool:
    """
    Devuelve True si la proporción de valores únicos supera el umbral.
    """
    return total > 0 and (n_unique / total) >= threshold
