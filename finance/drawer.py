from pydantic import BaseModel, PrivateAttr
from helper_functions import current_date_time
from typing import List, Tuple

class Drawer(BaseModel):
    _balance: int = PrivateAttr(default=0)
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

    @balance.setter
    def balance(self, value: int | str):
        if isinstance(value, int):
            if value < 0:
                raise ValueError("Balance cannot be negative")
            self._balance += value
            self._cash_flow_logs.append((value, self.time))
        elif isinstance(value, str):
            try:
                converted = int(value)
                if converted < 0:
                    raise ValueError("Balance cannot be negative")
                self._balance += converted
                self._cash_flow_logs.append((converted, self.time))
            except ValueError:
                raise ValueError("Value can only be a numeric type")
        else:
            raise TypeError("Balance must be an int or a numeric string")

# d = Drawer()
# d.balance += 50
# d.balance += 20
# d.balance -= 15
# print(d.cash_flow_logs)
# # print(repr(d))
# # print(d.time)
# # time.sleep(1)
# # print(d.time)