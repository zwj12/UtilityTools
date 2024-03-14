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


class ExternalSensors(SensorRuntime, PositionGenerator, SensorConfig, SensorInfo):
    name = "Example: external sensor"
    description = "Example: external sensor description"
    author = "Example: PMTW developer"
    version = "Example: 1.0"

    allThreads=[]
    allSensors=[]

    def configureSensor(self, sensorId):
        self.name = "ExternalSensors"
        if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':
            inputTitle: str = "ExternalSensor_1 configuration"
            sensor1 = SickFunctions.SickFunctions()
            if sensorId in self.sensorConfigurationDict.keys():
                configurationInfo = sensor1.showSensorConfigDialogSICK(inputTitle,
                                                                             self.sensorConfigurationDict[sensorId])
            else:
                configurationInfo = sensor1.showSensorConfigDialogSICK(inputTitle, "0")

            log = {'LogLevel': 0,
                   'Log': configurationInfo}
            self.fLogCallback.ShowPythonLog(log)
        elif self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_2':
            inputTitle: str = "ExternalSensor_2 configuration"
            sensor2 = CognexFunctions.CognexFunctions()
            if sensorId in self.sensorConfigurationDict.keys():
                configurationInfo = sensor2.showSensorConfigDialogCognex(inputTitle,
                                                                                 self.sensorConfigurationDict[sensorId])
            else:
                configurationInfo = sensor2.showSensorConfigDialogCognex(inputTitle, "0")

            log = {'LogLevel': 0,
                   'Log': configurationInfo}
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
