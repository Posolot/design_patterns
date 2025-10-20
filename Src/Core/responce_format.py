# Форматы ответов
import inspect
class response_formats:
    @staticmethod
    def csv() -> str:
        return "csv"

    @staticmethod
    def markdown() -> str:
        return "markdown"

    @staticmethod
    def md() -> str:
        return "markdown"

    @staticmethod
    def json() -> str:
        return "json"

    @staticmethod
    def xml() -> str:
        return "xml"

    @staticmethod
    def answers_types() -> list:
        # Получаем только функции, определённые в классе (inspect.isfunction)
        funcs = [
            member for name, member in inspect.getmembers(response_formats, predicate=inspect.isfunction)
            if name != "answers_types"
        ]
        # Вызываем каждую функцию и возвращаем результат
        return [f() for f in funcs]
