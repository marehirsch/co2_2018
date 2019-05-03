from gpiozero import Servo
import serial
import time
time.sleep(30)

from Hologram.HologramCloud import HologramCloud
hologram = HologramCloud(dict(), network='cellular')
result = hologram.network.connect()
if result == False:
     print ' Failed to connect to cell network'

servo = Servo(17)
ser = serial.Serial("/dev/ttyS0",baudrate =9600,timeout = .5)
print " AN-137: Raspberry Pi3 to K-30 Via UART\n"
ser.flushInput()
time.sleep(1)

while 1:
 # Servo Close
 servo.max()
 print "...closing chamber..."
 time.sleep(20)
 servo.detach()
 
 cReadings = []
 for i in range(300):
        print(i)
 # co2 sensor control
        ser.flushInput()
        time.sleep(.5)
        ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
        time.sleep(.5)
        resp = ser.read(7)
        high = ord(resp[3])
        low = ord(resp[4])
        co2 = (high*256) + low
        cReadings.append(co2)
 #print "closed lid CO2 = " +str(co2)
 print (cReadings)
 
 #send to hologram cloud
 responce_code = hologram.sendMessage("closed lid: " +str(cReadings))
 #responce_code = hologram.sendMessage("closed lid: "+ str(co2))
 time.sleep(.1)

 # Servo Open
 servo.min()
 print "...opening chamber..."
 time.sleep(20)
 servo.detach()
  
 #time.sleep(60)
 time.sleep(3540)
 oReadings = []
 for i in range(60):
        print(i)
        # co2 read closed
        ser.flushInput()
        time.sleep(.5)
        ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
        time.sleep(.5)
        resp = ser.read(7)
        high = ord(resp[3])
        low = ord(resp[4])
        co2 = (high*256) + low
        oReadings.append(co2)
        #print "open lid CO2 = " +str(co2)
 print(oReadings)
 #send to hologram cloud
 responce_code = hologram.sendMessage("open lid: " + str(oReadings))
 time.sleep(1)