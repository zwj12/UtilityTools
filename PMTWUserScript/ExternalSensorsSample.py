# ExternalSensorSamples
from ExternalSensorInterface import StoppableThread
from ExternalSensorInterface import SensorInfo
from ExternalSensorInterface import SensorConfig
from ExternalSensorInterface import PositionGenerator
from ExternalSensorInterface import SensorRuntime
import tkinter as tk
import operator as op
import time
import CognexFunctionsSample
import SickFunctionsSample
import logging
import os
import sys

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWExternalSensor.log'
configureSensorCounter = 0
configurePosGenCounter = 0
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

    def __init__(self):
        """__init__

        """
        self.name = "Example: external sensor"
        self.description = "Example: external sensor description"
        self.author = "Example: PMTW developer"
        self.version = "Example: 1.0"
        self.allThreads=[]
        self.allSensors=[] 

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

        if(self.sensorIdNameMapDict.get(sensorId) == None):
            logger.error(f'{sensorId} is not in sensorIdNameMapDict');
            return               
                
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':
            inputTitle: str = "ExternalSensor_1 configuration"            
            sensor1 = SickFunctionsSample.SickFunctions()            
            if sensorId in self.sensorConfigurationDict.keys():
                logger.debug(f'ShowSensorConfigDialog: {sensorId} {self.sensorConfigurationDict[sensorId]}')
                configurationInfo = sensor1.showSensorConfigDialogSICK(inputTitle, self.sensorConfigurationDict[sensorId])
            else:
                logger.debug(f'ShowSensorConfigDialog: {sensorId} "0"')
                configurationInfo = sensor1.showSensorConfigDialogSICK(inputTitle, "0")            
            log = {'LogLevel': 0, 'Log': configurationInfo}
            logger.debug(f'log = {log}')
            if(hasattr(self, 'fLogCallback')):
                self.fLogCallback.ShowPythonLog(log)
        else:
            inputTitle: str = "ExternalSensor_2 configuration"
            sensor2 = CognexFunctionsSample.CognexFunctions()
            if sensorId in self.sensorConfigurationDict.keys():
                logger.debug(f'ShowSensorConfigDialog: {sensorId} {self.sensorConfigurationDict[sensorId]}')
                configurationInfo = sensor2.showSensorConfigDialogCognex(inputTitle, self.sensorConfigurationDict[sensorId])
            else:
                logger.debug(f'ShowSensorConfigDialog: {sensorId} "0"')
                configurationInfo = sensor2.showSensorConfigDialogCognex(inputTitle, "0")
            log = {'LogLevel': 0, 'Log': configurationInfo}
            logger.debug(f'log = {log}')
            if(hasattr(self, 'fLogCallback')):
                self.fLogCallback.ShowPythonLog(log)
        self.sensorConfigurationDict[sensorId] = configurationInfo

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        logger.debug(f'posGenConfigurationDict = {self.posGenConfigurationDict}')     
        logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')
        logger.debug(f'posGenObjectMapDict = {self.posGenObjectMapDict}')

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

        if(self.posGenSensorMapDict.get(posGenId) == None):
            logger.error(f'{posGenId} is not in posGenSensorMapDict');
            return   

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        if(self.sensorIdNameMapDict.get(self.posGenSensorMapDict[posGenId]) == None):
            logger.error(f'{self.posGenSensorMapDict[posGenId]} is not in sensorIdNameMapDict');
            return   
                
        if self.sensorIdNameMapDict[self.posGenSensorMapDict[posGenId]] == 'ExternalSensor_1':
            inputTitle: str = "ExternalSensor_1 PosGen configuration"
            sensor1 = SickFunctionsSample.SickFunctions()
            if posGenId in self.posGenConfigurationDict.keys():
                logger.debug(f'ShowPosGenConfigDialog: {posGenId} {self.posGenConfigurationDict[posGenId]}')
                positionGeneratorInfo = sensor1.showPosGenConfigDialogSICK(inputTitle, self.posGenConfigurationDict[posGenId])
            else:
                logger.debug(f'ShowPosGenConfigDialog: {posGenId} “0”')
                positionGeneratorInfo = sensor1.showPosGenConfigDialogSICK(inputTitle, "0")

            log = {'LogLevel': 0, 'Log': positionGeneratorInfo}
            logger.debug(f'log = {log}')
            if(hasattr(self, 'fLogCallback')):
                self.fLogCallback.ShowPythonLog(log)
        else:
            inputTitle: str = "ExternalSensor_2 PosGen configuration"
            sensor2 = CognexFunctionsSample.CognexFunctions()
            if posGenId in self.posGenConfigurationDict.keys():
                positionGeneratorInfo = sensor2.showPosGenConfigDialogCognex(inputTitle, self.posGenConfigurationDict[posGenId])
            else:
                positionGeneratorInfo = sensor2.showPosGenConfigDialogCognex(inputTitle, "0")

            log = {'LogLevel': 0, 'Log': positionGeneratorInfo}
            logger.debug(f'log = {log}')
            if(hasattr(self, 'fLogCallback')):
                self.fLogCallback.ShowPythonLog(log)
        self.posGenConfigurationDict[posGenId] = positionGeneratorInfo

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        logger.debug(f'sensorConfigurationDict = {self.sensorConfigurationDict}')
        logger.debug(f'posGenConfigurationDict = {self.posGenConfigurationDict}')     
        logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')
        logger.debug(f'posGenObjectMapDict = {self.posGenObjectMapDict}')

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
            ExternalSensorsSample.monitorRecipeStatus(self, callBackFunc)

            logger.debug(f'posGenSensorMapDict = {self.posGenSensorMapDict}')  
            logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')  
            for posGenId in self.posGenSensorMapDict:
                sensorId = self.posGenSensorMapDict[posGenId]
                windowTitle = self.sensorIdNameMapDict[sensorId] + ' ' + self.posGenObjectMapDict[posGenId]
                logger.debug(f'windowTitle = {windowTitle}')  
                if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':
                    # thread_1 = Thread(target=SickFunctions.showStartDialogSICK, args=(callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    # SickFunctions.OpenCamera("40048608")
                    sensor1 = SickFunctionsSample.SickFunctions()
                    thread_1 = StoppableThread(target=sensor1.showStartDialogSICK
                                               , args=(callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    self.allThreads.append(thread_1)
                    self.allSensors.append(sensor1)
                elif self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_2':
                    # thread_2 = Thread(target=CognexFunctions.showStartDialogCognex, args=(callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    # CognexFunctions.OpenCamera("40048606")
                    sensor2 = CognexFunctionsSample.CognexFunctions()
                    thread_2 = StoppableThread(target=sensor2.showStartDialogCognex
                                               , args=(callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    self.allThreads.append(thread_2)
                    self.allSensors.append(sensor2)
            
            logger.debug(f'Trying to start all threads')  
            for td in self.allThreads:
                td.start() 
            logger.debug(f'All threads are started')  

            ExternalSensorsSample.waitForRecipeStop(self)

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
        es.loadPosGen('B460FC85-640B-4384-ABB4-3A75828A76E8', 'Position generator 1:SICK Algorithm 1,10,10,10')
        es.loadPosGen('B460FC85-640B-4384-ABB4-3A75828A76E9', 'Position generator 1:Geometric model')
        es.configurePosGen('B460FC85-640B-4384-ABB4-3A75828A76E8')
        es.configurePosGen('B460FC85-640B-4384-ABB4-3A75828A76E9')

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
