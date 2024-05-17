from main import init, fill, show, db, ORDERS, CLIENTS
from peewee import *
from os.path import exists

# проверка что база данных появляется после инита
def test_init():
    db.connect()
    #init()
    assert exists("lab1.db")
    db.close()

# def test_init_second_time():
#     db.connect()
#     init()
#     assert exists("lab1.db")
#     db.close()

# def test_show_empty():
#     db.connect()
#     for tablename in ("clients", "orders"):
#         show(tablename)
#     db.close()

# проверка что в базе данных есть 10 записей
def test_fill():
    db.connect()
    # for i in range(25):
    #     fill()
    assert CLIENTS.select().count() >= 10
    db.close()

# def test_show():
#     db.connect()
#     for tablename in ("clients", "orders"):
#         show(tablename)
#     db.close()

# дописать проверку что после инита появляются нужные колонки
# def test_columns():
#     db.connect()
#     assert 
