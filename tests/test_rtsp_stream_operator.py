import threading
import pytest
from kubernetes.config.config_exception import ConfigException
from app.rtsp_stream_operator import RTSPStreamOperator


class TestRTSPStreamOperator:
    """
    RTSPStreamOperator test class
    """
    def test_run_configuration_exception(self):
        """
        Test run function
        Check load config exception if cluster unavailable
        """
        crd_group = 'test_group'
        crd_version = 'test_version'
        crd_plural = 'test_plural'

        with pytest.raises(ConfigException):
            RTSPStreamOperator(crd_group, crd_version, crd_plural)

    def test_run_connection_exception(self, mocker):
        """
        Test run function
        Check child threads are killed due to connection exceptions
        """
        mocker.patch('app.rtsp_stream_operator.RTSPStreamOperator._load_configuration',
                     return_value=None)

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
