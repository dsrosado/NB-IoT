from network import LTE
import socket

def send_at_cmd_pretty(cmd):
    response = lte.send_at_cmd(cmd).split('\r\n')
    print()
    print("Comando: ", cmd)
    for line in response:
        if line != "":
            print("Respuesta: ", line)

def main():
    print("inicio")
    send_at_cmd_pretty('AT+CFUN=0')
    send_at_cmd_pretty('AT+CFUN=1') # Starts up the unit
    send_at_cmd_pretty('AT+NBAND=20') # To work in the spanish network you need to set band 20 to use 800MHz
    # send_at_cmd_pretty('AT+COPS=1,2,"21401"') # This is connection to vodafone ES
    # send_at_cmd_pretty('AT+COPS=0,0,"21401"') # This is connection to Telefonica ES
    send_at_cmd_pretty('AT+CIMI')
    send_at_cmd_pretty('AT+NUESTATS') # This is to check signal strength
    send_at_cmd_pretty('AT+NSOCR=DGRAM,17,8080') # Open socket (nunca ha funcionado así)
    send_at_cmd_pretty('AT+NSOST=0,00.000.00.000,8080,2,FFFF') # Send 2 dummy bytes to ip UPD server (idem ant)
    send_at_cmd_pretty('AT+COPS?') # Am I connected?
    send_at_cmd_pretty('AT+NSORF=0,3') # In case I receive any byte give me the last 3.

    send_at_cmd_pretty('AT+CGDCONT=1,"IP","ep.inetd.gdsp"') #  Comprueba asignación ip: '\r\n+CGDCONT: 1,"IP","ep.inetd.gdsp",,,,0,0,0,0,0,0,0,,0\r\n\r\nOK\r\n'
    #send_at_cmd_pretty('AT+CGDCONT=1,"IP","sm2ms.movistar.es"')
    send_at_cmd_pretty('AT+CSCON?')
    send_at_cmd_pretty('AT+CGPADDR=1')
    send_at_cmd_pretty('AT+CREG?') # Possible values of registration status are, 0 not registered,
    send_at_cmd_pretty('AT+CPIN?') # SIM status
    send_at_cmd_pretty('At+cgdcont?')
    send_at_cmd_pretty('AT+CGSN=1') # IMEI
    send_at_cmd_pretty('AT+CGSN')
    send_at_cmd_pretty('AT+CSQ') # signal strength of the device
    send_at_cmd_pretty('AT+CGACT')

    print('========================')
    if not lte.isattached():
        i = 0
        lte.attach(band=20, apn="ep.inetd.gdsp ")  #  ep.inetd.gdsp sm2ms.movistar.es
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

    lte.disconnect()
    lte.dettach()


main()
