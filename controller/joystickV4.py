import time
import socket
import json
import RPi.GPIO as GPIO
import playerClass
import tkinter as tk
import threading
import random



class GUI_base:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.window_list = [self.frame]

	def unpacker(self, window_list):
		for i in window_list:
			i.pack_forget()

	def packer(self, window_list):
		for i in window_list:
			i.pack()

	def new_window(self, window):
		self.app = window(self.master)

	def append_window_list(self, *args):
		for i in args:
			self.window_list.append(i)	

	def close_window(self, window_to_open):
		self.app = window_to_open(self.master)
		self.frame.destroy() 

class GUI_select_robot(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.img_robot_1 = tk.PhotoImage(file='./192.168.1.38.gif')
		self.img_robot_2 = tk.PhotoImage(file='./192.168.1.39.gif')  
		self.button_robot_1 = tk.Button(self.frame, image=self.img_robot_1, command = lambda *args:[player.change_settings(player.player_info, ['robot'], ['192.168.1.38']), Connect(player.player_info['robot'], PORT, turtle_conn), Connect(GAMEUNIT_IP, GAMEUNIT_PORT, gameunit_conn), self.unpacker(self.window_list), self.new_window(GUI_select_difficulty)])
		self.button_robot_2 = tk.Button(self.frame, image=self.img_robot_2, command = lambda *args:[player.change_settings(player.player_info, ['robot'], ['192.168.1.39']), Connect(player.player_info['robot'], PORT, turtle_conn), Connect(GAMEUNIT_IP, GAMEUNIT_PORT, gameunit_conn), self.unpacker(self.window_list), self.new_window(GUI_select_difficulty)])
		self.append_window_list(self.frame)
		self.button_robot_1.pack(side=tk.LEFT)
		self.button_robot_2.pack(side=tk.LEFT)
		self.packer(self.window_list)

class GUI_select_difficulty(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		#self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, height = 5, command = lambda *args:[self.close_window(GUI_select_robot)])
		self.difficulty_1 = tk.Button(self.frame, text = 'Difficulty 1', width = 25, height = 5, command = lambda *args:[player.easy(),self.unpacker(self.window_list), self.new_window(GUI_select_player)])
		self.difficulty_2 = tk.Button(self.frame, text = 'Difficulty 2', width = 25, height = 5, command = lambda *args:[player.medium(),self.unpacker(self.window_list), self.new_window(GUI_select_player)])
		self.difficulty_3 = tk.Button(self.frame, text = 'Difficulty 3', width = 25, height = 5, command = lambda *args:[player.hard(),self.unpacker(self.window_list), self.new_window(GUI_select_player)])
		self.difficulty_4 = tk.Button(self.frame, text = 'Difficulty 4', width = 25, height = 5, command = lambda *args:[player.very_hard(),self.unpacker(self.window_list), self.new_window(GUI_select_player)])
		self.cb_var = tk.BooleanVar()
		self.flip = tk.Checkbutton(self.frame, text = 'Flip', width = 25, variable = self.cb_var, onvalue = True, offvalue = False, command=self.change_flip_state)
		self.append_window_list( self.frame, self.difficulty_1, self.difficulty_2, self.difficulty_3, self.difficulty_4, self.flip)
		self.packer(self.window_list)
	
	def change_flip_state(self):
		print ("variable is {0}".format(self.cb_var.get()))
		player.flip_directions = self.cb_var.get() #gets the current value of cb_var and puts it into player.flipped
		print("This is player.flipped", player.flip_directions)


class GUI_select_player(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, height = 5, command = lambda *args:[self.close_window(GUI_select_player)])
		self.player_martin = tk.Button(self.frame, text = 'Martin', width = 25, height = 5, command = lambda *args:[player.change_settings(player.player_info,['name'],['Martin']), change_dict_pair(status, 'running', True), send_dict(gameunit_conn, dict([ ('name', player.player_info['name']), ('robot', player.player_info['robot']) ])), self.unpacker(self.window_list), self.new_window(GUI_player_screen)])
		self.player_nina = tk.Button(self.frame, text = 'Nina', width = 25, height = 5, command = lambda *args:[player.change_settings(player.player_info,['name'], ['Nina']), change_dict_pair(status, 'running', True), send_dict(gameunit_conn, dict([ ('name', player.player_info['name']), ('robot', player.player_info['robot']) ])), self.unpacker(self.window_list), self.new_window(GUI_player_screen)])
		self.player_natasja = tk.Button(self.frame, text = 'Natasja', width = 25, height = 5,  command = lambda *args:[player.change_settings(player.player_info, ['name'], ['Natasja']), change_dict_pair(status, 'running', True), send_dict(gameunit_conn, dict([ ('name', player.player_info['name']), ('robot', player.player_info['robot']) ])), self.unpacker(self.window_list), self.new_window(GUI_player_screen)])
		self.player_guest = tk.Button(self.frame, text = 'Gæst', width = 25, height = 5, command = lambda *args:[player.change_settings(player.player_info, ['name'], ['Gæst']), change_dict_pair(status, 'running', True), send_dict(gameunit_conn, dict([ ('name', player.player_info['name']), ('robot', player.player_info['robot']) ])), self.unpacker(self.window_list), self.new_window(GUI_player_screen)])
		self.reverse_var = tk.BooleanVar()
		self.reverse_directions = tk.Checkbutton(self.frame, text = 'Reverse', width = 25, variable = self.reverse_var, onvalue = True, offvalue = False, command=player.reverse_directions)
		self.append_window_list(self.quitButton, self.frame, self.player_martin, self.player_nina, self.player_natasja, self.player_guest, self.reverse_directions)
		self.packer(self.window_list)

class GUI_player_screen(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = lambda *args:[change_dict_pair(status, 'running', False), self.close_window(GUI_select_player)])
		self.img_player = tk.PhotoImage(file='./%s.gif' % player.player_info['name'])
		self.player_avatar_label = tk.Label(self.frame, image=self.img_player) #width = 25, height = 25,
		self.player_avatar_label.pack(side=tk.LEFT)
		self.player_name_label = tk.Label(self.frame, text=player.player_info['name'], width = 25,)
		self.player_name_label.pack()
		self.img_robot = tk.PhotoImage(file='./%s.gif' % player.player_info['robot'])
		#self.img_robot = self.img_robot.subsample()
		self.robot_img_label = tk.Label(self.frame, image=self.img_robot)
		self.robot_img_label.pack(side=tk.LEFT)
		self.append_window_list(self.quitButton,self.frame)
		self.packer(self.window_list)


def main(): 
	root = tk.Tk()
	#root.attributes('-fullscreen',True)
	GUI_select_robot(root)
	root.mainloop()


def change_dict_pair(dictionary, key, value):
	dictionary[key]=value

def drive():
	if status['running']:
		control_mode = player.control_mode
		if control_mode == 'four_way':
			four_Way()
		elif control_mode == 'eight_way':
			eight_Way()
		elif control_mode == 'two_way':
			two_Way()
		elif control_mode == 'angular':
			angular()
		elif control_mode == 'rotation':
			rotate_by_default()

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

def connect(*args):
	"""Connects to the desired units corresponding to the info
	passed to it through args. args hold be tuples consisting of (socket, host, port)"""
	while 1:
		try:
			for comm_info in args:
				print(comm_info)
				comm_info[0].connect(comm_info[1], comm_info[2])
			break
		except:
			pass#print("Couldn't connect to unit with address " + comm_info[1]) 

def wait_for_input():
	"""While joystick is idle nothing is done. When joystick is activated again 
	control returns to previous function where commands are sent."""
	while True:
		for channel in CHANNELS:
			if GPIO.input(channel)==False or not status['running']:
				print("returning to caller") # Debugging
				return #return to function sending control commands


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
	random.seed()
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		print("eight way") # Debugging
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
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [-player.speeds['ang_lin'], -player.speeds['ang_ang']]))

		elif GPIO.input(40) == False and GPIO.input(38) == False:
			print ('Back and Right')
			send_dict(turtle_conn, make_dict(['lin', 'ang'], [-player.speeds['ang_lin'], player.speeds['ang_ang']]))
		
		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('stop')
			send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', 0.0) ]))
			wait_for_input()
	if player.flipped:
		player.reverse_directions()

