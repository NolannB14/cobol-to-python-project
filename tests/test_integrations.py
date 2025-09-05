import pytest
from decimal import Decimal

# Import depuis le package src
from src.data_manager import DataManager
from src.operations import Operations
from src.main import MainProgram, _parse_amount, _format_balance


# -------------------------
# Tests de cohérence modules
# -------------------------

def test_credit_then_balance_persists():
    dm = DataManager()
    ops = Operations(dm)

    # Crédit 200
    ops.credit_balance(Decimal("200"))
    assert dm.read_balance() == Decimal("1200.00")

    # Vérification cohérence via Operations
    assert ops.get_balance() == Decimal("1200.00")


def test_debit_then_balance_persists():
    dm = DataManager()
    ops = Operations(dm)

    # Débit valide
    new_balance = ops.debit_balance(Decimal("300"))
    assert new_balance == Decimal("700.00")
    assert dm.read_balance() == Decimal("700.00")

    # Débit trop élevé
    result = ops.debit_balance(Decimal("9999"))
    assert result is None
    # Le solde reste inchangé
    assert dm.read_balance() == Decimal("700.00")


def test_interface_credit_and_debit(monkeypatch, capsys):
    program = MainProgram()

    # Simule : crédit 100 puis consulter solde
    inputs = iter(["2", "100", "1", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    program.run()

    output = capsys.readouterr().out
    # Vérification cohérence affichage
    assert "Amount credited" in output
    assert "Current balance" in output


def test_interface_invalid_choice(monkeypatch, capsys):
    program = MainProgram()

    # Simule : choix invalide puis sortie
    inputs = iter(["9", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    program.run()

    output = capsys.readouterr().out
    assert "Invalid choice" in output
    assert "Goodbye" in output


def test_parse_and_format_helpers():
    # Parsing valide
    assert _parse_amount("123") == Decimal("123")

    # Parsing invalide => renvoie 0
    assert _parse_amount("abc") == Decimal("0")

    # Formatage solde
    assert _format_balance(Decimal("45.5")) == "000045.50"
    assert _format_balance(Decimal("7")) == "000007.00"
    assert _format_balance(Decimal("123456")) == "123456.00"
    assert _format_balance(Decimal("0")) == "000000.00"
    assert _format_balance(Decimal("1234.567")) == "001234.57"  # Arrondi à 2 décimales