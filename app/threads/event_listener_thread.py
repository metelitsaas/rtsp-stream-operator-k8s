from abc import ABC
from kubernetes import client, watch
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
        core_v1_api = client.CoreV1Api()
        event_watcher = watch.Watch()

        while not self._shutdown_event.isSet():
            for event in event_watcher.stream(core_v1_api.list_namespace):
                logger.info(f"Event: {event['type']} "
                            f"{event['object'].kind} "
                            f"{event['object'].metadata.name}")

        event_watcher.stop()
