from kubernetes import config, client


class SingletonMeta(type):
    """
    Singleton metaclass realization
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Make sure shat object is single
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class KubernetesClient(metaclass=SingletonMeta):
    """
    Kubernetes API client
    """
    def __init__(self):
        """
        Initialization
        """
        config.load_incluster_config()
        self._custom_object_api = client.CustomObjectsApi()
        self._core_v1_api = client.CoreV1Api()
        self._apps_v1_api = client.AppsV1Api()

    def list_cluster_crd_object(self, object_metadata: dict) -> client.V1CustomResourceDefinition:
        """
        Get CRD Kubernetes objects in all namespaces
        :param object_metadata: K8S object metadata
        :return: dict of CRD objects
        """
        return self._custom_object_api.list_cluster_custom_object(
            object_metadata['crd_group'],
            object_metadata['crd_version'],
            object_metadata['crd_plural']
        )
