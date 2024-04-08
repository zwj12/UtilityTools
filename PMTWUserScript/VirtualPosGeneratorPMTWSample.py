import tkinter as tk
from tkinter import ttk
from enum import Enum
import socket
import xml.etree.ElementTree as ET
import validators
import re
import time
import threading
import math
import random

AcqNo = 0

class AcceptLevel(Enum):
    Accepted = 2
    Rejected = 1
    Discarded = 0
    
defaultValueDict = {
    "IP": '127.0.0.1',
    "Port": '5000',
    "Index": '0',
    "X": '0',
    "Y": '0',
    "Z": '0',
    "RX": '0',
    "RY": '0',
    "RZ": '0',
    "Val1": '0',
    "Val2": '0',
    "Val3": '0',
    "Val4": '0',
    "Val5": '0',
    "Score": '90',
    "MinRandNum": '1',
    "MaxRandNum": '5',
    "MaxMsgNum": '5'
}

def handlerArgs(event, type, param):
    if type == "IP":
        if not validators.ipv4(param.get()):
            param.delete(0, tk.END)
            param.insert(0, defaultValueDict["IP"])
    elif type == "Port":
        if not (re.match("^\d+$", param.get()) != None and validators.between(int(param.get()), min_val = 0, max_val = 65535)):
            param.delete(0, tk.END)
            param.insert(0, defaultValueDict["Port"])
    elif type == "Index":
        if not (re.match("^\d+$", param.get()) != None and validators.between(int(param.get()), min_val = 0, max_val = 1000)):
            param.delete(0, tk.END)
            param.insert(0, defaultValueDict["Index"])
    elif type == "MinRandNum":
        if re.match("^0*\d+$", param[0].get()) == None:
            param.delete(0, tk.END)
            param.insert(0, defaultValueDict["MinRandNum"])
        else:
            if int(param[0].get()) > int(param[1].get()):
                param[0].delete(0, tk.END)
                param[0].insert(0, defaultValueDict["MinRandNum"])
                param[1].delete(0, tk.END)
                param[1].insert(0, defaultValueDict["MaxRandNum"])
    elif type == "MaxRandNum":
        if re.match("^0*\d+$", param[1].get()) == None:
            param.delete(0, tk.END)
            param.insert(0, defaultValueDict["MaxRandNum"])
        else:
            if int(param[0].get()) > int(param[1].get()):
                param[0].delete(0, tk.END)
                param[0].insert(0, defaultValueDict["MinRandNum"])
                param[1].delete(0, tk.END)
                param[1].insert(0, defaultValueDict["MaxRandNum"])
    elif type == "Score":
        if not (re.match("^\d+$|^\d+\.\d+$", param.get()) != None and validators.between(float(param.get()), min_val = 0.0, max_val = 100.0)):
            param.delete(0, tk.END)
            param.insert(0, defaultValueDict["Score"])
    elif type == "MaxMsgNum":
        if not (re.match("^\d+$", param.get()) != None and validators.between(int(param.get()), min_val = 1, max_val = 50)):
            param.delete(0, tk.END)
            param.insert(0, defaultValueDict["MaxMsgNum"])
    else:
        if re.match("^-?0*\d+$|^-?0*\d+\.\d+$", param.get()) == None:
            param.delete(0, tk.END)
            param.insert(0, defaultValueDict["Val1"])

