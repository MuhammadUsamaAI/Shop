import time
from src.apis.user_menu import get_login_data, user_menu, admin_manager_menu
from src.apis.user_db import UserDBHandler
from src.apis.user_validation import user_type_main, validation_function
from src.helper_functions import main_path, path_corretor

path = main_path()
db_name = 'shop_database.db'
abs_path_db = path_corretor(path, key_to_add=db_name)
db_url = f"sqlite:///{abs_path_db}"
user_db = UserDBHandler(db_url)


def menu() -> bool:
    print('Welcome to the Automated Shop\n')
    acc_type = validation_function(user_type_main,
                                   'Select account type or write exit for exiting the application')

    if acc_type == 'admin':
        print('Welcome to the Administrator Manu\n')
        name, pin = get_login_data()
        if user_db.logged(account_type=acc_type, name=name, pin=pin):
            if admin_manager_menu(acc_type, name, user_db):
                pass
            else:
                print(f'Good buy {name}')
                time.sleep(2)
                return False
        return True
    elif acc_type == 'manager':
        print('Welcome to the Managerial Manu\n')
        name, pin = get_login_data()
        if user_db.logged(account_type=acc_type, name=name, pin=pin):
            if admin_manager_menu(acc_type, name, user_db):
                pass
            else:
                print(f'Good buy {name}')
                time.sleep(2)
                return False
        return True
    elif acc_type == 'user':
        print('Welcome to the User Manu\n')
        name, pin = get_login_data()
        print(acc_type, name, pin)
        #user_db.watch_db()
        if user_db.logged(account_type=acc_type, name=name, pin=pin):
            print(f'hi {acc_type}:{name}')
            if user_menu(name):
                pass
            else:
                print(f'Good buy {name}')
                time.sleep(2)
                return False
        return True
    elif acc_type == 'exit':
        print('Good Bye')
        time.sleep(2)
        return False


while True:
    if menu() is False:
        print("Exiting application...")
        break