from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class AbstractNotifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


class EmailNotifier(AbstractNotifier):
    def send(self, message: str):
        logger.info(f"[EMAIL] Отправлено: {message}")
        print(f"[EMAIL] Отправлено: {message}")
        return True