def showPositionGeneratorDialog():  
    positionGeneratorWindow = tk.Tk()
    positionGeneratorWindow.title("Virtual position generator")
    # scaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)/100
    # scaledX = int(scaleFactor*200)
    # scaledY = int(scaleFactor*680)
    # # positionGeneratorWindow.geometry(str(scaledX)+"x"+str(scaledY))
    positionGeneratorWindow.geometry("200x750")
    positionGeneratorWindow.resizable(0,0)
    positionGeneratorWindow.grid_columnconfigure(2, weight=1)
    positionGeneratorWindow.grid_rowconfigure(24, weight=1)
    
    lbIP = tk.Label(positionGeneratorWindow, text="IP: ")
    lbIP.grid(column=1, row=1, padx=10, pady=5)
    txtIP = tk.Entry(positionGeneratorWindow)
    txtIP.grid(column=2, row=1, padx=[0,10], sticky="we")
    txtIP.insert(0, defaultValueDict["IP"])
    txtIP.bind("<FocusOut>", lambda event: handlerArgs(event, "IP", txtIP))
    
    lbUDPPort = tk.Label(positionGeneratorWindow, text="UDP port: ")
    lbUDPPort.grid(column=1, row=2, padx=10, pady=5)
    txtUDPPort = tk.Entry(positionGeneratorWindow)
    txtUDPPort.grid(column=2, row=2, padx=[0,10], sticky="we")
    txtUDPPort.insert(0, defaultValueDict["Port"])
    txtUDPPort.bind("<FocusOut>", lambda event: handlerArgs(event, "Port", txtUDPPort))
    
    lbPosGenIndex = tk.Label(positionGeneratorWindow, text="PosGenIndex: ")
    lbPosGenIndex.grid(column=1, row=3, padx=10, pady=5)
    txtPosGenIndex = tk.Entry(positionGeneratorWindow)
    txtPosGenIndex.grid(column=2, row=3, padx=[0,10], sticky="we")
    txtPosGenIndex.insert(0, defaultValueDict["Index"])
    txtPosGenIndex.bind("<FocusOut>", lambda event: handlerArgs(event, "Index", txtPosGenIndex))

    lbX = tk.Label(positionGeneratorWindow, text="X: ")
    lbX.grid(column=1, row=4, padx=10, pady=5)
    txtX = tk.Entry(positionGeneratorWindow)
    txtX.grid(column=2, row=4, padx=[0,10], sticky="we")
    txtX.insert(0, defaultValueDict["X"])
    txtX.bind("<FocusOut>", lambda event: handlerArgs(event, "X", txtX))

    lbY = tk.Label(positionGeneratorWindow, text="Y: ", justify='left')
    lbY.grid(column=1, row=5, padx=10, pady=5)
    txtY = tk.Entry(positionGeneratorWindow)
    txtY.grid(column=2, row=5, padx=[0,10], sticky="we")
    txtY.insert(0, defaultValueDict["Y"])
    txtY.bind("<FocusOut>", lambda event: handlerArgs(event, "Y", txtY))

    lbZ = tk.Label(positionGeneratorWindow, text="Z: ")
    lbZ.grid(column=1, row=6, padx=10, pady=5)
    txtZ = tk.Entry(positionGeneratorWindow)
    txtZ.grid(column=2, row=6, padx=[0,10], sticky="we")
    txtZ.insert(0, defaultValueDict["Z"])
    txtZ.bind("<FocusOut>", lambda event: handlerArgs(event, "Z", txtZ))
    
    lbRX = tk.Label(positionGeneratorWindow, text="RX: ")
    lbRX.grid(column=1, row=7, padx=10, pady=5)
    txtRX = tk.Entry(positionGeneratorWindow)
    txtRX.grid(column=2, row=7, padx=[0,10], sticky="we")
    txtRX.insert(0, defaultValueDict["RX"])
    txtRX.bind("<FocusOut>", lambda event: handlerArgs(event, "RX", txtRX))
    
    lbRY = tk.Label(positionGeneratorWindow, text="RY: ")
    lbRY.grid(column=1, row=8, padx=10, pady=5)
    txtRY = tk.Entry(positionGeneratorWindow)
    txtRY.grid(column=2, row=8, padx=[0,10], sticky="we")
    txtRY.insert(0, defaultValueDict["RY"])
    txtRY.bind("<FocusOut>", lambda event: handlerArgs(event, "RY", txtRY))
    
    lbRZ = tk.Label(positionGeneratorWindow, text="RZ: ")
    lbRZ.grid(column=1, row=9, padx=10, pady=5)
    txtRZ = tk.Entry(positionGeneratorWindow)
    txtRZ.grid(column=2, row=9, padx=[0,10], sticky="we")
    txtRZ.insert(0, defaultValueDict["RZ"])
    txtRZ.bind("<FocusOut>", lambda event: handlerArgs(event, "RZ", txtRZ))
    
    lbVal1 = tk.Label(positionGeneratorWindow, text="Val1: ")
    lbVal1.grid(column=1, row=10, padx=10, pady=5)
    txtVal1 = tk.Entry(positionGeneratorWindow)
    txtVal1.grid(column=2, row=10, padx=[0,10], sticky="we")
    txtVal1.insert(0, defaultValueDict["Val1"])
    txtVal1.bind("<FocusOut>", lambda event: handlerArgs(event, "Val1", txtVal1))
    
    lbVal2 = tk.Label(positionGeneratorWindow, text="Val2: ")
    lbVal2.grid(column=1, row=11, padx=10, pady=5)
    txtVal2 = tk.Entry(positionGeneratorWindow)
    txtVal2.grid(column=2, row=11, padx=[0,10], sticky="we")
    txtVal2.insert(0, defaultValueDict["Val2"])
    txtVal2.bind("<FocusOut>", lambda event: handlerArgs(event, "Val2", txtVal2))
    
    lbVal3 = tk.Label(positionGeneratorWindow, text="Val3: ")
    lbVal3.grid(column=1, row=12, padx=10, pady=5)
    txtVal3 = tk.Entry(positionGeneratorWindow)
    txtVal3.grid(column=2, row=12, padx=[0,10], sticky="we")
    txtVal3.insert(0, defaultValueDict["Val3"])
    txtVal3.bind("<FocusOut>", lambda event: handlerArgs(event, "Val3", txtVal3))
    
    lbVal4 = tk.Label(positionGeneratorWindow, text="Val4: ")
    lbVal4.grid(column=1, row=13, padx=10, pady=5)
    txtVal4 = tk.Entry(positionGeneratorWindow)
    txtVal4.grid(column=2, row=13, padx=[0,10], sticky="we")
    txtVal4.insert(0, defaultValueDict["Val4"])
    txtVal4.bind("<FocusOut>", lambda event: handlerArgs(event, "Val4", txtVal4))
    
    lbVal5 = tk.Label(positionGeneratorWindow, text="Val5: ")
    lbVal5.grid(column=1, row=14, padx=10, pady=5)
    txtVal5 = tk.Entry(positionGeneratorWindow)
    txtVal5.grid(column=2, row=14, padx=[0,10], sticky="we")
    txtVal5.insert(0, defaultValueDict["Val5"])
    txtVal5.bind("<FocusOut>", lambda event: handlerArgs(event, "Val5", txtVal5))
    
    # lbValid = tk.Label(positionGeneratorWindow, text="Valid: ")
    # lbValid.grid(column=1, row=15, padx=10, pady=5)
    # txtValid = tk.Entry(positionGeneratorWindow, width=15)
    # txtValid.grid(column=2, row=15)
    # txtValid.insert(0, '1')
    
    lbLevel = tk.Label(positionGeneratorWindow, text="Level: ")
    lbLevel.grid(column=1, row=16, padx=10, pady=5)
    levelStr = tk.StringVar()
    selectLevel = ttk.Combobox(positionGeneratorWindow, width=12,textvariable=levelStr)
    selectLevel.grid(column=2, row=16, padx=[0,10], sticky="we")
    selectLevel["value"] = ("Accepted", "Rejected", "Discarded")
    selectLevel.current(1)
    
    lbScore = tk.Label(positionGeneratorWindow, text="Score: ")
    lbScore.grid(column=1, row=17, padx=10, pady=5)
    txtScore = tk.Entry(positionGeneratorWindow, width=15)
    txtScore.grid(column=2, row=17, padx=[0,10], sticky="we")
    txtScore.insert(0, defaultValueDict["Score"])
    txtScore.bind("<FocusOut>", lambda event: handlerArgs(event, "Score", txtScore))
    
    # lbTag = tk.Label(positionGeneratorWindow, text="Tag: ")
    # lbTag.grid(column=1, row=18, padx=10, pady=5)
    # txtTag = tk.Entry(positionGeneratorWindow, width=15)
    # txtTag.grid(column=2, row=18)
    # txtTag.insert(0, '0')
    
    CheckRandomPos = tk.IntVar()
    CheckRandomParam = tk.IntVar()
    CheckRandomDelay = tk.IntVar()
    
    def CheckDisableRandomPos():
        nonlocal txtX, txtY, txtZ, txtRZ, C2, txtMin, txtMax
        if(CheckRandomPos.get() == 1):
            txtX.config(state=tk.DISABLED)
            txtY.config(state=tk.DISABLED)
            txtZ.config(state=tk.DISABLED)
            txtRZ.config(state=tk.DISABLED)
        else:
            txtX.config(state=tk.NORMAL)
            txtY.config(state=tk.NORMAL)
            txtZ.config(state=tk.NORMAL)
            txtRZ.config(state=tk.NORMAL)
            
    def CheckDisableRandomParam():
        nonlocal txtVal1, txtVal2, txtVal3, txtVal4, txtVal5, txtScore
        if(CheckRandomParam.get() == 1):
            C1.select()
            CheckDisableRandomPos()
            txtVal1.config(state=tk.DISABLED)
            txtVal2.config(state=tk.DISABLED)
            txtVal3.config(state=tk.DISABLED)
            txtVal4.config(state=tk.DISABLED)
            txtVal5.config(state=tk.DISABLED)
            txtScore.config(state=tk.DISABLED)
        else:
            txtVal1.config(state=tk.NORMAL)
            txtVal2.config(state=tk.NORMAL)
            txtVal3.config(state=tk.NORMAL)
            txtVal4.config(state=tk.NORMAL)
            txtVal5.config(state=tk.NORMAL)
            txtScore.config(state=tk.NORMAL)   

    C1 = tk.Checkbutton(positionGeneratorWindow, text = "Random position \n (X, Y, Z, RZ)", variable = CheckRandomPos, \
                    command=CheckDisableRandomPos, onvalue = 1, offvalue = 0, height=2, width = 20, anchor='w')
    C2 = tk.Checkbutton(positionGeneratorWindow, text = "Random parameters \n (Val1-5, Score)", variable = CheckRandomParam, \
                    command=CheckDisableRandomParam, onvalue = 1, offvalue = 0, height=2, width = 20, anchor='w')
    C3 = tk.Checkbutton(positionGeneratorWindow, text = "Random position delay", variable = CheckRandomDelay, \
                    onvalue = 1, offvalue = 0, height=2, width = 20, anchor='w')
    C1.grid(column=1, columnspan=2, row=19, padx=[10,10], sticky="we")
    C2.grid(column=1, columnspan=2, row=20, padx=[10,10], sticky="we")
    C3.grid(column=1, columnspan=2, row=21, padx=[10,10], sticky="we")

    lbMin = tk.Label(positionGeneratorWindow, text="Min number: ", anchor='w')
    lbMin.grid(column=1, row=22, padx=10, pady=5, sticky='w')
    txtMin = tk.Entry(positionGeneratorWindow, width=10)
    txtMin.grid(column=2, row=22, padx=[0,10], sticky="we")
    txtMin.insert(0, defaultValueDict["MinRandNum"])
    txtMin.bind("<FocusOut>", lambda event: handlerArgs(event, "MinRandNum", (txtMin,txtMax)))
    
    lbMax = tk.Label(positionGeneratorWindow, text="Max number: ", anchor='w')
    lbMax.grid(column=1, row=23, padx=10, pady=5, sticky='w')
    txtMax = tk.Entry(positionGeneratorWindow, width=10)
    txtMax.grid(column=2, row=23, padx=[0,10], sticky="we")
    txtMax.insert(0, defaultValueDict["MaxRandNum"])
    txtMax.bind("<FocusOut>", lambda event: handlerArgs(event, "MaxRandNum", (txtMin,txtMax)))
    CheckDisableRandomPos()
    
    lbMaxMsg = tk.Label(positionGeneratorWindow, text="Pos per pack: ", anchor='w')
    lbMaxMsg.grid(column=1, row=24, padx=10, pady=5, sticky='w')
    txtMaxMsg = tk.Entry(positionGeneratorWindow, width=10)
    txtMaxMsg.grid(column=2, row=24, padx=[0,10], sticky="we")
    txtMaxMsg.insert(0, defaultValueDict["MaxMsgNum"])
    txtMaxMsg.bind("<FocusOut>", lambda event: handlerArgs(event, "MaxMsgNum", txtMaxMsg))
    
    def SendXML(type="Positions", currentAcq = ''):
        global AcqNo
        nonlocal txtPosGenIndex, levelStr,\
                 txtScore, txtX, txtY, txtZ, txtRX, txtRY, txtRZ,\
                 txtVal1, txtVal2, txtVal3, txtVal4, txtVal5
        def generateRandParamDict():
            nonlocal CheckRandomPos, CheckRandomParam
            contentDict = {}
            if(CheckRandomPos.get() == 1):
                contentDict = {"X": str(random.random()*50 - 25),
                               "Y": str(random.random()*50 - 25),
                               "Z": str(random.random()*50 - 25),
                               "RZ": str(random.random()*360)}
            if(CheckRandomParam.get() == 1):
                contentDict.update({"Val1": str(random.random()*50),
                                    "Val2": str(random.random()*50),
                                    "Val3": str(random.random()*50),
                                    "Val4": str(random.random()*50),
                                    "Val5": str(random.random()*50),
                                    "Score": str(random.random()*100)})
            return contentDict
        
        def portSendUDP(msg):
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.sendto(msg, (txtIP.get(), int(txtUDPPort.get())))
            print(msg)
            client.close()
            
        if currentAcq == '':
            currentAcq = AcqNo
            
        if type == "NewAcq":
            root = ET.Element(type)
            root.attrib = {"AcqNo": str(currentAcq)}
            msg = ET.tostring(root, encoding='utf-8', method='xml')
            portSendUDP(msg)
        else:
            cycle = random.randint(int(txtMin.get()), int(txtMax.get()))
            # print(cycle)
            maxMsgSize = int(txtMaxMsg.get())
            tempPosList = []
            for i in range(cycle):
                fullContentDict = {"Valid": str(1),
                                   "PosGen": str(txtPosGenIndex.get()),
                                   "Level": str(AcceptLevel[levelStr.get()].value),
                                   "Score": str(txtScore.get()),
                                   # "Tag": "",
                                   "X": str(txtX.get()),
                                   "Y": str(txtY.get()),
                                   "Z": str(txtZ.get()),
                                   "RX": str(txtRX.get()),
                                   "RY": str(txtRY.get()),
                                   "RZ": str(txtRZ.get()),
                                   "Val1": str(txtVal1.get()),
                                   "Val2": str(txtVal2.get()),
                                   "Val3": str(txtVal3.get()),
                                   "Val4": str(txtVal4.get()),
                                   "Val5": str(txtVal5.get())}
                fullContentDict.update(generateRandParamDict())
                tempPosList.append(fullContentDict)
                if (i + 1) % maxMsgSize == 0 or i + 1 >= cycle:
                    root = ET.Element(type)
                    defaultDict = {"AcqNo": str(currentAcq),
                                   "PackNo": str(i//maxMsgSize),
                                   "FinalPackNo": str(math.ceil(cycle/maxMsgSize) - 1)}
                    root.attrib = defaultDict
                    for pos in tempPosList:
                        ET.SubElement(root, "Position", pos)
                    msg = ET.tostring(root, encoding='utf-8', method='xml')
                    portSendUDP(msg)
                    tempPosList.clear()
                    # time.sleep(1/100)
                    # time.sleep(random.random()/100)

    def sendPosition():
        def sendPos(lock):
            global AcqNo
            global defaultValueDict
                          
            try:
                if lock.acquire():
                    AcqNo += 1
                    currentAcq = AcqNo
                    SendXML("NewAcq")
            finally:
                lock.release()
   
            if CheckRandomDelay.get() == 1:
                time.sleep(random.random()/2)
            SendXML("Positions", currentAcq)
            
        lock = threading.Lock()
        t = threading.Thread(target=sendPos, args=(lock,))
        t.setDaemon(True)
        t.start()
            
    btnSend = tk.Button(positionGeneratorWindow, text='Generate & Send', bd=1, width=20, command=sendPosition)
    btnSend.grid(column=1, columnspan=2, row=25, padx=40, pady=[5,10], sticky="we")

    def closeWindow():
        positionGeneratorWindow.destroy()

    positionGeneratorWindow.protocol('WM_DELETE_WINDOW', closeWindow)
    positionGeneratorWindow.mainloop()
    
showPositionGeneratorDialog()