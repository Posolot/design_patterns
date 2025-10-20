from abc import ABC, abstractmethod
from Src.Core.validator import validator, operation_exception
from Src.Core.responce_format import response_formats

# Абстрактный класс для фолрмирования ответов
class abstract_response(ABC):

    @abstractmethod
    def __init__(self):
        super().__init__()

    """Сформировать нужный ответ"""
    @abstractmethod
    def build(self, data: list, format: str) -> str:
        validator.validate(format, response_formats, "format")
        validator.is_list_of_same(data, "list of models")

        return ""