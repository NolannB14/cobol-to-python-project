import pytest # type: ignore
from decimal import Decimal
from src.main import _parse_amount, _format_balance

def test_parse_amount_integer():
    assert _parse_amount("100") == Decimal("100")

def test_parse_amount_decimal():
    assert _parse_amount("123.45") == Decimal("123.45")

def test_parse_amount_negative():
    assert _parse_amount("-50.25") == Decimal("-50.25")

def test_parse_amount_empty():
    assert _parse_amount("") == Decimal("0")

def test_parse_amount_non_numeric():
    assert _parse_amount("abc") == Decimal("0")

def test_parse_amount_spaces():
    assert _parse_amount("  42.42  ") == Decimal("42.42")

def test_format_balance_standard():
    assert _format_balance(Decimal("123.45")) == "000123.45"

def test_format_balance_zero():
    assert _format_balance(Decimal("0")) == "000000.00"

def test_format_balance_large():
    assert _format_balance(Decimal("1234567.89")) == "1234567.89"
