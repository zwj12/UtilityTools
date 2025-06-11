"""ExternalSensorsTriggerUDPSample
""" 

import socket
import struct
import logging
import os
import sys

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWExternalSensorTriggerUDP.log'

def get_logging():
    """get_logging

    """
    archiveAboveSize = 1024 * 1024 * 10
    if os.path.exists(logFilePath):
        if os.path.getsize(logFilePath) > 1024 * 1024 * 10:
            if os.path.exists(logFilePath + '.1'):
                os.remove(logFilePath + '.1')
            os.rename(logFilePath, logFilePath + '.1')
    else:
        os.makedirs(os.path.dirname(logFilePath), exist_ok=True)
    logger = logging.getLogger('PMTWExternalSensorInterface')
    if logger.hasHandlers() == False:
        logger.setLevel(logging.DEBUG)
        # logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler(logFilePath)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger

def TrigWorkArea(signalName='doManSync1', host='192.168.56.1', port=3003):
    """TriggerWorkArea

    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((host, port))
        dataRequest = struct.pack(f">BHBf{len(signalName)}s", 19, len(signalName) + 5, 0, 0, signalName.encode('utf-8'))
        print(f'Request: {dataRequest.hex()} {dataRequest}')
        s.sendall(dataRequest)
        dataReceive = s.recv(1024)
        print(f'Received: {dataReceive.hex()} {dataReceive}')

def main(argv):
    """main

    """
    print("Run from main: ", argv)
    try:
        logger = get_logging()
        logger.debug(argv)

        host = "192.168.56.1"
        port = 3003
        print(f"Connecting to UDP server at {host}:{port}")
        TrigWorkArea("doManSync1", host, port)

    except Exception:
        print("Error: ", sys.exc_info()[0])
        pass
    finally:
        print("Finally")
        pass


if __name__ == "__main__":
    main(sys.argv)
else:
    pass
