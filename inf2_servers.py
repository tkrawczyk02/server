# Tomasz Krawczyk
from typing import List, Dict
from abc import ABC, abstractmethod
import operator
import unittest

MAX_PRODUCTS = 3


class TooManyProducts(Exception):
    def __init__(self, message):
        super().__init__(message)


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Server(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_all_list(self) -> List[Product]:
        pass

    def filter_products(self, n: int = 3) -> List[Product]:
        temp_products = []
        for element in self.get_all_list():
            if element.name[n - 1].isalpha() and element.name[n].isdigit():
                temp_products.append(element)
                if len(temp_products) > MAX_PRODUCTS:
                    raise TooManyProducts("Too many products found in inventory")
        return sorted(temp_products, key=lambda product: product.price)


class ListServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__()
        self.products = products

    def get_all_list(self) -> List:
        return self.products


class DictServer(Server):
    def __init__(self, products: List[Product]):
        super().__init__()
        self.productsDict = {}
        for i in products:
            self.productsDict[i.name] = i

    def get_all_list(self) -> List[Product]:
        return list(self.productsDict.values())


class Client:
    def __init__(self, server: Server):
        self.server = server

    def calculate_price(self, n: int = 3) -> float:
        try:
            helper_list = self.server.filter_products(n)
        except TooManyProducts:
            return 0.0
        price_sum = 0.0
        for element in helper_list:
            price_sum += element.price
        return price_sum


class UnitTests(unittest.TestCase):
    test_db = [Product('x0129', 1), Product('AB12', 2), Product('ab123', 3), Product('A12', 4), Product('ab1', 5),
               Product('xx123', 6)]
    test_sorted = [Product('x0129', 1), Product('A12', 4)]

    test_server = ListServer(test_db)
    test_client = Client(test_server)

    def test_tooManyProductsException(self):
        with self.assertRaises(TooManyProducts):
            self.test_server.filter_products(2)

    def test_checkPriceSumException(self):
        self.assertEqual(0, self.test_client.calculate_price(2))

    def test_checkIfSorted(self):
        self.assertEqual(self.test_server.filter_products(1),
                         sorted(self.test_server.filter_products(1), key=lambda product: product.price))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
# Tomasz Krawczyk,
