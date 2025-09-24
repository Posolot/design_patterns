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
        if not isinstance(self._data, dict):
            raise TypeError("Полученные данные не словарь")
        company_data = self._data.get("company")
        if company_data is None or not isinstance(company_data, dict):
            raise ValueError("Settings: должен быть словарь 'company'")
        # Валидация данных
        self._settings.company.name = self._settings.validate_str(company_data.get("name"), len(company_data.get("name","")),"Наименование")
        self._settings.company.inn = self._settings.validate_str(company_data.get("inn"), 12, "ИНН")
        self._settings.company.account = self._settings.validate_str(company_data.get("account"), 11, "Счёт")
        self._settings.company.corr_account = self._settings.validate_str(company_data.get("corr_account"), 11, "Корреспондентский счет")
        self._settings.company.bik = self._settings.validate_str(company_data.get("bik"), 9, "БИК")
        self._settings.company.ownership = self._settings.validate_str(company_data.get("ownership"), 5, "Вид собственности")

        return self._settings
