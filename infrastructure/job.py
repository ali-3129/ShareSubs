import asyncio
from asyncio import Queue
from dataclasses import dataclass, field
from typing import ClassVar, DefaultDict
from uuid import uuid4, uuid5
from collections import defaultdict
SENTINEL = object()

async def db_worker(qeue : asyncio.Queue, name : str):
   while True:
        job = await qeue.get()
        if job is SENTINEL:
            break
        else:
            try:
                var = Task.get_data()
                instance = var[job]["instance"]
                await instance.update(**var[job])
                
            except:
                print(f"Error by {type(instance).__name__}")
            finally:
                qeue.task_done()

@dataclass
class Task:
    task_id : any
    instance : any
    obj : any
    field_name : str
    value : any
    tasks = defaultdict(list)
    task : dict = field(default_factory=dict)


    def __post_init__(self):
        self.task = {"instance": self.instance, "obj": self.obj, "field": self.field_name, "value": self.value}
        if self.task_id not in Task.tasks:
            Task.tasks[self.task_id] = {}
        else:
            Task.tasks[self.task_id].append(self.task)
    
    @staticmethod
    def get_data():
        return Task.tasks


async def producer(qeue):
    try:
        for id in Task.get_data():
            await qeue.put(id)
    except():
        pass