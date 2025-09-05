import pytest # type: ignore
from decimal import Decimal
from src.data_manager import DataManager

class TestDataManager:
    def setup_method(self):
        self.dm = DataManager()

    def test_initial_balance(self):
        assert self.dm.read_balance() == Decimal("1000.00")

    def test_update_balance_positive(self):
        self.dm.update_balance(Decimal("1234.56"))
        assert self.dm.read_balance() == Decimal("1234.56")

    def test_update_balance_zero(self):
        self.dm.update_balance(Decimal("0"))
        assert self.dm.read_balance() == Decimal("0")

    def test_update_balance_negative(self):
        self.dm.update_balance(Decimal("-500.25"))
        assert self.dm.read_balance() == Decimal("-500.25")

    def test_update_balance_centimes(self):
        self.dm.update_balance(Decimal("999.99"))
        assert self.dm.read_balance() == Decimal("999.99")

    def test_update_balance_large(self):
        self.dm.update_balance(Decimal("1000000.00"))
        assert self.dm.read_balance() == Decimal("1000000.00")

    def test_update_balance_multiple_changes(self):
        self.dm.update_balance(Decimal("500.00"))
        assert self.dm.read_balance() == Decimal("500.00")
        self.dm.update_balance(Decimal("250.50"))
        assert self.dm.read_balance() == Decimal("250.50")
        self.dm.update_balance(Decimal("0.01"))
        assert self.dm.read_balance() == Decimal("0.01")
