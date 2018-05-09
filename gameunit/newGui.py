#new gui for game unit 

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

class GUI_connect_devices(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.connect = tk.Button(self.frame, text = 'Connect', command = lambda *args:[self.unpacker(self.window_list), self.new_window(GUI_select_difficulty)])
		self.append_window_list(self.connect)
		self.packer(self.window_list)


root = tk.Tk()
#root.attributes('-fullscreen',True)
root.geometry('350x250+0+0')
GUI_connect_devices(root)
root.mainloop()