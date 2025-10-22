import asyncio
from abc import ABC
    

class Logger:
    async def update(self, obj, field, value):
        print(f"value {value} in {field} added")


class Observer(ABC):
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    async def notify(self, obj, field, value):
        for observer in self.observers:
            
            await observer.update(obj, field, value)


class AccountObserver(Observer):
    def __init__(self):
        super().__init__()


class UserObserver(Observer):
    def __init__(self):
        super().__init__()


class UserRoleObserver(Observer):
    def __init__(self):
        super().__init__()


class RoleObserver(Observer):
    def __init__(self):
        super().__init__()