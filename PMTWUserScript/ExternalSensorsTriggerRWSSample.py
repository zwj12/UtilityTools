"""ExternalSensorsTriggerRWSSample
""" 

import time
import json
import logging
import os
import sys
from web_service_connection import WebServiceConnection

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWExternalSensorTriggerRWS.log'

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

def TrigWorkArea(signalName, host='192.168.56.1', port=80, RWSVersion='1.0'):
    """TriggerWorkArea

    """
    username = "Default User"
    password = "robotics"
    web_service_connection = WebServiceConnection(host, port, username, password, RWSVersion)
    
    if RWSVersion == '1.0':    
        url = f"{WebServiceConnection.get_server()}/rw/iosystem/signals/EtherNetIP/PPABOARD/{signalName}?action=set"
    else:
        url = f"{WebServiceConnection.get_server()}/rw/iosystem/signals/EtherNetIP/PPABOARD/{signalName}/set-value"

    payload = {"lvalue": 1, "mode": "pulse", "Pulses":1, "ActivePulse": 200, "PassivePulse": 200, "userlog": "true"}
    # payload = {"lvalue": 1}

    resp = WebServiceConnection.get_session().post(url, cookies=WebServiceConnection.get_cookies(), headers=WebServiceConnection.get_headerContentType(), verify=False, data=payload)

    print(resp)

def main(argv):
    """main

    """
    print("Run from main: ", argv)
    try:
        logger = get_logging()
        logger.debug(argv)

        host = "127.0.0.1"
        port = 5466
        print(f"Connecting to RWS server at {host}:{port}")
        TrigWorkArea("doManSync1", host, port, '2.0')

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
