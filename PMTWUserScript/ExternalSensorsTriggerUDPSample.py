import socket
import struct

def TrigWorkArea(signalName):
    """TriggerWorkArea

    """
    HOST = '192.168.56.1'   
    PORT = 3003         
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((HOST, PORT))
        dataRequest = struct.pack(f">BHBf{len(signalName)}s", 19, len(signalName) + 5, 0, 0, signalName.encode('utf-8'))
        print(f'Request: {dataRequest.hex()} {dataRequest}')
        s.sendall(dataRequest)
        dataReceive = s.recv(1024)
        print(f'Received: {dataReceive.hex()} {dataReceive}')