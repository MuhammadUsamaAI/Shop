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


user_literal_types = ('user', 'manager', 'User', 'Manager', 'MANAGER', 'USER')
user_literal_choices = ('yes', 'no', 'Yes', 'No', 'YES', 'NO')
user_literal_add_remove = ('add', 'remove', 'ADD', 'REMOVE', 'Add', 'Remove')

user_age:TypeAdapter[int] = TypeAdapter(Annotated[int, Field(ge= 18, le=99)])
user_type:TypeAdapter[Literal[Tuple]] = TypeAdapter(Literal[user_literal_types])
user_pin:TypeAdapter[int] = TypeAdapter(Annotated[int, Field(ge=0, lt=9999)])
user_choice:TypeAdapter[str] = TypeAdapter(Literal[user_literal_choices])
user_add_remove:TypeAdapter[str] = TypeAdapter(Literal[user_literal_add_remove])

class UserValidation(enum.Enum):
    Name = user_name
    Acc_Type = user_type
    Choice = user_choice
    Pin = user_pin
    Age = user_age
    AddRmove = user_add_remove

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
