import json
import os
from app_store.models import DATABASE

PATH_WISHLIST = 'wishlist.json'  # Путь до файла корзины


def view_in_wishlist(username: str = '') -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое wishlist.json, если пользователя с именем username нет в корзине, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'wishlist.json'
    """
    empty_user_wishlist= {'products': []}  # Пустое избранное для пользователя

    if os.path.exists(PATH_WISHLIST):  # Если файл с избранным существует
        with open(PATH_WISHLIST, encoding='utf-8') as f:  # Открываем файл
            wishlist = json.load(f)  # Считываем избранное
            if username not in wishlist:  # Если пользователя нет в избранном, то создаем запись с пустым избранным для него
                wishlist[username] = empty_user_wishlist
    else:  # Если файла с избранным нет
        wishlist = {username: empty_user_wishlist}


    return wishlist  # Возвращаем содержимое избранного


def add_to_wishlist(request, id_product: str) -> bool:
    """
    Добавляет продукт в избранное. Если в избранном нет данного продукта, то добавляет его с количеством равное 1.
    Если в избранном есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    # TODO Помните, что у вас есть уже реализация просмотра избранного,
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]
    if id_product in DATABASE:
        if id_product in wishlist['products']:
            wishlist['products'][id_product] += 1
        elif id_product not in wishlist['products'] and id_product in DATABASE:
            wishlist['products'][id_product] = 1
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            json.dump(wishlist_users, f)
        return True
    return False
    # поэтому, чтобы загрузить данные из избранного, не нужно заново писать код.

    # ! Обратите внимание, что в переменной wishlist находится словарь с ключом products.
    # ! Именно в wishlist["products"] лежит словарь гдк по id продуктов можно получить число продуктов в корзине.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной wishlist нужно вызвать
    # ! wishlist["products"][id_product]
    # ! Далее уже сами решайте как и в какой последовательности дальше действовать.

    # TODO Проверьте, а существует ли такой товар в избранном, если нет, то перед тем как его добавить - проверьте есть ли такой id_product товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.

    # TODO Если товар существует, то увеличиваем его количество на 1

    # TODO Не забываем записать обновленные данные wishlist в 'wishlist.json'. Так как именно из этого файла мы считываем данные и если мы не запишем изменения, то считать измененные данные не получится.


def remove_from_wishlist(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из избранного. Если в избранном есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра избранного,
    # поэтому, чтобы загрузить данные из избранного, не нужно заново писать код.
    # С переменной wishlist функции remove_from_wishlist ситуация аналогичная, что с wishlist функции add_to_wishlist

    if id_product not in wishlist['products']:  # TODO Проверьте, а существует ли такой товар в избранном, если нет, то возвращаем False.
        return False
    if id_product in wishlist['products']:
        wishlist['products'].remove(id_product)
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            json.dump(wishlist_users, f)
        return True
    # TODO Если существует товар, то удаляем ключ 'id_product' у wishlist['products'].

    # TODO Не забываем записать обновленные данные wishlist в 'wishlist.json'

