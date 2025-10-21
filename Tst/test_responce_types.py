import unittest
import json
import os
import xml.etree.ElementTree as ET

from Src.Logics.responce_csv import responce_csv
from Src.Logics.responce_json import responce_json
from Src.Logics.responce_markdown import responce_markdown
from Src.Logics.responce_xml import responce_xml
from Src.Logics.factory_entities import facrtory_entities
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Models.receipt_model import receipt_model


class TestResponseFactory(unittest.TestCase):
    def setUp(self):
        # Подготовка
        self.output_dir = "tests/test_output"
        os.makedirs(self.output_dir, exist_ok=True)

        self.group = group_model()
        self.group.name = "Основная группа"

        self.unit = range_model.create("грамм")
        self.unit.name = "Штука"

        self.nomenclature1 = nomenclature_model("Товар 1", self.group, self.unit)
        self.nomenclature2 = nomenclature_model("Товар 2", self.group, self.unit)

        self.recipe = receipt_model(
            _number_of_servings=2,
            _ingredients=[self.nomenclature1, self.nomenclature2],
            _steps=["Шаг 1: Подготовка", "Шаг 2: Смешивание", "Шаг 3: Готовка"],
            _cooking_length=range_model.create("минуты")
        )

        self.factory = facrtory_entities()
        self.available_formats = ["csv", "json", "markdown", "xml"]

    def save_to_file(self, content, filename):
        # Подготовка
        path = os.path.join(self.output_dir, filename)
        # Действие
        with open(path, "w", encoding="utf-8") as f:
            if isinstance(content, list):
                f.write("".join(str(c) for c in content))
            else:
                f.write(str(content))
        # Проверки
        assert os.path.exists(path)
        return path

    # ==== Проверка, что build возвращает строку ====
    def test_build_returns_string_for_all_formats(self):
        # Подготовка
        models = [self.nomenclature1, self.nomenclature2]

        for fmt in self.available_formats:
            with self.subTest(format=fmt):
                instance = self.factory.create(fmt)
                # Действие
                result = instance.build(models)
                if isinstance(result, list):
                    result = "".join(str(r) for r in result)
                # Проверки
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)

    # ==== CSV ====
    def test_csv_contains_headers(self):
        # Подготовка
        models = [self.nomenclature1, self.nomenclature2]
        instance = self.factory.create("csv")

        # Действие
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        path = self.save_to_file(result, "nomenclature.csv")

        # Проверки
        self.assertIn("name", result)
        self.assertIn("unique_code", result)
        self.assertIn("Товар 1", result)
        self.assertTrue(os.path.exists(path))

    # ==== JSON ====
    def test_json_output_is_valid(self):
        # Подготовка
        models = [self.nomenclature1]
        instance = self.factory.create("json")

        # Действие
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        parsed = json.loads(result)

        # Проверки
        self.assertEqual(parsed[0]["name"], "Товар 1")

    # ==== Markdown ====
    def test_markdown_contains_headers(self):
        # Подготовка
        models = [self.nomenclature1]
        instance = self.factory.create("markdown")

        # Действие
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)

        # Проверки
        self.assertIn("# Список объектов класса 'nomenclature_model'", result)
        self.assertIn("## 1. Товар 1", result)

    # ==== XML ====
    def test_xml_output_is_valid(self):
        # Подготовка
        models = [self.nomenclature1]
        instance = self.factory.create("xml")

        # Действие
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        ET.fromstring(result)
        path = self.save_to_file(result, "nomenclature.xml")

        # Проверки
        self.assertTrue(os.path.exists(path))

    # ==== Фабрика создаёт все форматы корректно ====
    def test_factory_creates_all_formats(self):
        # Подготовка
        models = [self.nomenclature1, self.nomenclature2]

        for fmt in self.available_formats:
            with self.subTest(format=fmt):
                instance = self.factory.create(fmt)
                # Действие
                result = instance.build(models)
                if isinstance(result, list):
                    result = "".join(str(r) for r in result)
                # Проверки
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)

    # ==== Проверка JSON для группы ====
    def test_build_group_json_contains_group_name(self):
        # Подготовка
        instance = self.factory.create("json")
        models = [self.group]

        # Действие
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        parsed = json.loads(result)

        # Проверки
        self.assertEqual(parsed[0]["name"], "Основная группа")

    # ==== Проверка JSON для единицы измерения ====
    def test_build_unit_json_contains_unit_data(self):
        # Подготовка
        instance = self.factory.create("json")
        models = [self.unit]

        # Действие
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        parsed = json.loads(result)

        # Проверки
        self.assertEqual(parsed[0]["name"], "Штука")
        self.assertEqual(parsed[0]["value"], 1)

    # ==== Проверка JSON для рецепта ====
    def test_build_recipe_json_contains_recipe_data(self):
        # Подготовка
        instance = self.factory.create("json")
        models = [self.recipe]

        # Действие
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        parsed = json.loads(result)

        # Проверки
        self.assertEqual(parsed[0]["name"], "Рецепт 1")


if __name__ == "__main__":
    unittest.main()
