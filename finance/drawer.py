from pydantic import BaseModel, PrivateAttr
from helper_functions import current_date_time
from typing import List, Tuple


class Drawer(BaseModel):
    _balance: int = PrivateAttr(default=10000)
    _time: str = PrivateAttr(default=current_date_time())
    _cash_flow_logs: List[Tuple[int, str]] = PrivateAttr(default_factory=list)

    def __repr__(self):
        return f'({self._balance}, {self._time})'

    @property
    def cash_flow_logs(self):
        return self._cash_flow_logs

    @property
    def time(self):
        self._time = current_date_time()
        return self._time

    @property
    def balance(self) -> int:
        return self._balance

    def _parse_and_validate_value(self, value: int | str) -> int:
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                raise ValueError("Value can only be a numeric type")
        elif not isinstance(value, int):
            raise TypeError("Balance must be an int or a numeric string")

        if value < 0:
            raise ValueError("Transaction amount cannot be negative")
        return value

    @property
    def balance_adder(self) -> int:
        return self._balance

    @balance_adder.setter
    def balance_adder(self, value: int | str):
        clean_value = self._parse_and_validate_value(value)

        self._balance += clean_value
        self._cash_flow_logs.append((clean_value, self.time))

    @property
    def balance_negator(self) -> int:
        return self._balance

    @balance_negator.setter
    def balance_negator(self, value: int | str):
        clean_value = self._parse_and_validate_value(value)

        if clean_value > self._balance:
            raise ValueError("Insufficient Funds in Accounts")

        self._balance -= clean_value
        self._cash_flow_logs.append((-clean_value, self.time))



d = Drawer()
d.balance_negator = 650
d.balance_adder = 900
d.balance_negator = 1000
print(f"Current Balance: {d.balance}")
print(f"Cash Flow Logs: {d.cash_flow_logs}")
