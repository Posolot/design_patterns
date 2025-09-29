from Src.Core.validator import validator
from Src.Core.abstract_model import abstact_model
from Src.Core.validator import argument_exception


class unit_measure_model(abstact_model):
    _coefficient: int = 0

    def __init__(self, name: str, coefficient: int = 1, base_unit=None):
        super().__init__()
        self._name = name
        validator.validate(coefficient, int)
        if coefficient <= 0:
            raise argument_exception("Коэффициент должен быть положительным")
        self._coefficient = coefficient
        if base_unit is None:
            self.base_unit = self
            self.factor = 1
        else:
            validator.validate(base_unit, unit_measure_model)
            self.base_unit = base_unit
            self.factor = coefficient

    @property
    def coefficient(self):
        return self._coefficient

    @coefficient.setter
    def coefficient(self,value: int):
        validator.validate(value, int)
        self._coefficient = value
