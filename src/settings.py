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


