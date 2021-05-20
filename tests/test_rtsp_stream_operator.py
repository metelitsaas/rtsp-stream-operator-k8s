import threading
import pytest
import threads.abstract_thread
from rtsp_stream_operator import RTSPStreamOperator


class TestRTSPStreamOperator:
    """
    RTSPStreamOperator test class
    """
    def test_run_connection_exception(self, mocker):
        """
        Test run function
        Check child threads are killed due to connection exceptions
        """
        mocker.patch.object(threads.abstract_thread, 'KubernetesClient', return_value=None)

        crd_group = 'test_group'
        crd_version = 'test_version'
        crd_plural = 'test_plural'

        rtsp_stream_operator = RTSPStreamOperator(crd_group, crd_version, crd_plural)
        rtsp_stream_operator.run()

        assert threading.active_count() == 1

    @pytest.mark.skip(reason="Add test later")
    def test_run_event_occurred(self, mocker):
        """
        Test run function
        Check function finish due to an event occurred
        """
        pass
