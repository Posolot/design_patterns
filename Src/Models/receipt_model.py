from Src.Core.entity_model import entity_model
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator, argument_exception

"""
Модель рецепта
"""


class receipt_model(entity_model):
    _number_of_servings: int = 1
    _ingredients: list[nomenclature_model] = []
    _steps: list[str] = []
    _cooking_length: range_model = range_model()

    def __init__(self, _number_of_servings: int = 1, _ingredients: list[nomenclature_model] = [],
                 _steps: list[str] = [],
                 _cooking_length: range_model = range_model()):
        super().__init__()
        self.number_of_servings = _number_of_servings
        self.cooking_length = _cooking_length
        self.ingredients = _ingredients
        self.steps = _steps

    #Количество порций
    @property
    def number_of_servings(self):
        return self.__number_of_servings

    @number_of_servings.setter
    def number_of_servings(self, value: int):
        validator.validate(value, int)
        if value <= 0:
            raise argument_exception("Неверный аргумент!")
        self.__number_of_servings = value

    #Время приготовления
    @property
    def cooking_length(self):
        return self._cooking_length

    @cooking_length.setter
    def cooking_length(self, value: range_model):
        validator.validate(value, range_model)
        self._cooking_length = value

    #Список ингредиентов
    @property
    def ingredients(self):
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value: list):
        validator.validate(value, list)
        self.__ingredients = value

    #Пошаговый список инструкций
    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value: list):
        validator.validate(value, list)
        self._steps = value