# ExternalSensors
from ExternalSensorInterface import StoppableThread
from ExternalSensorInterface import SensorInfo
from ExternalSensorInterface import SensorConfig
from ExternalSensorInterface import PositionGenerator
from ExternalSensorInterface import SensorRuntime
import tkinter as tk
import operator as op
import time
import CognexFunctions
import SickFunctions
import logging
import os
import sys

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWExternalSensor.log'
configureSensorCounter = 0

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
    logger = logging.getLogger('PickMasterTwin')
    if logger.hasHandlers() == False:
        logger.setLevel(logging.DEBUG)
        # logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler(logFilePath)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger

class ExternalSensors(SensorRuntime, PositionGenerator, SensorConfig, SensorInfo):
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
        sensorId -- sensor id
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global configureSensorCounter
        configureSensorCounter += 1
        logger.debug(f'configureSensorCounter = {configureSensorCounter}')

        logger.debug(f'sensorIdNameMapDict = {self.sensorIdNameMapDict}')
        if(self.sensorIdNameMapDict.get(sensorId) == None):
            logger.error(f'{sensorId} is not in sensorIdNameMapDict');
            return               
                
        logger.debug(f'sensorIdNameMapDict = {self.sensorConfigurationDict}')
        if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':
            inputTitle: str = "ExternalSensor_1 configuration"            
            sensor1 = SickFunctions.SickFunctions()            
            if sensorId in self.sensorConfigurationDict.keys():
                logger.debug(f'SensorConfigDialog: {sensorId} {self.sensorConfigurationDict[sensorId]}')
                configurationInfo = sensor1.showSensorConfigDialogSICK(inputTitle, self.sensorConfigurationDict[sensorId])
            else:
                logger.debug(f'SensorConfigDialog: {sensorId} "0"')
                configurationInfo = sensor1.showSensorConfigDialogSICK(inputTitle, "0")            
            log = {'LogLevel': 0, 'Log': configurationInfo}
            logger.debug(f'log = {log}')
            if(hasattr(self, 'fLogCallback')):
                self.fLogCallback.ShowPythonLog(log)
        else:
            inputTitle: str = "ExternalSensor_2 configuration"
            sensor2 = CognexFunctions.CognexFunctions()
            if sensorId in self.sensorConfigurationDict.keys():
                logger.debug(f'SensorConfigDialog: {sensorId} {self.sensorConfigurationDict[sensorId]}')
                configurationInfo = sensor2.showSensorConfigDialogCognex(inputTitle, self.sensorConfigurationDict[sensorId])
            else:
                logger.debug(f'SensorConfigDialog: {sensorId} "0"')
                configurationInfo = sensor2.showSensorConfigDialogCognex(inputTitle, "0")
            log = {'LogLevel': 0, 'Log': configurationInfo}
            logger.debug(f'log = {log}')
            if(hasattr(self, 'fLogCallback')):
                self.fLogCallback.ShowPythonLog(log)
        self.sensorConfigurationDict[sensorId] = configurationInfo

    def configurePosGen(self, posGenId):
        if self.sensorIdNameMapDict[self.posGenSensorMapDict[posGenId]] == 'ExternalSensor_1':
            inputTitle: str = "ExternalSensor_1 PosGen configuration"
            sensor1 = SickFunctions.SickFunctions()
            if posGenId in self.posGenConfigurationDict.keys():
                positionGeneratorInfo = sensor1.showPosGenConfigDialogSICK(inputTitle,
                                                                        self.posGenConfigurationDict[posGenId])
            else:
                positionGeneratorInfo = sensor1.showPosGenConfigDialogSICK(inputTitle, "0")

            log = {'LogLevel': 0,
                   'Log': positionGeneratorInfo}
            self.fLogCallback.ShowPythonLog(log)
        elif self.sensorIdNameMapDict[self.posGenSensorMapDict[posGenId]] == 'ExternalSensor_2':
            inputTitle: str = "ExternalSensor_2 PosGen configuration"
            sensor2 = CognexFunctions.CognexFunctions()
            if posGenId in self.posGenConfigurationDict.keys():
                positionGeneratorInfo = sensor2.showPosGenConfigDialogCognex(inputTitle,
                                                                        self.posGenConfigurationDict[posGenId])
            else:
                positionGeneratorInfo = sensor2.showPosGenConfigDialogCognex(inputTitle, "0")

            log = {'LogLevel': 0,
                   'Log': positionGeneratorInfo}
            self.fLogCallback.ShowPythonLog(log)
        self.posGenConfigurationDict[posGenId] = positionGeneratorInfo

    def startSensor(self, callBackFunc):
        try:
            ExternalSensors.monitorRecipeStatus(self, callBackFunc)

            for posGenId in self.posGenSensorMapDict:
                sensorId = self.posGenSensorMapDict[posGenId]
                windowTitle = self.sensorIdNameMapDict[sensorId] + ' ' + self.posGenObjectMapDict[posGenId]
                if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':
                    # thread_1 = Thread(target=SickFunctions.showStartDialogSICK, args=(callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    # SickFunctions.OpenCamera("40048608")
                    sensor1 = SickFunctions.SickFunctions()
                    thread_1 = StoppableThread(target=sensor1.showStartDialogSICK, args=(
                    callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    self.allThreads.append(thread_1)
                    self.allSensors.append(sensor1)
                elif self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_2':
                    # thread_2 = Thread(target=CognexFunctions.showStartDialogCognex, args=(callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    # CognexFunctions.OpenCamera("40048606")
                    sensor2 = CognexFunctions.CognexFunctions()
                    thread_2 = StoppableThread(target=sensor2.showStartDialogCognex, args=(
                    callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    self.allThreads.append(thread_2)
                    self.allSensors.append(sensor2)
            
            for td in self.allThreads:
                td.start() 
                
            ExternalSensors.waitForRecipeStop(self)

            for sensor in self.allSensors:
                sensor.server.close()

            for td in self.allThreads:
                td.stop()            
            
            log = {'LogLevel': 0, 'Log': "StartSensor: stopped all threads."}
            self.fLogCallback.ShowPythonLog(log)
        except:
            log = {'LogLevel': 2,
                   'Log': "Python Error: Failed to start sensor"}
            self.fLogCallback.ShowPythonLog(log)

    def stopSensor(self):
        log = {'LogLevel': 0,
               'Log': "Python info: stop sensor"}
        self.fLogCallback.ShowPythonLog(log)


def main(argv):
    """main

    """
    print("Run from main: ", argv)
    try:
        logger = get_logging()
        logger.debug(argv)
        es = ExternalSensors()
        es.initializeSensorMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C04', 'ExternalSensor_1')
        es.initializeSensorMap('325D3EB5-B563-4F90-B0C5-2F1E770D5C05', 'ExternalSensor_2')
        es.configureSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C05')

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
