import ctypes
import threading
import time

class SensorInfo:
    name = "External sensor"
    description = "External sensor interfaces description"
    author = "PMTW developer"
    version = "1.0"
    sensorIdNameMapDict = {}#'sensorId': 'sensorName'
    sensorConfigurationDict = {}#'sensorId': 'configInfo'
    posGenConfigurationDict = {}#'posGenId': 'posGenConfigInfo'
    posGenSensorMapDict = {}#'posGenId': 'sensorId'
    posGenObjectMapDict = {}#'posGenId': 'objectName'
    
    def registerLogCallback(self, logCallBackFunc):
        self.fLogCallback = logCallBackFunc
        self.sensorIdNameMapDict.clear()
        self.sensorConfigurationDict.clear()
        self.posGenConfigurationDict.clear()
        self.posGenSensorMapDict.clear()
        self.posGenObjectMapDict.clear()
        
    def initializeSensorMap(self, sensorId, sensorName):
        self.sensorIdNameMapDict[sensorId] = sensorName

class SensorConfig(SensorInfo):
    def configureSensor(self, sensorId):
        pass

    def getSensorInfo(self):
        return self.name, self.author, self.version, self.description

    def loadSensor(self, sensorId, configurationInfo):
        self.sensorConfigurationDict[sensorId] = configurationInfo

    def saveSensor(self, sensorId):
        return self.sensorConfigurationDict[sensorId]


class PositionGenerator(SensorConfig, SensorInfo):
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
    recipeStatus = 0
    monitorThread = 0
    
    def startSensor(self, callBackFunc):
        pass

    def stopSensor(self):
        pass
        
    def monitorRecipeStatus(self, callBackFunc):
        self.recipeStatus = 1
        self.monitorThread = StoppableThread(target=SensorRuntime.checkRecipeStatus, args=(self, callBackFunc))
        self.monitorThread.start()

    def checkRecipeStatus(self, callBackFunc):
        while True:
            self.recipeStatus = callBackFunc.GetRecipeStatus()
            time.sleep(1)
            if self.recipeStatus == 0:
                break

    def waitForRecipeStop(self):
        while True:
            if self.recipeStatus == 0:
                break
        self.monitorThread.stop()
            


class StoppableThread(threading.Thread):
    def __init__(self, target=None, args=(), kwargs=None, daemon=True):
        super(StoppableThread, self).__init__(target=target, args=args, kwargs=kwargs, daemon=daemon)
        self.flag = threading.Event()

    def stop(self):
        if not self.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), exc)
        if res == 0:
            raise ValueError("cannot find thread id")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            raise SystemError("Thread is stopped")
