import tkinter as tk

settings = {"robot": 'x', "player": "notdefined", "difficulty": 1, "extra": 1}

def change_settings(name,value):
	settings[name] = value
	print(settings[name])


class GUI_select_robot:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.img_robot_1 = tk.PhotoImage(file="192.168.1.38.gif")
		self.img_robot_2 = tk.PhotoImage(file="192.168.1.39.gif")  
		self.button_robot_1 = tk.Button(self.frame, image=self.img_robot_1, command = lambda *args:[change_settings("robot",'192.168.1.38'),self.new_window()])
		self.button_robot_2 = tk.Button(self.frame, image=self.img_robot_2, command = lambda *args:[change_settings("robot",'192.168.1.39'),self.unpacker(self.window_select_robot), self.new_window()])
		self.button_robot_1.pack()
		self.button_robot_2.pack()
		self.frame.pack()
		self.window_select_robot = [self.button_robot_1,self.button_robot_2, self.frame]

	def unpacker(self, window_list):
		for i in window_list:
			i.pack_forget()

	def packer(self, window_list):
		for i in window_list:
			i.pack()

	def new_window(self):
		self.app = GUI_select_difficulty(self.master)

class GUI_select_difficulty:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = self.close_windows)
		self.quitButton.pack()
		self.frame.pack()
		self.difficulty_1 = tk.Button(self.frame, text = 'Difficulty 1', width = 25, command = lambda *args:[change_settings("difficulty",'1'),self.unpacker(self.window_select_difficulty),self.new_window()])
		self.difficulty_1.pack()
		self.difficulty_2 = tk.Button(self.frame, text = 'Difficulty 2', width = 25, command = lambda *args:[change_settings("difficulty",'2'),self.new_window()])
		self.difficulty_2.pack()
		self.difficulty_3 = tk.Button(self.frame, text = 'Difficulty 3', width = 25, command = lambda *args:[change_settings("difficulty",'3'),self.new_window()])
		self.difficulty_3.pack()
		self.difficulty_4 = tk.Button(self.frame, text = 'Difficulty 4', width = 25, command = lambda *args:[change_settings("difficulty",'4'),self.new_window()])
		self.difficulty_4.pack()
		self.window_select_difficulty = [self.quitButton,self.frame, self.difficulty_1, self.difficulty_2, self.difficulty_3, self.difficulty_4]
	
	def close_windows(self):
		self.app = GUI_select_robot(self.master)
		self.frame.destroy() 

	def unpacker(self, window_list):
		for i in window_list:
			i.pack_forget()

	def packer(self, window_list):
		for i in window_list:
			i.pack()

	def new_window(self):
		self.app = GUI_select_player(self.master)

class GUI_select_player:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = self.close_windows)
		self.quitButton.pack()
		self.frame.pack()
		self.player_martin = tk.Button(self.frame, text = 'Martin', width = 25, command = lambda *args:[change_settings("player",'Martin'),self.unpacker(self.window_select_player),self.new_window()])
		self.player_martin.pack()
		self.player_nina = tk.Button(self.frame, text = 'Nina', width = 25, command = lambda *args:[change_settings("player",'Nina'),self.new_window()])
		self.player_nina.pack()
		self.player_natasja = tk.Button(self.frame, text = 'Natasja', width = 25, command = lambda *args:[change_settings("player",'Natasja'),self.new_window()])
		self.player_natasja.pack()
		self.player_guest = tk.Button(self.frame, text = 'Gæst', width = 25, command = lambda *args:[change_settings("player",'Gæst'),self.new_window()])
		self.player_guest.pack()
		self.window_select_player = [self.quitButton,self.frame, self.player_martin, self.player_nina, self.player_natasja, self.player_guest]


	def new_window(self):
		self.app = GUI_player_screen(self.master)    

	def close_windows(self):
		self.app = GUI_select_difficulty(self.master)
		self.frame.destroy()    

	def unpacker(self, window_list):
		for i in window_list:
			i.pack_forget()


class GUI_player_screen:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = self.close_windows)
		self.quitButton.pack()
		self.frame.pack()
		self.img_player = tk.PhotoImage(file='%s.gif' % settings["player"])
		self.player_avatar_label = tk.Label(self.frame, image=self.img_player)
		self.player_avatar_label.pack(side=tk.LEFT)
		self.player_name_label = tk.Label(self.frame, text=settings["player"])
		self.player_name_label.pack()
		self.img_robot = tk.PhotoImage(file='%s.gif' % settings["robot"])
		self.robot_img_label = tk.Label(self.frame, image=self.img_robot)
		self.robot_img_label.pack(side=tk.LEFT)        



	def close_windows(self):
		self.app = GUI_select_player(self.master)
		self.frame.destroy()    



def main(): 
	root = tk.Tk()
	#root.attributes('-fullscreen',True)
	GUI_select_robot(root)
	root.mainloop()

while 1:
	main()
	print(settings)
