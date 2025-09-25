from src.settings import Settings
from src.models.company_model import company_model
from src.settings_manager import settings_manager

import unittest
import json
import pytest

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

    #def test_load_createmodel_companymodel(self):
        # Подготовка
        #file_name = "C:/Users/ilushenka/PycharmProjects/UI/shablons_programm/settings.json"
        #manager = settings_manager(file_name)
        # Действие
        #result = manager.load()
        # Проверки
        #assert result == True

    #def test_load_createmodel_companymodel(self):
        # Подготовка
        #file_name = "C:/Users/ilushenka/PycharmProjects/UI/shablons_programm/settings.json"
        #manager1 = settings_manager(file_name)
        #manager2 = settings_manager(file_name)
        # Действие
        #manager1.load()
        #manager2.load()
        # Проверки
        #assert manager1.company == manager2.company
    def test_check_object_create(self):
        # Подготовка
        file_name = "C:/Users/ilushenka/PycharmProjects/UI/design_patterns/settings.json"
        manager1 = settings_manager(file_name)
        # Действие
        manager1.load()
        result_manager_fun = manager1.convert()
        #Проверки
        self.assertIsInstance(result_manager_fun, Settings,"Не создан объект Settings")

    def test_check_attribute(self):
        # Подготовка
        file_name = "C:/Users/ilushenka/PycharmProjects/UI/design_patterns/settings.json"
        manager1 = settings_manager(file_name)
        # Действие
        manager1.load()
        settings_exemplar = manager1.convert().company
        # Проверки
        assert hasattr(settings_exemplar, 'name') is True
        assert hasattr(settings_exemplar, 'inn') is True
        assert hasattr(settings_exemplar, 'account') is True
        assert hasattr(settings_exemplar, 'corr_account') is True
        assert hasattr(settings_exemplar, 'bik') is True
        assert hasattr(settings_exemplar, 'ownership') is True

        assert settings_exemplar.name.strip() != ""
        assert settings_exemplar.inn.strip() != ""
        assert settings_exemplar.account.strip != ""
        assert settings_exemplar.corr_account.strip() != ""
        assert settings_exemplar.bik.strip() != ""
        assert settings_exemplar.ownership.strip() != ""

    def test_load_file_another_catalog(self):
        # Подготовка
        file_name = "C:/Users/ilushenka/Desktop/testing.json"#Абсолютный путь
        manager1 = settings_manager(file_name)
        file_name2 = "../settings.json" #Относительный путь
        manager2 = settings_manager(file_name2)
        # Действие
        manager1.load()
        manager2.load()
        assert manager1._data is not None
        assert manager2._data is not None

    def test_wrong_json_data_inn(self):
        # Подготовка
        file_name = "../settings.json"  # Относительный путь
        manager1 = settings_manager(file_name)
        # Действие
        manager1.load()
        manager1.settings.company.inn = "12312312312"  # 11 символов вместо 12
        # Тесты
        assert manager1.settings.company.inn == manager1.settings.validate_str(manager1.settings.company.inn, 12, "ИНН")

    def test_wrong_json_data_account(self):
        file_name = "../settings.json"
        manager1 = settings_manager(file_name)
        manager1.load()
        manager1.settings.company.account = "1231231231"  # 10 символов вместо 11
        assert manager1.settings.company.account == manager1.settings.validate_str(
            manager1.settings.company.account, 11, "Счёт"
        )

    def test_wrong_json_data_bik(self):
        file_name = "../settings.json"
        manager1 = settings_manager(file_name)
        manager1.load()
        manager1.settings.company.bik = "12312312"  # 8 символов вместо 9
        assert manager1.settings.company.bik == manager1.settings.validate_str(
            manager1.settings.company.bik, 9, "БИК"
        )

    def test_wrong_json_data_ownership(self):
        file_name = "../settings.json"
        manager1 = settings_manager(file_name)
        manager1.load()
        manager1.settings.company.ownership = "1231"  # 4 символа вместо 5
        assert manager1.settings.company.ownership == manager1.settings.validate_str(
            manager1.settings.company.ownership, 5, "Вид собственности"
        )

    def test_wrong_json_data_corr_account(self):
        file_name = "../settings.json"
        manager1 = settings_manager(file_name)
        manager1.load()
        manager1.settings.company.corr_account = "1231231231"  # 10 символов вместо 11
        assert manager1.settings.company.corr_account == manager1.settings.validate_str(
            manager1.settings.company.corr_account, 11, "Корреспондентский счет"
        )


if __name__ == '__main__':
    unittest.main()
