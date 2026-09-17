from apis.user_validation import validation_function, UserValidation
from apis.user_menu import get_login_data, admin_menu, manager_menu
from apis.user_db import UserDBHandler
user_db = UserDBHandler()


def menu() -> bool:
    print('Welcome to the Automated Shop\n')
    acc_type = validation_function(UserValidation.Main_Type.value, 'Select account type').lower()

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
        print('Welcom to the User Manu\n')
        name, pin = get_login_data()
        if user_db.logged(account_type=acc_type, name=name, pin=pin):
            print(f'hi {acc_type}:{name}')
        return True

    else:
        print('unspecified account type')
        return True


while True:
    if menu() is False:
        print("Exiting application...")
        break