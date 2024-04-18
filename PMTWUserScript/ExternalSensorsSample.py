# ExternalSensorSamples
from ExternalSensorInterfaceSample import StoppableThread
from ExternalSensorInterfaceSample import SensorInfo
from ExternalSensorInterfaceSample import SensorConfig
from ExternalSensorInterfaceSample import PositionGenerator
from ExternalSensorInterfaceSample import SensorRuntime
from ExternalSensorsUtilitySample import ExternalSensorsUtility
import tkinter as tk
import operator as op
import time
import Sensor1FunctionsSample
import Sensor2FunctionsSample
import logging
import os
import sys
import traceback

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWExternalSensor.log'
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
    logger = logging.getLogger('PMTWExternalSensor')
    if logger.hasHandlers() == False:
        logger.setLevel(logging.DEBUG)
        # logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler(logFilePath)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger

class ExternalSensorsSample(SensorRuntime, PositionGenerator, SensorConfig, SensorInfo):
    """ExternalSensors

    """

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

    def __init__(self):
        """__init__

        """
        super().__init__()
        self.name = "Example: external sensor"
        self.description = "Example: external sensor description"
        self.author = "Example: PMTW developer"
        self.version = "Example: 1.0"
        self.allThreads=[]
        self.allSensors=[] 

    # this interface must be implemented by users.
    def configureSensor(self, sensorId):
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
        
        if(self.sensorIdNameMapDict.get(sensorId) == None):
            logger.error(f'{sensorId} is not in sensorIdNameMapDict');
            return               
                
        configurationInfo = "0"
        if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':
            inputTitle: str = "ExternalSensor_1 configuration"       
            sensor1 = Sensor1FunctionsSample.Sensor1Functions()
            if sensorId in self.sensorConfigurationDict.keys():
                logger.debug(f'ShowSensorConfigDialog: {sensorId} {self.sensorConfigurationDict[sensorId]}')
                configurationInfo = sensor1.showSensorConfigDialog(inputTitle, self.sensorConfigurationDict[sensorId])
            else:
                logger.debug(f'ShowSensorConfigDialog: {sensorId} "0"')
                configurationInfo = sensor1.showSensorConfigDialog(inputTitle, "0")    
        else:
            inputTitle: str = "ExternalSensor_2 configuration"
            sensor2 = Sensor2FunctionsSample.Sensor2Functions()
            if sensorId in self.sensorConfigurationDict.keys():
                logger.debug(f'ShowSensorConfigDialog: {sensorId} {self.sensorConfigurationDict[sensorId]}')
                configurationInfo = sensor2.showSensorConfigDialog(inputTitle, self.sensorConfigurationDict[sensorId])
            else:
                logger.debug(f'ShowSensorConfigDialog: {sensorId} "0"')
                configurationInfo = sensor2.showSensorConfigDialog(inputTitle, "0")

        log = {'LogLevel': 0, 'Log': configurationInfo}
        logger.debug(f'log = {log}')
        if(hasattr(self, 'fLogCallback')):
            self.fLogCallback.ShowPythonLog(log)

        # Step 3:
        # parse the configuration data into one string and update it in self.sensorConfigurationDict[sensorId].
        self.sensorConfigurationDict[sensorId] = configurationInfo

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        logger.debug(f'posGenConfigurationDict = {self.posGenConfigurationDict}')     
        logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')
        logger.debug(f'posGenObjectMapDict = {self.posGenObjectMapDict}')

    # this interface must be implemented by users.
    def configurePosGen(self, posGenId):
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
        # analyze self.posGenConfigurationDict[posGenId] to get the settings from last configuration.
        # user-defined configuration logic.

        if(self.posGenSensorMapDict.get(posGenId) == None):
            logger.error(f'{posGenId} is not in posGenSensorMapDict');
            return   

        if(self.sensorIdNameMapDict.get(self.posGenSensorMapDict[posGenId]) == None):
            logger.error(f'{self.posGenSensorMapDict[posGenId]} is not in sensorIdNameMapDict');
            return   
        
        positionGeneratorInfo = "0"
        if self.sensorIdNameMapDict[self.posGenSensorMapDict[posGenId]] == 'ExternalSensor_1':
            inputTitle: str = "ExternalSensor_1 PosGen configuration"
            sensor1 = Sensor1FunctionsSample.Sensor1Functions()
            if posGenId in self.posGenConfigurationDict.keys():
                logger.debug(f'ShowPosGenConfigDialog: {posGenId} {self.posGenConfigurationDict[posGenId]}')                
                positionGeneratorInfo = sensor1.showPosGenConfigDialog(inputTitle, self.posGenConfigurationDict[posGenId])                
            else:
                logger.debug(f'ShowPosGenConfigDialog: {posGenId} “0”')
                positionGeneratorInfo = sensor1.showPosGenConfigDialog(inputTitle, "0")
        else:
            inputTitle: str = "ExternalSensor_2 PosGen configuration"
            sensor2 = Sensor2FunctionsSample.Sensor2Functions()
            if posGenId in self.posGenConfigurationDict.keys():
                logger.debug(f'ShowPosGenConfigDialog: {posGenId} {self.posGenConfigurationDict[posGenId]}')
                positionGeneratorInfo = sensor2.showPosGenConfigDialog(inputTitle, self.posGenConfigurationDict[posGenId])
            else:
                logger.debug(f'ShowPosGenConfigDialog: {posGenId} “0”')
                positionGeneratorInfo = sensor2.showPosGenConfigDialog(inputTitle, "0")

        log = {'LogLevel': 0, 'Log': positionGeneratorInfo}
        logger.debug(f'log = {log}')
        if(hasattr(self, 'fLogCallback')):
            self.fLogCallback.ShowPythonLog(log)

        # Step 3: 
        # parse the configuration data into one string and update it in self.posGenConfigurationDict[posGenId].
        self.posGenConfigurationDict[posGenId] = positionGeneratorInfo

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        logger.debug(f'posGenConfigurationDict = {self.posGenConfigurationDict}')     
        logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')
        logger.debug(f'posGenObjectMapDict = {self.posGenObjectMapDict}')

    # this interface must be implemented by users.
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

        try:
            # Step 1: call classname.monitorRecipeStatus(self, callBackFunc) to monitor the recipe status running in PMTW.
            ExternalSensorsSample.monitorRecipeStatus(self, callBackFunc)

            logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')  
            logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')  

            # Step 2: start logic defined by users. For each sensor, a StoppableThread must be created to generate positions and appended to self.allThreads.
            for posGenId in self.posGenSensorMapDict:
                sensorId = self.posGenSensorMapDict[posGenId]
                windowTitle = self.sensorIdNameMapDict[sensorId] + ' ' + self.posGenObjectMapDict[posGenId]
                logger.debug(f'windowTitle = {windowTitle}')  
                if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':
                    sensor1 = Sensor1FunctionsSample.Sensor1Functions()
                    thread_1 = StoppableThread(target=sensor1.startSensor
                                               , args=(callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    self.allThreads.append(thread_1)
                    self.allSensors.append(sensor1)
                    # thread_1.start()
                    logger.debug(f'Add sensor 1: {self.sensorIdNameMapDict[sensorId]}')
                else:
                    sensor2 = Sensor2FunctionsSample.Sensor2Functions()
                    thread_2 = StoppableThread(target=sensor2.startSensor
                                               , args=(callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    self.allThreads.append(thread_2)
                    self.allSensors.append(sensor2)
                    # thread_2.start()
                    logger.debug(f'Add sensor 2: {self.sensorIdNameMapDict[sensorId]}')
            
            # Step 3: start all threads in self.allThreads.
            logger.debug(f'Trying to start all threads')  
            for td in self.allThreads:
                td.start() 
            logger.debug(f'All threads are started')  

            # Step 4: call classname.waitForRecipeStop(self) to wait for the stop signal from PMTW.
            ExternalSensorsSample.waitForRecipeStop(self)

            # Step 5: stop all threads in self.allThreads. Note that the stop behavior of startSensor interface should be handled by users here.
            logger.debug(f'Trying to close sensor servers')  
            for sensor in self.allSensors:
                sensor.server.close()
            logger.debug(f'All the sensor servers are closed')  

            logger.debug(f'Trying to stop all threads')  
            for td in self.allThreads:
                td.stop()            
            logger.debug(f'All threads are stopped')  

            log = {'LogLevel': 0, 'Log': "StartSensor: stopped all threads."}
            logger.debug(f'log = {log}')  
            if(hasattr(self, 'fLogCallback')):
                self.fLogCallback.ShowPythonLog(log)
        except:
            log = {'LogLevel': 2, 'Log': "Python Error: Failed to start sensor"}
            logger.debug(f'log = {log}')  
            if(hasattr(self, 'fLogCallback')):
                self.fLogCallback.ShowPythonLog(log)

    # this interface must be implemented by users.
    def stopSensor(self):
        """stopSensor

        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global stopSensorCounter
        stopSensorCounter += 1
        logger.debug(f'stopSensorCounter = {stopSensorCounter}')

        log = {'LogLevel': 0, 'Log': "Python info: stop sensor"}
        logger.debug(f'log = {log}')  
        if(hasattr(self, 'fLogCallback')):
            self.fLogCallback.ShowPythonLog(log)


def main(argv):
    """main

    """
    print("Run from main: ", argv)
    try:
        logger = get_logging()
        logger.debug(argv)

        es = ExternalSensorsSample()
        
        es.loadSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C04', '1;2;3')
        es.loadSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C05', '1;2;3;4;5')
        es.initializeSensorMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C04', 'ExternalSensor_1')
        es.initializeSensorMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C05', 'ExternalSensor_2')
        es.configureSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C04')
        es.configureSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C05')

        es.initializePosGenRelatedMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C04','B460FC85-640B-4384-ABB4-3A75828A76E8',"Item_1")
        es.initializePosGenRelatedMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C05','B460FC85-640B-4384-ABB4-3A75828A76E9',"Item_2")
        es.loadPosGen('B460FC85-640B-4384-ABB4-3A75828A76E8', 'Position generator 1:Algorithm 1 model')
        es.loadPosGen('B460FC85-640B-4384-ABB4-3A75828A76E9', 'Position generator 1:Algorithm 2 model')
        es.configurePosGen('B460FC85-640B-4384-ABB4-3A75828A76E8')
        es.configurePosGen('B460FC85-640B-4384-ABB4-3A75828A76E9')       

        print(f'sensorIdNameMapDict = {es.sensorIdNameMapDict}')
        print(f'sensorConfigurationDict = {es.sensorConfigurationDict}')
        print(f'posGenConfigurationDict = {es.posGenConfigurationDict}')     
        print(f'posGenSensorMapDict = {es.posGenSensorMapDict}')
        print(f'posGenObjectMapDict = {es.posGenObjectMapDict}')

        utility = ExternalSensorsUtility()
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
