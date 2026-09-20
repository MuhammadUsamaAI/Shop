from enum import Enum


class UserEnum(str, Enum):
    def __str__(self):
        return str(self.value)

    @classmethod
    def _missing_(cls, value:str|int)->Enum | None:
        """Pydantic triggers this when Enum(value) raises a ValueError."""
        if isinstance(value, str):
            val_lower = value.strip().lower()
            for member in cls:
                if member.value == val_lower:
                    return member
        elif isinstance(value, int):
            val_str = str(value)
            for member in cls:
                if member.value == val_str:
                    return member
        return None


class UserTypesAdmin(UserEnum):
    USER = 'user'
    MANAGER = 'manager'
    ADMIN = 'admin'
    LOGOUT = 'exit'


class UserOptsYN(UserEnum):
    YES = 'yes'
    NO = 'no'


class UserOpts1to4(UserEnum):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'


class UserOptsAddRemove(UserEnum):
    ADD = 'add'
    REMOVE = 'remove'


class UserMenu(UserEnum):
    BUY = 'buy'
    SELL = 'sell'
    VIEW = 'view'
    BACK = 'back'
    ENTER = 'enter'
    EXIT = 'exit'
