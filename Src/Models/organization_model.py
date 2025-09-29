from Src.Core.validator import validator
from Src.Core.abstract_model import abstact_model


class organization_model(abstact_model):
    _inn: int = 0
    _bic: int = 0
    _account: int = 0
    _form_ownership = ""

    @property
    def inn(self) -> int:
        return self._inn

    @inn.setter
    def inn(self, value: int):
        validator.validate(value, int, 12)
        self._inn = value

    @property
    def bic(self) -> int:
        return self._bic

    @bic.setter
    def bic(self, value: int):
        validator.validate(value, int, 9)
        self._bic = value

    @property
    def account(self) -> int:
        return self._account

    @account.setter
    def account(self, value: int):
        validator.validate(value, int, 11)
        self._account = value

    @property
    def form_ownership(self) -> str:
        return self._form_ownership

    @form_ownership.setter
    def form_ownership(self, value: str):
        validator.validate(value, str)
