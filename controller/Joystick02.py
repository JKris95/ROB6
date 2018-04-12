import time
import socket
import RPi.GPIO as GPIO

PORT = 50007
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Forward
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Right
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Back

def eightWay(s):
    while True:
        time.sleep(0.1)
        if GPIO.input(38) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Forward')
                s.sendall(b'Forward')

        elif GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Back')
                s.sendall(b'Back')

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(33) == False:
                print ('Right')
                s.sendall(b'Right')

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == False:
                print ('Left')
                s.sendall(b'Left')

        elif GPIO.input(38) == False and GPIO.input(36) == False:
                print ('Forward and Left')
                s.sendall(b'Forward and Left')

        elif GPIO.input(38) == False and GPIO.input(33) == False:
                print ('Forward and Right')
                s.sendall(b'Forward and Right')

        elif GPIO.input(35) == False and GPIO.input(36) == False:
                print ('Back and Left')
                s.sendall(b'Back and Left')

        elif GPIO.input(35) == False and GPIO.input(33) == False:
                print ('Back and Right')
                s.sendall(b'Back and Right')
        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
                print (' ')
                s.sendall(b' ')

def fourWay(s):
    while True:
        time.sleep(0.1)
        if GPIO.input(38) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Forward')
                s.sendall(b'Forward')

        elif GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Back')
                s.sendall(b'Back')

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(33) == False:
                print ('Right')
                s.sendall(b'Right')

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == False:
                print ('Left')
                s.sendall(b'Left')

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
                print (' ')
                s.sendall(b' ')

def twoWay(s):
    while True:
        time.sleep(0.1)
        if GPIO.input(38) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Forward')
                s.sendall(b'Forward')

        elif GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
                print ('Back')
                s.sendall(b'Back')

        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
                print (' ')
                s.sendall(b' ')

def angularWay(s):
    while True:
        time.sleep(0.1)
        if GPIO.input(38) == False and GPIO.input(36) == False:
                print ('Forward and Left')
                s.sendall(b'Forward and Left')

        elif GPIO.input(38) == False and GPIO.input(33) == False:
                print ('Forward and Right')
                s.sendall(b'Forward and Right')

        elif GPIO.input(35) == False and GPIO.input(36) == False:
                print ('Back and Left')
                s.sendall(b'Back and Left')

        elif GPIO.input(35) == False and GPIO.input(33) == False:
                print ('Back and Right')
                s.sendall(b'Back and Right')
        elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
                print (' ')
                s.sendall(b' ')


