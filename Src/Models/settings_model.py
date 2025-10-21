from Src.Models.company_model import company_model
from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Core.responce_format import response_formats

class Settings(abstract_model):
    _company: company_model = None
    _response_format: response_formats = "json"  # значение по умолчанию json
    @property
    def company(self) -> company_model:
        return self._company

    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self._company = value
    """
    Формат ответа
    """

    @property
    def response_format(self) -> response_formats:
        return self._response_format

    @response_format.setter
    def response_format(self, value: response_formats):
        validator.validate(value, response_formats, "response format")
        self._response_format = value