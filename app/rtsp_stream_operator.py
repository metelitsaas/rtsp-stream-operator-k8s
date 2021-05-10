import time
from threading import Event
from threads.event_listener_thread import EventListenerThread
from threads.resource_controller_thread import ResourceControllerThread
from kubernetes import config


class RTSPStreamOperator:
    """
    RTSP Stream Operator
    """
    def __init__(self, crd_group: str, crd_version: str, crd_plural: str, sleep_period: float = 5):
        """
        Initialization
        :param crd_group: CustomResourceDefinition group name
        :param crd_version: CustomResourceDefinition version
        :param crd_plural: CustomResourceDefinition plural name
        :param sleep_period: sleep period between checks in seconds
        """
        self._object_metadata = {
            'crd_group': crd_group,
            'crd_version': crd_version,
            'crd_plural': crd_plural
        }
        self._sleep_period = sleep_period
        self._shutdown_event = Event()
        self._load_configuration()

    def run(self) -> None:
        """
        Run resource controller and event listener threads in loop
        """
        ResourceControllerThread(self._object_metadata, self._shutdown_event).start()
        EventListenerThread(self._object_metadata, self._shutdown_event).start()

        while not self._shutdown_event.is_set():
            time.sleep(self._sleep_period)

    @staticmethod
    def _load_configuration() -> None:
        """
        Load K8S connect configuration
        """
        config.load_incluster_config()
