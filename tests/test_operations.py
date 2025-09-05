import pytest  # type: ignore
from decimal import Decimal
from src.data_manager import DataManager
from src.operations import Operations

class TestOperations:
    def setup_method(self):
        self.data_manager = DataManager()
        self.ops = Operations(self.data_manager)

    def test_credit_balance_positive(self):
        result = self.ops.credit_balance(Decimal('100'))
        assert result == Decimal('1100.00')

    def test_credit_balance_negative(self):
        result = self.ops.credit_balance(Decimal('-50'))
        assert result == Decimal('1050.00')

    def test_debit_balance_valid(self):
        result = self.ops.debit_balance(Decimal('200'))
        assert result == Decimal('800.00')

    def test_debit_balance_insufficient(self):
        result = self.ops.debit_balance(Decimal('2000'))
        assert result is None

    def test_debit_balance_negative(self):
        result = self.ops.debit_balance(Decimal('-10'))
        assert result is None

    def test_get_balance(self):
        assert self.ops.get_balance() == Decimal('1000.00')

    def test_credit_balance_with_centimes(self):
        result = self.ops.credit_balance(Decimal('123.40'))
        assert result == Decimal('1123.40')

    def test_debit_balance_with_centimes(self):
        result = self.ops.debit_balance(Decimal('123.40'))
        assert result == Decimal('876.60')

    def test_credit_balance_zero(self):
        result = self.ops.credit_balance(Decimal('0'))
        assert result == Decimal('1000.00')

    def test_debit_balance_zero(self):
        result = self.ops.debit_balance(Decimal('0'))
        assert result == Decimal('1000.00')

    def test_multiple_operations(self):
        self.ops.credit_balance(Decimal('100'))
        self.ops.debit_balance(Decimal('50'))
        self.ops.credit_balance(Decimal('200'))
        self.ops.debit_balance(Decimal('100'))
        assert self.ops.get_balance() == Decimal('1150.00')

    def test_large_credit(self):
        result = self.ops.credit_balance(Decimal('1000000'))
        assert result == Decimal('1001000.00')

    def test_large_debit(self):
        result = self.ops.debit_balance(Decimal('999999'))
        assert result == None