import sys
from pathlib import Path
import pytest
from decimal import Decimal

# Import depuis le package src
from src.data_manager import DataManager
from src.operations import Operations
from src.main import MainProgram, _parse_amount, _format_balance


@pytest.fixture
def setup_system():
    dm = DataManager()
    ops = Operations(dm)
    return ops, dm


def test_initial_balance(setup_system):
    ops, dm = setup_system
    assert ops.get_balance() == Decimal("1000.00")
    assert dm.read_balance() == Decimal("1000.00")


def test_credit_balance_integration(setup_system):
    ops, dm = setup_system
    new_balance = ops.credit_balance(Decimal("250.00"))
    assert new_balance == Decimal("1250.00")
    assert dm.read_balance() == Decimal("1250.00")


def test_debit_balance_integration_success(setup_system):
    ops, dm = setup_system
    new_balance = ops.debit_balance(Decimal("400.00"))
    assert new_balance == Decimal("600.00")
    assert dm.read_balance() == Decimal("600.00")


def test_debit_balance_integration_failure(setup_system):
    ops, dm = setup_system
    result = ops.debit_balance(Decimal("1500.00"))  # trop grand
    assert result is None
    assert dm.read_balance() == Decimal("1000.00")  # solde pas changé


def test_credit_with_centimes(setup_system):
    ops, dm = setup_system
    new_balance = ops.credit_balance(Decimal("123.45"))
    assert new_balance == Decimal("1123.45")
    assert dm.read_balance() == Decimal("1123.45")


def test_debit_with_centimes(setup_system):
    ops, dm = setup_system
    new_balance = ops.debit_balance(Decimal("123.45"))
    assert new_balance == Decimal("876.55")
    assert dm.read_balance() == Decimal("876.55")


def test_credit_negative(setup_system):
    ops, dm = setup_system
    new_balance = ops.credit_balance(Decimal("-50.00"))
    assert new_balance == Decimal("950.00")
    assert dm.read_balance() == Decimal("950.00")


def test_debit_negative(setup_system):
    ops, dm = setup_system
    result = ops.debit_balance(Decimal("-10.00"))
    assert result is None
    assert dm.read_balance() == Decimal("1000.00")


def test_multiple_operations_sequence(setup_system):
    ops, dm = setup_system
    ops.credit_balance(Decimal("100"))
    ops.debit_balance(Decimal("50"))
    ops.credit_balance(Decimal("200"))
    ops.debit_balance(Decimal("100"))
    assert ops.get_balance() == Decimal("1150.00")
    assert dm.read_balance() == Decimal("1150.00")


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


def test_interface_debit_insufficient(monkeypatch, capsys):
    program = MainProgram()

    # Simule : débit avec fonds insuffisants
    inputs = iter(["3", "99999", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    program.run()

    output = capsys.readouterr().out
    assert "Insufficient funds for this debit." in output


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