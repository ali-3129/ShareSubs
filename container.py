class Container:
    def __init__(self):
        self.__singleton__ = {}
        self.__scoped__= {}
        self.__transient__= {}
    
    def get_singleton(self, cls, *args):
        if cls not in self.__singleton__:
            self.__singleton__[cls] = cls(*args)
            return self.__singleton__[cls]
        else:
            return self.__singleton__[cls]

    async def get_scoped(self, cls, name, id, status, instance=None, *args):

        if cls not in self.__scoped__:
            self.__scoped__[cls] = {}
        if id not in self.__scoped__[cls]:
                if hasattr(cls, "create") and callable(getattr(cls, "create")):
                    self.__scoped__[cls][id] = await cls.create(name, id, status)
                else:
                    self.__scoped__[cls][id] = await cls(name, id, status)

        return self.__scoped__[cls][id]
    
    def get_transient(self, cls):
        return cls()