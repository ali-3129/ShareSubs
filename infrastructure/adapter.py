from abc import ABC


class Adapter(ABC):
    @staticmethod
    def adapt(**kwargs) -> dict:
        pass


class AccountAdapter(Adapter):
    @staticmethod
    def adapt(**kwargs):
        return {
            
        }