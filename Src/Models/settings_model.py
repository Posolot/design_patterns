from Src.Models.company_model import company_model
from Src.Core.validator import validator


class Settings:
    _company: company_model = None

    @property
    def company(self) -> company_model:
        return self._company

    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self._company = value
