from abc import ABC, abstractmethod

class AbstractUserInterface(ABC):
    @abstractmethod
    def get_input(self, prompt: str):
        pass

    @abstractmethod
    def show_message(self, message: str):
        pass


class ConsoleUserInterface(AbstractUserInterface):
    def get_input(self, prompt: str):
        return input(prompt)

    def show_message(self, message: str) -> None:
        print(message)