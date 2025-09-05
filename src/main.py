from decimal import Decimal
from src.operations import Operations
from src.data_manager import DataManager

def _parse_amount(raw: str) -> Decimal:
    try:
        value = Decimal(raw.strip())
        return value  # On garde les centimes
    except Exception:
        return Decimal("0")

def _format_balance(balance: Decimal) -> str:
    return f"{balance:09.2f}"

class MainProgram:
    def __init__(self):
        self.data_manager = DataManager()
        self.operations = Operations(self.data_manager)
        self.running = True

    def _menu(self) -> None:
        print("--------------------------------")
        print("Account Management System")
        print("1. View Balance")
        print("2. Credit Account")
        print("3. Debit Account")
        print("4. Exit")
        print("--------------------------------")

    def _show_balance(self):
        balance = self.operations.get_balance()
        print(f"Current balance: {_format_balance(balance)}")

    def _credit(self):
        raw = input("Enter credit amount: \n")
        amount = _parse_amount(raw)
        new_balance = self.operations.credit_balance(amount)
        print(f"Amount credited. New balance: {_format_balance(new_balance)}")

    def _debit(self):
        raw = input("Enter debit amount: \n")
        amount = _parse_amount(raw)
        new_balance = self.operations.debit_balance(amount)
        if new_balance is not None:
            print(f"Amount debited. New balance: {_format_balance(new_balance)}")
        else:
            print("Insufficient funds for this debit.")

    def _process_selection(self, choice: int) -> None:
        match choice:
            case 1:
                self._show_balance()
            case 2:
                self._credit()
            case 3:
                self._debit()
            case 4:
                self.running = False
                print("Exiting the program. Goodbye!")
            case _:
                print("Invalid choice, please select 1-4.")

    def run(self) -> None:
        while self.running:
            self._menu()
            raw_choice = input("Enter your choice (1-4):\n")
            try:
                choice = int(raw_choice)
            except ValueError:
                print("Invalid choice, please select 1-4.")
                continue
            self._process_selection(choice)

if __name__ == "__main__":
    program = MainProgram()
    program.run()