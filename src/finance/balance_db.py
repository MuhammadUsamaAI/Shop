from typing import Optional
from sqlalchemy import Integer, String, create_engine, select, inspect
from sqlalchemy.orm import Mapped, mapped_column, Session, DeclarativeBase
from src.helper_functions import current_date_time


class FinanceBase(DeclarativeBase):
    pass

class Balance_Sheet(FinanceBase):
    __tablename__ = 'balance_sheet'

    id:Mapped['int'] = mapped_column(primary_key=True)
    balance:Mapped['int'] = mapped_column(Integer)
    transection_time:Mapped['str'] = mapped_column(String(50))
    comment:Mapped[Optional['str']] = mapped_column(String(100))

    def __repr__(self):
        return f'id = {self.id}, balance = {self.balance},' \
               f' transection_time = {self.transection_time},' \
               f' comment = {self.comment}'


class FinanceDBHandler:
    def __init__(self, db_url:str = "sqlite://"):
        self.engine = create_engine(db_url, echo=False)
        FinanceBase.metadata.create_all(self.engine)

    def last_row(self, session:Session)->Balance_Sheet|None:
        smt = select(Balance_Sheet).order_by(Balance_Sheet.id.desc()).limit(1)
        return session.scalars(smt).first()

    def add_to_db(self,
              amount:str|int,
              comment:str=None
              )->None:
        amount = int(amount)
        with Session(self.engine) as session:
            existing_record = self.last_row(session)
            if existing_record:
                last_balance = existing_record.balance
                session.add(Balance_Sheet(
                    balance = amount + last_balance,
                    transection_time = current_date_time(),
                    comment = comment
                ))
                session.commit()
                print(f'balance updated with {amount}, new amount is '
                      f'{amount+last_balance}', '\n')
            else:
                session.add(Balance_Sheet(
                    balance = amount,
                    transection_time = current_date_time(),
                    comment = comment
                ))
                session.commit()
                print(f'new table is made with balance = {amount}', '\n')

    def negate_balance(self,
                       amount:int,
                       comment:str = None
                       ):
        amount = int(amount)
        with Session(self.engine) as session:
            existing_record = self.last_row(session)
            if existing_record:
                last_balance = existing_record.balance
                if amount> last_balance:
                    raise ValueError('Print Insufficient Funds, '
                                     f'Available Balance is {last_balance} '
                                     f'Amount Required is {amount}')
                else:
                    session.add(
                        Balance_Sheet(
                            balance = last_balance - amount,
                            transection_time = current_date_time(),
                            comment = comment
                        )
                    )
                    session.commit()
                    print(f'remaining balance is {last_balance-amount}')
            else:
                print('no table exists')

    def last_balance(self) -> int:
        with Session(self.engine) as session:
            existing_record = self.last_row(session)
            if existing_record:
                return existing_record.balance
            else:
                return 5000  # Sets safe default starting funds if database is completely new

    def watch_db(self):
        with Session(self.engine) as session:
            if self.last_row(session):
                stmt = select(Balance_Sheet)
                for val in session.scalars(stmt):
                    print(val)
            else:
                print('empty db')

    def reset_db(self):
        inspector = inspect(self.engine)

        if inspector.has_table('balance_sheet'):
            print(f'Table Exists! {inspector.get_table_names()} Dropping the table now')
            Balance_Sheet.__table__.drop(bind=self.engine)
            print('Dropped Successfully')
            FinanceBase.metadata.create_all(bind=self.engine, tables=[Balance_Sheet.__table__])

        else:
            print('No Table Exists')



