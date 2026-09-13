from sqlalchemy import String, Integer, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional, Type, Any


class Base(DeclarativeBase):
    pass

class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str] = mapped_column(String(30))
    brand: Mapped[Optional[str]] = mapped_column(String(30))
    item_type: Mapped[Optional[str]] = mapped_column(String(30))
    date_created: Mapped[str] = mapped_column(String(30))
    price_each: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return (
            f"Inventory(item_id={self.id}, item_name={self.item}, "
            f"item_brand={self.brand}, item_type={self.item_type}, "
            f"item_price={self.price_each}, item_quantity={self.quantity}, "
            f"date_created={self.date_created}, total_items_price={self.total_price})"
        )


class InventoryManager:
    def __init__(self, db_url: str = "sqlite://") -> None:
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)

    def to_db(
            self,
            name: str,
            brand: str,
            type_: str,
            price_each: int | str,
            quantity: int | str,
            date_time: str,
            total_price: int | str
    ) -> None:
        # 1. Cast numeric fields to integers safely
        price_each = int(price_each)
        quantity = int(quantity)
        total_price = int(total_price)

        with Session(self.engine) as session:
            # 2. Query for existing record
            existing_record = session.scalars(
                select(Inventory).where(
                    Inventory.item == name,
                    Inventory.brand == brand,
                    Inventory.item_type == type_
                )
            ).first()

            if existing_record:
                # 3. Update the instance properties directly
                existing_record.quantity += quantity
                existing_record.total_price = price_each*existing_record.quantity
                existing_record.price_each = price_each
                existing_record.date_created = date_time

                session.commit()
                print(f'Updated existing record for {name}')
            else:
                # 4. Insert new record
                session.add(Inventory(
                    item=name,
                    brand=brand,
                    item_type=type_,
                    price_each=price_each,
                    quantity=quantity,
                    date_created=date_time,
                    total_price=total_price
                ))
                session.commit()
                print(f'New item = {name}, brand = {brand} added to the db')

    def from_db(
            self,
            name: str,
            brand: str,
            type_: str,
            quantity: int | str,
    ) -> int:
        try:
            quantity = int(quantity)
        except ValueError:
            print("❌ Error: Requested quantity must be a numeric value.")
            return 0

        with Session(self.engine) as session:
            existing_record = session.scalars(select(Inventory).where(
                Inventory.item == name,
                Inventory.brand == brand,
                Inventory.item_type == type_,
            )).first()

            if not existing_record:
                print(f'❌ Item "{name}" does not exist in inventory.')
                return 0

            print(f'🔍 Item "{name}" exists in inventory.')

            if existing_record.quantity == 0:
                print(f'⚠️ Sorry, item "{name}" is completely out of stock.')
                return 0
            elif existing_record.quantity < quantity:
                print(f'⚠️ Insufficient stock. Requested {quantity}, but only {existing_record.quantity} available.')
                return 0

            # Fulfill the order safely
            total_bill = existing_record.price_each * quantity
            existing_record.quantity -= quantity
            existing_record.total_price = existing_record.price_each * existing_record.quantity

            session.commit()
            return total_bill

    def watch_db(self, table: Type[Any]) -> None:
        with Session(self.engine) as session:
            stmt = select(table)
            for val in session.scalars(stmt):
                print(val, end='\n')