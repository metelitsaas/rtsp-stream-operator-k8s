import time
from threading import Event
from threads.event_listener_thread import EventListenerThread
from threads.resource_controller_thread import ResourceControllerThread


class RTSPStreamOperator:
    """
    RTSP Stream Operator
    """
    def __init__(self, group: str, version: str, plural: str, sleep_period: float = 5):
        """
        Initialization
        :param group: CustomResourceDefinition group name
        :param version: CustomResourceDefinition version
        :param plural: CustomResourceDefinition plural name
        :param sleep_period: sleep period between checks in seconds
        """
        self._object_metadata = {
            'group': group,
            'version': version,
            'plural': plural
        }
        self._sleep_period = sleep_period
        self._shutdown_event = Event()

    def run(self) -> None:
        """
        Run resource controller and event listener threads in loop
        """
        resource_controller_thread = ResourceControllerThread(self._object_metadata,
                                                              self._shutdown_event)
        event_listener_thread = EventListenerThread(self._object_metadata, self._shutdown_event)

        resource_controller_thread.start()
        event_listener_thread.start()

        while not self._shutdown_event.is_set():
            time.sleep(self._sleep_period)

        resource_controller_thread.join()
        event_listener_thread.join()
