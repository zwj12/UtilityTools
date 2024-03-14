import tkinter as tk
import operator as op
import threading
import socket
import time

class SickFunctions:
    position = []


    def showSensorConfigDialogSICK(self, inputTitle: str, configInfo: str):
        sensorConfigWindow = tk.Tk()
        sensorConfigWindow.title("SICK: " + inputTitle)
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


    def showPosGenConfigDialogSICK(self, inputTitle: str, configInfo: str):
        posGenConfigWindow = tk.Tk()
        posGenConfigWindow.title("SICK PosGens: " + inputTitle)
        posGenConfigWindow.geometry("500x1800")
        lbList = []
        lb2List = []
        lbXList = []
        txtXList = []
        lbYList = []
        txtYList = []
        lbZList = []
        txtZList = []
        clickCount = 0
        configurePosGenValue = "0"

        posGens = configInfo.split(';')
        for posGen in posGens:
            infos = posGen.split(':')
            if len(infos) == 2:
                clickCount = clickCount + 1
                if op.contains(infos[1], 'Algorithm 1'):
                    frame1 = tk.Frame(posGenConfigWindow, highlightbackground="yellow", bd=1, relief="groove")
                    frame1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=10, ipadx=10, ipady=5)
                    lb1 = tk.Label(frame1, text=infos[0] + ":", font=('arial', 10))
                    lb1.grid(column=1, columnspan=2, row=1, padx=10, pady=5)
                    lbList.append(lb1)
                    lb2 = tk.Label(frame1, text="Algo", font=('arial', 10, 'bold'))
                    lb2.grid(column=1, columnspan=2, row=2, padx=10, pady=5)
                    lb2List.append(lb2)
                    lb1_x = tk.Label(frame1, text="x: ")
                    lb1_x.grid(column=1, row=3, padx=10, pady=5)
                    lbXList.append(lb1_x)
                    txt1_x = tk.Entry(frame1, width=30)
                    txt1_x.grid(column=2, row=3)
                    txtXList.append(txt1_x)
                    lb1_y = tk.Label(frame1, text="y: ")
                    lb1_y.grid(column=1, row=4, padx=10, pady=5)
                    lbYList.append(lb1_y)
                    txt1_y = tk.Entry(frame1, width=30)
                    txt1_y.grid(column=2, row=4)
                    txtYList.append(txt1_y)
                    lb1_z = tk.Label(frame1, text="z: ")
                    lb1_z.grid(column=1, row=5, padx=10, pady=5)
                    lbZList.append(lb1_z)
                    txt1_z = tk.Entry(frame1, width=30)
                    txt1_z.grid(column=2, row=5)
                    txtZList.append(txt1_z)

                    pos = infos[1].split(',')
                    if len(pos) >= 4:
                        lb2.config(text=pos[0])
                        txt1_x.insert(0, pos[1])
                        txt1_y.insert(1, pos[2])
                        txt1_z.insert(2, pos[3])

                    def predefinedConfirm():
                        nonlocal configurePosGenValue
                        configurePosGenValue = configurePosGenValue + "," + txt1_x.get() + "," + txt1_y.get() + "," + txt1_z.get()

                    btnConfirm = tk.Button(frame1, text='Confirm', width=20, command=predefinedConfirm)
                    btnConfirm.grid(column=1, columnspan=2, row=6)
                elif op.contains(infos[1], 'Algorithm 2'):
                    frame1 = tk.Frame(posGenConfigWindow, highlightbackground="yellow", bd=1, relief="raised")
                    frame1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=10, ipadx=10, ipady=5)
                    lb1 = tk.Label(frame1, text=infos[0] + ":", font=('arial', 10))
                    lb1.grid(column=1, columnspan=2, row=1, padx=10, pady=5)
                    lbList.append(lb1)
                    lb2 = tk.Label(frame1, text="Algo", font=('arial', 10, 'bold'))
                    lb2.grid(column=1, columnspan=2, row=2, padx=10, pady=5)
                    lb2List.append(lb2)
                    lb1_x = tk.Label(frame1, text="x: ")
                    lb1_x.grid(column=1, row=3, padx=10, pady=5)
                    lbXList.append(lb1_x)
                    txt1_x = tk.Entry(frame1, width=30)
                    txt1_x.grid(column=2, row=3)
                    txtXList.append(txt1_x)
                    lb1_y = tk.Label(frame1, text="y: ")
                    lb1_y.grid(column=1, row=4, padx=10, pady=5)
                    lbYList.append(lb1_y)
                    txt1_y = tk.Entry(frame1, width=30)
                    txt1_y.grid(column=2, row=4)
                    txtYList.append(txt1_y)
                    lb1_z = tk.Label(frame1, text="z: ")
                    lb1_z.grid(column=1, row=5, padx=10, pady=5)
                    lbZList.append(lb1_z)
                    txt1_z = tk.Entry(frame1, width=30)
                    txt1_z.grid(column=2, row=5)
                    txtZList.append(txt1_z)

                    pos = infos[1].split(',')
                    if len(pos) >= 4:
                        lb2.config(text=pos[0])
                        txt1_x.insert(0, pos[1])
                        txt1_y.insert(1, pos[2])
                        txt1_z.insert(2, pos[3])

                    def predefinedConfirm():
                        nonlocal configurePosGenValue
                        configurePosGenValue = configurePosGenValue + "," + txt1_x.get() + "," + txt1_y.get() + "," + txt1_z.get()

                    btnConfirm = tk.Button(frame1, text='Confirm', width=20, command=predefinedConfirm)
                    btnConfirm.grid(column=1, columnspan=2, row=6)

                if configurePosGenValue == "0":
                    configurePosGenValue = infos[0] + ":" + infos[1]
                else:
                    configurePosGenValue = configurePosGenValue + ";" + infos[0] + ":" + infos[1]

        def newAlgo1():
            nonlocal clickCount
            nonlocal configurePosGenValue
            clickCount = clickCount + 1
            frame1 = tk.Frame(posGenConfigWindow, highlightbackground="yellow", bd=1, relief="groove")
            frame1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=10, ipadx=10, ipady=5)
            lb1 = tk.Label(frame1, text="Position generator " + str(clickCount) + ":", font=('arial', 10))
            lb1.grid(column=1, columnspan=2, row=1, padx=10, pady=5)
            lbList.append(lb1)
            lb2 = tk.Label(frame1, text="SICK Algorithm 1", font=('arial', 10, 'bold'))
            lb2.grid(column=1, columnspan=2, row=2, padx=10, pady=5)
            lb2List.append(lb2)

            lb1_x = tk.Label(frame1, text="x: ")
            lb1_x.grid(column=1, row=3, padx=10, pady=5)
            lbXList.append(lb1_x)
            txt1_x = tk.Entry(frame1, width=30)
            txt1_x.grid(column=2, row=3)
            txtXList.append(txt1_x)
            lb1_y = tk.Label(frame1, text="y: ")
            lb1_y.grid(column=1, row=4, padx=10, pady=5)
            lbYList.append(lb1_y)
            txt1_y = tk.Entry(frame1, width=30)
            txt1_y.grid(column=2, row=4)
            txtYList.append(txt1_y)
            lb1_z = tk.Label(frame1, text="z: ")
            lb1_z.grid(column=1, row=5, padx=10, pady=5)
            lbZList.append(lb1_z)
            txt1_z = tk.Entry(frame1, width=30)
            txt1_z.grid(column=2, row=5)
            txtZList.append(txt1_z)

            def predefinedConfirm():
                nonlocal configurePosGenValue
                configurePosGenValue = configurePosGenValue + "," + txt1_x.get() + "," + txt1_y.get() + "," + txt1_z.get()

            btnConfirm = tk.Button(frame1, text='Confirm', width=20, command=predefinedConfirm)
            btnConfirm.grid(column=1, columnspan=2, row=6)

            if configurePosGenValue == "0":
                configurePosGenValue = "Position generator " + str(clickCount) + ":SICK Algorithm 1"
            else:
                configurePosGenValue = configurePosGenValue + ";Position generator " + str(clickCount) + ":SICK Algorithm 1"

        btnAlgo1 = tk.Button(posGenConfigWindow, text='New Algo1', bd=1, width=20, command=newAlgo1)
        btnAlgo1.grid(column=1, row=1, padx=10, pady=5)

        def newAlgo2():
            nonlocal clickCount
            nonlocal configurePosGenValue
            clickCount = clickCount + 1
            frame1 = tk.Frame(posGenConfigWindow, highlightbackground="yellow", bd=1, relief="raised")
            frame1.grid(column=1, columnspan=2, row=clickCount + 1, padx=10, pady=10, ipadx=10, ipady=5)
            lb1 = tk.Label(frame1, text="Position generator " + str(clickCount) + ":", font=('arial', 10))
            lb1.grid(column=1, columnspan=2, row=1, padx=10, pady=5)
            lbList.append(lb1)
            lb2 = tk.Label(frame1, text="SICK Algorithm 2", font=('arial', 10, 'bold'))
            lb2.grid(column=1, columnspan=2, row=2, padx=10, pady=5)
            lb2List.append(lb2)

            lb1_x = tk.Label(frame1, text="x: ")
            lb1_x.grid(column=1, row=3, padx=10, pady=5)
            lbXList.append(lb1_x)
            txt1_x = tk.Entry(frame1, width=30)
            txt1_x.grid(column=2, row=3)
            txtXList.append(txt1_x)
            lb1_y = tk.Label(frame1, text="y: ")
            lb1_y.grid(column=1, row=4, padx=10, pady=5)
            lbYList.append(lb1_y)
            txt1_y = tk.Entry(frame1, width=30)
            txt1_y.grid(column=2, row=4)
            txtYList.append(txt1_y)
            lb1_z = tk.Label(frame1, text="z: ")
            lb1_z.grid(column=1, row=5, padx=10, pady=5)
            lbZList.append(lb1_z)
            txt1_z = tk.Entry(frame1, width=30)
            txt1_z.grid(column=2, row=5)
            txtZList.append(txt1_z)

            def predefinedConfirm():
                nonlocal configurePosGenValue
                configurePosGenValue = configurePosGenValue + "," + txt1_x.get() + "," + txt1_y.get() + "," + txt1_z.get()

            btnConfirm = tk.Button(frame1, text='Confirm', width=20, command=predefinedConfirm)
            btnConfirm.grid(column=1, columnspan=2, row=6)

            if configurePosGenValue == "0":
                configurePosGenValue = "Position generator " + str(clickCount) + ":SICK Algorithm 2"
            else:
                configurePosGenValue = configurePosGenValue + ";Position generator " + str(clickCount) + ":SICK Algorithm 2"

        btnAlgo2 = tk.Button(posGenConfigWindow, text='New Algo2', bd=1, width=20, command=newAlgo2)
        btnAlgo2.grid(column=2, row=1, padx=10, pady=5)

        def closeWindow():
            posGenConfigWindow.destroy()

        posGenConfigWindow.protocol('WM_DELETE_WINDOW', closeWindow)
        posGenConfigWindow.mainloop()
        return configurePosGenValue


    def showStartDialogSICK(self, callback, sensorId, posGenId, posGenConfigInfo, inputTitle):
        def sendNewPosition():
            f = open(r'C:\PMScriptsLog\PickInfo.txt', 'a')
            f.write(self.position[0].split(';')[0]+'\t'+self.position[0].split(';')[1]+'\n')
            f.close()
            objects = {'SensorId': sensorId}
            for index in range(0, len(self.position)):
                receivedTime = callback.GetStrobeTime()
                objects.update({'Time': receivedTime})
                key = "'" + str(index) + "'"
                newPos = {key: {'X': float(self.position[index].split(';')[0].split(':')[1])/100,
                                'Y': float(self.position[index].split(';')[1].split(':')[1])/100,
                                'Z': float(5),
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
            self.server.bind(("192.168.10.52", 8887))
            while True:
                data, addr = self.server.recvfrom(1024)
                recv_str = data.decode("ascii")
                self.position = recv_str.split('|')
                sendNewPosition()
                time.sleep(0.5)
            connection.close()

        # 启动线程
        threadPortUDP = threading.Thread(target=portRecvUDP)
        threadPortUDP.setDaemon(True)
        threadPortUDP.start()
        threadPortUDP.join()

