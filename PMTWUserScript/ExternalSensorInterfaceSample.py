"""ExternalSensorInterfaceSample
""" 

import ctypes
import threading
import time
import logging
import os
import sys

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWExternalSensorInterface.log'
registerLogCallbackCounter = 0
monitorRecipeStatusCounter = 0
checkRecipeStatusCounter = 0
waitForRecipeStopCounter = 0
stopThreadCounter = 0

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

class SensorInfo:
    def __init__(self):
        """__init__

        """
        self.name = "External sensor"
        self.description = "External sensor interfaces description"
        self.author = "PMTW developer"
        self.version = "1.0"
        self.sensorIdNameMapDict = {}#'sensorId': 'sensorName'
        self.sensorConfigurationDict = {}#'sensorId': 'configInfo'
        self.posGenConfigurationDict = {}#'posGenId': 'posGenConfigInfo'
        self.posGenSensorMapDict = {}#'posGenId': 'sensorId'
        self.posGenObjectMapDict = {}#'posGenId': 'objectName'
    
    def registerLogCallback(self, logCallBackFunc):
        """registerLogCallback

        Keyword arguments:
        logCallBackFunc -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global registerLogCallbackCounter
        registerLogCallbackCounter += 1
        logger.debug(f'registerLogCallbackCounter = {registerLogCallbackCounter}')
 
        self.fLogCallback = logCallBackFunc
        self.sensorIdNameMapDict.clear()
        self.sensorConfigurationDict.clear()
        self.posGenConfigurationDict.clear()
        self.posGenSensorMapDict.clear()
        self.posGenObjectMapDict.clear()
        
    def initializeSensorMap(self, sensorId, sensorName):
        self.sensorIdNameMapDict[sensorId] = sensorName

class SensorConfig(SensorInfo):
    def __init__(self):
        """__init__

        """
        super().__init__()

    def configureSensor(self, sensorId):
        pass

    def getSensorInfo(self):
        return self.name, self.author, self.version, self.description

    def loadSensor(self, sensorId, configurationInfo):
        self.sensorConfigurationDict[sensorId] = configurationInfo

    def saveSensor(self, sensorId):
        return self.sensorConfigurationDict[sensorId]


class PositionGenerator(SensorConfig, SensorInfo):
    def __init__(self):
        """__init__

        """     
        super().__init__()   
        
    def initializePosGenRelatedMap(self, sensorId, posGenId, objectName):
        self.posGenSensorMapDict[posGenId] = sensorId
        self.posGenObjectMapDict[posGenId] = objectName
    
    def configurePosGen(self, posGenId):
        pass
        
    def loadPosGen(self, posGenId, positionGeneratorInfo):
        self.posGenConfigurationDict[posGenId] = positionGeneratorInfo
        
    def savePosGen(self, posGenId):
        return self.posGenConfigurationDict[posGenId]


class SensorRuntime(PositionGenerator, SensorConfig, SensorInfo):
    def __init__(self):
        """__init__

        """     
        super().__init__()   
        self.recipeStatus = 0
        self.monitorThread = 0

    def startSensor(self, callBackFunc):
        pass

    def stopSensor(self):
        pass
        
    def monitorRecipeStatus(self, callBackFunc):
        """monitorRecipeStatus

        Keyword arguments:
        callBackFunc -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global monitorRecipeStatusCounter
        monitorRecipeStatusCounter += 1
        logger.debug(f'monitorRecipeStatusCounter = {monitorRecipeStatusCounter}')

        self.recipeStatus = 1
        self.monitorThread = StoppableThread(target=SensorRuntime.checkRecipeStatus, args=(self, callBackFunc))
        self.monitorThread.start()

    def checkRecipeStatus(self, callBackFunc):
        """checkRecipeStatus

        Keyword arguments:
        callBackFunc -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global checkRecipeStatusCounter
        checkRecipeStatusCounter += 1
        logger.debug(f'checkRecipeStatusCounter = {checkRecipeStatusCounter}')

        while True:
            self.recipeStatus = callBackFunc.GetRecipeStatus()
            time.sleep(1)
            if self.recipeStatus == 0:
                break

    def waitForRecipeStop(self):
        """waitForRecipeStop

        Keyword arguments:
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global waitForRecipeStopCounter
        waitForRecipeStopCounter += 1
        logger.debug(f'waitForRecipeStopCounter = {waitForRecipeStopCounter}')

        while True:
            if self.recipeStatus == 0:
                break
        self.monitorThread.stop()
            


class StoppableThread(threading.Thread):
    def __init__(self, target=None, args=(), kwargs=None, daemon=True):
        super().__init__(target=target, args=args, kwargs=kwargs, daemon=daemon)
        self.flag = threading.Event()

    def stop(self):
        """stop

        Keyword arguments:
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global stopThreadCounter
        stopThreadCounter += 1
        logger.debug(f'stopThreadCounter = {stopThreadCounter}')

        if not self.is_alive():
            logger.debug(f'thread is not alive')
            return
        
        logger.debug(f'call PyThreadState_SetAsyncExc with SystemExit: {self.ident}')
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), exc)
        if res == 0:
            logger.debug(f'cannot find thread id')
            raise ValueError("cannot find thread id")
        elif res > 1:
            logger.debug(f'call PyThreadState_SetAsyncExc with none: {self.ident}')
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            logger.debug(f'Thread is stopped')
            raise SystemError("Thread is stopped")
