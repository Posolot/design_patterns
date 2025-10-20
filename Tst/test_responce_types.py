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
        self.output_dir = "tests/test_output"
        os.makedirs(self.output_dir, exist_ok=True)

        # Базовые сущности
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

        # Фабрика и доступные форматы
        self.factory = facrtory_entities()
        self.available_formats = ["csv", "json", "markdown", "xml"]

    def save_to_file(self, content, filename):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            if isinstance(content, list):
                f.write("".join(str(c) for c in content))
            else:
                f.write(str(content))
        return path

    # ==== Проверка, что build возвращает строку ====
    def test_build_returns_string_for_all_formats(self):
        models = [self.nomenclature1, self.nomenclature2]
        for fmt in self.available_formats:
            with self.subTest(format=fmt):
                instance = self.factory.create(fmt)
                result = instance.build(models)
                if isinstance(result, list):
                    result = "".join(str(r) for r in result)
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)

    # ==== CSV ====
    def test_csv_contains_headers(self):
        models = [self.nomenclature1, self.nomenclature2]
        instance = self.factory.create("csv")
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        path = self.save_to_file(result, "nomenclature.csv")
        self.assertIn("name", result)
        self.assertIn("unique_code", result)
        self.assertIn("Товар 1", result)
        self.assertTrue(os.path.exists(path))

    # ==== JSON ====
    def test_json_output_is_valid(self):
        models = [self.nomenclature1]
        instance = self.factory.create("json")
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        parsed = json.loads(result)
        self.assertEqual(parsed[0]["name"], "Товар 1")

    # ==== Markdown ====
    def test_markdown_contains_headers(self):
        models = [self.nomenclature1]
        instance = self.factory.create("markdown")
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        # Проверяем наличие заголовков Markdown
        self.assertIn("# Список объектов класса 'nomenclature_model'", result)
        self.assertIn("## 1. Товар 1", result)

    # ==== XML ====
    def test_xml_output_is_valid(self):
        models = [self.nomenclature1]
        instance = self.factory.create("xml")
        result = instance.build(models)
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        ET.fromstring(result)  # Проверка валидности XML
        path = self.save_to_file(result, "nomenclature.xml")
        self.assertTrue(os.path.exists(path))

    # ==== Фабрика создаёт все форматы корректно ====
    def test_factory_creates_all_formats(self):
        models = [self.nomenclature1, self.nomenclature2]
        for fmt in self.available_formats:
            with self.subTest(format=fmt):
                instance = self.factory.create(fmt)
                result = instance.build(models)
                if isinstance(result, list):
                    result = "".join(str(r) for r in result)
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)

    # ==== Проверка JSON для разных сущностей ====
    def test_build_group_json_contains_group_name(self):
        instance = self.factory.create("json")
        result = instance.build([self.group])
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        parsed = json.loads(result)
        self.assertEqual(parsed[0]["name"], "Основная группа")

    def test_build_unit_json_contains_unit_data(self):
        instance = self.factory.create("json")
        result = instance.build([self.unit])
        if isinstance(result, list):
            result = "".join(str(r) for r in result)
        parsed = json.loads(result)
        self.assertEqual(parsed[0]["name"], "Штука")
        self.assertEqual(parsed[0]["value"], 1)



if __name__ == "__main__":
    unittest.main()
