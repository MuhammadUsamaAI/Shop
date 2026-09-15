import time
from user_validation import UserValidation, validation_function
from typing import Tuple
from enum import Enum
from pydantic import TypeAdapter

enter_your_string = 'please enter your '
enter_person_string = 'please enter person'


def get_login_data(name_validator: TypeAdapter | Enum = UserValidation.Name.value,
                   pin_validator: TypeAdapter | Enum = UserValidation.Pin.value) -> Tuple[str, int]:
    name = validation_function(name_validator, f'{enter_your_string} name')
    pin = validation_function(pin_validator, f'{enter_your_string} pin')
    return name, pin


def get_create_acc_data(name_validator: TypeAdapter | Enum = UserValidation.Name.value,
                        pin_validator: TypeAdapter | Enum = UserValidation.Pin.value,
                        age_validator: TypeAdapter | Enum = UserValidation.Age.value) -> Tuple[str, int, int]:
    name = validation_function(name_validator, f'{enter_person_string} name')
    age = validation_function(age_validator, f'{enter_person_string} age ')
    pin = validation_function(pin_validator, f'{enter_person_string} pin')
    return name, age, pin


def manu() -> bool|None:
    print('Welcome to the Automated Shop', '\n')
    acc_type = validation_function(UserValidation.Main_Type.value, 'Select account type')
    if acc_type.lower() == 'admin':
        print('Welcome to the Administrator Manu', '\n')
        name, pin = get_login_data()
        print(f'hello {acc_type}:{name}', '\n')
        choice_account_creation = validation_function(UserValidation.AddRmove.value,
                                                      'do you want to add or remove an account?')
        if choice_account_creation.lower() == 'add':
            choice_account_creation_ = validation_function(UserValidation.Acc_Type.value,
                                                           'do you want to create user account or manager account?')
            if choice_account_creation_.lower() == 'user':
                print("please enter the person's details below to add in users", '\n')
                name, age, pin = get_create_acc_data()
                print('\n')
                print(f'Person {name} is added to the database as User')
                time.sleep(2)
                return False
            elif choice_account_creation_.lower() == 'manager':
                print("please enter the person's details below to add in managers", '\n')
                name, age, pin = get_create_acc_data()
                print('\n')
                print(f'Person {name} is added to the database as Manager')
                time.sleep(2)
                return False
            elif choice_account_creation_.lower() == 'admin':
                print('admin account cannot be created')
            else:
                print('invalid choice')
        elif choice_account_creation.lower() == 'remove':
            choice_account_creation_ = validation_function(UserValidation.Acc_Type.value,
                                                           'do you want to remove user account or manager account?')
            if choice_account_creation_.lower() == 'user':
                print("please enter the user's details below to remove", '\n')
                name, age, pin = get_create_acc_data()
                print('\n')
                print(f'Person {name} is removed from the database')
                time.sleep(2)
                return False
            elif choice_account_creation_.lower() == 'manager':
                print("please enter the manager's details below to remove", '\n')
                name, age, pin = get_create_acc_data()
                print('\n')
                print(f'Person {name} is removed from the database')
                time.sleep(2)
                return False
            elif choice_account_creation_.lower() == 'admin':
                print('cant remove admin account')
            else:
                print('invalid choice')
    elif acc_type.lower() == 'manager':
        print('Welcome to the Managerial Manu', '\n')
        name, pin = get_login_data()
        print(f'hello {acc_type}:{name}', '\n')
        choice_account_creation = validation_function(UserValidation.AddRmove.value,
                                                      'do you want to add or remove user account?')
        if choice_account_creation.lower() == 'add':
            print("please enter the person's details below to add in users", '\n')
            name, age, pin = get_create_acc_data()
            print('\n')
            print(f'Person {name} is added to the database as User')
            time.sleep(2)
            return False
        elif choice_account_creation.lower() == ('remove'):
            print("please enter the person's details below to remove", '\n')
            name, age, pin = get_create_acc_data()
            print('\n')
            print(f'Person {name} is removed from the database as User')
            time.sleep(2)
            return False

    elif acc_type.lower() == 'user':
        print('Welcom to the User Manu', '\n')
        name, pin = get_login_data()
        print(f'hi {acc_type}:{name}')
        return False

    else:
        print('unspecified account type')
        return True


while True:
    should_continue = manu()
    if should_continue is False:
        print("Exiting application...")
        break
