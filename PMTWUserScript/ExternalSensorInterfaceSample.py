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
getSensorInfoCounter = 0
loadSensorCounter = 0
saveSensorCounter = 0
initializePosGenRelatedMapCounter = 0
configurePosGenCounter = 0
loadPosGenCounter = 0
savePosGenCounter = 0
startSensorCounter = 0
stopSensorCounter = 0

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
        super().__init__()
        self.name = "External sensor"
        self.description = "External sensor interfaces description"
        self.author = "PMTW developer"
        self.version = "1.0"
        self.sensorIdNameMapDict = {}#'sensorId': 'sensorName' # - stores the relationship between Id and name of used external sensors
        self.sensorConfigurationDict = {}#'sensorId': 'configInfo' # - stores the configuration info string of all used external sensors
        self.posGenConfigurationDict = {}#'posGenId': 'posGenConfigInfo' # - stores the configuration info string of all used position generators
        self.posGenSensorMapDict = {}#'posGenId': 'sensorId' # - stores the relationship between all used position generator Id and all used external sensor Id
        self.posGenObjectMapDict = {}#'posGenId': 'objectName' # - stores the relationship between all used position generator Id and object names
    
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
        # users can use the logCallBackFunc to show python log in PMTW with the following format:
        #   log = {'LogLevel': 0, 'Log': 'python log string'}
        #   self.fLogCallback.ShowPythonLog(log)

    def initializeSensorMap(self, sensorId, sensorName):
        self.sensorIdNameMapDict[sensorId] = sensorName


