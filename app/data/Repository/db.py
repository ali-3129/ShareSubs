from abc import ABC, abstractmethod


class Db(ABC):
    db = {"Account": {}, "User": {}, "Role": {}, "UserRole": {}, "UserAccount": {}}

    @staticmethod
    def shema():
        pass
    @staticmethod
    def get_branch():
        pass

    async def update(self, **kwargs):
        obj = kwargs["obj"]
        field = kwargs["field"]
        value = kwargs["value"]
        id = obj.get_id()
        if id not in Db.db[self.get_branch()]:
            Db.db[self.get_branch()][id] = self.shema()
        if field in Db.db[self.get_branch()][id] and isinstance(Db.db[self.get_branch()][id][field], list):
                Db.db[self.get_branch()][id][field].append(value)
        else:
                print(field)
                Db.db[self.get_branch()][id][field] = value

    def get_data(self):
        print(f"\n{self.db}\n")
    

    async def get_user_by_id(self, id):
        for user_id in self.db["User"].keys():
            if user_id == id:
                return self.db["User"][id]
         

db =Db()