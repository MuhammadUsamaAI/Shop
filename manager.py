import time
from finance.drawer import Drawer
from finance.balance_db import FinanceDBHandler
from inventory.inventory_handler import InventoryManager
from inventory.inventry_producer_module import schema_validator, schema_validator_from_db
from helper_functions import main_path, path_corretor

path = main_path()
db_name = 'shop_database.db'
abs_path_db = path_corretor(path, key_to_add=db_name)
db_url = f"sqlite:///{abs_path_db}"

inventory_manager = InventoryManager(db_url=db_url)
finance_handler = FinanceDBHandler(db_url=db_url)


def prompt_addition() -> bool:
    choice = input("Do you want to add an item? (y/n): ").strip().lower()

    if choice in ['yes', 'y']:
        name, brand, type_, price_each, quantity, date_time, total_price = schema_validator()
        print("\n📦 Created Object Blueprint:\n", name, brand, type_, price_each, quantity, date_time, total_price)

        try:
            current_balance = finance_handler.last_balance()
            print(f'Current available balance in DB: {current_balance}')
            validator_drawer = Drawer(balance=current_balance)
            validator_drawer.balance_negator = total_price
            finance_handler.negate_balance(total_price, comment=f"Purchase: {name} x{quantity}")
            inventory_manager.to_db(name, brand, type_, price_each, quantity, date_time, total_price)

            print(f'New balance in DB: {finance_handler.last_balance()}')
            print('✨ Stock added and funds transferred successfully!\n')

        except ValueError as ex:
            print(f"❌ Transaction Denied: {ex}")
        except Exception as ex:
            print(f'Unexpected DB error occurred: {ex}')
        return True

    elif choice in ['no', 'n']:
        print('Good Bye!')
        inventory_manager.watch_db()
        finance_handler.watch_db()
        print(f"Final DB Balance: {finance_handler.last_balance()}")
        time.sleep(1)
        return False

    else:
        print("Invalid choice. Please enter 'y' or 'n'.")
        return True


def prompt_negation() -> bool:
    choice = input("Do you want to sell an item? (y/n): ").strip().lower()

    if choice in ['yes', 'y']:
        name, brand, type_, quantity = schema_validator_from_db()
        total_price = inventory_manager.from_db(name, brand, type_, quantity)
        if total_price and total_price > 0:
            finance_handler.add_to_db(total_price, comment=f"Sale: {name} x{quantity}")
            print(f'🛒 Your total bill for item_{name} is {total_price}')
            print(f'Updated DB Balance: {finance_handler.last_balance()}')
        else:
            print("❌ Transaction cancelled: Item unavailable or insufficient stock.")
        time.sleep(1)
        return True
    elif choice in ['no', 'n']:
        print('Good Bye!')
        inventory_manager.watch_db()
        finance_handler.watch_db()
        print(f"Final DB Status Balance: {finance_handler.last_balance()}")
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

