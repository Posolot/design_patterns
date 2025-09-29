import json
from Src.Core.validator import validator


class company_model:
    _name: str = ""
    _inn: int = 0
    _corr_account: int = 0
    _bik: int = 0
    _account: int = 0
    _ownership: str = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self._name = value.strip()

    # ИНН
    @property
    def inn(self) -> int:
        return self._inn

    @inn.setter
    def inn(self, value: int):
        validator.validate(value, int, 12)
        self._inn = value

    # КПП
    @property
    def bic(self) -> int:
        return self._bic

    @bic.setter
    def bic(self, value: int):
        validator.validate(value, int, 9)
        self._bic = value

    # Корреспондентский счет
    @property
    def corr_account(self) -> int:
        return self._corr_account

    @corr_account.setter
    def corr_account(self, value: int):
        validator.validate(value, int, 11)
        self._corr_account = value

    @property
    def account(self) -> int:
        return self._account

    @account.setter
    def account(self, value: int):
        validator.validate(value, int, 11)
        self._account = value

    @property
    def ownership(self) -> str:
        return self._ownership

    @ownership.setter
    def ownership(self, value: str):
        validator.validate(value, str, 5)
        self._ownership = value.strip()



