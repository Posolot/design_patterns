from Src.Core.common import common
from typing import List, Any
from Src.Core.validator import validator
from Src.Core.responce_format import response_formats
from Src.Core.abstract_responce import abstract_response
from Src.Utils.handler_func import get_properties, obj_to_str

class response_scv(abstract_response):
    # Разделитель CSV
    delimitter: str = ","

    def __init__(self):
        super().__init__()

    """Сформировать CSV из списка моделей"""
    def build(self, data: List[Any]) -> str:
        text = super().build(data, response_formats.csv())

        # Шапка
        item = data[0]
        properties = get_properties(item)
        text += self.delimitter.join(properties) + "\n"

        # Данные
        rows = list()
        for item in data:
            values = list()
            for prop in properties:
                value = getattr(item, prop)
                values += [obj_to_str(value)]

            rows += [self.delimitter.join(values)]

        text += "\n".join(rows)
        return text

