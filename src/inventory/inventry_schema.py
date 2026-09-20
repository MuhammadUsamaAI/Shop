from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional
from src.helper_functions import current_date_time

# Use a Tuple directly with Literal[*...] via TypeAlias / unpacking (Python 3.11+)
ITEM_LIST = (
    'small', 'medium', 'large', 'small_pack', 'half_pack',
    'family_pack', '300_ml', '500_ml', '1000_ml', '250_ml',
    '200_ml', '1500_ml', '2250_ml'
)

# Alternative 1: Define Literal explicitly with items (works on all Python versions)
ItemType = Literal[
    'small', 'medium', 'large', 'small_pack', 'half_pack',
    'family_pack', '300_ml', '500_ml', '1000_ml', '250_ml',
    '200_ml', '1500_ml', '2250_ml'
]


class InventorySchema(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    brand: Optional[str] = Field(min_length=2, max_length=30, default=None)
    price_each: int = Field(gt=0)
    purchase_date: str = Field(default_factory=current_date_time)
    type_: Optional[ItemType] = Field(default=None)
    quantity: int = Field(default=0)
    total_price: int = Field(default=0)

    # Use model_validator to compute total_price automatically after fields are populated
    @model_validator(mode='after')
    def compute_total_price(self):
        self.total_price = self.price_each * self.quantity
        return self



# item = InventorySchema(
#     name='ddg',
#     brand=55,
#     price_each=100,
#     type_='half_pack',
#     quantity=5
# )

# print(item)
# Output: name='asg' brand=None price_each=100 purchase_date='...' type_='half_pack' quantity=5 total_price=500