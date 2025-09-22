import os.path
import json
from src.models.company_model import company_model

class settings_manager:
    _file_name:str = ""
    _company:company_model = None

    #singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.default()

    @property
    def company(self) -> company_model:
        return self._company

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value:str):
        if value.strip() == "":
            return
        if os.path.exists(value):
            self._file_name = value.strip()

    def load(self) -> bool:
        if self._file_name.strip() == "":
            raise Exception("Не найден файл настроек")
        try:
            with open(self._file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "company" in data.keys():
                item = data["company"]
                self._company.name = item["name"]
                return True
            return False
        except:
            return False

    def default(self):
        self._company = company_model()
        self._company.name = "Рога и Копыта"