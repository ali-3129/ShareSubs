class Container:
    def __init__(self):
        self.__singleton__ = {}
        self.__scoped__= {}
        self.__transient__= {}
        self.__factory__={}
    
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
        
    async def get_factory(self, cls, name, id, status, instance=None, *args):
        if cls not in self.__scoped__:
            self.__scoped__[cls] = {}
        if id not in self.__factory__[cls]:
                if hasattr(cls, "create") and callable(getattr(cls, "create")):
                    self.__factory__[cls][id] = await cls.create(name, id, status)
                else:
                    self.__factory__[cls][id] = cls(name, id, status)

        return self.__factory__[cls][id]
    
    def get_transient(self, cls):
        return cls()