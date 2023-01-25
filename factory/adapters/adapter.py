from abc import ABC, abstractmethod


class Adapter(ABC):
    @staticmethod
    @abstractmethod
    def adapt(entity):
        raise NotImplemented
