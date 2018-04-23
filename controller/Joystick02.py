import time
import socket
import json
import RPi.GPIO as GPIO
import playerClass
import tkinter as tk
import threading
import random

status = {'running':False}
PORT = 50007
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left #360
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Forward #320
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Right #380
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Back #400
GPIOs = (GPIO.input(32), GPIO.input(36), GPIO.input(38), GPIO.input(40))

player = playerClass.Player()

turtle_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""GUI_BEGIN"""

class GUI_select_robot:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.img_robot_1 = tk.PhotoImage(file='./192.168.1.38.gif')
		self.img_robot_2 = tk.PhotoImage(file='./192.168.1.39.gif')  
		self.button_robot_1 = tk.Button(self.frame, image=self.img_robot_1, command = lambda *args:[player.change_settings(player.player_info, ['robot'], ['192.168.1.36']), Connect(player.player_info['robot'], PORT, turtle_conn) ,self.new_window()])
		self.button_robot_2 = tk.Button(self.frame, image=self.img_robot_2, command = lambda *args:[player.change_settings(player.player_info, ['robot'],['192.168.1.39']), Connect(player.player_info['robot'], PORT, turtle_conn), self.new_window()])
		self.button_robot_1.pack()
		self.button_robot_2.pack()
		self.frame.pack()

	def new_window(self):
		self.newWindow = tk.Toplevel(self.master)
		self.app = GUI_select_difficulty(self.frame) #self.newWindow before

class GUI_select_difficulty:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = self.close_windows)
		self.quitButton.pack()
		self.frame.pack()
		self.difficulty_1 = tk.Button(self.frame, text = 'Difficulty 1', width = 25, command = lambda *args:[player.easy(),self.new_window()])
		self.difficulty_1.pack()
		self.difficulty_2 = tk.Button(self.frame, text = 'Difficulty 2', width = 25, command = lambda *args:[player.medium(),self.new_window()])
		self.difficulty_2.pack()
		self.difficulty_3 = tk.Button(self.frame, text = 'Difficulty 3', width = 25, command = lambda *args:[player.hard(),self.new_window()])
		self.difficulty_3.pack()
		self.difficulty_4 = tk.Button(self.frame, text = 'Difficulty 4', width = 25, command = lambda *args:[player.very_hard(),self.new_window()])
		self.difficulty_4.pack()

	def new_window(self):
		self.newWindow = tk.Toplevel(self.master)
		self.app = GUI_select_player(self.newWindow)

	def close_windows(self):
		self.master.destroy()


class GUI_select_player:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = self.close_windows)
		self.quitButton.pack()
		self.frame.pack()
		self.player_martin = tk.Button(self.frame, text = 'Martin', width = 25, command = lambda *args:[player.change_settings(player.player_info,['name'],['Martin']), change_dict_pair(status, 'running', True), spawn_thread(drive, 'Martin_drives', player.control_mode), self.new_window()])
		self.player_martin.pack()
		self.player_nina = tk.Button(self.frame, text = 'Nina', width = 25, command = lambda *args:[player.change_settings(player.player_info,['name'], ['Nina']), change_dict_pair(status, 'running', True), spawn_thread(drive, 'Nina_drives', player.control_mode), self.new_window()])
		self.player_nina.pack()
		self.player_natasja = tk.Button(self.frame, text = 'Natasja', width = 25, command = lambda *args:[player.change_settings(player.player_info, ['name'], ['Natasja']), change_dict_pair(status, 'running', True), spawn_thread(drive, 'Natasja_drives', player.control_mode), self.new_window()])
		self.player_natasja.pack()
		self.player_guest = tk.Button(self.frame, text = 'Gæst', width = 25, command = lambda *args:[player.change_settings(player.player_info, ['name'], ['Gæst']), change_dict_pair(status, 'running', True), spawn_thread(drive, 'Guest_drives', player.control_mode) ,self.new_window()])
		self.player_guest.pack()
		
	def new_window(self):
		self.newWindow = tk.Toplevel(self.master)
		self.app = GUI_player_screen(self.newWindow)    

	def close_windows(self):
		self.master.destroy()        

class GUI_player_screen:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = lambda *args:[change_dict_pair(status, 'running', False), self.close_windows()])
		self.quitButton.pack()
		self.frame.pack()
		self.img_player = tk.PhotoImage(file='./%s.gif' % player.player_info['name'])
		self.player_avatar_label = tk.Label(self.frame, image=self.img_player)
		self.player_avatar_label.pack()
		self.player_name_label = tk.Label(self.frame, text=player.player_info['name'])
		self.player_name_label.pack()
		self.img_robot = tk.PhotoImage(file='./%s.gif' % player.player_info['robot'])
		self.robot_img_label = tk.Label(self.frame, image=self.img_robot)
		self.robot_img_label.pack()        



	def close_windows(self):
		self.master.destroy()    

def main(): 
	root = tk.Tk()
	#root.attributes('-fullscreen',True)
	GUI_select_robot(root)
	root.mainloop()


def change_dict_pair(dictionary, key, value):
	dictionary[key]=value

def drive(control_mode): 
	if control_mode == 'four_way':
		four_Way()
		if player.flipped:
			player.unflip()
	elif control_mode == 'eight_way':
		eight_Way()
		if player.flipped:
			player.unflip()
	elif control_mode == 'two_way':
		two_Way()
		if player.flipped:
			player.unflip()
	elif control_mode == 'angular':
		angular()
		if player.flipped:
			player.unflip()

def spawn_thread(function, name, args):
	try:
		t = threading.Thread(target=function, name=name, args=(args,))
		t.start()
	except:
		print('Not able to start thread')

def Connect(HOST, PORT, socket_object):
	"""Connects to the desired turtlebot corresponding to the ip-address
	passed to it"""
	while 1:
		try:
			socket_object.connect((HOST, PORT))
			break
		except:
			print("Couldn't connect to TurtleBot with address " + HOST) 

def wait_for_input():
	"""While joystick is idle nothing is done. When joystick is activated again 
	control returns to previous function where commands are sent."""
	while True:
			if GPIO.input(32)==False or GPIO.input(36)==False or GPIO.input(38)==False or GPIO.input(40)== False:
				print("returning to caller") # Debugging
				break #return to function sending control commands


def send_dict(socket_object, info):
	"""Sends dictionary over socket as a series of bytes"""
	socket_object.sendall(json.dumps(info).encode())

def make_dict(keys, values):
	"""Takes a list of keys and a list of values
	and returns dictionary made from them"""
	d = {}
	for key, value in zip(keys, values):
		d[key]=value
	return d

def eight_Way():
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		print("Checking for input") # Debugging
		if GPIO.input(32) == False and GPIO.input(38) == True and GPIO.input(36) == True:
			print ('Forward')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [player.speeds['lin'], 0.0]))

		elif GPIO.input(40) == False and GPIO.input(38) == True and GPIO.input(36) == True:
			print ('Back')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [-player.speeds['lin'], 0.0]))

		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(38) == False:
			print ('Right')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [0.0, -player.speeds['ang']]))

		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == False:
			print ('Left')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [0.0, player.speeds['ang']]))

		elif GPIO.input(32) == False and GPIO.input(36) == False:
			print ('Forward and Left')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [player.speeds['ang_lin'], player.speeds['ang_ang']]))

		elif GPIO.input(32) == False and GPIO.input(38) == False:
			print ('Forward and Right')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [player.speeds['ang_lin'], -player.speeds['ang_ang']]))

		elif GPIO.input(40) == False and GPIO.input(36) == False:
			print ('Back and Left')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [-player.speeds['ang_lin'], player.speeds['ang_ang']]))

		elif GPIO.input(40) == False and GPIO.input(38) == False:
			print ('Back and Right')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [-player.speeds['ang_lin'], -player.speeds['ang_ang']]))
		
		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('stop')
			send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', 0.0) ]))
			wait_for_input()

def four_Way():
	random.seed()
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		if GPIO.input(32) == False and GPIO.input(38) == True and GPIO.input(36) == True:
			print ('Forward')
			send_dict(turtle_conn, dict([ ('lin', player.speeds['lin']), ('ang', 0.0) ]))

		elif GPIO.input(40) == False and GPIO.input(38) == True and GPIO.input(36) == True:
			print ('Back')
			send_dict(turtle_conn, dict([ ('lin', -player.speeds['lin']), ('ang', 0.0) ]))

		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(38) == False:
			print ('Right')
			send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', -player.speeds['ang']) ]))

		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == False:
			print ('Left')
			send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', player.speeds['ang']) ]))
		
		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('stop')
			send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', 0.0) ]))
			wait_for_input()
		
def two_Way():
	random.seed()
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		if GPIO.input(32) == False and GPIO.input(38) == True and GPIO.input(36) == True:
			print ('Forward')
			send_dict(turtle_conn, dict([ ('lin', player.speeds['lin']), ('ang', 0.0) ]))

		elif GPIO.input(40) == False and GPIO.input(38) == True and GPIO.input(36) == True:
			print ('Back')
			send_dict(turtle_conn, dict([ ('lin', -player.speeds['lin']), ('ang', 0.0) ]))
		
		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('stop')
			send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', 0.0) ]))
			wait_for_input()
		
def angular():
	random.seed()
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		if GPIO.input(32) == False and GPIO.input(36) == False:
			print ('Forward and Left')
			send_dict(turtle_conn, dict([ ('lin', player.speeds['ang_lin']), ('ang', player.speeds['ang_ang']) ]))

		elif GPIO.input(32) == False and GPIO.input(38) == False:
			print ('Forward and Right')
			send_dict(turtle_conn, dict([ ('lin', player.speeds['ang_lin']), ('ang', -player.speeds['ang_ang']) ]))

		elif GPIO.input(40) == False and GPIO.input(36) == False:
			print ('Back and Left')
			send_dict(turtle_conn, dict([ ('lin', -player.speeds['ang_lin']), ('ang', player.speeds['ang_ang']) ]))

		elif GPIO.input(40) == False and GPIO.input(38) == False:
			print ('Back and Right')
			send_dict(turtle_conn, dict([ ('lin', -player.speeds['ang_lin']), ('ang', -player.speeds['ang_ang']) ]))
		
		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == True and GPIO.input(38) == True:
				print ('stop')
				send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', 0.0) ]))
				wait_for_input()


while 1:
	main()
"""GUI_END"""        