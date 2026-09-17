from pydantic import TypeAdapter, StringConstraints, Field, ValidationError
from typing_extensions import Annotated, Literal
from typing import Callable, Any, Tuple
import enum

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


user_literal_types_main = ('user', 'manager', 'User', 'Manager',
                      'MANAGER', 'USER', 'admin', 'Admin', 'ADMIN')
user_literal_types = ('user', 'manager', 'User', 'Manager',
                      'MANAGER', 'USER')
user_literal_choices = ('yes', 'no', 'Yes', 'No', 'YES', 'NO')
user_literal_add_remove = ('add', 'remove', 'ADD', 'REMOVE', 'Add', 'Remove')
user_literal_choice_1_2 = ('1', 1, '2', 2)
user_literal_db_choices = ('buy', 'sell', 'Buy', 'sell', 'BUY', 'SELL')

user_age:TypeAdapter[int] = TypeAdapter(Annotated[int, Field(ge= 18, le=99)])
user_type_main:TypeAdapter[Literal[Tuple]] = TypeAdapter(Literal[user_literal_types_main])
user_type:TypeAdapter[Literal[Tuple]] = TypeAdapter(Literal[user_literal_types])
user_pin:TypeAdapter[int] = TypeAdapter(Annotated[int, Field(ge=1000, lt=9999)])
user_choice:TypeAdapter[str] = TypeAdapter(Literal[user_literal_choices])
user_add_remove:TypeAdapter[str] = TypeAdapter(Literal[user_literal_add_remove])
user_choice_1_2:TypeAdapter[int|str] = TypeAdapter(Literal[user_literal_choice_1_2])
user_inventory_choice:TypeAdapter[str, str, str, str, str, str] = TypeAdapter(Literal[user_literal_db_choices])


class UserValidation(enum.Enum):
    Name = user_name
    Acc_Type = user_type
    Choice = user_choice
    Pin = user_pin
    Age = user_age
    AddRmove = user_add_remove
    Main_Type = user_type_main
    user_selection = user_choice_1_2
    inventory_choice = user_inventory_choice


def validate_input_type(arg: str|int, validation_type: TypeAdapter):
    if isinstance(arg, str) and (validation_type == user_age or validation_type == user_pin):
        return int(arg)
    elif not isinstance(arg, str) and (validation_type == user_name or validation_type == user_type
                                  or validation_type == user_choice):
        raise ValueError('string types only')
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