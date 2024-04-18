# This software is provided 'as-is', without any express or
# implied warranty. In no event will ABB be held liable for 
# any damages arising from the use of this software.

# ExternalSensorUDP
# users should import all four base classes and the StoppableThread tool class from ExternalSensorInterface.
from ExternalSensorInterfaceSample import StoppableThread
from ExternalSensorInterfaceSample import SensorInfo
from ExternalSensorInterfaceSample import SensorConfig
from ExternalSensorInterfaceSample import PositionGenerator
from ExternalSensorInterfaceSample import SensorRuntime
from ExternalSensorsUtilitySample import ExternalSensorsUtility
from SensorFunctionsSample import SensorFunctions
import threading
import sys, traceback
import logging
import os
import time

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWExternalSensorUDP.log'
configureSensorCounter = 0
configurePosGenCounter = 0
startSensorCounter = 0
stopSensorCounter = 0
exceptHookCounter = 0

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
    logger = logging.getLogger('PMTWExternalSensorUDP')
    if logger.hasHandlers() == False:
        logger.setLevel(logging.DEBUG)
        # logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler(logFilePath)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger

class ExternalSensorUDPSample(SensorRuntime, PositionGenerator, SensorConfig, SensorInfo):
    """ExternalSensorUDPSample

    """

    def __init__(self):
        """__init__

        """
        super().__init__()
        self.name = "ExternalSensorUDP"
        self.description =  "The ExternalSensorUDP is an implemented Python solution based on the PickMaster Twin External" \
                            " Sensor function. The solution can receive item positions in all three dimensions and parameters" \
                            " from any kind of positions sensor represented by a UDP client and send them to Runtime to" \
                            " coordinate the robot pick & place operations."
        self.author = "ABB"
        self.version = "1.1"
        self.allThreads=[]
        self.allSensors=[]    

    def exceptHook(self, *args):
        """configureSensor

        Keyword arguments:
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global exceptHookCounter
        exceptHookCounter += 1
        logger.debug(f'exceptHookCounter = {exceptHookCounter}')

        tbType, tbValue, tbTraceback, _ = args[0]
        argsList = []
        i = 0
        while  i < len(tbValue.args) and i < 2:
            argsList.append(str(tbValue.args[i]))
            i += 1
        errorMessage = ", ".join(argsList)
        tracebackMessage = str(traceback.format_exception(tbType, tbValue, tbTraceback))
        logMessage = "[ExternalSensor] {}. {}".format(errorMessage, tracebackMessage)
        log = {'LogLevel': 2, 'Log': logMessage}
        logger.debug(f'log = {log}')
        if(hasattr(self, 'fLogCallback')):
            self.fLogCallback.ShowPythonLog(log)
       
    sys.excepthook = exceptHook
    
    def configureSensor(self, sensorId):# this interface must be implemented by users.
        """configureSensor

        Keyword arguments:
        sensorId -- '325D3EB5-B563-4F90-B0C5-2F1E770D5C04'
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')
        
        global configureSensorCounter
        configureSensorCounter += 1
        logger.debug(f'configureSensorCounter = {configureSensorCounter}')
        
        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        logger.debug(f'posGenConfigurationDict = {self.posGenConfigurationDict}')     
        logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')
        logger.debug(f'posGenObjectMapDict = {self.posGenObjectMapDict}')
        
        # Step 1 & Step 2:
        # analyze self.sensorConfigurationDict[sensorId] to get the settings from last configuration.
        # user-defined configuration logic.
        inputTitle: str = "Sensor configuration"
        sensor = SensorFunctions()        
                
        if sensorId in self.sensorConfigurationDict.keys():
            inputPort = self.sensorConfigurationDict[sensorId]
        else:
            inputPort = "5000"
                    
        (isPortValid, serverPort) = sensor.showSensorPortConfigDialog(inputTitle, inputPort, self.fLogCallback)

        # Step 3:
        # parse the configuration data into one string and update it in self.sensorConfigurationDict[sensorId].
        if(isPortValid):
            self.sensorConfigurationDict[sensorId] = serverPort

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        logger.debug(f'posGenConfigurationDict = {self.posGenConfigurationDict}')     
        logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')
        logger.debug(f'posGenObjectMapDict = {self.posGenObjectMapDict}')

    def configurePosGen(self, positionGeneratorId):# this interface must be implemented by users.
        """configurePosGen

        Keyword arguments:
        posGenId -- 'B460FC85-640B-4384-ABB4-3A75828A76E8'
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global configurePosGenCounter
        configurePosGenCounter += 1
        logger.debug(f'configurePosGenCounter = {configurePosGenCounter}')

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        logger.debug(f'posGenConfigurationDict = {self.posGenConfigurationDict}')     
        logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')
        logger.debug(f'posGenObjectMapDict = {self.posGenObjectMapDict}')

        # Step 1 & Step 2:
        # analyze self.posGenConfigurationDict[positionGeneratorId] to get the settings from last configuration.
        # user-defined configuration logic.

        inputTitle: str = "Position generator configuration"
        sensor = SensorFunctions()

        if positionGeneratorId in self.posGenConfigurationDict.keys():
            inputIndex = self.posGenConfigurationDict[positionGeneratorId]
        else:
            inputIndex = "0"
            
        (isIndexValid, positionGeneratorIndex) = sensor.showPositionGeneratorConfigDialog(inputTitle, inputIndex, self.fLogCallback)
        
        # # Step 3: 
        # # parse the configuration data into one string and update it in self.posGenConfigurationDict[positionGeneratorId].
        if(isIndexValid):
            self.posGenConfigurationDict[positionGeneratorId] = positionGeneratorIndex

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        logger.debug(f'posGenConfigurationDict = {self.posGenConfigurationDict}')     
        logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')
        logger.debug(f'posGenObjectMapDict = {self.posGenObjectMapDict}')

    def startSensor(self, callBackFunc):# this interface must be implemented by users.
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

        try:
            # Step 1: call classname.monitorRecipeStatus(self, callBackFunc) to monitor the recipe status running in PMTW.
            ExternalSensorUDPSample.monitorRecipeStatus(self, callBackFunc)
            
            # Step 2: start logic defined by users. For each sensor, a StoppableThread must be created to generate positions and appended to self.allThreads.
            for positionGeneratorId in self.posGenSensorMapDict:
                sensorId = self.posGenSensorMapDict[positionGeneratorId]
                sensor = SensorFunctions()
                sensor.sensorName = self.sensorIdNameMapDict[sensorId]
                thread = StoppableThread(target=sensor.startSensor, args=(callBackFunc, sensorId, positionGeneratorId, 
                                                                            self.sensorConfigurationDict[sensorId],
                                                                            self.posGenConfigurationDict[positionGeneratorId], 
                                                                            self.fLogCallback))
                self.allThreads.append(thread)
                self.allSensors.append(sensor)
            
            # Step 3: start all threads in self.allThreads.
            threading.excepthook = self.exceptHook
            for td in self.allThreads:
                td.start()
                
            # Step 4: call classname.waitForRecipeStop(self) to wait for the stop signal from PMTW.
            ExternalSensorUDPSample.waitForRecipeStop(self)

            # Step 5: stop all threads in self.allThreads. Note that the stop behavior of startSensor interface should be handled by users here.
            for sensor in self.allSensors:
                sensor.isRunning = False
                sensor.server.close()

            for td in self.allThreads:
                td.stop()

            logMessage = "[ExternalSensorUDP] {}.".format("StartSensor: all threads stopped")
            log = {'LogLevel': 0, 'Log': logMessage}
            self.fLogCallback.ShowPythonLog(log)
            
        except:
            logMessage = "[ExternalSensorUDP] {}.".format("Python Error: Failed to start sensor")
            log = {'LogLevel': 2, 'Log': logMessage}
            self.fLogCallback.ShowPythonLog(log)
            
    def stopSensor(self):# this interface must be implemented by users.
        logMessage = "[ExternalSensorUDP] {}.".format("StopSensor: stop sensor")
        log = {'LogLevel': 0, 'Log': logMessage}
        self.fLogCallback.ShowPythonLog(log)


def main(argv):
    """main

    """
    print("Run from main: ", argv)
    try:
        logger = get_logging()
        logger.debug(argv)

        utility = ExternalSensorsUtility()
        es = ExternalSensorUDPSample()
        es.registerLogCallback(utility)
        
        es.loadSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C04', '8887')
        es.loadSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C05', '8888')
        es.initializeSensorMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C04', 'ExternalSensor_1')
        es.initializeSensorMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C05', 'ExternalSensor_2')        

        es.configureSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C04')
        es.configureSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C05')
        
        es.initializePosGenRelatedMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C04','B460FC85-640B-4384-ABB4-3A75828A76E8',"Item_1")
        es.initializePosGenRelatedMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C05','B460FC85-640B-4384-ABB4-3A75828A76E9',"Item_2")
        es.loadPosGen('B460FC85-640B-4384-ABB4-3A75828A76E8', '3')
        es.loadPosGen('B460FC85-640B-4384-ABB4-3A75828A76E9', '4')
        
        es.configurePosGen('B460FC85-640B-4384-ABB4-3A75828A76E8')
        es.configurePosGen('B460FC85-640B-4384-ABB4-3A75828A76E9')       

        # print(f'sensorIdNameMapDict = {es.sensorIdNameMapDict}')
        # print(f'sensorConfigurationDict = {es.sensorConfigurationDict}')
        # print(f'posGenConfigurationDict = {es.posGenConfigurationDict}')     
        # print(f'posGenSensorMapDict = {es.posGenSensorMapDict}')
        # print(f'posGenObjectMapDict = {es.posGenObjectMapDict}')

        
        es.startSensor(utility)        
        print("Sensors started")
        time.sleep(30)
        es.stopSensor()
        print("Sensors stopped")

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