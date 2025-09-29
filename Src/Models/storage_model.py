from Src.Core.validator import validator
from Src.Core.abstract_model import abstact_model


class storage_model(abstact_model):
    _name: str = ""

    # Наименование
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self._name = value.strip()
