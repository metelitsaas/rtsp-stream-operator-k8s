from abc import ABC
from threads.abstract_thread import AbstractThread
from utils.logger import logger


class EventListenerThread(AbstractThread, ABC):
    """
    Thread listens K8S events and creates/updates/deletes resources if they changed
    """
    def _process(self) -> None:
        """
        Thread listens events in loop
        """
        while not self._shutdown_event.is_set():
            for event in self._kubernetes_client.listen_for_crd_events(self._object_metadata):
                logger.info(f"Event: {event}")
