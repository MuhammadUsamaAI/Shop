from finance.drawer import Drawer
d = Drawer(balance = 200)
print(d.balance)
d.balance_adder = 200
print(d.balance)
e = Drawer()
print(e.balance)
e.balance_adder = 200
## Need to improve this Drawer Class
