from rtsp_stream_operator import RTSPStreamOperator
from utils.logger import logger


def main():

    rtsp_stream_operator = RTSPStreamOperator()
    rtsp_stream_operator.run()


if __name__ == '__main__':

    try:
        logger.info('Starting')
        main()

    except Exception as error:
        logger.exception(error)