class SensorConfig(SensorInfo):
    def __init__(self):
        """__init__

        """
        super().__init__()

    def configureSensor(self, sensorId):
        # users should implement the configuration logic in their class. The content must contain the following parts:
        # Step 1: if configure for the first time, skip step 1.
        #         Otherwise, find the configurationInfo string by self.sensorConfigurationDict[sensorId]
        #         and analyze it to get the configuration setting from last time.
        # Step 2: configuration logic defined by users.
        # Step 3: parse the configuration data into one string and update it in self.sensorConfigurationDict[sensorId].
        pass

    def getSensorInfo(self):
        """getSensorInfo

        Keyword arguments:
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global getSensorInfoCounter
        getSensorInfoCounter += 1
        logger.debug(f'getSensorInfoCounter = {getSensorInfoCounter}')

        return self.name, self.author, self.version, self.description

    def loadSensor(self, sensorId, configurationInfo):
        """loadSensor

        Keyword arguments:
        sensorId -- 
        configurationInfo -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global loadSensorCounter
        loadSensorCounter += 1
        logger.debug(f'loadSensorCounter = {loadSensorCounter}')

        self.sensorConfigurationDict[sensorId] = configurationInfo

    def saveSensor(self, sensorId):
        """saveSensor

        Keyword arguments:
        sensorId -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global saveSensorCounter
        saveSensorCounter += 1
        logger.debug(f'saveSensorCounter = {saveSensorCounter}')

        return self.sensorConfigurationDict[sensorId]


class PositionGenerator(SensorConfig, SensorInfo):
    def __init__(self):
        """__init__

        """     
        super().__init__()   
        
    def initializePosGenRelatedMap(self, sensorId, posGenId, objectName):
        """initializePosGenRelatedMap

        Keyword arguments:
        sensorId -- 
        posGenId -- 
        objectName -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global initializePosGenRelatedMapCounter
        initializePosGenRelatedMapCounter += 1
        logger.debug(f'initializePosGenRelatedMapCounter = {initializePosGenRelatedMapCounter}')

        self.posGenSensorMapDict[posGenId] = sensorId
        self.posGenObjectMapDict[posGenId] = objectName
    
    def configurePosGen(self, posGenId):
        """initializePosGenRelatedMap

        Keyword arguments:
        posGenId -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global configurePosGenCounter
        configurePosGenCounter += 1
        logger.debug(f'configurePosGenCounter = {configurePosGenCounter}')

        # users should implement the position generator configuration logic in their class. The content must contain the following parts:
        # Step 1: if configure for the first time, skip step 1.
        #         Otherwise, find the configurationInfo string by self.posGenConfigurationDict[posGenId]
        #         and analyze it to get the configuration setting from last time.
        # Step 2: configuration logic defined by users.
        # Step 3: parse the configuration data into one string and update it in self.posGenConfigurationDict[posGenId].
        pass
        
    def loadPosGen(self, posGenId, positionGeneratorInfo):
        """loadPosGen

        Keyword arguments:
        posGenId -- 
        positionGeneratorInfo --
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global loadPosGenCounter
        loadPosGenCounter += 1
        logger.debug(f'loadPosGenCounter = {loadPosGenCounter}')

        self.posGenConfigurationDict[posGenId] = positionGeneratorInfo
        
    def savePosGen(self, posGenId):
        """savePosGen

        Keyword arguments:
        posGenId -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global savePosGenCounter
        savePosGenCounter += 1
        logger.debug(f'savePosGenCounter = {savePosGenCounter}')

        return self.posGenConfigurationDict[posGenId]


class SensorRuntime(PositionGenerator, SensorConfig, SensorInfo):
    def __init__(self):
        """__init__

        """     
        super().__init__()   
        self.recipeStatus = 0
        self.monitorThread = 0

    def startSensor(self, callBackFunc):
        """startSensor

        Keyword arguments:
        callBackFunc -- 
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global startSensorCounter
        startSensorCounter += 1
        logger.debug(f'startSensorCounter = {startSensorCounter}')

        # users should implement the start logic in their class. The content must contain the following parts:
        # Step 1: call classname.monitorRecipeStatus(self, callBackFunc) to monitor the recipe status running in PMTW.
        # Step 2: start logic defined by users. For each sensor, a StoppableThread must be created to generate positions and appended to self.allThreads.
        # Step 3: start all threads in self.allThreads.
        # Step 4: call classname.waitForRecipeStop(self) to wait for the stop signal from PMTW.
        # Step 5: stop all threads in self.allThreads. Note that the stop behavior of startSensor interface should be handled by users here.
        #
        # The following information may be helpful:
        # 1. users can use the following dictionaries to find all information:
        #    self.sensorIdNameMapDict
        #    self.sensorConfigurationDict
        #    self.posGenConfigurationDict
        #    self.posGenSensorMapDict
        #    self.posGenObjectMapDict
        # 2. after the sensor is triggered, users should call callBackFunc.GetStrobeTime() to get the strobe time from PMTW.
        # 3. after position is generated, users should call callBackFunc.NewPosition(pos) to send positions to PMTW.
        # 4. the format of position should be (more details refer to user guide document):
        #    newPos = {'SensorId': sensorId,
        #              'Time': strobeTime,
        #              'key':   {'X': 0.0,
        #                        'Y': 100.0,
        #                        'Z': 5.0,
        #                        'RX': 0.0,
        #                        'RY': 0.0,
        #                        'RZ': 0.0,
        #                        'Tag': 0,
        #                        'Score': 1.0,
        #                        'Val1': 0.0,
        #                        'Val2': 0.0,
        #                        'Val3': 0.0,
        #                        'Val4': 0.0,
        #                        'Val5': 0.0,
        #                        'Level': 2,
        #                        'PosGenId': posGenId}}
        pass

    def stopSensor(self):
        """startSensor

        Keyword arguments:
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global stopSensorCounter
        stopSensorCounter += 1
        logger.debug(f'stopSensorCounter = {stopSensorCounter}')
        
        # users should implement the stop logic in their class. If there is no specific logic, the interface can keep empty.s
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
            # logger.debug(f'checkRecipeStatus: recipeStatus = {self.recipeStatus}')
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
            # logger.debug(f'waitForRecipeStop: recipeStatus = {self.recipeStatus}')
            time.sleep(1)
            if self.recipeStatus == 0:
                break
        self.monitorThread.stop()
           

class StoppableThread(threading.Thread):
    """StoppableThread
        Tool to realize that the threading.Thread could be stopped.
    """

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
