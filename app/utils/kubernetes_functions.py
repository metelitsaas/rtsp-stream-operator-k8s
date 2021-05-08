from kubernetes import client


def list_cluster_crd_object(object_metadata: dict) -> dict:
    """
    Get CRD Kubernetes objects in all namespaces
    :param object_metadata: K8S object metadata
    :return: dict of CRD objects
    """
    custom_object_api = client.CustomObjectsApi()

    return custom_object_api.list_cluster_custom_object(
        object_metadata['crd_group'],
        object_metadata['crd_version'],
        object_metadata['crd_plural']
    )
