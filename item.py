from typing import Callable, override


class Item:
    def __init__(self, name: str, price: int, get_notification: Callable):
        self.name: str = name
        self.price: int = price
        self.get_notification: Callable = get_notification
