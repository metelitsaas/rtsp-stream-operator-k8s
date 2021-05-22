import pytest
from utils.kubernetes_client import KubernetesClient
from kubernetes.config.config_exception import ConfigException


class TestKubernetesClient:
    """
    KubernetesClient test class
    """
    def test_init_configuration_exception(self):
        """
        Test init function
        Check load config exception if cluster unavailable
        """
        with pytest.raises(ConfigException):
            KubernetesClient()

    @pytest.mark.skip(reason="Add test later")
    def test_listen_for_crd_events(self):
        pass

    @pytest.mark.skip(reason="Add test later")
    def test_list_cluster_crd_object(self):
        pass

    @pytest.mark.skip(reason="Add test later")
    def test_get_service(self):
        pass

    @pytest.mark.skip(reason="Add test later")
    def test_get_deployment(self):
        pass
