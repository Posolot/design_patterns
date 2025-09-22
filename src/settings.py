from src.models.company_model import company_model


class Settings:
    _company: company_model = None

    def __init__(self):
        self._company = company_model()
    @property
    def company(self) -> company_model:
        return self._company

    def validate_str(self, value: str, length: int, field: str) -> str:
        value = value.strip()
        if len(value) != length:
            raise ValueError(f"{field} должен содержать ровно {length} символов")
        return value

    def load_data_from_dic(self, data: dict):
        # Загружает данные из словаря
        if not isinstance(data, dict):
            raise TypeError("Полученные данные не словарь")

        company_data = data["company"]
        if company_data is None or not isinstance(company_data, dict):
            raise ValueError("Settings: должен быть словарь 'company'")

        # Валидация данных
        self._company.name = self.validate_str(company_data["name"], len(company_data["name"]),"Наименование")
        self._company.inn = self.validate_str(company_data["inn"], 12, "ИНН")
        self._company.account = self.validate_str(company_data["account"], 11, "Счёт")
        self._company.corr_account = self.validate_str(company_data["corr_account"], 11, "Корреспондентский счет")
        self._company.bik = self.validate_str(company_data["bik"], 9, "БИК")
        self._company.ownership = self.validate_str(company_data["ownership"], 5, "Вид собственности")
