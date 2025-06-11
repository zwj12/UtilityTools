import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.10.52', 6001))
time.sleep(10)
s.close()