import json
from typing import List, Any
from Src.Core.validator import validator
from Src.Core.responce_format import response_formats
from Src.Core.abstract_responce import abstract_response
from Src.Utils.handler_func import obj_to_dict, get_properties, obj_to_str


"""Класс для формирования ответа в формате Json"""
class responce_markdown(abstract_response):

    def __init__(self):
        super().__init__()

    def build(self, data: List[Any]) -> str:
        super().build(data, response_formats.markdown())

        item = data[0]
        properties = get_properties(item)

        # Заголовок 1-го уровня
        rows = [f"# Список объектов класса '{type(item).__name__}'"]

        for i, item in enumerate(data):
            # Заголовки 2-го уровня - обозначения моделей
            rows += [f"## {i+1}. {obj_to_str(item)}"]
            for j, prop in enumerate(properties):
                # Заголовки 3-го уровня и текст - поля и их значения
                value = getattr(item, prop)
                rows += [f"### {i+1}.{j+1}. {prop}"]
                rows += [obj_to_str(value)]

        return "\n\n".join(rows)