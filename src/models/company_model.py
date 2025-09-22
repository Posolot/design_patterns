import json
class company_model:
    _name: str = ""
    _inn: str = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value.strip() != "":
            self._name = value.strip()


