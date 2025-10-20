from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model
class start_service:
    _repo: reposity = reposity()

    def __init__(self):
        self._repo.data[reposity.range_key()] = []
        self._repo.data[reposity.group_key()] = []
        self._repo.data[reposity.nomenclature_key()] = []

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance
    # Создание эталона единиц измерения

    def _default_create_ranges(self):
        self._repo.data[reposity.range_key()].append(range_model.create_gramm())
        self._repo.data[reposity.range_key()].append(range_model.create_kill())

    # Создать эталон групп
    def _default_create_group(self):
        self._repo.append(reposity.group_key(), group_model())

    # Создать эталон номенклатур
    def _default_create_nomenclature(self):
        etalon = nomenclature_model()
        etalon.name = "Название группы номенклатуры"
        etalon.range_model = range_model.create_gramm()
        self._repo.append(reposity.nomenclature_key(), etalon)

    # Создание эталона рецептов
    def _create_receipts(self):
        my_receipt = receipt_model()
        another_receipt = receipt_model()

        my_receipt.name = "ОМЛЕТ С МОЛОКОМ И ЗЕЛЕНЬЮ"
        another_receipt.name = "ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ"

        my_receipt.number_of_servings = 3
        another_receipt.number_of_servings = 10

        my_receipt.cooking_length = range_model(_name="мин", _value=10)
        another_receipt.cooking_length = range_model(_name="мин", _value=20)
        my_receipt.ingredients = [
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
        another_receipt.ingredients = [
            nomenclature_model(
                _group=group_model(_name="Пшеничная мука"),
                _range=range_model(_name="гр", _value=100)
            ),
            nomenclature_model(
                _group=group_model(_name="Сахар"),
                _range=range_model(_name="гр", _value=80)
            ),
            nomenclature_model(
                _group=group_model(_name="Сливочное масло"),
                _range=range_model(_name="гр", _value=70)
            ),
            nomenclature_model(
                _group=group_model(_name="Яйца"),
                _range=range_model(_name="шт", _value=1)
            ),
            nomenclature_model(
                _group=group_model(_name="Ванилин(щепотка)"),
                _range=range_model(_name="гр", _value=5)
            )
        ]

        my_receipt.steps = [
            '''Подготовьте все ингредиенты для омлета.''',
            ''' Разбейте яйца в миску и слегка взбейте венчиком или вилкой.''',
            '''Влейте молоко и хорошо перемешайте до однородности.''',
            '''На сковороде растопите сливочное масло на среднем огне.''',
            '''Вылейте яично-молочную смесь на сковороду.''',
            '''Готовьте под крышкой на медленном огне 5–7 минут, пока омлет не схватится.''',
            '''Посыпьте сверху измельчённой зеленью и подавайте горячим.'''
        ]
        another_receipt.steps = [
            '''Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.''',
            '''Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.''',
            '''Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.''',
            '''Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.''',
            '''Всыпьте муку, добавьте ванилин.''',
            '''Перемешайте массу венчиком до состояния гладкого однородного теста.''',
            '''Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше.''',
            '''Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик.'''
        ]

        self._repo.receipts.append(my_receipt)
        self._repo.receipts.append(another_receipt)

    # Функция для создания эталонов Номенклатуре, Единицам измерения, Группам
    def _create(self):
        self._default_create_ranges()
        self._default_create_group()
        self._default_create_nomenclature()
    """
    Стартовый набор данных
    """

    def data(self):
        return self._repo.data

    def receipts(self):

        return self._repo.receipts
    """
    Основной метод для генерации эталонных данных
    """

    def start(self):
        self._create()
        self._create_receipts()

