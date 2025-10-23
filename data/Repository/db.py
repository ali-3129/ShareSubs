from abc import ABC, abstractmethod


class Db(ABC):
    db = {"Account": {}, "User": {}, "Role": {}, "UserRole": {}, "UserAccount": {}}

    @staticmethod
    def shema():
        pass
    @staticmethod
    def get_branch():
        pass

    async def update(self, obj, field, value):
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

db =Db()