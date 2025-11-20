import asyncio
from uuid import uuid4, uuid5
from abc import ABC
import time
from collections import defaultdict

class Metric:
    def __init__(self):
        self.start = time.perf_counter()
        self.duration = defaultdict(float)
        self.counter = defaultdict(int)

    
    def inc(self, key, amount=1):
        self.counter[key] += 1
    
    
    def dauration(self, key, time):
        self.duration[key] += time
    
    def get_all(self):
        uptime = time.perf_counter() - self.start
        return {
            "count": dict(self.counter),
            "duration": dict(self.duration),
            "uptime": uptime
        }



class Logger:
    async def update(self, obj, field, value):
        print(f"value {value} in {field} added")



class Observer(ABC):
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    async def notify(self, obj, field, value):
        from .job import Task
        job = ("UserDb", "User", "Role", "UserRole", "UserAccount")
        for observer in self.observers:
            if type(observer).__name__ in job:
                from .bootstrap import container
                task = container.get_task(cls=Task, instance=observer, obj=obj, field_name=field, value=value, task_id=get_uniq_id(field))

            else:
                await observer.update(obj, field, value)

def get_uniq_id(field):
    u_id : str = uuid4()
    task_id : uuid5 = uuid5(u_id, field)
    print(task_id)
    return task_id

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