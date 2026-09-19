from apis.user_menu import get_login_data, admin_menu, manager_menu
from apis.user_db import UserDBHandler
from apis.user_validation import user_type_main, validation_function

user_db = UserDBHandler()


def menu() -> bool:
    print('Welcome to the Automated Shop\n')
    acc_type = validation_function(user_type_main, 'Select account type')

    if acc_type == 'admin':
        print('Welcome to the Administrator Manu\n')
        name, pin = get_login_data()
        if user_db.logged(account_type=acc_type, name=name, pin=pin):
            admin_menu(name)
        return True

    elif acc_type == 'manager':
        print('Welcome to the Managerial Manu\n')
        name, pin = get_login_data()
        if user_db.logged(account_type=acc_type, name=name, pin=pin):
            manager_menu(name)
        return True

    elif acc_type == 'user':
        print('Welcome to the User Manu\n')
        name, pin = get_login_data()
        if user_db.logged(account_type=acc_type, name=name, pin=pin):
            print(f'hi {acc_type}:{name}')
        return True

    else:
        print('unspecified account type')
        return False


while True:
    if menu() is False:
        print("Exiting application...")
        break