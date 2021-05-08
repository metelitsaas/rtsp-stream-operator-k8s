import os
from rtsp_stream_operator import RTSPStreamOperator
from utils.logger import logger


def main():

    crd_group = os.environ['CRD_GROUP']
    crd_version = os.environ['CRD_VERSION']
    crd_plural = os.environ['CRD_PLURAL']

    rtsp_stream_operator = RTSPStreamOperator(crd_group, crd_version, crd_plural)
    rtsp_stream_operator.run()


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as error:
        logger.exception(error)
