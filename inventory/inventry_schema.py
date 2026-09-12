from pydantic import BaseModel, Field
from typing import Literal, Union
from helper_functions import current_date_time
item_list = ('small', 'medium', 'large', 'small_pack', 'half_pack',
                   'family_pack', '300_ml', '500_ml', '1000_ml', '250_ml',
                   '200_ml', '1500_ml', '2250_ml')

class Inventory_Schema(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    brand: Union[str, None] = Field(min_length=2, max_length=30, default=None)
    price_each: int = Field(gt=0)
    purchase_date: str = Field(default_factory=current_date_time)
    type_: Literal[*item_list] | None = Field(default=None)
    quantity: int|

print(Inventory_Schema(name = 'asg', price = 40, type_ = 'half_pack'))

