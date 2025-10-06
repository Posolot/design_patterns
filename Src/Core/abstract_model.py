from abc import ABC
import uuid
from Src.Core.validator import validator


class abstact_model(ABC):
    __unique_code: str
    __name: str

    def __init__(self) -> None:
        super().__init__()
        self._unique_code = uuid.uuid4().hex
        self._name = ""
    """
    Уникальный код
    """

    @property
    def unique_code(self) -> str:
        return self._unique_code

    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self._unique_code = value.strip()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str, 50)
        self._name = value.strip()
    """
    Перегрузка штатного варианта сравнения
    """

    def __eq__(self, value: str) -> bool:
        return self._unique_code == value
