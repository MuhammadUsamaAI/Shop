import time
from sqlalchemy import String, Integer, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional, Type, Any
from .inventry_producer_module import schema_validator
from finance.drawer import Drawer

drawr = Drawer()

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

    def to_db(self, name: str, brand: str, type_: str, price_each: int | str,quantity: int|str , date_time: str,
              total_price:int|str) -> None:
        with Session(self.engine) as session:
            session.add(Inventory(
                item=name, brand=brand, item_type=type_,
                price_each=price_each, quantity=quantity,
                date_created=date_time, total_price = total_price
            ))
            session.commit()

    def watch_db(self, table: Type[Any]) -> None:
        with Session(self.engine) as session:
            stmt = select(table)
            for val in session.scalars(stmt):
                print(val)

    def prompt_addition(self) -> bool:
        choice = input("Do you want to add an item? (y/n): ").strip().lower()

        if choice in ['yes', 'y']:
            name, brand, type_, price_each, quantity, date_time, total_price = schema_validator()
            print("\n📦 Created Object Blueprint:\n", name, brand, type_, price_each, quantity, date_time, total_price)
            self.to_db(name, brand, type_, price_each, quantity, date_time, total_price)
            drawr.balance+=total_price
            print('✨ Addition To DB Successful!\n')
            time.sleep(1)
            return True

        elif choice in ['no', 'n']:
            print('Good Bye!')
            self.watch_db(table=Inventory)
            print(drawr.cash_flow_logs)
            time.sleep(1)
            return False

        else:
            print("Invalid choice. Please enter 'y' or 'n'.")
            return True

    def run(self) -> None:
        while True:
            if not self.prompt_addition():
                break