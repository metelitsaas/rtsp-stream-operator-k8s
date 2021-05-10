from abc import ABC
from threads.abstract_thread import AbstractThread
from utils.logger import logger
from kubernetes import client, watch


class EventListenerThread(AbstractThread, ABC):
    """
    Thread listens K8S events and creates/updates/deletes resources if they changed
    """
    def _process(self) -> None:
        """
        Thread listens events in loop
        """
        custom_object_api = client.CustomObjectsApi()
        event_watcher = watch.Watch()

        while not self._shutdown_event.is_set():
            for event in event_watcher.stream(custom_object_api.list_cluster_custom_object,
                                              self._object_metadata['crd_group'],
                                              self._object_metadata['crd_version'],
                                              self._object_metadata['crd_plural']):
                logger.info(f"Event: {event['type']} "
                            f"{event['object'].kind} "
                            f"{event['object'].metadata.name}")

        event_watcher.stop()
