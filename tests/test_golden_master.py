from __future__ import annotations

import os
import sys
import difflib
import subprocess
from pathlib import Path
import pytest  # type: ignore


# --- Réglages généraux -------------------------------------------------------


ROOT = Path(__file__).resolve().parents[1]
SCEN_DIR = ROOT / "tests" / "scenarios"
GOLD_DIR = ROOT / "tests" / "golden_out" / "cobol"

# Construction dynamique du chemin vers src/main.py
MAIN = "src.main"
PY_CLI = os.getenv("PY_CLI", f'"{sys.executable}" -m {MAIN}')

# Timeout (seconds) pour éviter qu'un test reste bloqué
TIMEOUT = float(os.getenv("GM_TIMEOUT", "10.0"))

# --- Utilitaires -------------------------------------------------------------

def _normalize_bytes(b: bytes) -> bytes:
    """
    Normalisation simple pour rendre la comparaison robuste:
        - supprimer les espaces de fin de ligne
        - normaliser CRLF -> LF
        - garantir une ligne vide finale
    """
    # Normalise les fins de ligne d'abord
    text = b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    lines = text.split(b"\n")
    # strip trailing spaces/tabs at end of each line
    lines = [line.rstrip() for line in lines]
    # recompose with LF and ensure trailing newline
    out = b"\n".join(lines)
    if not out.endswith(b"\n"):
        out += b"\n"
    return out


def _run_cmd(cmd: str, stdin_path: Path) -> bytes:
    """Exécute la commande CLI avec un fichier d'entrée .in et retourne stdout normalisé."""
    with open(stdin_path, "rb") as fin:
        # shell=True pour autoriser PY_CLI en string "python -m module"
        proc = subprocess.run(
            cmd,
            input=fin.read(),
            shell=True,
            capture_output=True,
            timeout=TIMEOUT,
        )
    # On veut que ce test échoue si la CLI retourne un code ≠ 0
    if proc.returncode != 0:
        raise AssertionError(
            f"Commande échouée (code {proc.returncode}) pour {stdin_path.name}\n"
            f"STDERR:\n{proc.stderr.decode(errors='replace')}"
        )
    return _normalize_bytes(proc.stdout)


def _read_golden(path: Path) -> bytes:
    return _normalize_bytes(path.read_bytes())


def _scenario_files() -> list[Path]:
    # Tous les .in du dossier scénarios
    return sorted(SCEN_DIR.glob("*.in"), key=lambda p: p.name)


def _golden_for(scen_path: Path) -> Path:
    return GOLD_DIR / (scen_path.stem + ".out")


# --- Paramétrage des cas -----------------------------------------------------

SCENARIOS = _scenario_files()

if not SCENARIOS:
    pytest.skip("Aucun scénario .in trouvé dans tests/scenarios/ — rien à tester.", allow_module_level=True)


@pytest.mark.parametrize("scen", SCENARIOS, ids=[p.name for p in SCENARIOS])
def test_cli_matches_golden_master(scen: Path):
    """
    Compare la sortie de la CLI Python à la référence COBOL (Golden Master)
    pour chaque fichier d'entrée .in présent.
    """
    gold_path = _golden_for(scen)
    if not gold_path.exists():
        pytest.skip(f"Golden manquante pour {scen.name}: {gold_path.name}")

    py_out = _run_cmd(PY_CLI, scen)
    gold_out = _read_golden(gold_path)

    if py_out != gold_out:
        # Produit un diff lisible pour aider au diagnostic
        py_lines = py_out.decode(errors="replace").splitlines(keepends=True)
        gold_lines = gold_out.decode(errors="replace").splitlines(keepends=True)
        diff = "".join(
            difflib.unified_diff(
                gold_lines, py_lines,
                fromfile=f"golden/{gold_path.name}",
                tofile=f"python/{scen.stem}.out",
                lineterm=""
            )
        )
        raise AssertionError(
            f"Mismatch pour le scénario: {scen.name}\n"
            f"Commande: {PY_CLI}\n\nDiff (golden -> python):\n{diff}"
        )
