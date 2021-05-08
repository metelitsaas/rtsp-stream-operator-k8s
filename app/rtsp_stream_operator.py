import time
from threading import Event
from kubernetes import config
from threads.event_listener_thread import EventListenerThread

SLEEP_SEC = 5


class RTSPStreamOperator:
    """
    RTSP Stream Operator
    """
    def __init__(self):
        """
        Initialization
        """
        self._shutdown_event = Event()
        self._load_configuration()

    def run(self) -> None:
        """
        Run resource controller and event listener threads in loop
        """
        EventListenerThread(self._shutdown_event).start()

        while not self._shutdown_event.isSet():
            time.sleep(SLEEP_SEC)

    @staticmethod
    def _load_configuration() -> None:
        """
        Load K8S connect configuration
        """
        config.load_incluster_config()
