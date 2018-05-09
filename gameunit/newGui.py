#new gui for game unit 

import tkinter as tk
import time

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

class GUI_connect_devices(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.connect_button = tk.Button(self.frame, text = 'Connect', command = lambda *args:[self.unpacker(self.window_list), self.create_connection()])
		self.nr_cones_slider = tk.Scale(root, from_=1, to=3, orient = tk.HORIZONTAL, label="Number of cones")
		self.nr_turtlebots_slider = tk.Scale(root, from_=1, to=2, orient = tk.HORIZONTAL, label="Number of Turtlebots")
		self.append_window_list(self.connect_button, self.nr_cones_slider, self.nr_turtlebots_slider)
		self.packer(self.window_list)

	def create_connection(self): #TODO: add in the socket_bind + socket_accept and the correct paremeters. 
		x = self.nr_cones_slider.get()
		y = self.nr_turtlebots_slider.get()
		print(x,y)
		time.sleep(3) #for debugging without flag for connection
		#socket_bind(HOST,PORT,numberofclients+1)
		#socket_accept(numberofclients,displayunit_address)

		self.new_window(GUI_select_game_type)
	
class GUI_select_game_type(GUI_base): #TODO: make the button presses to stuff
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.game_battle = tk.Button(self.frame, text = 'Battle', width = 25, height = 5, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_game_settings)])
		self.game_coop = tk.Button(self.frame, text = 'Coop', width = 25, height = 5, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_game_settings)])
		self.append_window_list(self.frame, self.game_battle, self.game_coop)
		self.packer(self.window_list)

class GUI_game_settings(GUI_base): #TODO: make the button presses to stuff
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, height = 5, command = lambda *args:[self.close_window(GUI_select_game_type)])


		"""
		if game == coop: #TODO: find correct flag
			self.timer_seconds = tk.Scale(root, from_=1, to=20, orient = tk.HORIZONTAL, label="Number seconds")
			self.timer_seconds.set(10) #sets the starting position to 10
			self.append_window_list(self.timer_seconds)
		"""
		self.MODES = [
			("Colors"),
			("Animals"),
			("Clocks"),
			("Random"),
		]

		self.v = tk.StringVar()
		self.v.set("Colors") # initialize

		for text in self.MODES:
			self.b = tk.Radiobutton(self.frame, text=text, variable=self.v, value=text)
			self.append_window_list(self.b)

		self.start_game = tk.Button(self.frame, text = 'START', width = 25, height = 5, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_running_window)])
		self.append_window_list(self.frame, self.start_game, self.quitButton)
		self.packer(self.window_list)		

class GUI_running_window(GUI_base): #TODO: make the button presses to stuff
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, height = 5, command = lambda *args:[self.close_window(GUI_game_settings)])
		self.cb_var = tk.BooleanVar()
		self.loop_game = tk.Checkbutton(self.frame, text = 'Loop game', width = 25, variable = self.cb_var, onvalue = True, offvalue = False, command=self.change_loop_state)
		self.current_game = tk.Label(self.frame, text="Current game")
		self.current_category = tk.Label(self.frame, text="Current category")
		self.current_player_1 = tk.Label(self.frame, text="Current player1")
		self.current_player_2 = tk.Label(self.frame, text="Current player2")
		self.current_correct_answers = tk.Label(self.frame, text="Correct answers")
		self.append_window_list(self.frame, self.loop_game, self.current_game, self.current_category, self.current_correct_answers, self.current_player_1, self.current_player_2, self.quitButton)
		self.packer(self.window_list)


	def change_loop_state(self):
		print ("variable is {0}".format(self.cb_var.get()))
		#BOOL = self.cb_var.get() #gets the current value of cb_var and puts it into player.flipped


root = tk.Tk()
#root.attributes('-fullscreen',True)
root.geometry('350x250+0+0')
GUI_connect_devices(root)
root.mainloop()