def four_Way():
	random.seed()
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		print('four way')
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
	if player.flipped:
		player.reverse_directions()

def rotate_by_default():
	random.seed()
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		for channel in CHANNELS:
			if GPIO.input(channel) == False:
				print ('Forward')
				send_dict(turtle_conn, dict([ ('lin', player.speeds['lin']), ('ang', 0.0) ]))
			elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == True and GPIO.input(38) == True:
				print('rotate')
				send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', player.speeds['ang'])]))
				wait_for_input()
	if player.flipped:
		player.reverse_directions()

def two_Way():
	random.seed()
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		print('two way')
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
	if player.flipped:
		player.reverse_directions()
		
def angular():
	random.seed()
	while status['running'] == True:
		if player.flip_directions:
			player.flip_direction()
		time.sleep(0.1)
		print('angular')
		if GPIO.input(32) == False and GPIO.input(36) == False:
			print ('Forward and Left')
			send_dict(turtle_conn, dict([ ('lin', player.speeds['ang_lin']), ('ang', player.speeds['ang_ang']) ]))

		elif GPIO.input(32) == False and GPIO.input(38) == False:
			print ('Forward and Right')
			send_dict(turtle_conn, dict([ ('lin', player.speeds['ang_lin']), ('ang', -player.speeds['ang_ang']) ]))

		elif GPIO.input(40) == False and GPIO.input(36) == False:
			print ('Back and Left')
			send_dict(turtle_conn, dict([ ('lin', -player.speeds['ang_lin']), ('ang', -player.speeds['ang_ang']) ]))

		elif GPIO.input(40) == False and GPIO.input(38) == False:
			print ('Back and Right')
			send_dict(turtle_conn, dict([ ('lin', -player.speeds['ang_lin']), ('ang', player.speeds['ang_ang']) ]))
		
		elif GPIO.input(32) == True and GPIO.input(40) == True and GPIO.input(36) == True and GPIO.input(38) == True:
			print ('stop')
			send_dict(turtle_conn, dict([ ('lin', 0.0), ('ang', 0.0) ]))
			wait_for_input()
	if player.flipped:
		player.reverse_directions()

"""Global variables"""
player = playerClass.Player()
PORT = 50000 # port for communication between controller and turtlebots
GAMEUNIT_PORT = 50007
GAMEUNIT_IP = '192.168.1.34'
turtle_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Turtlebot communication
gameunit_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Game unit communication
status = {'running':False}

#Initialize thread object
#drive_thread = threading.Thread(target=drive, name='driving', args=(player.control_mode,))

#GPIO
CHANNELS = (32, 36, 38, 40) # FORWARD, LEFT, RIGHT, BACK
"""Global variables"""

#GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CHANNELS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Run the GUI
GUI = threading.Thread(target=main, name='GUI')
GUI.start()
while True:	
	drive()
        