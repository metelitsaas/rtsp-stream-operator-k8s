import pytest
from kubernetes.config.config_exception import ConfigException
from utils.kubernetes_client import KubernetesClient


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
    def test_list_cluster_crd_object(self):
        pass
