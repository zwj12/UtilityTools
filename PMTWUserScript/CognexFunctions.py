import tkinter as tk
import operator as op
import socket
import time
import threading

class CognexFunctions:
    position = []


    def showSensorConfigDialogCognex(self, inputTitle: str, configInfo: str):
        sensorConfigWindow = tk.Tk()
        sensorConfigWindow.title("Cognex: " + inputTitle)
        sensorConfigWindow.geometry("500x250")
        lb1 = tk.Label(sensorConfigWindow, text="Device: ")
        lb1.grid(column=1, row=1)
        txt1 = tk.Entry(sensorConfigWindow, width=30)
        txt1.grid(column=2, row=1)

        lb2 = tk.Label(sensorConfigWindow, text="IP: ")
        lb2.grid(column=1, row=2)
        txt2 = tk.Entry(sensorConfigWindow, width=30)
        txt2.grid(column=2, row=2)

        lb3 = tk.Label(sensorConfigWindow, text="White Balance: ")
        lb3.grid(column=1, row=3)
        txt3 = tk.Entry(sensorConfigWindow, width=30)
        txt3.grid(column=2, row=3)

        txt4 = tk.Entry(sensorConfigWindow, width=30)
        txt4.grid(column=2, row=4)

        txt5 = tk.Entry(sensorConfigWindow, width=30)
        txt5.grid(column=2, row=5)

        infos = configInfo.split(';')
        if len(infos) == 5:
            txt1.insert(0, infos[0])
            txt2.insert(1, infos[1])
            txt3.insert(2, infos[2])
            txt4.insert(3, infos[3])
            txt5.insert(4, infos[4])

        configureSensorValue = configInfo

        def closeWindow():
            nonlocal configureSensorValue
            configureSensorValue = txt1.get() + ";" + txt2.get() + ";" + txt3.get() + ";" + txt4.get() + ";" + txt5.get()
            sensorConfigWindow.destroy()

        sensorConfigWindow.protocol('WM_DELETE_WINDOW', closeWindow)
        sensorConfigWindow.mainloop()
        return configureSensorValue


    def showPosGenConfigDialogCognex(self, inputTitle: str, configInfo: str):
        posGenConfigWindow = tk.Tk()
        posGenConfigWindow.title("Cognex PosGens: " + inputTitle)
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
                if op.contains(infos[1], 'Geometric'):
                    button_frame_1 = tk.Canvas(posGenConfigWindow, bg="#8DB6CD", height=120, highlightcolor="black",
                                               highlightthickness=1)
                    button_frame_1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
                    button_frame_1.create_text(80, 10, text=infos[0] + ":", font=('arial', 10))
                    button_frame_1.create_text(80, 30, text=infos[1], font=('arial', 10, 'bold'))
                    button_frame_1.create_text(150, 60, text="Geometric parameter setting", font=('arial', 15))
                elif op.contains(infos[1], 'Blob'):
                    button_frame_2 = tk.Canvas(posGenConfigWindow, bg="#7CCD7C", height=120, highlightcolor="black",
                                               highlightthickness=1)
                    button_frame_2.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
                    button_frame_2.create_text(80, 10, text=infos[0] + ":", font=('arial', 10))
                    button_frame_2.create_text(80, 30, text=infos[1], font=('arial', 10, 'bold'))
                    button_frame_2.create_text(150, 60, text="Blob parameter setting", font=('arial', 15))

                if configurePosGenValue == "0":
                    configurePosGenValue = infos[0] + ":" + infos[1]
                else:
                    configurePosGenValue = configurePosGenValue + ";" + infos[0] + ":" + infos[1]

        def newGeometric():
            nonlocal clickCount
            nonlocal configurePosGenValue
            clickCount = clickCount + 1
            button_frame_1 = tk.Canvas(posGenConfigWindow, bg="#8DB6CD", height=120, highlightcolor="black",
                                       highlightthickness=1)
            button_frame_1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
            button_frame_1.create_text(80, 10, text="Position generator " + str(clickCount) + ":", font=('arial', 10))
            button_frame_1.create_text(80, 30, text="Geometric model", font=('arial', 10, 'bold'))
            button_frame_1.create_text(150, 60, text="Geometric parameter setting", font=('arial', 15))
            if configurePosGenValue == "0":
                configurePosGenValue = "Position generator " + str(clickCount) + ":Geometric model"
            else:
                configurePosGenValue = configurePosGenValue + ";Position generator " + str(clickCount) + ":Geometric model"

        btnGeometric = tk.Button(posGenConfigWindow, text='New Geometric', bd=1, width=20, command=newGeometric)
        btnGeometric.grid(column=1, row=1, padx=10, pady=5)

        def newBlob():
            nonlocal clickCount
            nonlocal configurePosGenValue
            clickCount = clickCount + 1
            button_frame_2 = tk.Canvas(posGenConfigWindow, bg="#7CCD7C", height=120, highlightcolor="black",
                                       highlightthickness=1)
            button_frame_2.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=5)
            button_frame_2.create_text(80, 10, text="Position generator " + str(clickCount) + ":", font=('arial', 10))
            button_frame_2.create_text(80, 30, text="Blob model", font=('arial', 10, 'bold'))
            button_frame_2.create_text(150, 60, text="Blob parameter setting", font=('arial', 15))
            if configurePosGenValue == "0":
                configurePosGenValue = "Position generator " + str(clickCount) + ":Blob model"
            else:
                configurePosGenValue = configurePosGenValue + ";Position generator " + str(clickCount) + ":Blob model"

        btnBlob = tk.Button(posGenConfigWindow, text='New Blob', bd=1, width=20, command=newBlob)
        btnBlob.grid(column=2, row=1, padx=10, pady=5)

        def closeWindow():
            posGenConfigWindow.destroy()

        posGenConfigWindow.protocol('WM_DELETE_WINDOW', closeWindow)
        posGenConfigWindow.mainloop()
        return configurePosGenValue


    def showStartDialogCognex(self, callback, sensorId, posGenId, posGenConfigInfo, inputTitle):
        def sendNewPosition():
            f = open(r'C:\PMScriptsLog\PlaceInfo.txt', 'a')
            f.write(self.position[0].split(';')[0]+'\t'+self.position[0].split(';')[1]+'\n')
            f.close()
            objects = {'SensorId': sensorId}
            for index in range(0, len(self.position)):
                receivedTime = callback.GetStrobeTime()
                objects.update({'Time': receivedTime})
                key = "'" + str(index) + "'"
                newPos = {key: {'X': float(self.position[index].split(';')[0].split(':')[1])/100,
                                'Y': float(self.position[index].split(';')[1].split(':')[1])/100,
                                'Z': float(6),
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

        def portRecvUDP():
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server.bind(("127.0.0.1", 8888))
            while True:
                data, addr = self.server.recvfrom(1024)
                recv_str = data.decode("ascii")
                self.position = recv_str.split('|')
                # txt1.insert(0, position[0].split(':')[1])
                # txt2.insert(1, position[1].split(':')[1])
                sendNewPosition()
                time.sleep(0.5)
            connection.close()

        # 启动线程
        threadPortUDP = threading.Thread(target=portRecvUDP)
        threadPortUDP.setDaemon(True)
        threadPortUDP.start()
        threadPortUDP.join()

