from abc import ABC, abstractmethod
from Src.Core.validator import validator, operation_exception
from Src.Core.responce_format import response_formats

# Абстрактный класс для фолрмирования ответов
class abstract_response(ABC):
    @abstractmethod
    def build(self, data: list, format: str) -> str:
        """
        data: список моделей
        format: строка, одна из допустимых форматов (json, csv, markdown, xml)
        """
        validator.validate(format, str)
        if format.lower() not in [f.lower() for f in response_formats.answers_types()]:
            raise ValueError(f"Unsupported format: {format}")

        # Проверяем, что data — список однотипных объектов
        validator.is_list_of_same(data, "list of models")