  GNU nano 2.2.6                                                                                                                                                                                                                                                                                                                                                                                                       File: Joystick.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

import time
import json
import socket
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Forward
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Right
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Back

speedAngular = 1.0 #Change turning speed
speedLinear = 0.15 #Change linear speed
speedAngularAngular = 0.15 #Change turning speed when driving linear and turning
speedAngularLinear = 0.1 #Change linear speed when driving linear and turning
sleep = 0.05

def Connect(HOST, PORT, s):
    i=0
    while i == 0:
        if GPIO.input(38) == False and GPIO.input (33) == True and GPIO.input(36) == True:
            HOST = '192.168.1.64'
            s.connect((HOST, PORT))
            i = 1
        if GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
            HOST = '192.168.1.39'
            s.connect((HOST, PORT))
            i = 1


def eightWay(s):
    while True:
        time.sleep(sleep)
        if GPIO.input(38) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Forward')
                arr = [-speedLinear,0.0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Back')
                arr = [speedLinear,0.0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())
        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
                print ('Stop')
                arr = [0.0,0.0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(33) == False:
                print ('Right')
                arr = [0.0,-speedAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == False:
                print ('Left')
                arr = [0.0,speedAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(38) == False and GPIO.input(36) == False:
                print ('Forward and Left')
                arr = [-speedAngularLinear,speedAngularAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(38) == False and GPIO.input(33) == False:
                print ('Forward and Right')
                arr = [-speedAngularLinear,-speedAngularAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(35) == False and GPIO.input(36) == False:
                print ('Back and Left')
                arr = [speedAngularLinear,speedAngularAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(35) == False and GPIO.input(33) == False:
                print ('Back and Right')
                arr = [speedAngularLinear,-speedAngularAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

def fourWay(s):
    while True:
        time.sleep(sleep)
        if GPIO.input(38) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Forward')
                arr = [-speedLinear,0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Back')
                arr = [speedLinear,0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())
        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
                print ('Stop')
                arr = [0,0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(33) == False:
                print ('Right')
                arr = [0,-speedAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == False:
                print ('Left')
                arr = [0,speedAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

def twoWay(s):
    while True:
        time.sleep(sleep)
        if GPIO.input(38) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Forward')
                arr = [-speedLinear,0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Back')
                arr = [speedLinear,0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())
        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
                print ('Stop')
                arr = [0,0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

def angularWay(s):
    while True:
        time.sleep(sleep)
        if GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
                print ('Stop')
                arr = [0,0]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(38) == False and GPIO.input(36) == False:
                print ('Forward and Left')
                arr = [-speedAngularLinear,speedAngularAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(38) == False and GPIO.input(33) == False:
                print ('Forward and Right')
                arr = [-speedAngularLinear,-speedAngularAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(35) == False and GPIO.input(36) == False:
                print ('Back and Left')
                arr = [speedAngularLinear,speedAngularAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())

        elif GPIO.input(35) == False and GPIO.input(33) == False:
                print ('Back and Right')
                arr = [speedAngularLinear,-speedAngularAngular]
                data = json.dumps({"a": arr})
                s.sendall(data.encode())
def choseMode():
    i=0
    while i == 0:
        if GPIO.input(38) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('8-way')
                chose = 1
                i=1
                return chose

        elif GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('2-way')
                chose = 2
                i=1
                return chose

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(33) == False:
                print ('4-way')
                chose = 3
                i=1
                return chose

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == False:
                print ('angular-way')
                chose = 4
                i=1
                return chose


if __name__=="__main__":
    HOST = ''
    PORT = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Connect(HOST, PORT, s)
    time.sleep(0.5)
    chose = choseMode()
    if chose == 1:
        eightWay(s)
    elif chose == 2:
        twoWay(s)
    elif chose == 3:
        fourWay(s)
    elif chose == 4:
        angularWay(s)














































