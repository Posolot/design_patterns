"""
Репозиторий данных
"""
from Src.Models.receipt_model import receipt_model
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator


class reposity:
    _data = {}
    _receipts: list[receipt_model] = []

    @property
    def receipts(self):
        return self._receipts
    @property
    def data(self):
        return self._data

    # Ключ для групп
    @staticmethod
    def group_key():
        return "group_model"

    # Ключ для номенклатур
    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"

    """
    Ключ для единц измерений
    """

    @staticmethod
    def range_key():
        return "range_model"

    def append(self, key: str, value: abstract_model):
        validator.validate(value, abstract_model)
        validator.validate(key, str)
        if not key in self.data:
            self.data[key] = [value]
        else:
            self.data[key].append(value)

    def view_simple(self, key: str):
        if key not in self.data:
            return []
        result = []
        for item in self.data[key]:
            # если есть to_dict — используем
            if hasattr(item, "to_dict"):
                result.append(item.to_dict())
                continue
            attrs = [a for a in dir(item) if not a.startswith("_") and not callable(getattr(item, a))]
            if attrs:
                result.append({a: getattr(item, a) for a in attrs})
            else:
                result.append(item.__dict__)  # fallback: всё что есть
        return result