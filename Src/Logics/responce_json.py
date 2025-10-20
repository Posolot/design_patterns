import json
from typing import List, Any
from Src.Core.validator import validator
from Src.Core.responce_format import response_formats
from Src.Core.abstract_responce import abstract_response
from Src.Utils.handler_func import obj_to_dict


"""Класс для формирования ответа в формате Json"""
class responce_json(abstract_response):

    def __init__(self):
        super().__init__()

    def build(self, data: List[Any]) -> str:
        super().build(data, response_formats.json())

        dict_ = obj_to_dict(data)
        return json.dumps(dict_, ensure_ascii=False)