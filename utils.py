import string
import random


# Функция генерации случайного ID сессии(6 значное значение)
def generate_session_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# Словарь для хранения сессий, нужен для фильтрации входящих сообщений, проверка и присвоению значений будет выполняться
# в функции handle_join через БД
sessions = {}
