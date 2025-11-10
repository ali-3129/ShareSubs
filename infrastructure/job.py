import asyncio
from asyncio import Queue
from dataclasses import dataclass, field
from typing import ClassVar, DefaultDict
from collections import defaultdict
import random
from time import sleep
async def po(instance, **kwargs):
    await asyncio.sleep(7)
    await instance.update(**kwargs)

async def retry(instance, max_try : int =5, max_delay=20, base_delay=5.0, **kwargs ):
    for attempt in range(1, max_try + 1):
       try:
            return await asyncio.wait_for(po(instance ,**kwargs), timeout=base_delay)
       except:
           print("timeout try")
           if attempt == max_try or base_delay >= max_delay:
               print(attempt)
               raise
           delay = min(max_delay, (base_delay+attempt) *2 )
           jitter = random.uniform(0, 0.3 * delay)
           base_delay = delay
           await asyncio.sleep(jitter)
    



async def db_worker(qeue : asyncio.Queue, name : str):
   from .bootstrap import SENTINEL
   while True:
        job = await qeue.get()
        if job is SENTINEL:
            qeue.task_done()
            break
        else:
            try:
                if Task.get_done_task(job):
                    qeue.task_done()
                    continue
                else:
                    var = Task.get_data()
                    instance = var[job]["instance"]
                    #print(instance)
                    field = var[job]["field"]
                    obj = var[job]["obj"]
                    value = var[job]["value"]
                    await retry(instance, field=field, obj=obj, value=value)

            except:
                print(f"Error by {type(instance).__name__}")
            finally:
                
                Task.add_to_done(job)
                print(f"job: {job} is done and losed")
                qeue.task_done()
                Task.del_task(job)

@dataclass
class Task:
    task_id : any
    instance : any
    obj : any
    field_name : str
    value : any
    tasks : ClassVar[dict] = defaultdict(list)
    task : dict = field(default_factory=dict)
    done_list : ClassVar[list] = []

    def __post_init__(self):
        self.task = {"instance": self.instance, "obj": self.obj, "field": self.field_name, "value": self.value}
        Task.tasks[self.task_id] = self.task

    
    @staticmethod
    def get_data():
        #print(Task.tasks)
        return Task.tasks
    
    @staticmethod
    def add_to_done(task_id):
        Task.done_list.append(task_id)
    
    @staticmethod
    def get_done_task(id):
        if id in Task.done_list:
            return True
        return False
    
    @staticmethod
    def del_task(id):
        from .bootstrap import container
        try:
            container.del_task(id)
        except:
            pass


async def producer(qeue):
    try:
        for id in Task.get_data().keys():
            await qeue.put(id)
    except():
        pass