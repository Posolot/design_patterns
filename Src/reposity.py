"""
Репозиторий данных
"""
from Src.Models.receipt_model import receipt_model
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import validator
import inspect


class reposity:
    def __init__(self):
        # инстансные контейнеры — безопаснее, чем атрибуты класса
        self._data = {}
        self._receipts: list[receipt_model] = []

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

    # Ключ для единиц измерений
    @staticmethod
    def range_key():
        return "range_model"

    def append(self, key: str, value: abstract_model):
        validator.validate(value, abstract_model)
        validator.validate(key, str)
        if key not in self.data:
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

    @staticmethod
    def keys() -> list[str]:
        # безопасно собираем статические методы, оканчивающиеся на _key
        # используем __dict__ чтобы не поймать посторонние callables из базовых классов
        results = []
        for name, member in reposity.__dict__.items():
            if not name.endswith("_key"):
                continue
            # получить вызываемый атрибут (staticmethod возвращается через getattr)
            try:
                candidate = getattr(reposity, name)
            except Exception:
                continue
            if callable(candidate):
                try:
                    results.append(candidate())
                except Exception:
                    continue
        return results

    def get_models(self, key: str) -> list:
        """
        Возвращает список моделей по ключу в едином формате.
        Поддерживает dict (ключ->model) и list (список моделей).
        """
        container = self.data.get(key, [])
        if isinstance(container, dict):
            return list(container.values())
        if isinstance(container, list):
            return list(container)
        try:
            return list(container)
        except Exception:
            return []
