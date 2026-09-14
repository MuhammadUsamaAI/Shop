from finance.drawer import Drawer
from finance.balance_db import FinanceDBHandler
f = FinanceDBHandler()
print(f.last_balance())


d = Drawer(balance_=f.last_balance())
print(d.balance)
d.balance_adder = 200
print(d.balance)
d.balance_negator = 25
print(d.balance)
e = Drawer()
print(e.balance)
e.balance_adder = 200
print(e.balance_)
## Need to improve this Drawer Class
