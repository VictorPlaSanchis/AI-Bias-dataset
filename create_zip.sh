#!/usr/bin/env bash

# Nombre del archivo ZIP de salida (puedes cambiarlo)
OUTPUT_ZIP="backup_$(date +%Y%m%d_%H%M%S).zip"

# Directorio raíz (actual)
ROOT_DIR="."

# Lista de patrones a excluir
EXCLUDES=(
  "node_modules/*"
  "compilaciones/*"
  "test/datasets/*"
  "test/data/*"
  ".pytest_cache/*"
  "backup*"
  "*.exe"
)

# Construimos la línea de exclusión para zip
EXCLUDE_ARGS=()
for pattern in "${EXCLUDES[@]}"; do
  EXCLUDE_ARGS+=("-x" "$pattern")
done

echo "Creando ZIP: $OUTPUT_ZIP"
echo "Excluyendo patrones: ${EXCLUDES[*]}"

# Ejecutamos zip recursivamente
zip -r "$OUTPUT_ZIP" "$ROOT_DIR" "${EXCLUDE_ARGS[@]}"

echo "¡Listo! Archivo generado: $OUTPUT_ZIP"
