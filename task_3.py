from datetime import datetime
from functools import wraps


# Можно было импортировать декоратор logger из модуля task_2.py.
# Но он вставлен сюда целиком чтобы была возможность менять параметр записи 'a' или 'w'
# в этом модуле.
def logger(path):
    # Присваиваем переменной logfile значение path (название файла) из кортежа paths
    logfile = path
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            res_write = [f'Дата и время вызова функции: {datetime.now()}\n',
                         f'Функция: "{old_function.__name__}"\n',
                         f'Аргументы функции: args: {args}, kwargs: {kwargs}\n',
                         f'Возвращаемое значение: result: {result}\n\n']
            # Открываем файл path из кортежа paths для записи с параметром 'a' (доп запись в конец)
            # Можно вместо параметра 'a' вставить 'w', тогда файл 'task_3.log' не заполняется
            # повторяющимися данными при каждом запуске программы
            with open(logfile, 'w', encoding='utf-8') as file:
                # Записываем в него требуемые данные
                for res in res_write:
                    file.write(res)
            return result
        return new_function

    return __logger

@logger('task_3.log')
class FlatIterator:

    def __init__(self, list_of_list):
        # Определяет атрибут для хранения списка списков
        self.list_of_list = list_of_list

    def __iter__(self):
        # Индекс списка внутри общего списка
        self.list_num = 0
        # Индекс элемента списка
        self.num_in_list = -1
        return self

    def __next__(self):
        # Индекс элемента списка увеличиваем на 1, первый индекс будет 0
        self.num_in_list += 1
        # Проверяем, что индекс элемента списка не сравнялся с длинной списка
        if self.num_in_list == len(self.list_of_list[self.list_num]):
            # Если сравнялся - переходим к следующему списку внутри общего списка
            self.list_num += 1
            # Сбрасываем индекс элемента списка до 0
            self.num_in_list = 0
            # Если номер списка сравнялся с длинной общего списка останавливаем итерацию
            if self.list_num == len(self.list_of_list):
                raise StopIteration
        # Присваиваем переменной item значение элемента списка по
        # индексу списка и индексу элемента списка и возвращаем ее
        item = self.list_of_list[self.list_num][self.num_in_list]
        return item


# Функция, сравнивающая результат, возвращенный FlatIterator с эталонным
def test_1(lists):
    # Исходный список списков
    list_of_lists_1 = lists
    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]):
        assert flat_iterator_item == check_item
    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

if __name__ == '__main__':

    # Исходный список списков
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    # Вызываем итератор FlatIterator
    print(f'Вызываем итератор ********************************')
    for item in FlatIterator(list_of_lists_1):
        print(item)

    # Списочное выражение по итератору
    print()
    flat_list_iter = [item for item in FlatIterator(list_of_lists_1)]
    print('list comprehension  по итератору *****************')
    print(flat_list_iter)

    # Вызываем проверочную функцию по итераторам
    test_1(list_of_lists_1)
    print()