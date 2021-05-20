import time
import threading
from threading import Event
from abc import ABC
import pytest
import threads.abstract_thread
from threads.abstract_thread import AbstractThread


class TestAbstractThread:
    """AbstractThread test class"""

    @pytest.fixture()
    def set_up(self):
        """set up basic resources"""
        object_metadata = {
            'crd_group': 'test_group',
            'crd_version': 'test_version',
            'crd_plural': 'test_plural'
        }
        shutdown_event = Event()

        return object_metadata, shutdown_event

    @pytest.fixture()
    def correct_object_abstract_thread(self):
        """create correct child class"""
        class ObjectAbstractThread(AbstractThread, ABC):
            """AbstractThread inherited class with abstract method realization"""
            def _process(self) -> None:
                pass

        return ObjectAbstractThread

    @pytest.fixture()
    def incorrect_object_abstract_thread(self):
        """create incorrect child class"""
        class ObjectAbstractThread(AbstractThread, ABC):
            """AbstractThread inherited class without abstract method realization"""

        return ObjectAbstractThread

    @pytest.fixture()
    def exception_object_abstract_thread(self):
        """create correct child class"""
        class ObjectAbstractThread(AbstractThread, ABC):
            """
            AbstractThread inherited class with abstract method realization
            which raises unhandled exception
            """
            def _process(self) -> None:
                raise Exception

        return ObjectAbstractThread

    def test_abstractmethod(self, set_up, incorrect_object_abstract_thread):
        """Test that _process test_abstractmethod is necessary to be realized"""
        object_metadata, shutdown_event = set_up

        with pytest.raises(TypeError):
            incorrect_object_abstract_thread(object_metadata, shutdown_event)

    def test_thread_end_exception(self, set_up, mocker, exception_object_abstract_thread):
        """Test correct thread end due to unhandled exception"""
        mocker.patch.object(threads.abstract_thread, 'KubernetesClient', return_value=None)

        object_metadata, shutdown_event = set_up
        exception_object_abstract_thread(object_metadata, shutdown_event).start()
        time.sleep(1)

        assert threading.active_count() == 1
        assert shutdown_event.is_set() is True

    def test_thread_end_process(self, set_up, mocker, correct_object_abstract_thread):
        """ Test correct thread end due to exit from processing function"""
        mocker.patch.object(threads.abstract_thread, 'KubernetesClient', return_value=None)

        object_metadata, shutdown_event = set_up
        correct_object_abstract_thread(object_metadata, shutdown_event).start()
        time.sleep(1)

        assert threading.active_count() == 1
        assert shutdown_event.is_set() is True
