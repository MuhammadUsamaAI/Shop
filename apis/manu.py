from user_validation import UserValidation, validation_function
enter_string = 'please enter your '


def manu()->None:

    print('Welcome to the Automated Shop', '\n')
    acc_type = validation_function(UserValidation.Acc_Type.value, 'Select account type')
    if acc_type.lower() == 'manager':
        print('Welcome to the Managerial Manu', '\n')
        name = validation_function(UserValidation.Name.value, f'{enter_string} name')
        age = validation_function(UserValidation.Age.value, f'{enter_string} age ')
        pin = validation_function(UserValidation.Pin.value, f'{enter_string} pin')
        print(f'hello {acc_type}:{name}')

    elif acc_type.lower() == 'user':
        print('Welcom to the User Manu', '\n')
        name = validation_function(UserValidation.Name.value, f'{enter_string} name')
        age = validation_function(UserValidation.Age.value, f'{enter_string} age ')
        pin = validation_function(UserValidation.Pin.value, f'{enter_string} pin')
        print(f'hi {acc_type}:{name}')
    else:
        print('unspecified account type')
        return True


manu()


