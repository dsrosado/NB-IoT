import time
import socket
import ssl
import pycom
import machine
from network import LTE

def send_at_cmd_pretty(cmd):
    response = lte.send_at_cmd(cmd).split('\r\n')
    print()
    print("Comando: ", cmd)
    for line in response:
        if line != "":
            print("Respuesta: ", line)

def send_UDP_socket(mymensaje):
    rtc = machine.RTC()
    mytime = rtc.now()
    #madseconds = float(str(time.time()) + '.' + str(mytime[6]))
    #MESSAGE =  mymensaje + str(madseconds) # Micropython no gestiona más de tres decimales
    # Decimas de segundo: mytime[6]
    sendtime = str(time.time()) + '.' + str(mytime[6])
    MESSAGE =  mymensaje + sendtime
    #print (MESSAGE)
    sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
    #recibe respuesta
    data = sock.recv(BUFFER_SIZE)
    mytime = rtc.now()
    rectime = str(time.time()) + '.' + str(mytime[6])
    mydata = str(data)
    mensaje, seconds_server = mydata.split(";")

    # print ("\nEnviado...")
    # print('RTC Set from NTP to UTC:', mytime)
    # print ("UDP target IP:", UDP_IP)
    # print ("UDP target port:", UDP_PORT)
    # print ("Date/Time:", rtc.now())
    # print ("Enviado:", MESSAGE)
    longitud = len(seconds_server) - 1
    # Salida del servidos ; Enrtrada al cliente
    print (seconds_server[0:longitud],';',rectime)

def main():
    print("inicio: Telefonica")
    # send_at_cmd_pretty('AT+CGDCONT=1,"IP","ep.inetd.gdsp"')
    # send_at_cmd_pretty('AT+CSCON?')
    # send_at_cmd_pretty('AT+CGPADDR=1')
    # send_at_cmd_pretty('AT+CREG?')
    # send_at_cmd_pretty('AT+CPIN?')
    # send_at_cmd_pretty('AT+COPS?')
    # send_at_cmd_pretty('AT+CGPADDR=1')
    # #send_at_cmd_pretty('AT+CGDCONT=1,"IP","ep.inetd.gdsp"')
    # send_at_cmd_pretty('AT+CFUN=1') #Start up the unit
    # send_at_cmd_pretty('AT+NUESTATS') #Chequea estado de ka cibexuñib
    if not lte.isattached():
        i = 0
        lte.attach(band=20, apn="sm2ms.movistar.es") #ep.inetd.gdsp sm2ms.movistar.es
        while not lte.isattached():
            i = i + 1
            print("not attached: {}".format(i))
            time.sleep(2)
        print("Attached!")

    if not lte.isconnected():
        lte.connect()       # start a data session and obtain an IP address
        while not lte.isconnected():
            time.sleep(2)
            print('Connecting...')
        print("Connected!")

    # Realizamos 5 tandas de 10 envíos cada una. 1 tanda cada 1 segundos
    str3 = "00000000000000000000000000000000000000000000000000" # 99 bytes
    str1024 = ""
    for i in range(19): # MAX Payload admitido 1600 bytes
        str1024 = str1024 + str3

    bytes50 = "00000000000000000000000000000000000000000000000000" # para llegar a 150 bytes
    bytes79 = "000000000000000000000000000000" # Al sumarlos a mymensaje son 100 bytes
    for i in range(1):
        for j in range(100):
            # mymensaje= str(i) + " " + str(j) + " #"
            # mymensaje= bytes50 + str(i) + " " + str(j) + " #"
            # mymensaje= bytes50 + bytes79 + str(i) + " " + str(j) + " #"
            mymensaje= str1024 + str(i) + " " + str(j) + " #"
            send_UDP_socket(mymensaje)
            time.sleep (1)
        #time.sleep(1)

BUFFER_SIZE = 2048 #100 #1024

lte = LTE()
UDP_IP = 'yourIPcloud'
UDP_PORT = 8080 #5005
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
print("Socket abierto!")
main()
sock.close()
lte.disconnect()
lte.dettach()
