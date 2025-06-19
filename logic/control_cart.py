import json
import os
from app_store.models import DATABASE
from django.contrib.auth import get_user

PATH_CART = 'cart.json'  # Путь до файла корзины


def view_in_cart(username: str = '') -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое корзины cart.json, если пользователя с именем username нет в корзине, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'cart.json'
    """
    empty_user_cart = {'products': []}  # Пустая корзина для пользователя

    if os.path.exists(PATH_CART):  # Если файл с корзиной существует
        with open(PATH_CART, encoding='utf-8') as f:  # Открываем файл
            cart = json.load(f)  # Считываем корзину
            if username not in cart:  # Если пользователя нет в корзине, то создаем запись с пустой корзиной для него
                cart[username] = empty_user_cart
    else:  # Если файла с корзиной нет
        cart = {username: empty_user_cart}

    # Запись словаря cart в cart.json
    # with open(PATH_CART, mode='w', encoding='utf-8') as f:  # Создаём файл и записываем корзину
    #     json.dump(cart, f)

    return cart  # Возвращаем содержимое корзины


def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    # TODO Помните, что у вас есть уже реализация просмотра корзины,
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    if id_product in DATABASE:
        if id_product in cart['products']:
            cart['products'][id_product] += 1
        elif id_product not in cart['products'] and id_product in DATABASE:
            cart['products'][id_product] = 1
        with open('cart.json', mode='w', encoding='utf-8') as f:
            json.dump(cart_users, f)
        return True
    return False
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # ! Обратите внимание, что в переменной cart находится словарь с ключом products.
    # ! Именно в cart["products"] лежит словарь гдк по id продуктов можно получить число продуктов в корзине.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной cart нужно вызвать
    # ! cart["products"][id_product]
    # ! Далее уже сами решайте как и в какой последовательности дальше действовать.

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то перед тем как его добавить - проверьте есть ли такой id_product товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.

    # TODO Если товар существует, то увеличиваем его количество на 1

    # TODO Не забываем записать обновленные данные cart в 'cart.json'. Так как именно из этого файла мы считываем данные и если мы не запишем изменения, то считать измененные данные не получится.


def remove_from_cart(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.
    # С переменной cart функции remove_from_cart ситуация аналогичная, что с cart функции add_to_cart

    if id_product not in cart['products']:  # TODO Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.
        return False
    if id_product in cart['products']:
        cart['products'].pop(id_product)
        with open('cart.json', mode='w', encoding='utf-8') as f:
            json.dump(cart_users, f)
    return True
    # TODO Если существует товар, то удаляем ключ 'id_product' у cart['products'].

    # TODO Не забываем записать обновленные данные cart в 'cart.json'



if __name__ == "__main__":
    # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
    if os.path.exists('cart.json'):  # Если файл существует
        os.remove('cart.json')  # Удаляем корзину

    print('Проверяем корзину', "Ответ:     {'': {'products': {}}}", f'Результат: {view_in_cart()}\n', sep='\n')
    print('Добавляем товар с id = 1', 'Ответ:     True', f'Результат: {add_to_cart("1")}\n', sep='\n')
    print('Добавляем товар с id = 0', 'Ответ:     False', f'Результат: {add_to_cart("0")}\n', sep='\n')
    print('Добавляем товар с id = 1', 'Ответ:     True', f'Результат: {add_to_cart("1")}\n', sep='\n')
    print('Добавляем товар с id = 2', 'Ответ:     True', f'Результат: {add_to_cart("2")}\n', sep='\n')
    print('Проверяем корзину', "Ответ:     {'': {'products': {'1': 2, '2': 1}}}", f'Результат: {view_in_cart()}\n', sep='\n')
    print('Удаляем товар с id = 0', "Ответ:     False", f'Результат: {remove_from_cart("0")}\n', sep='\n')
    print('Удаляем товар с id = 1', "Ответ:     True", f'Результат: {remove_from_cart("1")}\n', sep='\n')
    print('Проверяем корзину', "Ответ:     {'': {'products': {'2': 1}}}", f'Результат: {view_in_cart()}\n', sep='\n')

    if os.path.exists('cart.json'):  # Если файл существует
        os.remove('cart.json')  # Удаляем корзину
