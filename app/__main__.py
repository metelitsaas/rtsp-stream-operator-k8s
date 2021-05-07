from kubernetes import config, client, watch
from utils.logger import logger


def main():

    config.load_incluster_config()
    core_v1_api = client.CoreV1Api()
    event_watcher = watch.Watch()

    for event in event_watcher.stream(core_v1_api.list_namespace):
        logger.info(f"""Event: {event['type']} {event['object'].kind} {event['object'].metadata.name}""")


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as error:
        logger.exception(error)
