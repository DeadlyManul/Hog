"""Функции симулурующие бросаемые кости.

Функция dice (кость) не принимает аргументов и возвращает число от 1 до n
(включительно), где n -- число граней у кости.

Типы кости:

 -  Настоящая кость, это означает, что она выдает возможные значения с равной вероятностью.
    Примеры: four_sided, six_sided

 -  Для тестирования функций, использующих dice (кость), детерминированная тестовая кость
    циклически возвращает элементы последовательности заданной аргументами функции make_test_dice.
"""

from random import randint

def make_fair_dice(sides):
    """Возвращает настоящую кость с SIDES гранями."""
    assert type(sides) == int and sides >= 1, 'Неверное значение граней'
    def dice():
        return randint(1,sides)
    return dice

four_sided = make_fair_dice(4)
six_sided = make_fair_dice(6)

def make_test_dice(*outcomes):
    """Возвращает детерминированную циклическую кость (цикл по OUTCOMES).

    >>> dice = make_test_dice(1, 2, 3)
    >>> dice()
    1
    >>> dice()
    2
    >>> dice()
    3
    >>> dice()
    1
    >>> dice()
    2

    Эта функция использует синтаксис выходящий за рамки курса.
    Лучший способ понять этот синтаксис -- почитать документацию и примеры.
    """
    assert len(outcomes) > 0, 'Нужно указать последовательность фиксированных результатов'
    for o in outcomes:
        assert type(o) == int and o >= 1, 'Результат должен быть положительным и целым'
    index = len(outcomes) - 1
    def dice():
        nonlocal index
        index = (index + 1) % len(outcomes)
        return outcomes[index]
    return dice
