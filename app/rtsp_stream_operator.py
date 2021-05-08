import time
from threading import Event
from threads.event_listener_thread import EventListenerThread
from threads.resource_controller_thread import ResourceControllerThread
from kubernetes import config

SLEEP_SEC = 5


class RTSPStreamOperator:
    """
    RTSP Stream Operator
    """
    def __init__(self, crd_group: str, crd_version: str, crd_plural: str):
        """
        Initialization
        """
        self._object_metadata = {
            'crd_group': crd_group,
            'crd_version': crd_version,
            'crd_plural': crd_plural
        }
        self._shutdown_event = Event()
        self._load_configuration()

    def run(self) -> None:
        """
        Run resource controller and event listener threads in loop
        """
        ResourceControllerThread(self._object_metadata, self._shutdown_event).start()
        EventListenerThread(self._object_metadata, self._shutdown_event).start()

        while not self._shutdown_event.isSet():
            time.sleep(SLEEP_SEC)

    @staticmethod
    def _load_configuration() -> None:
        """
        Load K8S connect configuration
        """
        config.load_incluster_config()
