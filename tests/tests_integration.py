import sys
from pathlib import Path
from decimal import Decimal
import pytest

# Ajouter la racine du projet au chemin Python
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_manager import DataManager
from src.operations import Operations

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
