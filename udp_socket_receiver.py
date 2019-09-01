import socket
import time
from datetime import datetime

UDP_IP = ""
UDP_PORT = 8080
BUFFER_SIZE = 100 #26 #1024

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
myfile = "logs/log_nbiot" + str(int(time.time()))
f=open('%s.csv' % myfile, "a+")
try:
    while True:
        print ("Servidor a la escucha...")
        data, addr = sock.recvfrom(BUFFER_SIZE) # buffer size
        mensaje, seconds_client = data.split("#")
        seconds_server = time.time()
                mynow = datetime.now()
        st = datetime.fromtimestamp(float(seconds_client)).strftime('%Y-%m-%d %$
        diferencia = float(seconds_server) - float(seconds_client)
        reg = str(st) + ',' + str(addr) + ',' + \
                data + ',' + \
                str(float(seconds_client)) + ',' + \
                str(float(seconds_server)) + ',' + \
                str(diferencia) + \
                '\n'
        f.write(reg)
                st = datetime.fromtimestamp(float(seconds_client)).strftime('%Y-%m-%d %$
        diferencia = float(seconds_server) - float(seconds_client)
        reg = str(st) + ',' + str(addr) + ',' + \
                data + ',' + \
                str(float(seconds_client)) + ',' + \
                str(float(seconds_server)) + ',' + \
                str(diferencia) + \
                '\n'
        f.write(reg)
        print ("received message:", data, addr)
        #reenvia dato a cliente
        second_server = time.time()
        data = mensaje + ';' + str(second_server)
        sock.sendto(data.encode('utf-8'),addr)
        #print ("Mensaje:", mensaje)
        #print ("Send time   :", seconds_client)
        #print ("Receive time:", seconds_server)
        #print ("   Tiempo transcurrido:", diferencia)
except KeyboardInterrupt:
        f.close()
