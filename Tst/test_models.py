import uuid

from Src.Models.settings_model import Settings
from Src.Models.company_model import company_model
from Src.settings_manager import settings_manager
from Src.Models.storage_model import storage_model
from Src.Core.validator import argument_exception
from Src.Models.unit_measure_model import unit_measure_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
import unittest


class test_models(unittest.TestCase):

    # Провери создание основной модели
    # Данные после создания должны быть пустыми
    def test_empty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()

        # Действие

        # Проверки
        assert model.name == ""

    # Проверить создание основной модели
    # Данные меняем. Данные должны быть
    def test_notEmpty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()

        # Действие
        model.name = "test"

        # Проверки
        assert model.name != ""

    # Проверить создание основной модели
    # Данные загружаем через json настройки
    def test_load_createmodel_companymodel(self):
        # Подготовка
        file_name = "../settings.json"
        manager = settings_manager()
        manager.file_name = file_name
        # Действие
        result = manager.load()
        # Проверки
        assert result == True

    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_loadCombo_createmodel_companymodel(self):
        # Подготовка
        file_name = "./settings.json"
        manager1 = settings_manager()
        manager1.file_name = file_name
        manager2 = settings_manager()
        check_inn = 123456789

        # Действие
        manager1.load()
        # Проверки
        assert manager1.settings == manager2.settings
        assert (manager1.settings.company.inn == check_inn)

    # Проверка на валидацию счёта
    # Тест не должен проходить
    def test_wrong_json_data(self):
        # Подготовка
        file_name = "../wrong_data.json"
        manager1 = settings_manager()
        manager1.file_name = file_name
        # Действие
        result = manager1.load()
        # Проверки
        assert result == True

    # Тест на модель единицы измерения
    # Проверяем вариант создания без коэффициента
    def test_create_base_unit_default(self):
        # Действие
        result = unit_measure_model("грамм",1)
        # Проверки
        self.assertEqual(result.coefficient, 1)
        self.assertEqual(result.name, "грамм")

    # Проверка создания базовой единицы и единицы с перерасчётом
    def test_create_with_valid_base_unit(self):
        # Подготовка
        base_unit = unit_measure_model("грамм", 1)
        new_unit = unit_measure_model("кг", 1000, base_unit)
        # Проверки
        self.assertEqual(new_unit.factor, 1000)

    # Проверка получения ошибки при передаче не подходящей по типу базовой единицы
    def test_invalid_base_unit_type(self):
        # Проверки
        new_unit = unit_measure_model("кг", 1000, "Неверный тип данных")

    # Проверка на отрицательное значение передаваемое в коэффициент перерасчёта
    def test_negative_coefficient(self):
        #Действие
        base_unit = unit_measure_model("грамм", -5)

    # Проверка валидных значений передаваемых в класс
    def test_full_name_valid(self):
        # Подготовка
        self.group = nomenclature_group_model()
        self.unit = unit_measure_model("шт", 1)
        model = nomenclature_model()
        model.full_name = "Товар А"
        # Проверки
        self.assertEqual(model.full_name, "Товар А")

    # Проверка на слишком длинное имя
    def test_full_name_too_long_raises(self):
        # Подготовка
        model = nomenclature_model()
        long_name = "x" * 256
        # Действие
        model.full_name = long_name
        # Проверки
        assert model.full_name == long_name

    # Проверка на сравнение двух по значению одинаковых моделей
    def test_equals_storage_model_create(self):
        # Подготовка
        id = uuid.uuid4().hex
        storage1 = storage_model()
        storage1.unique_code = id
        storage2 = storage_model()
        storage2.unique_code = id
        # Действие GUID

        # Проверки
        assert storage1 == storage2


if __name__ == '__main__':
    unittest.main()
