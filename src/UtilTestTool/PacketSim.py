import socket

UDP_IP = "10.42.0.1"
UDP_PORT = 5005
MESSAGE = "Hello World"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
