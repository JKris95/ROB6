import time
import socket
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Forward
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Right
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Back

HOST = ''
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)


while True:
    time.sleep(0.1)
    if GPIO.input(38) == False and GPIO.input(33) == True and GPIO.input(36) == True:
        print ('Forward')
        conn.sendall(b'Forward')

    elif GPIO.input(35) == False and GPIO.input(33) == True and GPIO.input(36) == True:
        print ('Back')
        conn.sendall(b'Back')

    elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(33) == False:
        print ('Right')
        conn.sendall(b'Right')

    elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == False:
        print ('Left')
        conn.sendall(b'Left')

    elif GPIO.input(38) == False and GPIO.input(36) == False:
        print ('Forward and Left')
        conn.sendall(b'Forward and left')

    elif GPIO.input(38) == False and GPIO.input(33) == False:
        print ('Forward and Right')
        conn.sendall(b'Forward and Right')

    elif GPIO.input(35) == False and GPIO.input(36) == False:
        print ('Back and Left')
        conn.sendall(b'Back and Left')

    elif GPIO.input(35) == False and GPIO.input(33) == False:
        print ('Back and Right')
        conn.sendall(b'Back and Right')
    elif GPIO.input(38) == True and GPIO.input(35) == True and GPIO.input(36) == True and GPIO.input(33) == True:
        print ('')
        conn.sendall(b' ')







