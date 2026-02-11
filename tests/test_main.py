import pytest
from src.main import Product, Category, Smartphone, LawnGrass
from unittest.mock import patch


def test_product(fixture_product):
    """тестируем класс Product"""
    product1 = fixture_product
    assert product1.name == "Samsung Galaxy S23 Ultra"
    assert product1.description == "256GB, Серый цвет, 200MP камера"
    assert product1.price == 180000.0
    assert product1.quantity == 5


def test_product_raises():
    with pytest.raises(ValueError):
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 0)


def test_new_product(fixture_product, fixture_category):
    category1 = fixture_category
    new_product = Product.new_product(
        {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
         "quantity": 15}, category1)
    assert new_product.name == 'Samsung Galaxy S23 Ultra'
    assert new_product.description == '256GB, Серый цвет, 200MP камера'
    assert new_product.price == 180000.0
    assert new_product.quantity == 20

    new_product = Product.new_product(
        {"name": "Samsung Galaxy S230 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 380000.0,
         "quantity": 1}, category1)

    assert new_product.name == 'Samsung Galaxy S230 Ultra'
    assert new_product.description == '256GB, Серый цвет, 200MP камера'
    assert new_product.price == 380000.0
    assert new_product.quantity == 1


def test_product_mystical_methods(fixture_product):
    product1 = fixture_product
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    assert str(product1) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток:5 шт."
    assert product1 + product2 == 2580000.0


def test_category(fixture_category):
    """тестируем класс Category"""
    category = fixture_category
    assert category.products == ['Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток:5 шт.',
                                 'Iphone 15, 210000.0 руб. Остаток:8 шт.',
                                 'Xiaomi Redmi Note 11, 31000.0 руб. Остаток:14 шт.']
    assert category.category_count == 1
    assert category.product_count == 3
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category.add_product(product4)
    assert category.products == ['Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток:5 шт.',
                                 'Iphone 15, 210000.0 руб. Остаток:8 шт.',
                                 'Xiaomi Redmi Note 11, 31000.0 руб. Остаток:14 шт.',
                                 '55" QLED 4K, 123000.0 руб. Остаток:7 шт.']
    assert str(category) == "Смартфоны, количество продуктов: 34 шт."


def test_smartphone(fixture_smartphone):
    smartphone1 = fixture_smartphone
    assert smartphone1.name == "Samsung Galaxy S23 Ultra"
    assert smartphone1.description == "256GB, Серый цвет, 200MP камера"
    assert smartphone1.price == 180000.0
    assert smartphone1.quantity == 5
    assert smartphone1.efficiency == 95.5
    assert smartphone1.model == "S23 Ultra"
    assert smartphone1.memory == 256
    assert smartphone1.color == "Серый"


def test_lawngrass(fixture_lawngrass):
    grass1 = fixture_lawngrass
    assert grass1.name == "Газонная трава"
    assert grass1.description == "Элитная трава для газона"
    assert grass1.price == 500.0
    assert grass1.quantity == 20
    assert grass1.country == "Россия"
    assert grass1.germination_period == "7 дней"
    assert grass1.color == "Зеленый"


def test_product_add(fixture_lawngrass, fixture_smartphone):
    smartphone1 = fixture_smartphone
    grass1 = fixture_lawngrass
    with pytest.raises(TypeError):
        var = (smartphone1 + grass1)


def test_category_add_product(fixture_category):
    category1 = fixture_category
    with pytest.raises(TypeError):
        category1.add_product("Not a product")


def test_category_middle_price(fixture_category, capsys):
    category1 = fixture_category
    category_empty = Category("Пустая категория", "Категория без продуктов", [])

    assert category1.middle_price() == 140333.33
    assert category_empty.middle_price() == 0


def test_category_middle_price_exceptions(capsys):
    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    category_empty.middle_price()
    captured = capsys.readouterr()
    assert 'division by zero: Список товаров пустой' in captured.out



def test_set_price_zero_or_negative(fixture_product, capsys):
    fixture_product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert fixture_product.price == 180000.0

    fixture_product.price = -10
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert fixture_product.price == 180000.0


@patch("builtins.input", return_value='y')
def test_set_price_decrease_confirm(mock_input, fixture_product):
    fixture_product.price = 80.0
    assert fixture_product.price == 80.0


@patch("builtins.input", return_value='n')
def test_set_price_decrease_cancel(mock_input, fixture_product):
    fixture_product.price = 90.0
    assert fixture_product.price == 180000.0  # осталась старая цена
