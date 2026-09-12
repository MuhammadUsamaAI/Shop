import time
from pydantic import TypeAdapter, ValidationError
from typing import Any, Callable, Optional, Literal, Tuple
from .inventry_schema import Inventory_Schema

input_validator: TypeAdapter[Literal['y', 'yes', 'no', 'n']] = TypeAdapter(Literal['y', 'yes', 'no', 'n'])
name_validator: TypeAdapter[Any] = TypeAdapter(Inventory_Schema.__pydantic_core_schema__['schema']['fields']['name']['schema'])
brand_validator: TypeAdapter[Any] = TypeAdapter(Inventory_Schema.__pydantic_core_schema__['schema']['fields']['brand']['schema'])
price_validator: TypeAdapter[Any] = TypeAdapter(Inventory_Schema.__pydantic_core_schema__['schema']['fields']['price']['schema'])
type_validator: TypeAdapter[Any] = TypeAdapter(Inventory_Schema.__pydantic_core_schema__['schema']['fields']['type_']['schema'])


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


def schema_validator() -> Tuple[str, Optional[str], Optional[str], int, str]:
    name: str = validator_func(name_validator, 'Please enter name: ')
    brand: Optional[str] = validator_func(brand_validator, f'Please enter the brand name of {name} : ')
    type_: Optional[str] = validator_func(
        type_validator,
        f'Please enter the size or type of {name} (small/medium/large/etc.): '
    )
    price: int = validator_func(price_validator, f'Please enter the price of {name}: ', cast_to=int)
    new_item: Inventory_Schema = Inventory_Schema(name=name, brand=brand, type_=type_, price=price)
    date_time: str = new_item.purchase_date

    return name, brand, type_, price, date_time


def inventry_addititor() -> bool:
    choice: str = input("Do you want to add an item? (y/n): ").strip().lower()

    if choice in ['yes', 'y']:
        name, brand, type_, price, date_time = schema_validator()
        print("\n📦 Created Object Blueprint:\n", name, brand, type_, price, date_time)
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