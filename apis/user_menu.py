import time
#from apis.user_db import UserDBHandler
from typing import Tuple
from pydantic import TypeAdapter
from manager import prompt_addition, prompt_negation, prompt_view

from apis.user_validation import (user_name, user_age, user_pin, user_type_main,
                                  user_choice_1_4, user_menu_validator,
                                  user_add_remove, validation_function)

ENTER_YOUR = 'please enter your '
ENTER_PERSON = 'please enter person'

# user_db = UserDBHandler()


def get_login_data(name_validator: TypeAdapter = user_name,
                    pin_validator: TypeAdapter = user_pin) -> Tuple[str, int]:
    name = validation_function(name_validator, f'{ENTER_YOUR}name')
    pin = validation_function(pin_validator, f'{ENTER_YOUR}pin')
    return name, pin


def get_create_acc_data(name_validator: TypeAdapter = user_name,
                         pin_validator: TypeAdapter = user_pin,
                         age_validator: TypeAdapter = user_age ) -> Tuple[str, int, int]:
    name = validation_function(name_validator, f'{ENTER_PERSON} name')
    age = validation_function(age_validator, f'{ENTER_PERSON} age ')
    pin = validation_function(pin_validator, f'{ENTER_PERSON} pin')
    return name, age, pin


def add_account(target_type: str, database) -> None:
    """Collect a person's details and add them to the DB as 'user' or 'manager'."""
    print(f"please enter the person's details below to add in {target_type}s\n")
    name, age, pin = get_create_acc_data()
    database.add_to_db(account_type=target_type, name=name, age=age, pin=pin)
    print(f'\nPerson {name} is added to the database as {target_type.capitalize()}')
    time.sleep(2)


def remove_account(target_type: str, database) -> None:
    """Collect a person's details and remove them from the DB as 'user' or 'manager'."""
    print(f"please enter the {target_type}'s details below to remove\n")
    name, age, pin = get_create_acc_data()
    if database.remove_id(account_type=target_type, name=name, age=age):
        print(f'\nPerson {name} is removed from the database')
        time.sleep(2)


def handle_add_remove(action: str, target_type: str, database) -> None:
    if target_type == 'admin':
        print('admin account cannot be created' if action == 'add' else "cant remove admin account")
    elif target_type in ('user', 'manager'):
        (add_account if action == 'add' else remove_account)(target_type, database)
    else:
        print('invalid choice')


def add_remove_user(database):
    action = validation_function(user_add_remove,
                                 'do you want to add or remove user account?')
    if action == 'add':
        add_account('user', database)
    elif action == 'remove':
        remove_account('user', database)


def add_remove_user_manager(database):
    action = validation_function(user_add_remove,
                                 'do you want to add or remove an account?')

    verb = 'create' if action == 'add' else 'remove'
    target_type = validation_function(user_type_main,
                                      f'do you want to {verb} user account or manager account?')
    handle_add_remove(action, target_type, database)


def shop_menu() -> bool:
    while True:
        action = validation_function(user_menu_validator, 'do you want to buy or sell or view inventory or exit')

        if action == 'buy':
            prompt_addition()
        elif action == 'sell':
            prompt_negation()
        elif action == 'view':
            prompt_view()
        elif action == 'back':
            return True
        elif action == 'exit':
            return False


def shop_user_menu():
    while True:
        action = validation_function(user_menu_validator, 'do you want to sell or view inventory or exit')
        if action == 'sell':
            prompt_negation()
        elif action == 'view':
            prompt_view()
        elif action == 'back':
            return True
        elif action == 'exit':
            return False


def admin_manager_menu(acc_type:str, name: str, database) -> bool:
    while True:
        print(f'hello manager: {name}\n')
        print('For Adding or Removing an account press 1')
        print('For Shop Menu Press 2')
        print('For Main Menu Press 3')
        print('To Exit App Press 4')
        selection = validation_function(user_choice_1_4,
                                        'please enter value')
        if selection == '1' or selection == 1:
            if acc_type == 'admin':
                add_remove_user_manager(database)
            elif acc_type == 'manager':
                add_remove_user(database)
            else:
                raise ValueError('Invalid Account Type')

        elif selection == '2' or selection == 2:
            should_continue = shop_menu()
            if not should_continue:
                return False
        elif selection == '3' or selection == 3:
            return True

        elif selection == '4' or selection == 4:
            return False


def user_menu(name:str)->None:
    print(f'hello manager: {name}\n')
    shop_user_menu()
