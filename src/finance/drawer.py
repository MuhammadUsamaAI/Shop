from pydantic import BaseModel, PrivateAttr, Field
from src.helper_functions import current_date_time
from typing import List, Tuple


class Drawer(BaseModel):
    balance_: int = Field(default=5000)
    _time: str = PrivateAttr(default=current_date_time())
    _cash_flow_logs: List[Tuple[int, str]] = PrivateAttr(default_factory=list)

    def __repr__(self):
        return f'({self.balance_}, {self._time})'

    @property
    def cash_flow_logs(self):
        return self._cash_flow_logs

    @property
    def time(self):
        self._time = current_date_time()
        return self._time

    @property
    def balance(self) -> int:
        return self.balance_

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
        return self.balance_

    @balance_adder.setter
    def balance_adder(self, value: int | str):
        clean_value = self._parse_and_validate_value(value)

        self.balance_ += clean_value
        self._cash_flow_logs.append((clean_value, self.time))

    @property
    def balance_negator(self) -> int:
        return self.balance_

    @balance_negator.setter
    def balance_negator(self, value: int | str):
        clean_value = self._parse_and_validate_value(value)

        if clean_value > self.balance_:
            raise ValueError("Insufficient Funds in Accounts")

        self.balance_ -= clean_value
        self._cash_flow_logs.append((-clean_value, self.time))
