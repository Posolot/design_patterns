import os.path
import json
from src.settings import Settings

class settings_manager:
    _file_name: str = ""
    _settings: Settings = None

    #singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self, file_name: str):
        self.file_name = file_name
        self._data = None


    @property
    def file_name(self):
        return self._file_name

    @property
    def settings(self):
        return self._settings
    @file_name.setter
    def file_name(self, value: str):
        if value.strip() == "":
            return
        if os.path.exists(value):
            self._file_name = value.strip()
        self._file_name = os.path.abspath(value)
        print(self._file_name)

    def load(self) -> bool:
        if self._file_name.strip() == "":
            raise Exception("Не найден файл настроек")
        try:
            with open(self._file_name, "r", encoding="utf-8") as f:
                self._data = json.load(f)
            if self._data is None:
                return False
        except:
            return False

    def convert(self) -> Settings:
        if self._data is None:
            raise ValueError("Сначала вызови load() для загрузки данных")
        self._settings = Settings()
        self._settings.load_data_from_dic(self._data)
        return self._settings
