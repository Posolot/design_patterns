from Src.Core.validator import validator
from Src.Core.abstract_model import abstract_model
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model


class nomenclature_model(abstract_model):
    _full_name: str = ""
    _group: group_model = group_model()
    _range: range_model = range_model()

    def __init__(self, _name: str = "", _group: group_model = group_model(), _range: range_model = range_model()):
        super().__init__(_name)
        self.group = _group
        self.range = _range
    """
    Полное имя(255 символов)
    """
    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        validator.validate(value, str, 255)
        self._full_name = value.strip()

    """
    Группа номенклатуры
    """
    @property
    def nomenclature_group(self):
        return self._group

    @nomenclature_group.setter
    def nomenclature_group(self, value: group_model):
        validator.validate(value, group_model)
        self._group = value

    """
    Единица измерения
    """
    @property
    def unit_measure(self):
        return self._range

    @unit_measure.setter
    def unit_measure(self, value: range_model):
        validator.validate(value, range_model)
        self._range = value

