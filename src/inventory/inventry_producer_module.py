import time
from pydantic import TypeAdapter, ValidationError
from typing import Any, Callable, Optional, Literal, Tuple, Annotated
from .inventry_schema import InventorySchema

input_validator: TypeAdapter[Literal['y', 'yes', 'no', 'n']] = TypeAdapter[Literal['y', 'yes', 'no', 'n']]
def get_field_validator(model_cls, field_name: str) -> TypeAdapter[Any]:
    field_info = model_cls.model_fields[field_name]

    # If the field has constraints (e.g. min_length, gt=0), combine them using Annotated
    if field_info.metadata:
        annotated_type = Annotated[(field_info.annotation, *field_info.metadata)]
        return TypeAdapter(annotated_type)

    # Standard type without extra constraints
    return TypeAdapter(field_info.annotation)


name_validator = get_field_validator(InventorySchema, 'name')
brand_validator = get_field_validator(InventorySchema, 'brand')
price_each_validator = get_field_validator(InventorySchema, 'price_each')
purchase_date_validator = get_field_validator(InventorySchema, 'purchase_date')
type_validator = get_field_validator(InventorySchema, 'type_')
quantity_validator = get_field_validator(InventorySchema, 'quantity')
total_price_validator = get_field_validator(InventorySchema, 'total_price')


def prompt() -> str:
    try:
        user_input: str = input('Do you want to add to the list? (yes/no): ').strip().lower()
        return input_validator.validate_python(user_input)
    except ValidationError:
        print("❌ Invalid selection. Please enter 'yes', 'y', 'no', or 'n'.")
        return prompt()


def validator_func(
        validator: TypeAdapter[Any],
        message: str,
        cast_to: Optional[Callable[[str], Any]] = None
) -> Any:
    while True:
        # Flush stdout so error messages print BEFORE input() pauses execution
        raw_input: str = input(message).strip()

        try:
            # 1. Apply explicit casting if specified
            if cast_to:
                parsed_input = cast_to(raw_input)
            else:
                parsed_input = raw_input

            # 2. Validate using Pydantic (automatically handles string-to-type parsing)
            return validator.validate_python(parsed_input)

        except ValidationError as ex:
            # Extract precise failure message from Pydantic
            print(f"❌ Input Error: {ex.errors()[0]['msg']}", flush=True)

        except (ValueError, TypeError):
            print("❌ Input Error: Invalid value format.", flush=True)



def schema_validator() -> Tuple[str, Optional[str], Optional[str], int, int, str, int]:
    name: str = validator_func(name_validator, 'Please enter name: ')
    brand: Optional[str] = validator_func(brand_validator, f'Please enter the brand name of {name} : ')
    type_: Optional[str] = validator_func(
        type_validator,
        f'Please enter the size or type of {name} (small/medium/large/etc.): '
    )
    price_each: int = validator_func(price_each_validator, f'Please enter the price of {name}: ', cast_to=int)
    quantity: int = validator_func(quantity_validator, f'Please enter the quantity of the items to be inserted: ', cast_to=int)
    new_item: InventorySchema = InventorySchema(name=name, brand=brand, type_=type_, price_each=price_each, quantity=quantity)
    date_time: str = new_item.purchase_date
    total_price = new_item.total_price

    return name, brand, type_, price_each, quantity, date_time, total_price


def schema_validator_from_db() -> Tuple[str, Optional[str], Optional[str], int]:
    name: str = validator_func(name_validator, 'Please enter name: ')
    brand: Optional[str] = validator_func(brand_validator, f'Please enter the brand name of {name} : ')
    type_: Optional[str] = validator_func(
        type_validator,
        f'Please enter the size or type of {name} (small/medium/large/etc.): '
    )
    quantity: int = validator_func(quantity_validator, f'Please enter the quantity of the items to be bought: ', cast_to=int)
    return name, brand, type_, quantity