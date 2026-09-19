import time
from apis.user_db import UserDBHandler
from typing import Tuple
from pydantic import TypeAdapter
from manager import prompt_addition, prompt_negation

from apis.user_validation import (user_name, user_age, user_pin, user_type_main,
                                  user_choice_y_n, user_choice_1_2, user_menut,
                                  user_add_remove, validation_function)

ENTER_YOUR = 'please enter your '
ENTER_PERSON = 'please enter person'

user_db = UserDBHandler()


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


def add_account(target_type: str) -> None:
    """Collect a person's details and add them to the DB as 'user' or 'manager'."""
    print(f"please enter the person's details below to add in {target_type}s\n")
    name, age, pin = get_create_acc_data()
    user_db.add_to_db(account_type=target_type, name=name, age=age, pin=pin)
    print(f'\nPerson {name} is added to the database as {target_type.capitalize()}')
    time.sleep(2)


def remove_account(target_type: str) -> None:
    """Collect a person's details and remove them from the DB as 'user' or 'manager'."""
    print(f"please enter the {target_type}'s details below to remove\n")
    name, age, pin = get_create_acc_data()
    if user_db.remove_id(account_type=target_type, name=name, age=age):
        print(f'\nPerson {name} is removed from the database')
        time.sleep(2)


def handle_add_remove(action: str, target_type: str) -> None:
    """Route to add_account/remove_account, handling the 'admin' special case."""
    if target_type == 'admin':
        print('admin account cannot be created' if action == 'add' else "cant remove admin account")
    elif target_type in ('user', 'manager'):
        (add_account if action == 'add' else remove_account)(target_type)
    else:
        print('invalid choice')


def admin_menu(name: str) -> None:
    print(f'hello admin:{name}\n')
    print('to add or remove an account press 1')
    print('to add or remove items from shop inventory press 2')
    selection = validation_function(user_choice_1_2,
                                    'please enter value')
    if selection == '1' or selection == 1:
        action = validation_function(user_add_remove,
                                      'do you want to add or remove an account?')
        if action not in ('add', 'remove'):
            print('invalid choice')
            return
        verb = 'create' if action == 'add' else 'remove'
        target_type = validation_function(user_type_main,
                                           f'do you want to {verb} user account or manager account?')
        handle_add_remove(action, target_type)
    elif selection == '2' or selection == 2:
        action = validation_function(user_menut, 'do you want to buy or sell inventory')
        if action == 'buy':
            prompt_addition()
        elif action == 'sell':
            prompt_negation()
        else:
            return


def manager_menu(name: str) -> None:
    print(f'hello manager: {name}\n')
    print('to add or remove an account press 1')
    print('to add or remove items from shop inventory press 2')
    selection = validation_function(user_choice_1_2,
                                    'please enter value')
    if selection == '1' or selection == 1:
        action = validation_function(user_add_remove,
                                      'do you want to add or remove user account?')
        if action == 'add':
            add_account('user')
        elif action == 'remove':
            remove_account('user')

    elif selection == '2' or selection == 2:
        action = validation_function(user_menut, 'do you want to buy or sell inventory')
        if action == 'buy':
            prompt_addition()
        elif action == 'sell':
            prompt_negation()
        else:
            return


def user_menu(name:str)->None:
    print(f'hello manager: {name}\n')
    prompt_negation()

