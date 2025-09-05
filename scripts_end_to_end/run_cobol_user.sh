#!/usr/bin/env bash
set -euo pipefail

# Emule un utilisateur en alimentant l'exécutable COBOL 'accountsystem' avec les fichiers .in
# Écrit les sorties correspondantes dans tests/golden_out/cobol

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCENARIO_DIR="$ROOT_DIR/tests/scenarios"
OUT_DIR="$ROOT_DIR/tests/golden_out/cobol"
COBOL_EXEC="$ROOT_DIR/cobol/accountsystem"

mkdir -p "$OUT_DIR"

for infile in "$SCENARIO_DIR"/*.in; do
  base=$(basename "$infile" .in)
  outfile="$OUT_DIR/${base}.out"
  if [ ! -x "$COBOL_EXEC" ]; then
    echo "COBOL executable not found or not executable: $COBOL_EXEC" >&2
    exit 2
  fi
  echo "Running COBOL scenario: $base"
  # Redirige entrée depuis infile, capture stdout/stderr dans outfile
  "$COBOL_EXEC" < "$infile" > "$outfile" 2>&1 || true
done

echo "COBOL runs complete. Outputs in $OUT_DIR"
