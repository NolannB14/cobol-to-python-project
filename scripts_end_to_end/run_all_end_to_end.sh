#!/usr/bin/env bash
set -euo pipefail

# Wrapper: lance les scripts COBOL et Python pour tous les scénarios
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$ROOT_DIR/scripts_end_to_end"
SCENARIO_DIR="$ROOT_DIR/tests/scenarios"
COBOL_OUT_DIR="$ROOT_DIR/tests/golden_out/cobol"
PY_OUT_DIR="$ROOT_DIR/tests/golden_out/python"
DIFF_DIR="$ROOT_DIR/tests/golden_out/diffs"

mkdir -p "$DIFF_DIR"

COBOL_EXEC="$ROOT_DIR/cobol/accountsystem"

if [ -x "$COBOL_EXEC" ]; then
	echo "Running COBOL scenarios..."
	bash "$SCRIPTS_DIR/run_cobol_user.sh"
else
	echo "Skipping COBOL runs: executable not found or not executable at $COBOL_EXEC"
fi

echo "Running Python scenarios..."
bash "$SCRIPTS_DIR/run_python_user.sh"

echo "Comparing outputs..."

matched=0
mismatched=0
missing_cobol=0
missing_python=0

for infile in "$SCENARIO_DIR"/*.in; do
	base=$(basename "$infile" .in)
	cobol_file="$COBOL_OUT_DIR/${base}.out"
	py_file="$PY_OUT_DIR/${base}.out"
	diff_file="$DIFF_DIR/${base}.diff"

	if [ ! -f "$py_file" ]; then
		echo "[MISSING] Python output missing for $base: $py_file"
		missing_python=$((missing_python+1))
		continue
	fi

	if [ ! -f "$cobol_file" ]; then
		echo "[MISSING] COBOL output missing for $base: $cobol_file"
		missing_cobol=$((missing_cobol+1))
		continue
	fi

		# Normalize files (strip trailing whitespace) then compare; write unified diff if different
		norm_cobol="$DIFF_DIR/${base}.cobol.norm"
		norm_py="$DIFF_DIR/${base}.py.norm"
		# strip trailing whitespace and remove CR
		sed -e 's/[[:space:]]\+$//' "$cobol_file" | tr -d '\r' > "$norm_cobol"
		sed -e 's/[[:space:]]\+$//' "$py_file" | tr -d '\r' > "$norm_py"

		if diff -u "$norm_cobol" "$norm_py" > "$diff_file"; then
		matched=$((matched+1))
			rm -f "$diff_file"
		fi
		# cleanup normalized files
		rm -f "$norm_cobol" "$norm_py"
		if [ -f "$diff_file" ] && [ -s "$diff_file" ]; then
			mismatched=$((mismatched+1))
			echo "[DIFF] $base -> $diff_file"
		fi

done

echo
echo "Comparison summary:"
echo "  matched:    $matched"
echo "  mismatched: $mismatched (diffs in $DIFF_DIR)"
echo "  missing cobol outputs:  $missing_cobol"
echo "  missing python outputs: $missing_python"

if [ $mismatched -eq 0 ] && [ $missing_cobol -eq 0 ] && [ $missing_python -eq 0 ]; then
	echo "All outputs match."
	exit 0
else
	echo "Some outputs differ or are missing. See above and $DIFF_DIR for details."
	exit 1
fi
