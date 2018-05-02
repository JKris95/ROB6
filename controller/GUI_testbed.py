import tkinter as tk

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
		self.img_robot_1 = tk.PhotoImage(file="192.168.1.38.gif")
		self.img_robot_2 = tk.PhotoImage(file="192.168.1.39.gif")  
		self.button_robot_1 = tk.Button(self.frame, image=self.img_robot_1, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_select_difficulty)])
		self.button_robot_2 = tk.Button(self.frame, image=self.img_robot_2, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_select_difficulty)])
		self.append_window_list(self.button_robot_1,self.button_robot_2)
		self.packer(self.window_list)


class GUI_select_difficulty(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = lambda *args:[self.close_window(GUI_select_robot)])
		self.difficulty_1 = tk.Button(self.frame, text = 'Difficulty 1', width = 25, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_select_player)])
		self.difficulty_2 = tk.Button(self.frame, text = 'Difficulty 2', width = 25, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_select_player)])
		self.difficulty_3 = tk.Button(self.frame, text = 'Difficulty 3', width = 25, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_select_player)])
		self.difficulty_4 = tk.Button(self.frame, text = 'Difficulty 4', width = 25, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_select_player)])
		self.dummy = 0
		self.flip = tk.Checkbutton(self.frame, text = 'Flip', width = 25, variable = self.dummy, onvalue = 1, offvalue = 0)
		self.append_window_list(self.quitButton,self.frame, self.difficulty_1, self.difficulty_2, self.difficulty_3, self.difficulty_4, self.flip)
		self.packer(self.window_list)

class GUI_select_player(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = lambda *args:[self.close_window(GUI_select_difficulty)])
		self.player_martin = tk.Button(self.frame, text = 'Martin', width = 25, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_player_screen)])
		self.player_nina = tk.Button(self.frame, text = 'Nina', width = 25, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_player_screen)])
		self.player_natasja = tk.Button(self.frame, text = 'Natasja', width = 25, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_player_screen)])
		self.player_guest = tk.Button(self.frame, text = 'Gæst', width = 25, command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_player_screen)])
		self.append_window_list(self.quitButton,self.frame, self.player_martin, self.player_nina, self.player_natasja, self.player_guest)
		self.packer(self.window_list)

class GUI_player_screen(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, command = lambda *args:[self.close_window(GUI_select_player)])
		self.img_player = tk.PhotoImage(file='%s.gif' % "Martin") #TODO: change
		self.player_avatar_label = tk.Label(self.frame, image=self.img_player)
		self.player_avatar_label.pack(side=tk.LEFT)
		self.player_name_label = tk.Label(self.frame, text="Martin")
		self.player_name_label.pack()
		self.img_robot = tk.PhotoImage(file='%s.gif' % "Martin")
		self.robot_img_label = tk.Label(self.frame, image=self.img_robot)
		self.robot_img_label.pack(side=tk.LEFT)
		self.append_window_list(self.quitButton,self.frame)
		self.packer(self.window_list)





def main(): 
	root = tk.Tk()
	#root.attributes('-fullscreen',True)
	GUI_select_robot(root)
	root.mainloop()
while 1:
	main()
