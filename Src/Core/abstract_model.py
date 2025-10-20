from abc import ABC
import uuid
from Src.Core.validator import validator


class abstract_model(ABC):
    __unique_code: str
    __name: str = ""

    def __init__(self, _name: str = "") -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex
        if _name != "":
            self.name = _name

    """
    Наименование
    """
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str, 50)
        self.__name = value.strip()

    """
    Уникальный код
    """

    @property
    def unique_code(self) -> str:
        return self.__unique_code

    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self.__unique_code = value.strip()

    """
    Перегрузка штатного варианта сравнения
    """

    def __eq__(self, value) -> bool:
        if value is None: return False
        if not isinstance(value, abstract_model): return False

        return self.unique_code == value.unique_code
