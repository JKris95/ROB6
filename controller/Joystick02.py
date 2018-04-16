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
GPIOs = (GPIO.input(40), GPIO.input(38), GPIO.input(36), GPIO.input(32))

player = playerClass.Player()

turtle_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Connect(self, HOST, PORT, socket_object):
    """Connects to the desired turtlebot corresponding to the ip-address
    passed to it"""
    try:
        socket_object.connect((HOST, PORT))
    except:
        print("Couldn't connect to TurtleBot with address " + HOST) 

def wait_for_input():
	"""While joystick is idle nothing is done. When joystick is activated again 
	control returns to previous function where commands are sent."""
	while True:
		for GPIO in GPIOs:
			if not GPIO:
				return #return to function sending control commands 

def send_dict(socket_object, info):
	"""Sends dictionary over socket as a series of bytes"""
	socket_object.sendall(json.dumps(info).decode())

def make_dict(keys, values):
	"""Takes a list of keys and a list of values
	and returns dictionary made from them"""
	d = {}
	for key, value in zip(keys, values):
		d[key]=value
	return d

def eight_Way():
    while status['running'] == True:
        time.sleep(0.1)
        if GPIO.input(40) == False and GPIO.input(36) == True and GPIO.input(38) == True:
            print ('Forward')
            send_dict(turtle_conn, make_dict(['lin', 'ang'], [player.lin_speed, 0]))

        elif GPIO.input(32) == False and GPIO.input(36) == True and GPIO.input(38) == True:
            print ('Back')
            send_dict(turtle_conn, make_dict(['lin', 'ang'], [-player.lin_speed, 0]))

        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(36) == False:
            print ('Right')
            send_dict(turtle_conn, make_dict(['lin', 'ang'], [0, -player.ang_speed]))

        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == False:
            print ('Left')
            send_dict(turtle_conn, make_dict(['lin', 'ang'], [0, player.ang_speed]))

        elif GPIO.input(40) == False and GPIO.input(38) == False:
            print ('Forward and Left')
            send_dict(turtle_conn, make_dict(['lin', 'ang'], [player.ang_lin, player.ang_ang]))

        elif GPIO.input(40) == False and GPIO.input(36) == False:
            print ('Forward and Right')
            send_dict(turtle_conn, make_dict(['lin', 'ang'], [player.ang_lin, -player.ang_ang]))

        elif GPIO.input(32) == False and GPIO.input(38) == False:
            print ('Back and Left')
            send_dict(turtle_conn, make_dict(['lin', 'ang'], [-player.ang_lin, player.ang_ang]))

        elif GPIO.input(32) == False and GPIO.input(36) == False:
            print ('Back and Right')
            send_dict(turtle_conn, make_dict(['lin', 'ang'], [-player.ang_lin, -player.ang_ang]))
        
        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == True and GPIO.input(36) == True:
            print ('stop')
            send_dict(turtle_conn, dict([ ('lin', 0), ('ang', 0) ]))
            wait_for_input()

def four_Way():
	while status['running'] == True:
		time.sleep(0.1)
		if GPIO.input(40) == False and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('Forward')
			send_dict(turtle_conn, dict([ ('lin', player.lin_speed), ('ang', 0) ]))

		elif GPIO.input(32) == False and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('Back')
			send_dict(turtle_conn, dict([ ('lin', -player.lin_speed), ('ang', 0) ]))

		elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(36) == False:
			print ('Right')
			send_dict(turtle_conn, dict([ ('lin', 0), ('ang', -player.ang_speed) ]))

		elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == False:
			print ('Left')
			send_dict(turtle_conn, dict([ ('lin', 0), ('ang', player.ang_speed) ]))
        
		elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == True and GPIO.input(36) == True:
			print ('stop')
			send_dict(turtle_conn, dict([ ('lin', 0), ('ang', 0) ]))
			wait_for_input()
        
def two_Way():
    while status['running'] == True:
        time.sleep(0.1)
        if GPIO.input(40) == False and GPIO.input(36) == True and GPIO.input(38) == True:
            print ('Forward')
            send_dict(turtle_conn, dict([ ('lin', player.lin_speed), ('ang', 0) ]))

        elif GPIO.input(32) == False and GPIO.input(36) == True and GPIO.input(38) == True:
            print ('Back')
            send_dict(turtle_conn, dict([ ('lin', -player.lin_speed), ('ang', 0) ]))
        
        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == True and GPIO.input(36) == True:
            print ('stop')
            send_dict(turtle_conn, dict([ ('lin', 0), ('ang', 0) ]))
            wait_for_input()
        
def angular():
    while status['running'] == True:
        time.sleep(0.1)
        if GPIO.input(40) == False and GPIO.input(38) == False:
            print ('Forward and Left')
            send_dict(turtle_conn, dict([ ('lin', player.ang_lin), ('ang', player.ang_ang) ]))

        elif GPIO.input(40) == False and GPIO.input(36) == False:
            print ('Forward and Right')
            send_dict(turtle_conn, dict([ ('lin', player.ang_lin), ('ang', -player.ang_ang) ]))

        elif GPIO.input(32) == False and GPIO.input(38) == False:
            print ('Back and Left')
            send_dict(turtle_conn, dict([ ('lin', -player.ang_lin), ('ang', player.ang_ang) ]))

        elif GPIO.input(32) == False and GPIO.input(36) == False:
            print ('Back and Right')
            send_dict(turtle_conn, dict([ ('lin', -player.ang_lin), ('ang', -player.ang_ang) ]))
        
        elif GPIO.input(40) == True and GPIO.input(32) == True and GPIO.input(38) == True and GPIO.input(36) == True:
                print ('stop')
                send_dict(turtle_conn, dict([ ('lin', 0), ('ang', 0) ]))
                wait_for_input()
        
def drive(control_mode): 
    if control_mode == 'four_way':
        four_Way()
    elif control_mode == 'eight_way':
        eight_Way()
    elif control_mode == 'two_way':
        two_Way()
    elif control_mode == 'angular':
        angular()



"""		
#Possibly redundant - currently trying out difficulty handling from the class
def set_difficulty(settings):
    global player
    player = playerClass.Player(settings)
"""
