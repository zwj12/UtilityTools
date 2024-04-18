# This software is provided 'as-is', without any express or
# implied warranty. In no event will ABB be held liable for 
# any damages arising from the use of this software.

import tkinter as tk
import xml.etree.ElementTree as ET
import socket
import re
import os
import ctypes
from collections import OrderedDict
import ctypes.wintypes
import logging
import os
import sys
import ExternalSensorsTriggerUDPSample

logFilePath = r'C:\ProgramData\ABB\PickMaster Twin\PickMaster Twin Runtime\PickMaster Runtime\Log\PMTWSensorFunctions.log'
showSensorPortConfigDialogCounter = 0
showPositionGeneratorConfigDialogCounter = 0
startSensorCounter = 0
sendNewPositionCounter = 0
XMLDataExtractorCounter = 0


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
    logger = logging.getLogger('PMTWSensorFunctions')
    if logger.hasHandlers() == False:
        logger.setLevel(logging.DEBUG)
        # logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler(logFilePath)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    return logger


class PortOccupiedError(Exception):
    # PortOccupiedError will be thrown when the port is occupied.
    def __init__(self, *args) -> None:
        super().__init__()
        self.args = f"{args[0][2]}. Sensor name: {args[0][0]} , Port: {args[0][1]}"
    
