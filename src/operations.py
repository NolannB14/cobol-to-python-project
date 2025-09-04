from decimal import Decimal
from typing import Optional
from data_manager import DataManager

class Operations:
  def __init__(self, data_manager: DataManager) -> None:
    self.data = data_manager

  def get_balance(self) -> Decimal:
    return self.data.read_balance()

  def compute_credit(self, amount: Decimal) -> Decimal:
    return abs(amount)

  def compute_debit(self, amount: Decimal) -> Optional[Decimal]:
    if amount < 0:
      return None
    current_balance = self.get_balance()
    if current_balance >= amount:
      return amount
    return None

  def credit_balance(self, amount: Decimal) -> Decimal:
    credit = self.compute_credit(amount)
    new_balance = self.get_balance() + credit
    self.data.update_balance(new_balance)
    return new_balance

  def debit_balance(self, amount: Decimal) -> Optional[Decimal]:
    debit = self.compute_debit(amount)
    if debit is not None:
      new_balance = self.get_balance() - debit
      self.data.update_balance(new_balance)
      return new_balance
    return None