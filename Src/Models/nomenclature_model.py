from Src.Core.validator import validator
from Src.Core.abstract_model import abstact_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.unit_measure_model import unit_measure_model


class nomenclature_model(abstact_model):
    _full_name: str = ""
    _nomenclature_group: nomenclature_group_model = None
    _unit_measure: unit_measure_model = None

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        validator.validate(value, str, 255)
        self._full_name = value.strip()

    @property
    def nomenclature_group(self):
        return self._nomenclature_group

    @nomenclature_group.setter
    def nomenclature_group(self, value: nomenclature_group_model):
        validator.validate(value, nomenclature_group_model)
        self._nomenclature_group = value

    @property
    def unit_measure(self):
        return self._unit_measure

    @unit_measure.setter
    def unit_measure(self, value: unit_measure_model):
        validator.validate(value, unit_measure_model)
        self._unit_measure = value

