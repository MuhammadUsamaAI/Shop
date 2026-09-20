from pydantic import TypeAdapter, StringConstraints, Field, ValidationError
from typing_extensions import Annotated
from typing import Callable, Any
from .user_enums import UserOpts1to4, UserOptsYN, UserOptsAddRemove, UserTypesAdmin, UserMenu




user_name = TypeAdapter(
    Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=10,
            strip_whitespace=True,
            to_lower=True,
            pattern=r"^[a-zA-Z]+$"  # Fixed typo: a-z and A-Z
        )
    ]
)
user_age:TypeAdapter= TypeAdapter(Annotated[int, Field(ge= 18, le=99)])
user_type_main:TypeAdapter = TypeAdapter(UserTypesAdmin)
user_pin:TypeAdapter= TypeAdapter(Annotated[int, Field(ge=1000, lt=9999)])
user_choice_y_n:TypeAdapter = TypeAdapter(UserOptsYN)
user_add_remove:TypeAdapter= TypeAdapter(UserOptsAddRemove)
user_choice_1_4:TypeAdapter = TypeAdapter(UserOpts1to4)
user_menu_validator = TypeAdapter(UserMenu)


def validate_input_type(arg: str|int, validation_type: TypeAdapter):
    if isinstance(arg, str) and (validation_type == user_age or validation_type == user_pin):
        return int(arg)
    elif isinstance(arg, int) and (validation_type == user_choice_1_4):
        return str(arg)
    elif not isinstance(arg, str) and (validation_type == user_name or validation_type == user_type_main
                                  or validation_type == user_choice_y_n or validation_type == user_menu_validator):
        raise ValueError('Must be valid string')
    else:
        return arg


def validation_function(validation_type:TypeAdapter|Any,
                        message_prompt: str,
                        type_validation_function: Callable = validate_input_type,
                        ) -> int | str:
    while True:
        prompt = input(f'{message_prompt} :')
        try:
            type_validation_function(prompt, validation_type)
            validated_value = validation_type.validate_python(prompt)
            return validated_value
        except ValidationError as ex:
            print(ex)
        except ValueError as ex:
            print(ex)
        except Exception as ex:
            print(ex)


# validation_function(user_type_main, 'please enter user_type')