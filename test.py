from main import init, fill, show, db, ORDERS, CLIENTS
from peewee import *
from os.path import exists

# проверка что база данных есть
def test_init():
    assert exists("lab1.db")

# проверка что есть нужные столбцы
def test_columns():
    assert 'NAME' in Clients._meta.fields
    assert 'CITY' in Clients._meta.fields
    assert 'ADDRESS' in Clients._meta.fields
    assert 'CLIENT' in Orders._meta.fields
    assert 'DATE' in Orders._meta.fields
    assert 'AMOUNT' in Orders._meta.fields
    assert 'DESCRIPTION' in Orders._meta.fields

# проверка что в базе данных есть 10 записей
def test_fill():
    assert CLIENTS.select().count() >= 10
