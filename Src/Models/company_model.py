import json
from Src.Core.validator import validator
from Src.Core.entity_model import entity_model


class company_model(entity_model):
    _inn: int = 0
    _corr_account: int = 0
    _bik: int = 0
    _account: int = 0
    _ownership: str = ""

    # ИНН : 12 симв
    # Счет 11 симв
    # Корреспондентский счет 11 симв
    # БИК 9 симв
    # Наименование
    # Вид собственности 5 симв


    # ИНН
    @property
    def inn(self) -> int:
        return self._inn

    @inn.setter
    def inn(self, value: int):
        validator.validate(value, int, 12,True)
        self._inn = value

    # КПП
    @property
    def bic(self) -> int:
        return self._bic

    @bic.setter
    def bic(self, value: int):
        validator.validate(value, int, 9,True)
        self._bic = value

    # Корреспондентский счет
    @property
    def corr_account(self) -> int:
        return self._corr_account

    @corr_account.setter
    def corr_account(self, value: int):
        validator.validate(value, int, 11,True)
        self._corr_account = value

    @property
    def account(self) -> int:
        return self._account

    @account.setter
    def account(self, value: int):
        validator.validate(value, int, 11,True)
        self._account = value

    @property
    def ownership(self) -> str:
        return self._ownership

    @ownership.setter
    def ownership(self, value: str):
        validator.validate(value, str, 5,True)
        self._ownership = value.strip()



