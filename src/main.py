from typing import Optional
from abc import ABC, abstractmethod


# Миксин для логирования
class InitLoggerMixin:
    def __init__(self, *args, **kwargs):
        # __repr__ используется для красивого и подробного вывода
        print(f'Создан объект: {self.__repr__()} с args={args}, kwargs={kwargs}')
        super().__init__(*args, **kwargs)

    def __repr__(self):
        # Подробное представление объекта для отладки
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f"<{self.__class__.__name__}({attrs})>"


# Абстрактный базовый класс
class BaseProduct(ABC):
    name: str
    description: str
    __price: float
    quantity: int

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price > 0:
            if self.price > new_price:
                user_confirm_price_reduction = input("\nConfirm the price reduction (y/n)\n") == 'y'
                if user_confirm_price_reduction:
                    self.__price = new_price
            else:
                self.__price = new_price
        else:
            print('Цена не должна быть нулевая или отрицательная')


class Product(InitLoggerMixin, BaseProduct):
    """Класс для определения продуктов"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Конструктор класса"""
        if quantity == 0:
            raise ValueError('Товар с нулевым количеством не может быть добавлен')
        super().__init__(name, description, price, quantity)

    def __str__(self) -> str:
        return f'{self.name}, {self.price} руб. Остаток:{self.quantity} шт.'

    def __add__(self, other) -> float:
        """Возвращает сумму стоимости (цена * количество) двух продуктов"""
        if type(self) is not type(other):
            raise TypeError(f"Нельзя складывать {type(self).__name__} и {type(other).__name__}")
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_data: dict, category: 'Category'):
        """
        Создает новый продукт или обновляет существующий в переданной категории.
        """
        name = product_data.get("name")
        description = product_data.get("description", "")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)
        for existing_product in category.get_product_list():
            if existing_product.name == name:
                # Обновляем существующий продукт
                existing_product.quantity += quantity
                existing_product.price = max(existing_product.price, price)
                return existing_product

        # Если товара не было — создаём и добавляем в категорию
        new_prod = cls(name, description, price, quantity)
        category.add_product(new_prod)
        return new_prod

    # @property
    # def price(self):
    #     """Возвращает цену"""
    #     return self.__price
    #
    # @price.setter
    # def price(self, new_price: float):
    #     """Проверяет на снижение цены продукта и устанавливает новую"""
    #     if new_price > 0:
    #         if self.price > new_price:
    #             user_confirm_price_reduction = input("\nConfirm the price reduction (y/n)\n") == 'y'
    #             if user_confirm_price_reduction:
    #                 self.__price = new_price
    #         else:
    #             self.__price = new_price
    #     else:
    #         print('Цена не должна быть нулевая или отрицательная')


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, efficiency: float, model: str,
                 memory: int,
                 color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, country: str, germination_period: str,
                 color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс для определения категорий продуктов"""
    __name: str = ''
    __description: str = ''
    __products: list = []
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Optional[list[Product]] = None):
        """Конструктор класса Category"""
        self.__name = name
        self.__description = description
        self.__products = products or []
        self.category_count += 1
        self.product_count += len(products)

    def __str__(self) -> str:
        all_product_count_in_category = sum([product.quantity for product in self.__products])
        return f'{self.__name}, количество продуктов: {all_product_count_in_category} шт.'

    def middle_price(self):
        try:
            all_prices = [product.price for product in self.__products]
            avg_price = sum(all_prices) / len(all_prices)
            return round(avg_price, 2)
        except ZeroDivisionError as e:
            print(f'{e}: Список товаров пустой')
            return 0

    def add_product(self, new_product_of_category: Optional[Product]):
        """Добавляет продукт к категории"""
        if not isinstance(new_product_of_category, Product):
            raise TypeError
        self.__products.append(new_product_of_category)
        self.product_count += 1

    @property
    def products(self) -> list:
        """Возвращает Список продуктов list[Формат f строки]"""
        result = [str(product) for product in self.__products]
        return result

    def get_product_list(self):
        """Возвращает простой список продуктов list"""
        return self.__products
