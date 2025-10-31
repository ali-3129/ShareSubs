class Container:
    def __init__(self):
        self.__singleton__ = {}
        self.__scoped__= {}
        self.__transient__= {}
        self.__factory__={}
        self.__task__={}
    
    def get_singleton(self, cls, *args):
        if cls not in self.__singleton__:
            self.__singleton__[cls] = cls(*args)
            return self.__singleton__[cls]
        else:
            return self.__singleton__[cls]

    def get_scoped(self, cls):

        if cls not in self.__scoped__:
            self.__scoped__[cls] = cls()
            return self.__scoped__[cls]
        else:
            return self.__scoped__[cls]

    def get_task(self, cls, **kwargs):
        task_id = kwargs["task_id"]
        if task_id not in self.__task__:
            self.__task__[task_id] = cls(**kwargs)
            return self.__task__[task_id]
        else:
            return self.__task__[task_id]
        
    async def get_factory(self, cls, **kwargs):
        if cls not in self.__factory__:
            self.__factory__[cls] = {}
        if kwargs["user"] not in self.__factory__[cls]:
                if hasattr(cls, "create") and callable(getattr(cls, "create")):
                    self.__factory__[cls][kwargs["user"]] = await cls.create( **kwargs)
                else:
                    self.__factory__[cls][kwargs["user"]] = cls(**kwargs)

        return self.__factory__[cls][kwargs["user"]]
    
    def get_transient(self, cls):
        return cls()