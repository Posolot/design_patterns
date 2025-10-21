import os
import json
from Src.Models.settings_model import Settings
from Src.Core.validator import validator
from Src.Core.validator import argument_exception
from Src.Core.validator import operation_exception
from Src.Models.company_model import company_model
from Src.Core.responce_format import response_formats
class settings_manager:
    # Наименование файла (полный путь)
    _file_name: str = ""

    # Настройки
    _settings: Settings = None
    #singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        self.set_default()
    @property
    def file_name(self):
        return self._file_name

    @property
    def settings(self):
        return self._settings
    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self._file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    def load(self) -> bool:
        if self._file_name.strip() == "":
            raise operation_exception("Не найден файл настроек!")
        try:
            with open(self._file_name, 'r') as file_instance:
                settings = json.load(file_instance)

                if "company" in settings.keys():
                    data = settings["company"]
                    return self.convert(data)
                # Загружаем формат ответа
                if "response_format" in settings.keys():
                    self._settings.response_format = settings["response_format"]
                return False
        except:
            return False

    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        fields = list(filter(lambda x: not x.startswith("_"), dir(self._settings.company)))
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self._settings.company, key, data[key])
        except:
            return False

        return True

    def set_default(self):
        company = company_model()
        company.name = "Рога и копыта"
        company.inn = -1

        self._settings = Settings()
        self._settings.company = company
