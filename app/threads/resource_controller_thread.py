import time
from abc import ABC
from utils.kubernetes_functions import list_cluster_crd_object
from utils.logger import logger
from threads.abstract_thread import AbstractThread
from kubernetes import client

SLEEP_SEC = 5


class ResourceControllerThread(AbstractThread, ABC):
    """
    Thread controls existence of K8S resources
    """
    def _process(self) -> None:
        """
        Thread checks resources in loop
        """
        while not self._shutdown_event.is_set():
            self._check_resources()
            self._collect_garbage()

            time.sleep(SLEEP_SEC)

    def _check_resources(self) -> None:
        """
        Checks resources existence
        """
        object_list = list_cluster_crd_object(self._object_metadata)

        self._check_deployments(object_list)
        self._check_services(object_list)

    def _collect_garbage(self) -> None:
        """
        Deletes irrelevant resources
        """
        pass

    @staticmethod
    def _check_deployments(object_list: dict) -> None:
        """
        Checks deployments existence and creates them if necessary
        :param object_list: dict of CRD objects
        """
        apps_v1_api = client.AppsV1Api()

        for resource in object_list['items']:

            name = resource['metadata']['name']
            namespace = resource['metadata']['namespace']

            deployments = apps_v1_api.read_namespaced_deployment(name, namespace)
            logger.info(f"Deployments found: {deployments}")

    @staticmethod
    def _check_services(object_list: dict) -> None:
        """
        Checks services existence and creates them if necessary
        :param object_list: dict of CRD objects
        """
        core_v1_api = client.CoreV1Api()

        for resource in object_list['items']:

            name = resource['metadata']['name']
            namespace = resource['metadata']['namespace']

            services = core_v1_api.read_namespaced_service(name, namespace)
            logger.info(f"Services found: {services}")
