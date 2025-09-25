import json


class company_model:
    _name: str = ""
    _inn: int = ""
    _corr_account: int = ""
    _bik: int = ""
    _account: int = ""
    _ownership: str = ""


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value.strip() != "":
            self._name = value.strip()