class SensorFunctions:
    """Sensor2Functions

    """

    def __init__(self):
        """__init__

        """
        super().__init__()
        self.isRunning = True
        self.sensorName = ""        
        self.docPath = self.getDocumentsPath()
        self.host = '' #INADDR_ANY   
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def showLog(self, message:str, logLevel:int, logCallback):  
        logMessage = "[ExternalSensorUDP] {}.".format(message)
        log = {'LogLevel': logLevel, 'Log': logMessage}
        logCallback.ShowPythonLog(log)

    def getDocumentsPath(self):        
        CSIDL_PERSONAL = 5 # My Documents
        SHGFP_TYPE_CURRENT = 0 # Get current, not default value
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)        
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        return buf.value

    def showSensorPortConfigDialog(self, inputTitle: str, configInfo: str, callBackFunc):
        """showSensorPortConfigDialog

        Keyword arguments:
        inputTitle -- ''
        configInfo -- ''
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global showSensorPortConfigDialogCounter
        showSensorPortConfigDialogCounter += 1
        logger.debug(f'showSensorPortConfigDialogCounter = {showSensorPortConfigDialogCounter}')

        sensorConfigWindow = tk.Tk()
        sensorConfigWindow.title(inputTitle)

        scaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)/100
        scaledX = int(scaleFactor*470)
        scaledY = int(scaleFactor*139)
        ww = sensorConfigWindow.winfo_screenwidth()
        wh = sensorConfigWindow.winfo_screenheight()
        posX = int(ww/2-470*scaleFactor/2)
        posY = int(wh/2-139*scaleFactor/2)
        sensorConfigWindow.geometry(str(scaledX)+"x"+str(scaledY)+"+"+str(posX)+"+"+str(posY))
        sensorConfigWindow.resizable(0,0)
        sensorConfigWindow.attributes('-topmost', True)
        path = os.path.join(self.docPath, 'PickMaster', 'PMScripts', 'ExternalSensorIcon.ico')
        sensorConfigWindow.iconbitmap(path)
        sensorConfigWindow['bg'] = '#ffffff'
        serverPort = []
        isPortValid = False
               
        frameBlk1 = tk.Frame(sensorConfigWindow, background='#ffffff',highlightbackground='#ffffff', highlightcolor='#ffffff', borderwidth=0)
        frameBlk1.pack(side='top',expand='yes', fill='x')
        lbUDP = tk.Label(frameBlk1, text="UDP server port: ", font=("ABBvoice", 9), background='#ffffff')
        lbUDP.pack(side='left',anchor='nw', padx=(22,10), pady=(0,0))
        framePort = tk.Frame(frameBlk1, highlightbackground='#bababa', highlightcolor='#bababa', borderwidth=2)
        framePort.pack(side='top', expand='yes', fill='both', padx=(0,16))
        txtPort = tk.Entry(framePort, font=("ABBvoice", 9), relief='solid', borderwidth=0)
        txtPort.pack(expand='yes', fill='both')
        txtPort.columnconfigure(0,weight=1)
        labelInfo = tk.Label(frameBlk1, text="port should be integer between 0 - 65535", justify='left', font=("ABBvoice", 9), foreground='#bababa', background='#ffffff')
        labelInfo.pack(side='top', anchor='w')
        frameBlk2 = tk.Frame(frameBlk1, background='#ffffff', borderwidth=0)
        frameBlk2.pack(side='left', anchor='w', fill='y')
        lbWrongInput = tk.Label(frameBlk1, text="The entered port number is invalid, please check your input.", \
            wraplength=int(290*scaleFactor), font=("ABBvoice", 9), justify='left', fg= '#ffffff', background='#ffffff')
        lbWrongInput.pack(side='left',anchor='w')
        txtPort.insert(0, configInfo)

        def inputChecker(input: str):
            return re.match('^\d+$', input) and int(input) >= 0 and int(input) <= 65535 
            
        def closeWindow():
            nonlocal serverPort, isPortValid, callBackFunc
            if(inputChecker(txtPort.get())):
                serverPort = txtPort.get()
                isPortValid = True
                sensorConfigWindow.destroy()
            else:
                lbWrongInput.config(fg='red')

        btnOK = tk.Button(sensorConfigWindow, text = "OK", font=("ABBvoice", 9), width=12, height=1, command = closeWindow,\
            relief='solid', borderwidth=0, bg='#3366FF', fg='white', activebackground='#3366FF')
        btnOK.pack(side='right', anchor='se', padx=(12,16), pady=(0,17))

        frameBtn = tk.Frame(sensorConfigWindow, bg='#3366FF', highlightbackground='#3366FF', highlightcolor='#3366FF', borderwidth=1)
        frameBtn.pack(side='right', anchor='s', padx=(12,12), pady=(0,16))
        btnCancel = tk.Button(frameBtn, text = "Cancel", font=("ABBvoice", 9), width=12, height=1, command = sensorConfigWindow.destroy,\
            relief='solid', borderwidth=0, bg='#ffffff', activebackground='#ffffff')
        btnCancel.pack()

        sensorConfigWindow.protocol('WM_DELETE_WINDOW', sensorConfigWindow.destroy)
        sensorConfigWindow.mainloop()
        
        return (isPortValid, serverPort)

    def showPositionGeneratorConfigDialog(self, inputTitle: str, configInfo: str, callBackFunc):
        """showPositionGeneratorConfigDialog

        Keyword arguments:
        inputTitle -- ''
        configInfo -- ''
        """
        kwargs = locals()
        logger = get_logging()
        logger.debug(f"Call {sys._getframe().f_code.co_name}")
        logger.debug(f'kwargs = {kwargs}')

        global showPositionGeneratorConfigDialogCounter
        showPositionGeneratorConfigDialogCounter += 1
        logger.debug(f'showPositionGeneratorConfigDialogCounter = {showPositionGeneratorConfigDialogCounter}')

        positionGeneratorConfigWindow = tk.Tk()
        positionGeneratorConfigWindow.title(inputTitle)
        scaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)/100
        scaledX = int(scaleFactor*470)
        scaledY = int(scaleFactor*139)
        ww = positionGeneratorConfigWindow.winfo_screenwidth()
        wh = positionGeneratorConfigWindow.winfo_screenheight()
        posX = int(ww/2-470*scaleFactor/2)
        posY = int(wh/2-139*scaleFactor/2)
        positionGeneratorConfigWindow.geometry(str(scaledX)+"x"+str(scaledY)+"+"+str(posX)+"+"+str(posY))
        positionGeneratorConfigWindow.resizable(0,0)
        positionGeneratorConfigWindow.attributes('-topmost', True)
        path = os.path.join(self.docPath, 'PickMaster', 'PMScripts', 'ExternalSensorIcon.ico')
        positionGeneratorConfigWindow.iconbitmap(path)
        positionGeneratorConfigWindow['bg'] = '#ffffff'
        positionGeneratorIndex = []
        isIndexValid = False

        frameBlk1 = tk.Frame(positionGeneratorConfigWindow, background='#ffffff',highlightbackground='#ffffff', highlightcolor='#ffffff', borderwidth=0)
        frameBlk1.pack(side='top',expand='yes', fill='x')
        labelPositionGeneratorIndex = tk.Label(frameBlk1, text="Position generator index: ", font=("ABBvoice", 9), background='#ffffff')
        labelPositionGeneratorIndex.pack(side='left',anchor='nw', padx=(22,10), pady=(0,0))
        frameIndex = tk.Frame(frameBlk1, highlightbackground='#bababa', highlightcolor='#bababa', borderwidth=2)
        frameIndex.pack(side='top', expand='yes', fill='both', padx=(0,16))
        positionGeneratorIndexNum = tk.Entry(frameIndex, font=("ABBvoice", 9), relief='solid', borderwidth=0)
        positionGeneratorIndexNum.pack(expand='yes', fill='both')
        labelInfo = tk.Label(frameBlk1, text="use semicolon to split indexes", justify='left', font=("ABBvoice", 9), foreground='#bababa', background='#ffffff')
        labelInfo.pack(side='top', anchor='w')
        frameBlk2 = tk.Frame(frameBlk1, background='#ffffff', borderwidth=0)
        frameBlk2.pack(side='left', anchor='w', fill='y')
        lbWrongInput = tk.Label(frameBlk1, text="The entered index is invalid, please check your input.", \
            wraplength=int(260*scaleFactor), font=("ABBvoice", 9), justify='left', fg= '#ffffff', background='#ffffff')
        lbWrongInput.pack(side='left',anchor='w')
        
        positionGeneratorIndexNum.insert(0, configInfo)
        
        def inputChecker(input:str):
            nonlocal positionGeneratorIndexNum, lbWrongInput
            pattern='^(\d+;)+(?=\d+$)|^\d+$'
            if(re.match(pattern, input)):
                positionGeneratorIndexList = re.findall('\d+', input)
                positionGeneratorIndexSet = set(positionGeneratorIndexList)
                for index in positionGeneratorIndexSet:
                    if positionGeneratorIndexList.count(index) > 1:
                        lbWrongInput.config(text="Duplicated index detected, please check your input.")
                        return False
                for index in positionGeneratorIndexList:
                    if(int(index) < 0 or int(index) > 1000):
                        lbWrongInput.config(text="The entered index is invalid, please check your input.")
                        return False    
            else:
                lbWrongInput.config(text="The entered index is invalid, please check your input.")
                return False
            return True
            
        def closeWindow():
            nonlocal positionGeneratorIndex, isIndexValid

            if(inputChecker(positionGeneratorIndexNum.get())):
                positionGeneratorIndex = positionGeneratorIndexNum.get()
                isIndexValid = True
                positionGeneratorConfigWindow.destroy()
            else:
                lbWrongInput.config(fg='red')
            
        btnOK = tk.Button(positionGeneratorConfigWindow, text = "OK", font=("ABBvoice", 9), width=12, command = closeWindow,\
        relief='solid', borderwidth=0, bg='#3366FF', fg='white', activebackground='#3366FF')
        btnOK.pack(side='right', anchor='se', padx=(12,16), pady=(0,17))
        frameBtn = tk.Frame(positionGeneratorConfigWindow, bg='#3366FF', highlightbackground='#3366FF', highlightcolor='#3366FF', borderwidth=1)
        frameBtn.pack(side='right', anchor='s', padx=(12,12), pady=(0,16))
        btnCancel = tk.Button(frameBtn, text = "Cancel", font=("ABBvoice", 9), width=12, command = positionGeneratorConfigWindow.destroy,\
            relief='solid', borderwidth=0, bg='#ffffff', activebackground='#ffffff')
        btnCancel.pack()

        positionGeneratorConfigWindow.protocol('WM_DELETE_WINDOW', positionGeneratorConfigWindow.destroy)
        positionGeneratorConfigWindow.mainloop()

        return (isIndexValid, positionGeneratorIndex)
    
    def startSensor(self, callback, sensorId, positionGeneratorId, sensorConfigInfo, positionGeneratorConfigInfo, logCallback):
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
 
        #Initialize a UDP server. The server is continuing receiving messages, transfer the message to the item position, and send the position to RT.
        acqStrobeDict = OrderedDict()
        positionDict = OrderedDict()
        currentAcqNo = -65535
        hasNewPos = False
        maxLimitAcq = 15
        maxLimitPos = 15
        
        def XMLDataExtractor(msg, logCallback):
            """sendNewPosition

            Keyword arguments:
            """
            kwargs = locals()
            logger = get_logging()
            logger.debug(f"Call {sys._getframe().f_code.co_name}")
            logger.debug(f'kwargs = {kwargs}')

            global XMLDataExtractorCounter
            XMLDataExtractorCounter += 1
            logger.debug(f'XMLDataExtractorCounter = {XMLDataExtractorCounter}')

            #Extract position from message in XML form. The strobe time is recorded and is saved in acqStrobeDict when a new AcqNo message is received. All positions in a same image is saved in positionDict[currentAcqNo]. Positions are sent to RT when PackNo equals to FinalPackNo.
            nonlocal acqStrobeDict, callback, positionDict, hasNewPos, currentAcqNo, maxLimitAcq, maxLimitPos
            def dictLimitCheck(dict, maxLimit):
                if len(dict) >= maxLimit:
                    dict.popitem(last = False)
            hasNewPos = False
            tree = ET.ElementTree(ET.fromstring(msg))
            root = tree.getroot()
            currentAcqNo = root.attrib['AcqNo']
            if root.tag == "NewAcq":
                dictLimitCheck(acqStrobeDict, maxLimitAcq)
                acqStrobeDict[currentAcqNo] = callback.GetStrobeTime()
                return
            if not acqStrobeDict[currentAcqNo]:
                self.showLog("Failed to find strobe time. AcqNo not found. AcqNo: {}".format(currentAcqNo), 1, logCallback)
                return
            if currentAcqNo in positionDict.keys():
                posInfo = positionDict[currentAcqNo]
            else:
                posInfo = ()
            for itemPos in root.iter('Position'): 
                if len(itemPos.attrib) > 0:
                    posInfo += (itemPos.attrib,)
            dictLimitCheck(positionDict, maxLimitPos)
            positionDict[currentAcqNo] = posInfo

            if (int(root.attrib['PackNo']) >= int(root.attrib['FinalPackNo'])):
                hasNewPos = True
            
        def sendNewPosition(callback, sensorId, positionGeneratorId, logCallback):
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

            # Compatible to the format of PM3. Positions are sent to RT.
            nonlocal acqStrobeDict, positionDict, currentAcqNo
            positionGeneratorIndexList = re.findall('\d+', positionGeneratorConfigInfo)
            objects = {}
            objects.update({'SensorId': sensorId,
                            'Time': acqStrobeDict[currentAcqNo]})
            position = positionDict[currentAcqNo]

            logger.debug(f'positionGeneratorIndexList = {positionGeneratorIndexList}')
            logger.debug(f'position = {position}')

            for index in range(0, len(position)):
                if 'PosGen' not in position[index] or \
                        'PosGen' in position[index] and position[index]['PosGen'] not in positionGeneratorIndexList:
                    self.showLog("Index not match, skip", 2, logCallback)
                    continue
                    
                logger.debug(f'position[{index}] = {position[index]}')
                ############################
                # adapt for PM3
                if 'XAngle' in position[index]:
                    RX = 'XAngle'
                    RY = 'YAngle'
                    RZ = 'ZAngle'
                else:
                    RX = 'RX'
                    RY = 'RY'
                    RZ = 'RZ'
                if 'Accept' in position[index] and position[index]['Accept'] == '1':
                    position[index]['Level'] = "2"
                elif 'Accept' in position[index]:
                    position[index]['Level'] = "1"
                ############################
                
                key = "'" + str(index) + "'"
                newPos = {key: {'X': float(position[index]['X']) if 'X' in position[index] else 0.0,
                                'Y': float(position[index]['Y']) if 'Y' in position[index] else 0.0,
                                'Z': float(position[index]['Z']) if 'Z' in position[index] else 0.0,
                                'RX': float(position[index][RX]) if RX in position[index] else 0.0,
                                'RY': float(position[index][RY]) if RY in position[index] else 0.0,
                                'RZ': float(position[index][RZ]) if RZ in position[index] else 0.0,
                                'Tag': int(position[index]['Tag']) if 'Tag' in position[index] else 0,
                                'Score': float(position[index]['Score']) if 'Score' in position[index] else 1.0,
                                'Val1': float(position[index]['Val1']) if 'Val1' in position[index] else 0.0,
                                'Val2': float(position[index]['Val2']) if 'Val2' in position[index] else 0.0,
                                'Val3': float(position[index]['Val3']) if 'Val3' in position[index] else 0.0,
                                'Val4': float(position[index]['Val4']) if 'Val4' in position[index] else 0.0,
                                'Val5': float(position[index]['Val5']) if 'Val5' in position[index] else 0.0,
                                'PosGenId': positionGeneratorId,
                                'Level': int(position[index]['Level']) if 'Level' in position[index] else 1}}
                if 'Valid' in position[index] and int(position[index]['Valid']) == 1:
                    objects.update(newPos)   
            # Use this function to record the item position. The logPath should be created before using this function.
            logger.debug(f'objects = {objects}')
            callback.NewPosition(objects)
            if positionGeneratorIndexList == '3':
                logger.debug('Trying to pulse doManSync1')
                ExternalSensorsTriggerUDPSample.TrigWorkArea("doManSync1", '192.168.56.1')
            else:
                logger.debug('Trying to pulse doManSync2')
                ExternalSensorsTriggerUDPSample.TrigWorkArea("doManSync2", '192.168.56.1')      

        def portRecvUDP(): 
            try:
                self.port = int(sensorConfigInfo)
                logger.debug(f'trying to bind {self.host}:{self.port}')  
                self.server.bind((self.host, self.port)) 
                logger.debug(f'{self.host}:{self.port} is listening...')   
            except OSError as ex:
                if ex.errno == 10048:
                    raise PortOccupiedError((self.sensorName,sensorConfigInfo,ex.args[1]))
                raise ex
            while self.isRunning:
                try:
                    data, addr = self.server.recvfrom(4096)
                    recv_str = data.decode("utf-8")
                    # self.showLog("Received message: {}".format(recv_str), 0, logCallback)
                    XMLDataExtractor(recv_str, logCallback)
                except OSError as ex:
                    if ex.errno == 10040:
                        self.showLog("Received data is too large. Please send less positions at the same time", 2, logCallback)
                        return
                    raise ex
                except ET.ParseError:
                    self.showLog("Invalid XML format. Please check the message", 2, logCallback)
                else:    
                    if hasNewPos:
                        sendNewPosition(callback, sensorId, positionGeneratorId, logCallback)
                        acqStrobeDict.pop(currentAcqNo)
                        positionDict.pop(currentAcqNo)

        portRecvUDP()