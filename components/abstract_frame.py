from abc import ABC, abstractmethod

class AbstractFrame(ABC):
    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def hide(self):
        pass
