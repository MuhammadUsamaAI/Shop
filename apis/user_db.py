from helper_functions import current_date_time
from sqlalchemy import (create_engine, String,
                        select, inspect, Enum)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Literal
import enum


class User_Types_Literal(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class UserBase(DeclarativeBase):
    pass


class UserDB(UserBase):
    __tablename__ = 'user_database'

    id:Mapped[int] = mapped_column(primary_key=True)
    acc_type:Mapped[User_Types_Literal] = mapped_column(Enum(User_Types_Literal))
    name:Mapped[str] = mapped_column(String(30))
    time_created:Mapped[str] = mapped_column(String(30))
    time_last_logged_in: Mapped[str] = mapped_column(String(30), nullable=True)

    def __repr__(self):
        return f'user_database (prm_key = {self.id}, acc_type = {self.acc_type},' \
               f'person name = {self.name}, acc_created_at = {self.time_created},' \
               f'last_logged = {self.time_last_logged_in}'

def first_row(session:Session)->UserDB|None:
    smt = select(UserDB).order_by(UserDB.id.asc()).limit(1)
    return session.scalars(smt).first()

class UserDBHandler:
    def __init__(self, db_url = 'sqlite://'):
        self.engine = create_engine(db_url, echo=False)
        UserBase.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            row = first_row(session)
            if row:
                print('pass')
            else:
                print('do something')


user = UserDBHandler()
