from abc import ABC, abstractmethod
from Src.Core.validator import validator, operation_exception
from Src.Core.responce_format import response_formats

# Абстрактный класс для фолрмирования ответов
class abstract_response(ABC):
    @abstractmethod
    def build(self, data: list, format: str | response_formats):
        # Проверка формата
        if isinstance(format, str):
            format = format.lower()
            if format not in [f.lower() for f in response_formats.answers_types()]:
                raise ValueError(f"Unsupported format: {format}")
        else:
            validator.validate(format, response_formats)

        # Проверка данных
        validator.is_list_of_same(data, "list of models")

        # Возвращаем **структуру**, а не строку
        result = [item.to_dict() if hasattr(item, "to_dict") else item.__dict__ for item in data]
        return result