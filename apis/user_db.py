import time
from helper_functions import current_date_time
from sqlalchemy import (create_engine, String, Integer,
                        select, Enum, CheckConstraint,
                        DDL, event
                        )
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import enum


class UserTypesLiteral(str ,enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

    def __str__(self):
        return self.value


class UserBase(DeclarativeBase):
    pass


class UserDB(UserBase):
    __tablename__ = 'user_database'

    id:Mapped[int] = mapped_column(primary_key=True)
    acc_type:Mapped[UserTypesLiteral] = mapped_column(
        Enum(
            UserTypesLiteral,
            name = 'user_types_enum',
            values_callable = lambda x: [e.value for e in x]

        )
    )
    name:Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(
        Integer(),
        CheckConstraint(
            'age BETWEEN 18 AND 124', name= 'check_age_range'
        )
    )
    pin: Mapped[int] = mapped_column(
        Integer(),
        CheckConstraint(
            'pin >= 1000 AND pin <= 9999', name='check_pin_range'
        )
    )
    time_created:Mapped[str] = mapped_column(String(30))
    time_last_logged: Mapped[str] = mapped_column(String(30), nullable=True)

    def __repr__(self):
        return f'user_database (prm_key = {self.id}, acc_type = {self.acc_type},' \
               f'person name = {self.name}, acc_created_at = {self.time_created},' \
               f'last_logged = {self.time_last_logged}'


def first_row(session:Session)->UserDB|None:
    smt = select(UserDB).order_by(UserDB.id.asc()).limit(1)
    return session.scalars(smt).first()


class UserDBHandler:
    prevent_admin_delete = DDL("""
    CREATE TRIGGER IF NOT EXISTS protect_admin_deletion
    BEFORE DELETE ON user_database
    FOR EACH ROW
    WHEN OLD.acc_type = 'admin'
    BEGIN
        SELECT RAISE(ABORT, 'CRITICAL ERROR: Admin accounts cannot be deleted from the database.');
    END;
    """)

    def __init__(self, db_url = 'sqlite://'):
        self.engine = create_engine(db_url, echo=False)

        event.listen(UserDB.__table__,
                     'after_create',
                     self.prevent_admin_delete)

        UserBase.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            has_admin = session.scalars(select(UserDB).where(
                UserDB.acc_type == UserTypesLiteral.admin
            )).first()
            if not has_admin:
                session.add(
                    UserDB(
                        acc_type=UserTypesLiteral.admin,
                        name='usama',
                        age=29,
                        pin=1234,
                        time_created=current_date_time()
                    )
                )
                session.commit()
                print('DB Initiated with Admin ')

    def add_to_db(self,
              account_type: str,
              name:str,
              age:int,
              pin:int
              )->None:
        with Session(self.engine) as session:
            session.add(
                UserDB(
                    acc_type = account_type,
                    name = name,
                    age = age,
                    pin = pin,
                    time_created = current_date_time()
                )
            )
            session.commit()
            print('new person added to the DB', '\n')
            print(f'UserDB(account_type = {account_type}, name = {name}, age = {age})')

    def logged(self,
               account_type:str,
               name:str,
               pin:int
               )->bool:
        with Session(self.engine) as session:
            db_records = session.scalars(select(UserDB).where(
                 UserDB.acc_type == account_type,
                 UserDB.name == name,
                 UserDB.pin == pin
            )).first()
            if db_records:
                print(f'Sucessful Account found for {name}, {account_type}')
                db_records.time_last_logged = current_date_time()
                session.commit()
                return True
            else:
                print('False Logged in ID not Exists')
                return False

    def remove_id(self,
                  account_type:str,
                  name:str,
                  age:int
                  ):
        with Session(self.engine) as session:
            account = session.scalars(select(UserDB).where(
                UserDB.acc_type == account_type,
                UserDB.name == name,
                UserDB.age == age
                )
            ).first()
            if account:
                session.delete(account)
                session.commit()
                print(f'deleted {account_type}, {name}, {age}')
            else:
                print('Account non existent')

    def watch_db(self):
        with Session(self.engine) as session:
            stmt = select(UserDB)
            for val in session.scalars(stmt):
                print(val)


# user = UserDBHandler()
# user.to_db(account_type='manager', name='Falak', age=31, pin = 1234)
# time.sleep(3)
# user.logged(name='usama', account_type='admin', pin = 1234)
# user.watch_db()
# time.sleep(3)
# user.logged(name='usama', account_type='admin', pin = 1234)
# user.logged(name='Falak', account_type='manager', pin = 1234)
# user.watch_db()
# user.remove_id(name='usama', age=29, account_type='admin')
# user.watch_db()
