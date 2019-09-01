import machine
import utime
from network import WLAN
import time
import os

def setRTCLocalTime():
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    mytime=rtc.now()
    utime.sleep_ms(750)
    print('\nRTC Set from NTP to UTC:', mytime)
    utime.timezone(+3600)
    print (utime.localtime())
    print (time.time())

    mytime = rtc.now()
    myseconds = calcMicroseconds(time.time(), mytime[6])
    print(myseconds)

def calcMicroseconds(seconds, microsecs):
    #seconds_int = int(rtcnow-sec)
    decimals = 10 ** (-1 * len(str(microsecs)))
    second_tot = int(seconds) + (microsecs * decimals)
    print('Seconds:', seconds)
    print('decimals:', decimals)
    print('microSeconds:', microsecs)
    print('(microsecs * decimals):', (microsecs * decimals))
    print('second_tot:', second_tot)

    return second_tot

print('FW:',os.uname()[2])
wlan = WLAN(mode=WLAN.STA, power_save=True)
wlan.connect('youruser', auth=(3, 'yourpasswd'), timeout=5000)
while not wlan.isconnected():
    print('Connecting to WIFI')
    time.sleep(1)
print('WIFI connected')
time.sleep(1)
setRTCLocalTime()
