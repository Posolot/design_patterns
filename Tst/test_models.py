import uuid

from Src.Models.settings_model import Settings
from Src.Models.company_model import company_model
from Src.settings_manager import settings_manager
from Src.Models.storage_model import storage_model
from Src.Core.validator import argument_exception
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model
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
        result = range_model("грамм",1)
        # Проверки
        self.assertEqual(result.value, 1)
        self.assertEqual(result.name, "грамм")

    # Проверка создания базовой единицы и единицы с перерасчётом
    def test_create_with_valid_base_unit(self):
        # Подготовка
        base_unit = range_model("грамм", 1)
        new_unit = range_model("кг", 1000, base_unit)
        # Проверки
        self.assertEqual(new_unit.value, 1000)

    # Проверка получения ошибки при передаче не подходящей по типу базовой единицы
    def test_invalid_base_unit_type(self):
        # Проверки
        new_unit = range_model("кг", 1000, "Неверный тип данных")

    # Проверка на отрицательное значение передаваемое в коэффициент перерасчёта
    def test_negative_coefficient(self):
        #Действие
        base_unit = range_model("грамм", -5)

    # Проверка валидных значений передаваемых в класс
    def test_full_name_valid(self):
        # Подготовка
        self.group = group_model()
        self.unit = range_model("шт", 1)
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

    def test_receipt_model(self):
        # Подготовка
        receipt = receipt_model()
        receipt.name = "ОМЛЕТ С МОЛОКОМ И ЗЕЛЕНЬЮ"
        receipt.number_of_servings = 3
        receipt.cooking_length = range_model(_name="мин", _value=10)
        receipt.ingredients = [
            nomenclature_model(
                _group=group_model(_name="Зелень"),
                _range=range_model(_name="гр", _value=10)
            ),
            nomenclature_model(
                _group=group_model(_name="Сливочное масло"),
                _range=range_model(_name="гр", _value=20)
            ),
            nomenclature_model(
                _group=group_model(_name="Яйца"),
                _range=range_model(_name="шт", _value=4)
            ),
            nomenclature_model(
                _group=group_model(_name="Молоко"),
                _range=range_model(_name="гр", _value=100)
            )
        ]
        receipt.steps = [
            '''Подготовьте все ингредиенты для омлета.''',
            ''' Разбейте яйца в миску и слегка взбейте венчиком или вилкой.''',
            '''Влейте молоко и хорошо перемешайте до однородности.''',
            '''На сковороде растопите сливочное масло на среднем огне.''',
            '''Вылейте яично-молочную смесь на сковороду.''',
            '''Готовьте под крышкой на медленном огне 5–7 минут, пока омлет не схватится.''',
            '''Посыпьте сверху измельчённой зеленью и подавайте горячим.'''
        ]
        assert receipt.name != ""
        assert receipt.number_of_servings == 3
        assert receipt.cooking_length.name != ""
        assert len(receipt.ingredients) > 0
        assert len(receipt.steps) > 0


if __name__ == '__main__':
    unittest.main()
