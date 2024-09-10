from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar


CT = TypeVar(name="CT")
CR = TypeVar(name="CR")


@dataclass(frozen=True)
class BaseCommand(ABC):
    ...


@dataclass(eq=False, frozen=True)
class BaseCommandHandler(ABC, Generic[CT, CR]):

    @staticmethod
    @abstractmethod
    def handle(command: CT) -> CR:
        ...
