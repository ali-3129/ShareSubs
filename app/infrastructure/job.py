import asyncio
from asyncio import Queue, timeout
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
import time
from typing import ClassVar, DefaultDict
from collections import defaultdict
import random
from time import sleep


async def retry(job, instance, max_try: int = 5, max_delay=20, base_delay=5.0, **kwargs):
    for attempt in range(1, max_try + 1):
        try:
            print("touch")
            return await attempt_run(base_delay, instance, **kwargs)
        except:
            from .bootstrap import metric
            metric.inc(f"attempt_{job}")
            if attempt == max_try or base_delay >= max_delay:
                print(attempt)
                raise
            delay = min(max_delay, (base_delay + attempt) * 2)
            jitter = random.uniform(0, 0.3 * delay)
            base_delay = delay
            await asyncio.sleep(jitter)


async def attempt_run(delay, instance, **kwargs):
    async with timeout(delay):
        print("touched")
        return await po(instance, **kwargs)


async def safe_run(job, instance, **kwargs):
    from .bootstrap import sem
    async with sem:
        return await retry(job, instance, **kwargs)


async def po(instance, **kwargs):
    await asyncio.sleep(1)
    print("toucccc")
    await instance.update(**kwargs)


async def db_worker(qeue: asyncio.Queue, name: str):
    from .bootstrap import shot_down
    while not shot_down.is_set():
        try:

            job = await asyncio.wait_for(qeue.get(), timeout=0.5)
        except TimeoutError:
            continue
        async with masure(job):
            try:

                if Task.get_done_task(job):
                    qeue.task_done()
                    continue
                else:
                    var = Task.get_data()
                    instance = var[job]["instance"]
                    # print(instance)
                    field = var[job]["field"]
                    obj = var[job]["obj"]
                    value = var[job]["value"]
                    await safe_run(job, instance, field=field, obj=obj, value=value)
            except:
                print(f"Error by {type(instance).__name__}")
            finally:

                Task.add_to_done(job)
                print(f"job: {job} is done and losed")
                qeue.task_done()
                Task.del_task(job)


@dataclass
class Task:
    task_id: any
    instance: any
    obj: any
    field_name: str
    value: any
    tasks: ClassVar[dict] = defaultdict(list)
    task: dict = field(default_factory=dict)
    done_list: ClassVar[list] = []

    def __post_init__(self):
        from .bootstrap import qeue
        self.task = {"instance": self.instance, "obj": self.obj, "field": self.field_name, "value": self.value}
        Task.tasks[self.task_id] = self.task
        asyncio.create_task(qeue.put(self.task_id))
        print(self.task)

    @staticmethod
    def get_data():
        print(Task.tasks)
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


@asynccontextmanager
async def masure(job: str):
    from .bootstrap import metric
    start = time.perf_counter()

    try:
        yield
        duration = time.perf_counter() - start
        metric.inc(f"attempt_{job}")
        metric.dauration(f"duration_{job}", duration)
    except:
        metric.inc(f"faild_{job}")
        raise


async def producer(qeue):
    from .bootstrap import shot_down

    tasks = Task.get_data()
    try:
        print("id : ")
        for id in tasks.keys():
            print("id : ")
            await qeue.put(id)
    except:
        pass
