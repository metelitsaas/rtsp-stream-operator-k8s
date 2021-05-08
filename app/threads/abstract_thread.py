from threading import Thread, Event
from abc import ABCMeta, abstractmethod
from utils.logger import logger


class AbstractThread(Thread, metaclass=ABCMeta):
    """
    Thread abstract class
    """
    def __init__(self, shutdown_event: Event):
        """
        Initialization
        """
        Thread.__init__(self, daemon=True, target=self._run)
        self._shutdown_event = shutdown_event

    def _run(self) -> None:
        """
        Run thread with exception handling
        """
        try:
            logger.info(f"Starting thread")
            self._process()

        except Exception as error:
            logger.exception(error)

        finally:
            self._shutdown_event.set()
            self.join()

    @abstractmethod
    def _process(self) -> None:
        """
        Thread processing loop
        """
        pass
