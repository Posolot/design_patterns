"""
Исключение при проверки аргумента
"""
from typing import Optional, Any, Union, Type, List, Tuple

class argument_exception(Exception):
    pass


"""
Исключение при выполнении бизнес операции
"""


class operation_exception(Exception):
    pass


"""
Набор проверок данных
"""


class validator:

    @staticmethod
    def validate(value, type_, len_=None,strong_check=False):
        """
            Валидация аргумента по типу и длине
        Args:
            value (any): Аргумент
            type_ (object): Ожидаемый тип
            len_ (int): Максимальная длина
        Raises:
            arguent_exception: Некорректный тип
            arguent_exception: Неулевая длина
            arguent_exception: Некорректная длина аргумента
        Returns:
            True или Exception
        """

        if value is None:
            raise argument_exception("Пустой аргумент")

        # Проверка типа
        if not isinstance(value, type_):
            raise argument_exception(f"Некорректный тип!\nОжидается {type_}. Текущий тип {type(value)}")

        # Проверка аргумента
        if len(str(value).strip()) == 0:
            raise argument_exception("Пустой аргумент")

        if len_ is not None and len(str(value).strip()) > len_:
            if strong_check and len(str(value).strip()) != len_:
                raise argument_exception(f"Некорректная длина аргумента,длина должна быть равна {len_}")
            raise argument_exception("Некорректная длина аргумента")
        return True

    @staticmethod
    def is_list(
            value: list,
            field_name: str,
            strong_check: bool = False,
    ) -> bool:
        return validator.validate(value, list, None)

    def is_list_of(
            value: list,
            list_: list,
            types: Union[Type, List[Type], Tuple[Type]],
            field_name: str,
            list_name: str,
            could_item_be_none: bool = False
    ) -> bool:
        for lst, name in [(value, field_name), (list_, list_name)]:
            validator.is_list(lst, name)
            for item in lst:
                validator.validate(item, types, f"item of {name}", could_item_be_none)
        return True

    def is_list_of_same(
            list_: list,
            list_name: str,
            could_be_empty: bool = False,
            could_item_be_none: bool = False
    ) -> bool:
        validator.is_list(list_, list_name)

        if not list_:
            if could_be_empty:
                return True
            raise Exception(f"List '{list_name}' can't be empty")

        first_type = type(list_[0])
        for i, item in enumerate(list_):
            if item is None and could_item_be_none:
                continue
            if not isinstance(item, first_type):
                raise Exception(
                    f"#{i + 1} item must be '{first_type.__name__}' like "
                    f"first item in list, not '{type(item).__name__}'"
                )

        return True