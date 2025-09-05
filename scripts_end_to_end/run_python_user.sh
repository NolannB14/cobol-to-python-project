#!/usr/bin/env bash
set -euo pipefail

# Emule un utilisateur en alimentant la version Python (module src.main) avec les fichiers .in
# Écrit les sorties correspondantes dans tests/golden_out/python

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCENARIO_DIR="$ROOT_DIR/tests/scenarios"
OUT_DIR="$ROOT_DIR/tests/golden_out/python"

mkdir -p "$OUT_DIR"

for infile in "$SCENARIO_DIR"/*.in; do
  base=$(basename "$infile" .in)
  outfile="$OUT_DIR/${base}.out"
  echo "Running Python scenario: $base"
  # Exécute le module en s'assurant que la racine du projet est dans PYTHONPATH
  (cd "$ROOT_DIR" && PYTHONPATH="." python -m src.main < "$infile" > "$outfile" 2>&1) || true
done

echo "Python runs complete. Outputs in $OUT_DIR"
