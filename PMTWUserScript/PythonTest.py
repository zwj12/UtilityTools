#ExternalSensorsDemo
# users should import all four base classes and the StoppableThread tool class from ExternalSensorInterface.
from ExternalSensorInterface import StoppableThread
from ExternalSensorInterface import SensorInfo
from ExternalSensorInterface import SensorConfig
from ExternalSensorInterface import PositionGenerator
from ExternalSensorInterface import SensorRuntime
import tkinter as tk
import sys
import traceback
import os
import logging

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWExternalSensor.log'
configureSensorCounter = 0
configurePosGenCounter = 0
startSensorCounter = 0
stopSensorCounter = 0
showSensorConfigDialogCounter = 0
showPosGenConfigDialogCounter = 0
showStartDialogCounter = 0
sendNewPositionCounter = 0

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
    
class ExternalSensorsDemo(SensorRuntime, PositionGenerator, SensorConfig, SensorInfo):
    # users should let the new class inherit all four base classes.
    # the class name must be the same as the file name.
    name = "Demo: external sensor"
    description = "Demo: external sensor description"
    author = "Demo: PMTW developer"
    version = "Demo: 1.0"    

    allThreads=[]
    
    def exceptHook(self, *args):
        tbType, tbValue, tbTraceback, _ = args[0]
        argsList = []
        i = 0
        while  i < len(tbValue.args) and i < 2:
            argsList.append(str(tbValue.args[i]))
            i += 1
        errorMessage = ", ".join(argsList)
        tracebackMessage = str(traceback.format_exception(tbType, tbValue, tbTraceback))
        logMessage = "[ExternalSensorDemo] {}. {}".format(errorMessage, tracebackMessage)
        log = {'LogLevel': 2, 'Log': logMessage}
        self.fLogCallback.ShowPythonLog(log)
        
    sys.excepthook = exceptHook
    
    def configureSensor(self, sensorId):# this interface must be implemented by users
        # Step 1 & Step 2:
        # analyze self.sensorConfigurationDict[sensorId] to get the settings from last configuration.
        # user-defined configuration logic.
        self.name = "ExternalSensorsDemo02"
        
        if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':            
            inputTitle = "ExternalSensor_1 configuration"
        elif self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_2':
            inputTitle = "ExternalSensor_2 configuration"
        
        if sensorId in self.sensorConfigurationDict.keys():
            configurationInfo = ExternalSensorsDemo.showSensorConfigDialog(self, inputTitle, self.sensorConfigurationDict[sensorId])
        else:
            configurationInfo = ExternalSensorsDemo.showSensorConfigDialog(self, inputTitle, '0')
        
        log = {'LogLevel': 0,'Log': configurationInfo}
        self.fLogCallback.ShowPythonLog(log)
        # Step 3:
        # parse the configuration data into one string and update it in self.sensorConfigurationDict[sensorId].
        self.sensorConfigurationDict[sensorId] = configurationInfo
        
    def configurePosGen(self, posGenId):# this interface must be implemented by users.
        """configurePosGen
        this interface must be implemented by users.

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
        if self.sensorIdNameMapDict[self.posGenSensorMapDict[posGenId]] == 'ExternalSensor_1':         
            logger.debug("1");
            inputTitle = "ExternalSensor_1 PosGen configuration"
        elif self.sensorIdNameMapDict[self.posGenSensorMapDict[posGenId]] == 'ExternalSensor_2':            
            logger.debug("2");
            inputTitle = "ExternalSensor_2 PosGen configuration"
            
        logger.debug("3");
        
        if posGenId in self.posGenConfigurationDict.keys():
            logger.debug("4");
            positionGeneratorInfo = ExternalSensorsDemo.showPosGenConfigDialog(self, inputTitle, self.posGenConfigurationDict[posGenId])
        else:
            logger.debug("5");
            positionGeneratorInfo = ExternalSensorsDemo.showPosGenConfigDialog(self, inputTitle, "0")
                
        log = {'LogLevel': 0,'Log': positionGeneratorInfo}
        self.fLogCallback.ShowPythonLog(log)
        logger.debug("6");
        # Step 3: 
        # parse the configuration data into one string and update it in self.posGenConfigurationDict[posGenId].
        self.posGenConfigurationDict[posGenId] = positionGeneratorInfo
        logger.debug("7");
        
    def startSensor(self, callBackFunc):# this interface must be implemented by users.
        try:
            # Step 1: call classname.monitorRecipeStatus(self, callBackFunc) to monitor the recipe status running in PMTW.
            ExternalSensorsDemo.monitorRecipeStatus(self, callBackFunc)

            # Step 2: start logic defined by users. For each sensor, a StoppableThread must be created to generate positions and appended to self.allThreads.
            for posGenId in self.posGenSensorMapDict:
                sensorId = self.posGenSensorMapDict[posGenId]
                windowTitle = self.sensorIdNameMapDict[sensorId] + ' ' + self.posGenObjectMapDict[posGenId]
                if self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_1':
                    thread_1 = StoppableThread(target=ExternalSensorsDemo.showStartDialog, args=(self, callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    self.allThreads.append(thread_1)
                elif self.sensorIdNameMapDict[sensorId] == 'ExternalSensor_2':
                    thread_2 = StoppableThread(target=ExternalSensorsDemo.showStartDialog, args=(self, callBackFunc, sensorId, posGenId, self.posGenConfigurationDict[posGenId], windowTitle))
                    self.allThreads.append(thread_2)            
        
            # Step 3: start all threads in self.allThreads.
            for td in self.allThreads:
                td.start() 

            # Step 4: call classname.waitForRecipeStop(self) to wait for the stop signal from PMTW.
            ExternalSensorsDemo.waitForRecipeStop(self)
            
            # Step 5: stop all threads in self.allThreads. Note that the stop behavior of startSensor interface should be handled by users here.
            for td in self.allThreads:
                td.stop()            
            
            log = {'LogLevel': 0, 'Log': "StartSensor: stopped all threads."}
            self.fLogCallback.ShowPythonLog(log)
        except:
            log = {'LogLevel': 2,'Log': "Python Error: Failed to start sensor"}
            self.fLogCallback.ShowPythonLog(log)
       
    def stopSensor(self):# this interface must be implemented by users.
        log = {'LogLevel': 0,'Log': "Python info: stop sensor"}
        self.fLogCallback.ShowPythonLog(log)
        
    def showSensorConfigDialog(self, inputTitle: str, configInfo:str):
        sensorConfigWindow = tk.Tk()
        sensorConfigWindow.title("Sensor: " + inputTitle)
        sensorConfigWindow.geometry("500x250")
        lb1 = tk.Label(sensorConfigWindow, text="Device: ")
        lb1.grid(column=1, row=1)
        txt1 = tk.Entry(sensorConfigWindow, width=30)
        txt1.grid(column=2, row=1)

        lb2 = tk.Label(sensorConfigWindow, text="IP: ")
        lb2.grid(column=1, row=2)
        txt2 = tk.Entry(sensorConfigWindow, width=30)
        txt2.grid(column=2, row=2)

        lb3 = tk.Label(sensorConfigWindow, text="Exposure: ")
        lb3.grid(column=1, row=3)
        txt3 = tk.Entry(sensorConfigWindow, width=30)
        txt3.grid(column=2, row=3)
        
        infos = configInfo.split(';')
        if len(infos) == 3:
            txt1.insert(0, infos[0])
            txt2.insert(1, infos[1])    
            txt3.insert(2, infos[2])
        configureSensorValue = configInfo

        def closeWindow():
            nonlocal configureSensorValue
            configureSensorValue = txt1.get() + ";" + txt2.get() + ";" + txt3.get()
            sensorConfigWindow.destroy()

        sensorConfigWindow.protocol('WM_DELETE_WINDOW', closeWindow)
        sensorConfigWindow.mainloop()
        return configureSensorValue
        
    def showPosGenConfigDialog(self, inputTitle: str, configInfo:str):
        posGenConfigWindow = tk.Tk()
        posGenConfigWindow.title("Sensor PosGens: " + inputTitle)
        posGenConfigWindow.geometry("500x800")
        button_frame_1 = None
        button_frame_2 = None
        clickCount = 0
        configurePosGenValue = "0"
        
        posGens = configInfo.split(';')
        for posGen in posGens:
            infos = posGen.split(':')
            if len(infos) == 2:
                clickCount = clickCount + 1
                if op.contains(infos[1], 'Method1'):                
                    button_frame_1 = tk.Canvas(posGenConfigWindow, bg="#8DB6CD", height=120, highlightcolor="black", highlightthickness=1)
                    button_frame_1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
                    button_frame_1.create_text(80, 10, text=infos[0] + ":", font=('arial', 10))
                    button_frame_1.create_text(80, 30, text=infos[1], font=('arial', 10, 'bold'))
                    button_frame_1.create_text(200, 60, text="Method1 parameter setting", font=('arial', 15))
                elif op.contains(infos[1], 'Method2'):
                    button_frame_2 = tk.Canvas(posGenConfigWindow, bg="#7CCD7C", height=120, highlightcolor="black", highlightthickness=1)
                    button_frame_2.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
                    button_frame_2.create_text(80, 10, text=infos[0] + ":", font=('arial', 10))
                    button_frame_2.create_text(80, 30, text=infos[1], font=('arial', 10, 'bold'))
                    button_frame_2.create_text(200, 60, text="Method2 parameter setting", font=('arial', 15))
                
                if configurePosGenValue == "0":
                    configurePosGenValue = infos[0] + ":" + infos[1]
                else:
                    configurePosGenValue = configurePosGenValue + ";" + infos[0] + ":" + infos[1]
        
        def newMethod1():
            nonlocal clickCount
            nonlocal configurePosGenValue
            clickCount = clickCount + 1
            button_frame_1 = tk.Canvas(posGenConfigWindow, bg="#8DB6CD", height=120, highlightcolor="black",
                                       highlightthickness=1)
            button_frame_1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
            button_frame_1.create_text(80, 10, text="Position generator " + str(clickCount) + ":", font=('arial', 10))
            button_frame_1.create_text(80, 30, text="Method1 model", font=('arial', 10, 'bold'))
            button_frame_1.create_text(200, 60, text="Method1 parameter setting", font=('arial', 15))
            if configurePosGenValue == "0":
                configurePosGenValue = "Position generator " + str(clickCount) + ":Method1 model"
            else:
                configurePosGenValue = configurePosGenValue + ";Position generator " + str(clickCount) + ":Method1 model"

        btnMethod1 = tk.Button(posGenConfigWindow, text='New Method1', bd=1, width=20, command=newMethod1)
        btnMethod1.grid(column=1, row=1, padx=10, pady=5)

        def newMethod2():
            nonlocal clickCount
            nonlocal configurePosGenValue
            clickCount = clickCount + 1
            button_frame_2 = tk.Canvas(posGenConfigWindow, bg="#7CCD7C", height=120, highlightcolor="black",
                                       highlightthickness=1)
            button_frame_2.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
            button_frame_2.create_text(80, 10, text="Position generator " + str(clickCount) + ":", font=('arial', 10))
            button_frame_2.create_text(80, 30, text="Method2 model", font=('arial', 10, 'bold'))
            button_frame_2.create_text(200, 60, text="Method2 parameter setting", font=('arial', 15))
            if configurePosGenValue == "0":
                configurePosGenValue = "Position generator " + str(clickCount) + ":Method2 model"
            else:
                configurePosGenValue = configurePosGenValue + ";Position generator " + str(clickCount) + ":Method2 model"

        btnMethod2 = tk.Button(posGenConfigWindow, text='New Method2', bd=1, width=20, command=newMethod2)
        btnMethod2.grid(column=2, row=1, padx=10, pady=5)

        def closeWindow():
            posGenConfigWindow.destroy()

        posGenConfigWindow.protocol('WM_DELETE_WINDOW', closeWindow)
        posGenConfigWindow.mainloop()
        return configurePosGenValue
        
    def showStartDialog(self, callback, sensorId, posGenId, posGenConfigInfo, inputTitle):
        startWindow = tk.Tk()
        startWindow.title("Sensor production: " + inputTitle)
        startWindow.geometry("400x400")
        rowCount = 0
        lbList=[]
        lbXList=[]
        txtXList=[]
        lbYList=[]
        txtYList=[]
        lbZList=[]
        txtZList=[]
        
        posGens = posGenConfigInfo.split(';')
        for posGen in posGens:
            infos = posGen.split(':')
            if len(infos) == 2:
                lb1 = tk.Label(startWindow, text=infos[0] + ":" + infos[1],fg="blue",font=("Arial",10,"bold"))
                lb1.grid(column=1, columnspan=2, row=rowCount + 1, padx=10, pady=5)
                lbList.append(lb1)
                lb1_x = tk.Label(startWindow, text="x: ")
                lb1_x.grid(column=1, row=rowCount + 2, padx=10, pady=5)
                lbXList.append(lb1_x)
                txt1_x = tk.Entry(startWindow, width=30)
                txt1_x.grid(column=2, row=rowCount + 2)
                txtXList.append(txt1_x)
                lb1_y = tk.Label(startWindow, text="y: ")
                lb1_y.grid(column=1, row=rowCount + 3, padx=10, pady=5)
                lbYList.append(lb1_y)
                txt1_y = tk.Entry(startWindow, width=30)
                txt1_y.grid(column=2, row=rowCount + 3)
                txtYList.append(txt1_y)
                lb1_z = tk.Label(startWindow, text="z: ")
                lb1_z.grid(column=1, row=rowCount + 4, padx=10, pady=5)
                lbZList.append(lb1_z)
                txt1_z = tk.Entry(startWindow, width=30)
                txt1_z.grid(column=2, row=rowCount + 4)
                txtZList.append(txt1_z)
                rowCount = rowCount+5

        def sendNewPosition():# define positions and call callbackfunction to return positions to PMTW.
            objects = {'SensorId': sensorId}
            for index in range(0,len(txtXList)):
                receivedTime = callback.GetStrobeTime()
                objects.update({'Time': receivedTime})            
                key = "'" + str(index) + "'"
                newPos ={key: {'X': float(txtXList[index].get()),
                               'Y': float(txtYList[index].get()),
                               'Z': float(txtZList[index].get()),
                               'RX': 0.0,
                               'RY': 0.0,
                               'RZ': 0.0,
                               'Tag': 0,
                               'Score': 1.0,
                               'Val1': 0.0,
                               'Val2': 0.0,
                               'Val3': 0.0,
                               'Val4': 0.0,
                               'Val5': 0.0,
                               'Level': 2,
                               'PosGenId': posGenId}}
                objects.update(newPos)
            callback.NewPosition(objects)

        btnGenerate = tk.Button(startWindow, text='Generate position', bd=1, width=20, command=sendNewPosition)
        btnGenerate.grid(column=1,columnspan=2, row=rowCount)

        def closeWindow():
            startWindow.destroy()

        startWindow.protocol('WM_DELETE_WINDOW', closeWindow)
        startWindow.mainloop()


def main(argv):
    """main

    """
    print("Run from main: ", argv)
    try:
        logger = get_logging()
        logger.debug(argv)
        es = ExternalSensorsDemo()
        es.loadSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C04', '1;2;3')
        es.loadSensor('325D3EB5-B563-4F90-B0C5-2F1E770D5C05', '11;12;13')
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