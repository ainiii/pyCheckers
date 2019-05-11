from abc import ABC, abstractmethod

class AbstractThread(ABC):
    @abstractmethod
    def stop(self):
        pass
