"""Необходимо реализовать декоратор `@strict`
Декоратор проверяет соответствие типов переданных в вызов функции аргументов типам аргументов, объявленным в прототипе функции.
(подсказка: аннотации типов аргументов можно получить из атрибута объекта функции `func.__annotations__` или с помощью модуля `inspect`)
При несоответствии типов бросать исключение `TypeError`
Гарантируется, что параметры в декорируемых функциях будут следующих типов: `bool`, `int`, `float`, `str`
Гарантируется, что в декорируемых функциях не будет значений параметров, заданных по умолчанию"""

from copy import deepcopy

def strict(func):
    def wrapper(*args, **kwargs):
        annotations = deepcopy(func.__annotations__)
        annotations.pop('return')
        errors = []
        for arg_name, arg_cls, arg_value in zip(annotations.keys(), annotations.values(), args):
            if arg_cls is not type(arg_value):
                errors.append(f'arg {arg_name} - must be {arg_cls}, got {type(arg_value)}')
        if errors:
            # можно убрать try-except елси ошибка обрабатывается в другом месте
            # в противном случае, после первого раза все, очевидно, ломается
            try:
                raise TypeError(f'TypeError "{func.__name__}": ' + '; '.join(errors))
            except TypeError as e:
                return e

        return func(*args, **kwargs)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
print(sum_two('aaa', False))