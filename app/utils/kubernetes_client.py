from functools import wraps
from utils.logger import logger
from kubernetes import config, client, watch as e_watch


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


def exception_handler(function):
    """
    Exception handler decorator
    :param function: wrapped function
    :return: wrapper function
    """
    @wraps(function)
    def wrapper(*method_args, **method_kwargs):

        try:
            return function(*method_args, **method_kwargs)

        except client.exceptions.ApiException as error:
            logger.warning(error)

            return None

    return wrapper


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
        self._event_watcher = e_watch.Watch()

    @exception_handler
    def listen_for_crd_events(self, object_metadata: dict) -> dict:
        """
        Listens Kubernetes API for CRD events
        :param object_metadata: K8S object metadata
        :return: CRD event object
        """
        for event in self._event_watcher.stream(self.list_cluster_crd_object,
                                                object_metadata):
            yield event

    @exception_handler
    def list_cluster_crd_object(self, object_metadata: dict, **kwargs) -> dict:
        """
        Get CRD Kubernetes objects in all namespaces
        :param object_metadata: K8S object metadata
        """
        return self._custom_object_api.list_cluster_custom_object(
            object_metadata['group'],
            object_metadata['version'],
            object_metadata['plural'],
            **kwargs
        )

    @exception_handler
    def get_service(self, name: str, namespace: str) -> client.V1Service:
        """
        Get service object
        :param name: name of the object
        :param namespace: namespace of the object
        :return: service K8S object
        """
        return self._core_v1_api.read_namespaced_service(name, namespace)

    @exception_handler
    def get_deployment(self, name: str, namespace: str) -> client.V1Service:
        """
        Get deployment object
        :param name: name of the object
        :param namespace: namespace of the object
        :return: deployment K8S object
        """
        return self._apps_v1_api.read_namespaced_deployment(name, namespace)
