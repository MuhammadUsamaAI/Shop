from user_validation import UserValidation, validation_function

enter_your_string = 'please enter your '
enter_person_string = 'please enter person'


def manu()->None:

    print('Welcome to the Automated Shop', '\n')
    acc_type = validation_function(UserValidation.Acc_Type.value, 'Select account type')
    if acc_type.lower() == 'manager':
        print('Welcome to the Managerial Manu', '\n')
        name = validation_function(UserValidation.Name.value, f'{enter_your_string} name')
        #age = validation_function(UserValidation.Age.value, f'{enter_your_string} age ')
        pin = validation_function(UserValidation.Pin.value, f'{enter_your_string} pin')

        print(f'hello {acc_type}:{name}', '\n')
        choice_account_creation = validation_function(UserValidation.AddRmove.value,
                                     'do you want to add or remove user account?')
        if choice_account_creation.lower() == ('add'):
            print("please enter the person's details below to add", '\n')
            name = validation_function(UserValidation.Name.value, f'{enter_person_string} name')
            age = validation_function(UserValidation.Age.value, f'{enter_person_string} age ')
            pin = validation_function(UserValidation.Pin.value, f'{enter_person_string} pin')
            print('\n')
            print(f'Person {name} is added to the database as User')
        elif choice_account_creation.lower() == ('remove'):
            print("please enter the person's details below to remove", '\n')
            name = validation_function(UserValidation.Name.value, f'{enter_person_string} name')
            #age = validation_function(UserValidation.Age.value, f'{enter_person_string} age ')
            pin = validation_function(UserValidation.Pin.value, f'{enter_person_string} pin')
            print('\n')
            print(f'Person {name} is removed from the database as User')




    elif acc_type.lower() == 'user':
        print('Welcom to the User Manu', '\n')
        name = validation_function(UserValidation.Name.value, f'{enter_your_string} name')
        age = validation_function(UserValidation.Age.value, f'{enter_your_string} age ')
        pin = validation_function(UserValidation.Pin.value, f'{enter_your_string} pin')
        print(f'hi {acc_type}:{name}')

    else:
        print('unspecified account type')
        return True


manu()


