import time
import socket
import json
import RPi.GPIO as GPIO
import playerClass

status = {'running':False}
PORT = 50007
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Forward
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Right
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Back


player = playerClass.Player()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Connect(self, HOST, PORT, socket_object):
    """Connects to the desired turtlebot corresponding to the ip-address
    passed to it"""
    try:
        socket_object.connect((HOST, PORT))
    except:
        print("Couldn't connect to TurtleBot with address " + HOST) 

def wait_for_input(control_mode):
	GPIOs = (GPIO.input(40), GPIO.input(38), GPIO.input(36), GPIO.input(32))
	while True:
		for GPIO in GPIOs:
			if not GPIO:
				return # returns control to drive()

def eight_Way(socket_object):
    while status['running'] == True:
        time.sleep(0.1)
        if GPIO.input(40) == False and GPIO.input(36) == True and GPIO.input(38) == True:
            print ('Forward')
            s.sendall(json.dumps(player.speeds).decode)

        elif GPIO.input(32) == False and GPIO.input(36) == True and GPIO.input(38) == True:
            print ('Back')
            s.sendall(b'Back')

        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(36) == False:
            print ('Right')
            s.sendall(b'Right')

        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == False:
            print ('Left')
            s.sendall(b'Left')

        elif GPIO.input(40) == False and GPIO.input(38) == False:
            print ('Forward and Left')
            s.sendall(b'Forward and Left')

        elif GPIO.input(40) == False and GPIO.input(36) == False:
            print ('Forward and Right')
            s.sendall(b'Forward and Right')

        elif GPIO.input(32) == False and GPIO.input(38) == False:
            print ('Back and Left')
            s.sendall(b'Back and Left')

        elif GPIO.input(32) == False and GPIO.input(36) == False:
            print ('Back and Right')
            s.sendall(b'Back and Right')
        
        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == True and GPIO.input(36) == True:
            print ('stop')
            s.sendall(json.dumps({'lin': 0, 'ang': 0}).decode())
        
def four_Way(socket_object):
	while status['running'] == True:
		time.sleep(0.1)
		if GPIO.input(40) == False and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('Forward')
			s.sendall(b'Forward')

		elif GPIO.input(32) == False and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('Back')
			s.sendall(b'Back')

		elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(36) == False:
			print ('Right')
			s.sendall(b'Right')

		elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == False:
			print ('Left')
			s.sendall(b'Left')
        
		elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == True and GPIO.input(36) == True:
			print ('stop')
			s.sendall(json.dumps({'lin': 0, 'ang': 0}).decode())
			break #Returns control to drive()
        
def two_Way(socket_object):
    while status['running'] == True:
        time.sleep(0.1)
        if GPIO.input(40) == False and GPIO.input(36) == True and GPIO.input(38) == True:
            print ('Forward')
            s.sendall(b'Forward')

        elif GPIO.input(32) == False and GPIO.input(36) == True and GPIO.input(38) == True:
            print ('Back')
            s.sendall(b'Back')
        
        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == True and GPIO.input(36) == True:
                print ('stop')
                s.sendall(json.dumps({'lin': 0, 'ang': 0}).decode())
        
def angular(socket_object):
    while status['running'] == True:
        time.sleep(0.1)
        if GPIO.input(40) == False and GPIO.input(38) == False:
            print ('Forward and Left')
            s.sendall(b'Forward and Left')

        elif GPIO.input(40) == False and GPIO.input(36) == False:
            print ('Forward and Right')
            s.sendall(b'Forward and Right')

        elif GPIO.input(32) == False and GPIO.input(38) == False:
            print ('Back and Left')
            s.sendall(b'Back and Left')

        elif GPIO.input(32) == False and GPIO.input(36) == False:
            print ('Back and Right')
            s.sendall(b'Back and Right')
        
        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == True and GPIO.input(36) == True:
                print ('stop')
                s.sendall(json.dumps({'lin': 0, 'ang': 0}).decode())
        

def send_dict(socket_object, info):
	"""Sends dictionary with relevant info to turtlebot"""
	socket_object.sendall(json.dumps(info).decode())

def drive(control_mode):
    while status['running']==True: 
        if control_mode == 'four_way':
            four_Way(s)
        elif control_mode == 'eight_way':
                eight_Way(s)
        elif control_mode == 'two_way':
            two_Way(s)
        elif control_mode == 'angular':
            angular(s)
		else:
			wait_for_input(control_mode)
#Possibly redundant - currently trying out difficulty handling from the class
def set_difficulty(settings):
    global player
    player = playerClass.Player(settings)

