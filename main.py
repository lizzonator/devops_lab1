# Программа при вызове без параметров выводит справку.
# С параметром init - создаёт базу данных (если её нет, а если есть - удаляет базу и создаёт заново).
# С параметром fill - заполняет тестовыми данными, минимум 10 строк в каждой таблице.
# С параметром show [tablename] - показывает содержимое таблицы в виде набора строк с разделителем-табуляцией между колонками.

from peewee import *    
import argparse

db = SqliteDatabase("lab1.db")

class CLIENTS(Model):
    NAME = CharField()
    CITY = CharField()
    ADDRESS = CharField()

    class Meta:
        database = db
        table_name = "Clients"

class ORDERS(Model):
    CLIENT = ForeignKeyField(CLIENTS)
    DATE = DateField()
    AMOUNT = IntegerField()
    DESCRIPTION = CharField()

    class Meta:
        database = db
        table_name = "Orders"

clients_data = [
    {"NAME": "Владимир Петров",     "CITY": "Москва",           "ADDRESS": "ул. Космонавтов, д. 73"},
    {"NAME": "Александра Смирнова", "CITY": "Санкт-Петербург",  "ADDRESS": "ул. Чехова, д. 51"},
    {"NAME": "София Иванова",       "CITY": "Новосибирск",      "ADDRESS": "ул. Лермонтова, д. 12"},
    {"NAME": "Татьяна Прокопенко",  "CITY": "Томск",            "ADDRESS": "ул. Пушкина, д. 68"},
    {"NAME": "Алиса Новикова",      "CITY": "Красноярск",       "ADDRESS": "ул. Ленина, д. 32"},
    {"NAME": "Максим Алексеев",     "CITY": "Уфа",              "ADDRESS": "ул. Гагарина, д. 88"},
    {"NAME": "Иван Тихонов",        "CITY": "Владивосток",      "ADDRESS": "ул. Нефтяников, д. 50"},
    {"NAME": "Людмила Баранова",    "CITY": "Хабаровск",        "ADDRESS": "ул. Строителей, д. 48"},
    {"NAME": "Андрей Зайцев",       "CITY": "Пермь",            "ADDRESS": "ул. Первопроходцев, д. 81"},
    {"NAME": "Сергей Рыбаков",      "CITY": "Екатеринбург",     "ADDRESS": "ул. Пролетарская, д. 3"},
]

orders_data = [
    {"CLIENT": None, "DATE": "2024-03-03", "AMOUNT": 2,     "DESCRIPTION": "Подушка", },
    {"CLIENT": None, "DATE": "2024-03-02", "AMOUNT": 3,     "DESCRIPTION": "Контейнер", },
    {"CLIENT": None, "DATE": "2024-03-01", "AMOUNT": 10,    "DESCRIPTION": "Ручка", },
    {"CLIENT": None, "DATE": "2024-02-29", "AMOUNT": 6,     "DESCRIPTION": "Носки", },
    {"CLIENT": None, "DATE": "2024-02-28", "AMOUNT": 2,     "DESCRIPTION": "Перчатки", },
    {"CLIENT": None, "DATE": "2024-02-27", "AMOUNT": 1,     "DESCRIPTION": "Шапка", },
    {"CLIENT": None, "DATE": "2024-02-26", "AMOUNT": 1,     "DESCRIPTION": "Чехол для смартфона", },
    {"CLIENT": None, "DATE": "2024-02-25", "AMOUNT": 15,    "DESCRIPTION": "Картонная коробка", },
    {"CLIENT": None, "DATE": "2024-02-24", "AMOUNT": 1,     "DESCRIPTION": "Кроссовки", },
    {"CLIENT": None, "DATE": "2024-02-23", "AMOUNT": 1,     "DESCRIPTION": "Рюкзак", },
]

def pretty_print(*args, FIRST=False):
    MAX = 12
    data = []
    for arg in args:
        if len(arg) > MAX:
            data.append(arg[:MAX])
        else:
            data.append(arg + (" " * (MAX - len(arg))))
    print(" | ".join(data))
    if FIRST:
        print("_" * ((MAX + 3) * len(args)))

def init():
    if db.get_tables():
        db.drop_tables([CLIENTS, ORDERS])
    db.create_tables([CLIENTS, ORDERS])

def fill():
    for i in range(10):
        order_data = orders_data[i].copy()
        order_data["CLIENT"] = CLIENTS.create(**clients_data[i])
        ORDERS.create(**order_data)

def show(tablename):
    table = {"orders": ORDERS, "clients": CLIENTS}[tablename]
    pretty_print(*table._meta.sorted_field_names, FIRST=True)
    for i in table.select():
        # print(f"{i.CLIENT} | {i.DATE} | {i.AMOUNT} | {i.DESCRIPTION}")
        pretty_print(
            *tuple(str(getattr(i, field)) for field in table._meta.sorted_field_names)
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
    parser.add_argument("parameter", help="Возможные значения: init, fill, show")
    parser.add_argument("tablename", nargs="?", default="")
    try:
        args = parser.parse_args()
    except SystemExit:
        print("Использование: python3 main.py init/fill/show [tablename]\n\ninit инициализирует базу данных\nfill заполняет базу данных случайными данными\nshow [tablename] показывает таблицу из базы данных")
        quit(1)
    parameter = args.parameter.lower()
    tablename = args.tablename.lower()
    if parameter not in ("init", "fill", "show"):
        parser.error("Возможные значения parameter: init, fill, show")
    if parameter == "show" and tablename not in ("orders", "clients"):
        parser.error("Возможные значения [tablename]: orders, clients")
    args = [tablename] if tablename else []
    db.connect()
    try:
        {"init": init, "fill": fill, "show": show}[parameter](*args)
    finally:
        db.close()