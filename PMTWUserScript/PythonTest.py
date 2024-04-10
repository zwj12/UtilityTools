import socket
import struct

# str1 = "Hello world"
# bytes = str1.encode('utf-8')
# str2 = bytes.decode('utf-8')
# print(bytes)
# print(str2)

# s = struct.pack(f"@{len('123')}s", '123'.encode('utf-8'))
# print(s)

HOST = '192.168.56.1'   
PORT = 3003         
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((HOST, PORT))
    signalName = "doManSync1"
    # dataRequest = struct.pack(f">BH{len(signalName)}s", 8, len(signalName), signalName.encode('utf-8'))
    # print(f'Request: {dataRequest.hex()} {dataRequest}')
    # s.sendall(dataRequest)
    # dataReceive = s.recv(1024)
    # print(f'Received: {dataReceive.hex()} {dataReceive}')

    # dataRequest = struct.pack(f">BHB{len(signalName)}s", 16, len(signalName) + 1, 0, signalName.encode('utf-8'))
    # print(f'Request: {dataRequest.hex()} {dataRequest}')
    # s.sendall(dataRequest)
    # dataReceive = s.recv(1024)
    # print(f'Received: {dataReceive.hex()} {dataReceive}')

    dataRequest = struct.pack(f">BHBf{len(signalName)}s", 19, len(signalName) + 5, 0, 0, signalName.encode('utf-8'))
    print(f'Request: {dataRequest.hex()} {dataRequest}')
    s.sendall(dataRequest)
    dataReceive = s.recv(1024)
    print(f'Received: {dataReceive.hex()} {dataReceive}')