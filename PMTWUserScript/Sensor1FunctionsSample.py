"""Sensor1FunctionsSample
"""

import tkinter as tk
import operator as op
import threading
import socket
import time
import logging
import os
import sys
import ExternalSensorsTriggerUDPSample

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWSensor1Functions.log'
showSensorConfigDialogCounter = 0
showPosGenConfigDialogCounter = 0
startSensorCounter = 0
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
    logger = logging.getLogger('PMTWSensor1Functions')
    if logger.hasHandlers() == False:
        logger.setLevel(logging.DEBUG)
        # logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler(logFilePath)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger


class Sensor1Functions:
    """Sensor1Functions

    """

    def __init__(self):
        """__init__

        """
        super().__init__()
        self.position = []
        self.host = '' #INADDR_ANY               
        self.port = 8887    
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def showSensorConfigDialog(self, inputTitle: str, configInfo: str):
        """showSensorConfigDialog

        Keyword arguments:
        inputTitle -- ''
        configInfo -- ''
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global showSensorConfigDialogCounter
        showSensorConfigDialogCounter += 1
        logger.debug(f'showSensorConfigDialogCounter = {showSensorConfigDialogCounter}')

        sensorConfigWindow = tk.Tk()
        sensorConfigWindow.title("Sensor1: " + inputTitle)
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

        logger.debug(f'configureSensorValue = {configureSensorValue}')
        return configureSensorValue


    def showPosGenConfigDialog(self, inputTitle: str, configInfo: str):
        """showPosGenConfigDialog

        Keyword arguments:
        inputTitle -- ''
        configInfo -- ''
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global showPosGenConfigDialogCounter
        showPosGenConfigDialogCounter += 1
        logger.debug(f'showPosGenConfigDialogCounter = {showPosGenConfigDialogCounter}')

        posGenConfigWindow = tk.Tk()
        posGenConfigWindow.title("Sensor1 PosGens: " + inputTitle)
        posGenConfigWindow.geometry("500x800")
        clickCount = 0
        configurePosGenValue = "0"        
    
        posGens = configInfo.split(';')
        for posGen in posGens:
            infos = posGen.split(':')
            if len(infos) == 2:
                clickCount = clickCount + 1
                if op.contains(infos[1], 'Algorithm 1'):
                    button_frame_1 = tk.Canvas(posGenConfigWindow, bg="#CC99FF", height=120, highlightcolor="black", highlightthickness=1)
                    button_frame_1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
                    button_frame_1.create_text(80, 10, text=infos[0] + ":", font=('arial', 10))
                    button_frame_1.create_text(80, 30, text=infos[1], font=('arial', 10, 'bold'))
                    button_frame_1.create_text(200, 60, text="Algorithm 1 parameter setting", font=('arial', 15))
                elif op.contains(infos[1], 'Algorithm 2'):
                    button_frame_2 = tk.Canvas(posGenConfigWindow, bg="#FF9933", height=120, highlightcolor="black", highlightthickness=1)
                    button_frame_2.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
                    button_frame_2.create_text(80, 10, text=infos[0] + ":", font=('arial', 10))
                    button_frame_2.create_text(80, 30, text=infos[1], font=('arial', 10, 'bold'))
                    button_frame_2.create_text(200, 60, text="Algorithm 2 parameter setting", font=('arial', 15))

                if configurePosGenValue == "0":
                    configurePosGenValue = infos[0] + ":" + infos[1]
                else:
                    configurePosGenValue = configurePosGenValue + ";" + infos[0] + ":" + infos[1]

        def newAlgo1():
            nonlocal clickCount
            nonlocal configurePosGenValue
            clickCount = clickCount + 1
            button_frame_1 = tk.Canvas(posGenConfigWindow, bg="#CC99FF", height=120, highlightcolor="black", highlightthickness=1)
            button_frame_1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
            button_frame_1.create_text(80, 10, text="Position generator " + str(clickCount) + ":", font=('arial', 10))
            button_frame_1.create_text(80, 30, text="Algorithm 1 model", font=('arial', 10, 'bold'))
            button_frame_1.create_text(200, 60, text="Algorithm 1 parameter setting", font=('arial', 15))
            if configurePosGenValue == "0":
                configurePosGenValue = "Position generator " + str(clickCount) + ":Algorithm 1 model"
            else:
                configurePosGenValue = configurePosGenValue + ";Position generator " + str(clickCount) + ":Algorithm 1 model"


        btnAlgo1 = tk.Button(posGenConfigWindow, text='New Algorithm 1', bd=1, width=20, command=newAlgo1)
        btnAlgo1.grid(column=1, row=1, padx=10, pady=5)

        def newAlgo2():
            nonlocal clickCount
            nonlocal configurePosGenValue
            clickCount = clickCount + 1
            button_frame_2 = tk.Canvas(posGenConfigWindow, bg="#FF9933", height=120, highlightcolor="black",
                                       highlightthickness=1)
            button_frame_2.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
            button_frame_2.create_text(80, 10, text="Position generator " + str(clickCount) + ":", font=('arial', 10))
            button_frame_2.create_text(80, 30, text="Algorithm 2 model", font=('arial', 10, 'bold'))
            button_frame_2.create_text(200, 60, text="Algorithm 2 parameter setting", font=('arial', 15))
            if configurePosGenValue == "0":
                configurePosGenValue = "Position generator " + str(clickCount) + ":Algorithm 2 model"
            else:
                configurePosGenValue = configurePosGenValue + ";Position generator " + str(clickCount) + ":Algorithm 2 model"

        btnAlgo2 = tk.Button(posGenConfigWindow, text='New Algorithm 2', bd=1, width=20, command=newAlgo2)
        btnAlgo2.grid(column=2, row=1, padx=10, pady=5)

        def closeWindow():
            posGenConfigWindow.destroy()

        posGenConfigWindow.protocol('WM_DELETE_WINDOW', closeWindow)
        posGenConfigWindow.mainloop()

        logger.debug(f'configurePosGenValue = {configurePosGenValue}')
        return configurePosGenValue


    def startSensor(self, callback, sensorId, posGenId, posGenConfigInfo, logCallback):
        """startSensor

        Keyword arguments:
        callback -- 
        sensorId -- ''
        posGenId -- ''
        posGenConfigInfo -- ''
        logCallback -- ''
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global startSensorCounter
        startSensorCounter += 1
        logger.debug(f'startSensorCounter = {startSensorCounter}')

        def sendNewPosition(callback, sensorId, posGenId):     
            """sendNewPosition

            Keyword arguments:
            """
            kwargs = locals()
            logger = get_logging()
            logger.debug(f"Call {sys._getframe().f_code.co_name}")
            logger.debug(f'kwargs = {kwargs}')

            global sendNewPositionCounter
            sendNewPositionCounter += 1
            logger.debug(f'sendNewPositionCounter = {sendNewPositionCounter}')
               
            objects = {'SensorId': sensorId}
            logger.debug(f'self.position = {self.position}')
            logger.debug(f'objects = {objects}')
            for index in range(0, len(self.position)):
                receivedTime = callback.GetStrobeTime()
                objects.update({'Time': receivedTime})
                key = "'" + str(index) + "'"
                newPos = {key: {'X': float(self.position[index].split(';')[0].split(':')[1]),
                                'Y': float(self.position[index].split(';')[1].split(':')[1]),
                                'Z': float(self.position[index].split(';')[2].split(':')[1]),
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
            logger.debug(f'objects = {objects}')
            callback.NewPosition(objects)
            logger.debug('Trying to pulse doManSync1')
            ExternalSensorsTriggerUDPSample.TrigWorkArea("doManSync1", '192.168.56.1')

        def portRecvUDP():
            logger.debug(f'trying to bind {self.host}:{self.port}')          
            self.server.bind((self.host, self.port))
            logger.debug(f'{self.host}:{self.port} is listening...')   
            while True:
                data, addr = self.server.recvfrom(1024)
                logger.debug(f'received from {addr}: {data}')  
                recv_str = data.decode("ascii")             
                logger.debug(f'recv_str: {recv_str}')                 
                self.position = recv_str.split('|')
                sendNewPosition(callback, sensorId, posGenId)

        portRecvUDP()

