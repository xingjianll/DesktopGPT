# Importing required module
from abc import ABC, abstractmethod


class IfView(ABC):
    @abstractmethod
    def display_msg(self, msg: str) -> None:
        pass
