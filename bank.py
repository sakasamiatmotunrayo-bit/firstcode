from decimal import Decimal


class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the account balance."""


class BankAccount:
    """A bank account class with private balance and account number fields."""

    def __init__(self, account_number: str):
        self.__account_number = account_number  # Private field
        self.__balance = Decimal("0")           # Private field, starts at 0

    @staticmethod
    def _to_decimal(amount) -> Decimal:
        """Convert numeric input to Decimal without float rounding artifacts."""
        if isinstance(amount, Decimal):
            return amount
        return Decimal(str(amount))

    def deposit(self, amount) -> str:
        """Adds amount to balance. Amount must be greater than 0."""
        amount = self._to_decimal(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0.")
        self.__balance += amount
        return f"Deposited ${amount:,.2f}. New balance: ${self.__balance:,.2f}"

    def withdraw(self, amount) -> str:
        """Subtracts amount from balance if funds are sufficient."""
        amount = self._to_decimal(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0.")
        if amount > self.__balance:
            raise InsufficientFundsError(
                f"Insufficient funds. Current balance: ${self.__balance:,.2f}"
            )
        self.__balance -= amount
        return f"Withdrew ${amount:,.2f}. New balance: ${self.__balance:,.2f}"

    @property
    def balance(self) -> Decimal:
        """Read-only current balance."""
        return self.__balance

    def get_account_number(self) -> str:
        """Returns the account number."""
        return self.__account_number

    def __str__(self):
        return f"BankAccount(account_number={self.__account_number}, balance=${self.__balance:,.2f})"


# ── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    account = BankAccount("ACC-001")
    print(account)

    print(account.deposit(Decimal("1000")))
    print(account.deposit(Decimal("500")))
    print(account.withdraw(Decimal("200")))
    print(f"Current balance: ${account.balance:,.2f}")

    try:
        account.withdraw(Decimal("99999"))
    except InsufficientFundsError as e:
        print(f"Overdraft blocked: {e}")
