import time
import socket
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Forward
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Right
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Back

#memes

def Connect(HOST, PORT, s):
    i=0
    while i == 0:
        if GPIO.input(38) == False and GPIO.input (33) == True and GPIO.input(36) == True:
            HOST = '192.168.1.38'
            s.connect((HOST, PORT))
            i = 1
        if GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
            HOST = '192.168.1.39'
            s.connect((HOST, PORT))
            i = 1


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


