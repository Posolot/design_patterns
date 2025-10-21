from typing import Union
from Src.Core.validator import validator
from Src.Core.responce_format import response_formats
from Src.Core.abstract_responce import abstract_response
from Src.Logics.responce_csv import responce_csv
from Src.Logics.responce_xml import responce_xml
from Src.Logics.responce_json import responce_json
from Src.Logics.responce_markdown import responce_markdown
from Src.settings_manager import settings_manager
class facrtory_entities:

    # Подключаем менеджер настроек
    __settings = settings_manager()

    __match_formats = {
        "csv": response_formats.csv(),
        "markdown": response_formats.markdown(),
        "md": response_formats.markdown(),
        "json": response_formats.json(),
        "xml": response_formats.xml(),
    }

    # Сопоставление форматов и классов-ответов
    __match_responses = {
        response_formats.csv(): responce_csv,
        response_formats.markdown(): responce_markdown,
        response_formats.json(): responce_json,
        response_formats.xml(): responce_xml
    }

    """Метод получения экземпляра ответа"""
    def create(self, format: Union[str, response_formats]) -> abstract_response:
        validator.validate(format, (str, response_formats))
        if isinstance(format, str):
            format = format.lower().strip()
            if format not in self.__match_formats:
                raise Exception(
                    f"Format '{format}' isn't supported. Available formats: "
                    f"{self.__match_formats.keys()}"
                )
            format = self.__match_formats[format]

        return self.__match_responses[format]()

    """Получение экземпляра ответа по умолчанию (из настроек)"""
    def create_default(self) -> abstract_response:
        return self.create(settings_manager().settings.response_format)