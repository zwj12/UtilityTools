import tkinter
import tkinter.messagebox
import threading
import time
import socket

host = '' #INADDR_ANY               
port = 8888    
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:    
    print(f'trying to bind {host}:{port}')          
    server.bind((host, port))
    print(f'{host}:{port} is listening...')   
    data, addr = server.recvfrom(1024)
    print(f'received from {addr}: {data}')  

while True:
    time.sleep(1)