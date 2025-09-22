from src.models.company_model import company_model
from src.settings_manager import settings_manager
import unittest
import json


class test_models(unittest.TestCase):
    # Проверка создания основной модели
    # Данные после проверки должны быть пустыми
    def test_empty_createmodel_company_model(self):
        # Подготовка
        model = company_model()
        # Действие
        assert model.name == ""

    # Проверка создания основной модели
    # Данные после проверки должны быть пустыми
    def test_not_empty_createmodel_company_model(self):
        # Подготовка
        model = company_model()
        model.name = "test"
        # Действие
        assert model.name != ""

    def test_load_createmodel_companymodel(self):
        # Подготовка
        file_name = "C:/Users/ilushenka/PycharmProjects/UI/shablons_programm/settings.json"
        manager = settings_manager(file_name)
        # Действие
        result = manager.load()
        # Проверки
        assert result == True

    def test_load_createmodel_companymodel(self):
        # Подготовка
        file_name = "C:/Users/ilushenka/PycharmProjects/UI/shablons_programm/settings.json"
        manager1 = settings_manager(file_name)
        manager2 = settings_manager(file_name)
        # Действие
        manager1.load()
        #manager2.load()
        # Проверки
        assert manager1.company == manager2.company


if __name__ == '__main__':
    unittest.main()
