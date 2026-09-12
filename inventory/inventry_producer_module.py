import time
from pydantic import TypeAdapter, ValidationError
from typing import Any, Callable, Optional, Literal, Tuple
from .inventry_schema import InventorySchema

# 1. User input validator
input_validator: TypeAdapter[Literal['y', 'yes', 'no', 'n']] = TypeAdapter[Literal['y', 'yes', 'no', 'n']]

# 2. Field validators extracted safely from model fields
name_validator = TypeAdapter(InventorySchema.model_fields['name'].annotation)
brand_validator = TypeAdapter(InventorySchema.model_fields['brand'].annotation)
price_each_validator = TypeAdapter(InventorySchema.model_fields['price_each'].annotation)
type_validator = TypeAdapter(InventorySchema.model_fields['type_'].annotation)
quantity_validator = TypeAdapter(InventorySchema.model_fields['quantity'].annotation)



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
    try:
        raw_input: str = input(message).strip()

        # Explicitly cast input types (e.g., string to integer for price)
        parsed_input: Any = cast_to(raw_input) if cast_to else raw_input

        return validator.validate_python(parsed_input)
    except (ValidationError, ValueError) as ex:
        # Gracefully extract the precise failure reason text from Pydantic
        if isinstance(ex, ValidationError):
            print(f"❌ Input Error: {ex.errors()[0]['msg']}")
        else:
            print("❌ Input Error: Must be a valid numeric whole number.")

        return validator_func(validator, message, cast_to)


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


def inventry_addititor() -> bool:
    choice: str = input("Do you want to add an item? (y/n): ").strip().lower()

    if choice in ['yes', 'y']:
        name, brand, type_, price_each, quantity, date_time, total_price = schema_validator()
        print("\n📦 Created Object Blueprint:\n", name, brand, type_, price_each, quantity, date_time, total_price)
        print('✨ Addition Successful!\n')
        time.sleep(1)
        return True

    elif choice in ['no', 'n']:
        print('Good Bye!')
        time.sleep(1)
        return False

    else:
        print("Invalid choice. Please enter 'y' or 'n'.")
        return True  # Keeps the loop running on invalid input