import struct,socket
import hashlib
import threading,random
import time
import struct
from base64 import b64encode, b64decode
import  RPi.GPIO as GPIO
import time
from flask import Flask
from Adafruit_PWM_Servo_Driver import PWM
import os

SensorRight = 16
SensorLeft  = 12


PWMA   = 18
AIN1   = 22
AIN2   = 27

PWMB   = 23
BIN1   = 25
BIN2   = 24

BtnPin  = 19
Gpin    = 5
Rpin    = 6

TRIG = 20
ECHO = 21
# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40,debug = False)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

class Test:
  STOPSIGNAL = 0

def setServoPulse(channel, pulse):
  pulseLength = 1000000.0                   # 1,000,000 us per second
  pulseLength /= 50.0                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096.0                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000.0
  pulse /= (pulseLength*1.0)
# pwmV=int(pluse)
  print "pluse: %f  " % (pulse)
  pwm.setPWM(channel, 0, int(pulse))

#Angle to PWM
def write(servonum,x):
  y=x/90.0+0.5
  y=max(y,0.5)
  y=min(y,2.5)
  setServoPulse(servonum,y)

def setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        
        GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
        GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
        GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

        GPIO.setup(SensorRight,GPIO.IN)
        GPIO.setup(SensorLeft,GPIO.IN)

        GPIO.setup(AIN2,GPIO.OUT)
        GPIO.setup(AIN1,GPIO.OUT)
        GPIO.setup(PWMA,GPIO.OUT)
        
        GPIO.setup(BIN1,GPIO.OUT)
        GPIO.setup(BIN2,GPIO.OUT)
        GPIO.setup(PWMB,GPIO.OUT)
        pwm.setPWMFreq(50)                        # Set frequency to 60 Hz

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def front_detection():
        write(0,90)
        time.sleep(0.5)
        dis_f = distance()
        return dis_f
def left_detection():
         write(0, 175)
         time.sleep(0.5)
         dis_l = distance()
         return dis_l
        
def right_detection():
        write(0,5)
        time.sleep(0.5)
        dis_r = distance()
        return dis_r
 
app = Flask(__name__)
def t_up(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)
        
def t_stop(t_time):
        L_Motor.ChangeDutyCycle(0)
        R_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def t_down(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def t_left(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_right(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
def keyscan():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)

@app.route('/')
def hello_world():
   return "RUNNING"

@app.route("/duoleft")
def duoleft():
   if(Test.STOPSIGNAL==0):
     Test.STOPSIGNAL = 1
     time.sleep(1)
   left_detection()
   return "duoleft"

@app.route("/duoright")
def duoright():
   if(Test.STOPSIGNAL==0):
     Test.STOPSIGNAL = 1
     time.sleep(1)  
   right_detection()
   return "duoright"

@app.route("/duofront")
def duofront():
   if(Test.STOPSIGNAL==0):
     Test.STOPSIGNAL = 1
     time.sleep(1)
   front_detection()
   return "duofront"

@app.route("/shutdown")
def shutdown():
    if(Test.STOPSIGNAL==0):
     Test.STOPSIGNAL = 1
     time.sleep(1)
    val = os.system('sudo poweroff')
    print(val)
    return "poweroff"

@app.route('/up')
def hello_world2():
   while True:
      SR_2 = GPIO.input(SensorRight)
      SL_2 = GPIO.input(SensorLeft)
      print(SL_2)
      print(SR_2) 
      #print(Test.STOPSIGNAL)
      if (SL_2 == True and SR_2 ==False):
         t_stop(0)
         time.sleep(0.4)
         t_right(50,0)
         time.sleep(0.4)
         t_stop(0)
         return "SIGLEFT"
      elif (SL_2==False and SR_2 ==True):
         t_stop(0)
         time.sleep(0.4)
         t_left(50,0)
         time.sleep(0.4)
         t_stop(0)
         return "SIGRIGHT"
      if (Test.STOPSIGNAL==1):
         return "SIGSTOP"
      dis1 = front_detection()
      if (dis1 < 40) == True:
         t_stop(0.2)
         t_down(50,0.5)
         t_stop(0.2)
         dis2 = left_detection()
         dis3 = right_detection()
         if (dis2 < 40) == True and (dis3 < 40) == True:
            t_left(50,1)
            return "Turn Left"
         elif (dis2 > dis3) == True:
            t_right(50,0.3)
            t_stop(0.1)
            return "Turn Right"
         else:
            t_left(50,0.3)
            t_stop(0.1)
            return "Turn Left"
      else:
         t_up(60,0)
         time.sleep(0.4)
         t_stop(0)


@app.route('/down')
def hello_world3():
   if(Test.STOPSIGNAL==0):
     Test.STOPSIGNAL = 1
     time.sleep(1)
   t_down(50,0)
   return "DOWN"

@app.route('/left')
def hello_world4():
   if(Test.STOPSIGNAL==0):
     Test.STOPSIGNAL = 1
     time.sleep(1) 
   t_left(50,0)
   return "LEFT"

@app.route('/right')
def hello_world5():
   if(Test.STOPSIGNAL==0):
     Test.STOPSIGNAL = 1
     time.sleep(1)
   t_right(50,0)
   return "RIGHT"

@app.route('/stop')
def hello():
   Test.STOPSIGNAL = 1
   t_stop(0)
   return "STOP"

@app.route('/start')
def start():
   Test.STOPSIGNAL = 0
   t_stop(0)
   return "SIGSTART"

if __name__ == '__main__':
   setup()
   GPIO.output(Rpin,1)
   L_Motor= GPIO.PWM(PWMA,100)
   L_Motor.start(0)
   R_Motor = GPIO.PWM(PWMB,100)
   R_Motor.start(0)
   app.run(host='0.0.0.0')