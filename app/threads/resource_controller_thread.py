import time
from abc import ABC
from utils.logger import logger
from threads.abstract_thread import AbstractThread

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
        object_list = self._kubernetes_client.list_cluster_crd_object(self._object_metadata)
        logger.info(f"CRD objects: {object_list}")

        self._check_deployments(object_list)
        self._check_services(object_list)

    def _collect_garbage(self) -> None:
        """
        Deletes irrelevant resources
        """
        pass

    def _check_deployments(self, object_list: dict) -> None:
        """
        Checks deployments existence and creates them if necessary
        :param object_list: dict of CRD objects
        """
        for resource in object_list['items']:

            name = resource['metadata']['name']
            namespace = resource['metadata']['namespace']

            deployment = self._kubernetes_client.get_deployment(name, namespace)
            logger.info(f"Deployment found: {deployment}")

    def _check_services(self, object_list: dict) -> None:
        """
        Checks services existence and creates them if necessary
        :param object_list: dict of CRD objects
        """
        for resource in object_list['items']:

            name = resource['metadata']['name']
            namespace = resource['metadata']['namespace']

            service = self._kubernetes_client.get_service(name, namespace)
            logger.info(f"Service found: {service}")
