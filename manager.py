from finance.drawer import Drawer
from finance.balance_db import FinanceDBHandler
from inventory.inventory_handler import InventoryManager
from helper_functions import main_path, path_corretor

path = main_path()
db_name = 'shop_database.db'
abs_path_db = path_corretor(path, key_to_add=db_name)
db_url = f"sqlite:///{abs_path_db}"
inventory_manager = InventoryManager(db_url=db_url)
finance_handler = FinanceDBHandler(db_url=db_url)
drawer = Drawer()

print(inventory_manager.watch_db())
print(finance_handler.watch_db())