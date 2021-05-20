from threading import Thread, Event
from abc import ABCMeta, abstractmethod
from utils.logger import logger
from utils.kubernetes_client import KubernetesClient


class AbstractThread(Thread, metaclass=ABCMeta):
    """
    Thread abstract class
    """
    def __init__(self, object_metadata: dict, shutdown_event: Event):
        """
        Initialization
        :param object_metadata: K8S object metadata
        :param shutdown_event: event to shutdown thread
        """
        Thread.__init__(self, name=self.__class__.__name__, daemon=True, target=self._run)
        self._object_metadata = object_metadata
        self._shutdown_event = shutdown_event
        self._kubernetes_client = KubernetesClient()

    def _run(self) -> None:
        """
        Run thread with exception handling
        """
        try:
            logger.info("Starting thread")
            self._process()

        except Exception as error:
            logger.exception(error)

        finally:
            logger.info("Stopping thread")
            self._shutdown_event.set()

    @abstractmethod
    def _process(self) -> None:
        """
        Thread processing loop
        """
        pass
