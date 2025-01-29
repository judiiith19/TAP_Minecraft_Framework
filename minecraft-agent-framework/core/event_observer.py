from abc import ABC, abstractmethod
class EventObserver(ABC):
    @abstractmethod
    def update(self):
        pass