from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model


class storage_model(abstract_model):
    __address: str = ""

    """
    Адрес
    """

    @property
    def address(self) -> str:
        return self.__address.strip()

    @address.setter
    def address(self, value: str):
        validator.validate(value, str)
        self.__address = value.strip()

