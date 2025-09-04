from decimal import Decimal

class DataManager:
  def __init__(self) -> None:
    self._balance: Decimal = Decimal("1000.00")

  def read_balance(self) -> Decimal:
    return self._balance

  def update_balance(self, new_balance: Decimal) -> None:
    self._balance = new_balance
