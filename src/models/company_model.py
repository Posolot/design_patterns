import json


class company_model:
    _name: str = ""
    _inn: str = ""
    _corr_account: str = ""
    _bik: str = ""
    _account: str = ""
    _ownership: str = ""


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value.strip() != "":
            self._name = value.strip()


