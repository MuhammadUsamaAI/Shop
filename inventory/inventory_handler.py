import time
from helper_functions import main_path
from .inventry_producer_module import schema_validator, schema_validator_from_db
from .inventory import Inventory, InventoryManager
from finance.drawer import Drawer
import os


file_path = main_path()
drawer = Drawer()
db_name = 'shop_database.db'
abs_path = os.path.join(file_path, db_name)
inventory_manager = InventoryManager(db_url = f"sqlite:///{abs_path}")

def prompt_addition() -> bool:
    choice = input("Do you want to add an item? (y/n): ").strip().lower()

    if choice in ['yes', 'y']:
        name, brand, type_, price_each, quantity, date_time, total_price = schema_validator()
        print("\n📦 Created Object Blueprint:\n", name, brand, type_, price_each, quantity, date_time, total_price)
        inventory_manager.to_db(name, brand, type_, price_each, quantity, date_time, total_price)
        #drawer.balance -= total_price
        print('✨ Addition To DB Successful!\n')
        time.sleep(1)
        return True

    elif choice in ['no', 'n']:
        print('Good Bye!')
        inventory_manager.watch_db(table=Inventory)
        print(drawer.cash_flow_logs)
        time.sleep(1)
        return False

    else:
        print("Invalid choice. Please enter 'y' or 'n'.")
        return True


def prompt_negation() -> bool:
    choice = input("Do you want to buy an item? (y/n): ").strip().lower()

    if choice in ['yes', 'y']:
        name, brand, type_, quantity = schema_validator_from_db()
        total_price = inventory_manager.from_db(name, brand, type_, quantity)
        #drawer.balance += total_price
        if total_price:
            print(f'your total bill for item_{name} is {total_price}')
        time.sleep(1)
        return True

    elif choice in ['no', 'n']:
        print('Good Bye!')
        inventory_manager.watch_db(table=Inventory)
        print(drawer.cash_flow_logs)
        time.sleep(1)
        return False

    else:
        print("Invalid choice. Please enter 'y' or 'n'.")
        return True


def run_add() -> None:
    while True:
        if not prompt_addition():
            break
def run_negate() -> None:
    while True:
        if not prompt_negation():
            break
