from Src.start_service import start_service
from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.start_service import start_service
import unittest

class test_start(unittest.TestCase):

    # Проверка на создание эталонных данных
    def test_start_service_start_rangeNotEmpty(self):
        # Подготовка
        test = start_service()
        test.start()
        assert len(test.data()) > 0
        assert len(test.data()[reposity.group_key()]) > 0
        assert len(test.data()[reposity.nomenclature_key()]) > 0
        assert len(test.data()[reposity.range_key()]) > 0
        assert range_model.create_kill().base.name == range_model.create_gramm().name
        assert len(test.receipts()) > 0