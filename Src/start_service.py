import os
import json
from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model


class start_service:
    _repo: reposity = reposity()

    def __init__(self):
        # Инициализируем контейнеры (списки) в репозитории
        self._repo.data[reposity.range_key()] = []
        self._repo.data[reposity.group_key()] = []
        self._repo.data[reposity.nomenclature_key()] = []

    # Singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    def _default_create_ranges(self):
        self._repo.data[reposity.range_key()].append(range_model.create_gramm())
        self._repo.data[reposity.range_key()].append(range_model.create_kill())

    def _default_create_group(self):
        self._repo.append(reposity.group_key(), group_model())

    def _default_create_nomenclature(self):
        etalon = nomenclature_model()
        etalon.name = "Название группы номенклатуры"
        etalon.range_model = range_model.create_gramm()
        self._repo.append(reposity.nomenclature_key(), etalon)

    def get_models(self, key: str) -> list:
        """
        Возвращает список моделей по ключу в едином формате.
        Поддерживает как dict (ключ->model), так и list (список моделей).
        """
        container = self._data.get(key, [])
        if isinstance(container, dict):
            return list(container.values())
        if isinstance(container, list):
            return list(container)
        try:
            return list(container)
        except TypeError:
            return []
    def _create_receipts(self):
        # оставляем этот метод без изменений (пример ручного создания рецептов)
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
            "Подготовьте все ингредиенты для омлета.",
            "Разбейте яйца в миску и слегка взбейте венчиком или вилкой.",
            "Влейте молоко и хорошо перемешайте до однородности.",
            "На сковороде растопите сливочное масло на среднем огне.",
            "Вылейте яично-молочную смесь на сковороду.",
            "Готовьте под крышкой на медленном огне 5–7 минут, пока омлет не схватится.",
            "Посыпьте сверху измельчённой зеленью и подавайте горячим."
        ]

        another_receipt.steps = [
            "Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты.",
            "Масло положите в сотейник с толстым дном. Растопите его на маленьком огне.",
            "Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения.",
            "Добавьте в масло яйцо. Перемешайте до однородности.",
            "Всыпьте муку, добавьте ванилин.",
            "Перемешайте массу венчиком до состояния гладкого однородного теста.",
            "Разогрейте вафельницу. Выпекайте до золотистого цвета."
        ]

        self._repo.receipts.append(my_receipt)
        self._repo.receipts.append(another_receipt)

    # Создание эталонов (как раньше)
    def _create(self):
        self._default_create_ranges()
        self._default_create_group()
        self._default_create_nomenclature()

    # Геттеры
    def data(self):
        return self._repo.data

    def receipts(self):
        return self._repo.receipts

    # Основной метод старта (ручной)
    def start(self):
        self._create()
        self._create_receipts()

    def load_from_file(self, file_path: str) -> bool:
        """
        Загружает эталонные данные из JSON-файла и наполняет репозиторий.
        Ожидаемая структура файла: { "models": { "measure_units": [...], "nomenclature_groups": [...],
                                                 "nomenclatures": [...], "recipes": [...] } }
        """
        if not file_path or not os.path.exists(file_path):
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
        except Exception:
            return False

        models = payload.get("models", {})
        if not isinstance(models, dict):
            return False

        # Быстрые lookup-словари, чтобы не создавать дубликаты
        ranges_by_name = {}
        groups_by_name = {}
        nomen_by_name = {}

        for mu in models.get("measure_units", []):
            name = mu.get("name")
            coeff = mu.get("coefficient", None)
            if not name:
                continue
            rm = range_model(_name=name, _value=coeff)
            self._repo.data[reposity.range_key()].append(rm)
            ranges_by_name[name] = rm

        for g in models.get("nomenclature_groups", []):
            name = g.get("name")
            if not name:
                continue
            gm = group_model(_name=name)
            self._repo.data[reposity.group_key()].append(gm)
            groups_by_name[name] = gm


        for n in models.get("nomenclatures", []):
            name = n.get("name")
            group_name = n.get("group")
            mu_name = n.get("measure_unit")

            nm = nomenclature_model()
            if name:
                nm.name = name

            # group
            if group_name:
                if group_name in groups_by_name:
                    nm.group = groups_by_name[group_name]
                else:
                    gm = group_model(_name=group_name)
                    self._repo.data[reposity.group_key()].append(gm)
                    groups_by_name[group_name] = gm
                    nm.group = gm

            # range / measure unit
            if mu_name:
                if mu_name in ranges_by_name:
                    nm.range_model = ranges_by_name[mu_name]
                else:
                    rm = range_model(_name=mu_name, _value=None)
                    self._repo.data[reposity.range_key()].append(rm)
                    ranges_by_name[mu_name] = rm
                    nm.range_model = rm

            # сохраняем номенклатуру в репозитории и lookup
            self._repo.append(reposity.nomenclature_key(), nm)
            if getattr(nm, "name", None):
                nomen_by_name[nm.name] = nm


        for r in models.get("recipes", []):
            rec = receipt_model()
            rec.name = r.get("name")
            rec.description = r.get("description")
            rec.number_of_servings = r.get("portions") or r.get("number_of_servings")

            cooking_time = r.get("cooking_time") or r.get("cooking_length")
            rec.cooking_length = range_model(_name="мин", _value=cooking_time) if cooking_time is not None else None

            ing_list = []
            for ing in r.get("ingredients", []):
                ing_name = ing.get("nomenclature")
                mu_name = ing.get("measure_unit")
                count = ing.get("count")

                # Если номенклатура уже есть в репозитории — используем её как основу
                if ing_name and ing_name in nomen_by_name:
                    base = nomen_by_name[ing_name]
                    nm_for_recipe = nomenclature_model()
                    nm_for_recipe.name = base.name
                    nm_for_recipe.group = getattr(base, "group", None)
                    # предпочитаем указанную в ингредиенте measure_unit, иначе базовую
                    if mu_name and mu_name in ranges_by_name:
                        nm_for_recipe.range_model = ranges_by_name[mu_name]
                    else:
                        nm_for_recipe.range_model = getattr(base, "range_model", None)
                else:
                    # создаём локальную номенклатуру для рецепта
                    grp = None
                    if ing.get("group"):
                        grp = groups_by_name.get(ing.get("group")) or group_model(_name=ing.get("group"))
                        groups_by_name.setdefault(getattr(grp, "name", None), grp)
                    else:
                        # fallback: если нет group — попробуем взять группу из nomen_by_name (по имени) или не указывать
                        grp = None

                    rmodel = ranges_by_name.get(mu_name) or range_model(_name=mu_name, _value=count)
                    nm_for_recipe = nomenclature_model(_group=grp, _range=rmodel)
                    if ing_name:
                        nm_for_recipe.name = ing_name

                # сохранить количество ингредиента, если модель это поддерживает (необязательно)
                try:
                    setattr(nm_for_recipe, "count", count)
                except Exception:
                    pass

                ing_list.append(nm_for_recipe)

            rec.ingredients = ing_list
            rec.steps = r.get("steps", [])
            self._repo.receipts.append(rec)

        return True

    @property
    def repo(self):
        return self._repo
