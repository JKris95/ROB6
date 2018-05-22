import socket
from random import randrange
import time
import tkinter as tk
import _thread
from gameClass import GameType
import json
from sqlalchemy import create_engine




#Global variables
all_connections = {'cones': [], 'displayunit': [], 'turtlebots': [], 'turtlebot_masters': [], 'controllers':[]}
all_addresses = {'cones': [], 'displayunit': [], 'turtlebots': [], 'turtlebot_masters': [], 'controllers':[]}
turtlebot_ips = ['192.168.1.36', '192.168.1.40','192.168.1.38', '192.168.1.39' ]
controller_ips = ['192.168.1.43', '192.168.1.45']
displayunit_address = ['192.168.1.44']
HOST=''
PORT=50007
conesInGame = False
receive_threads_created = False
controller_started = False
times_lock = _thread.allocate_lock()
game_instance = GameType()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
engine = create_engine('sqlite:///GAMEDATA.db', echo=False)

#GUI START
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
		self.nr_cones_slider = tk.Scale(self.frame, from_=1, to=3, orient = tk.HORIZONTAL, label="Number of cones")
		self.nr_turtlebots_slider = tk.Scale(self.frame, from_=0, to=2, orient = tk.HORIZONTAL, label="Number of Turtlebots")
		self.append_window_list(self.connect_button, self.nr_cones_slider, self.nr_turtlebots_slider)
		self.packer(self.window_list)

	def create_connection(self): 
		game_instance.nr_of_clients["cones"] = self.nr_cones_slider.get()
		game_instance.nr_of_clients["turtlebots"] = self.nr_turtlebots_slider.get()
		game_instance.nr_of_clients['controllers'] = self.nr_turtlebots_slider.get()
		socket_bind(s, HOST, PORT, sum(game_instance.nr_of_clients.values()))
		socket_accept(sum(game_instance.nr_of_clients.values()), all_connections, all_addresses)
		self.new_window(GUI_select_game_type)
	
class GUI_select_game_type(GUI_base): 
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.game_battle = tk.Button(self.frame, text = 'Battle', width = 25, height = 5, command = lambda *args:[self.unpacker(self.window_list), setattr(game_instance, 'game_type', 'battle'), self.new_window(GUI_game_settings)])
		self.game_coop = tk.Button(self.frame, text = 'Coop', width = 25, height = 5, command = lambda *args:[self.unpacker(self.window_list), setattr(game_instance, 'game_type', 'coop'), self.new_window(GUI_game_settings)])
		#self.save_data = tk.Button(self.frame, text = 'Save game data', width = 25, height = 5, command = lambda *args:[self.transfer_dataframe_to_database()])
		self.append_window_list(self.frame, self.game_battle, self.game_coop)
		self.packer(self.window_list)

	def transfer_dataframe_to_database(self):
		game_instance.results.to_sql('game_data', con=engine, if_exists='append')
		print("Game data saved in database")

	def fetch_data_from_database(self):
		"""
		Loads all the data placed into the database. 
		"""
		loaded_data = engine.execute("SELECT * FROM game_data").fetchall()
		print(loaded_data)
class GUI_game_settings(GUI_base): #TODO: make the button presses to stuff
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.quitButton = tk.Button(self.frame, text = 'Back', width = 25, height = 5, command = lambda *args:[self.close_window(GUI_select_game_type)])

		self.timer_seconds = tk.Scale(self.frame, from_=1, to=20, orient = tk.HORIZONTAL, label="Number seconds")
		self.timer_seconds.set(10) #sets the starting position to 10
		if game_instance.game_type == 'coop': 
			self.append_window_list(self.timer_seconds)
			setattr(game_instance, 'nr_true', 2)
		elif game_instance.game_type == 'battle':
			setattr(game_instance, 'nr_true', 1)
		
		self.MODES = [
			("colors"),
			("animals"),
			("times"),
			("random"),
		]

		self.v = tk.StringVar()
		self.v.set("Colors") # initialize

		for text in self.MODES:
			self.b = tk.Radiobutton(self.frame, text=text, variable=self.v, value=text)
			self.append_window_list(self.b)

		self.start_game = tk.Button(self.frame, text = 'START', width = 25, height = 5, command = lambda *args:[self.unpacker(self.window_list), setattr(game_instance, 'category', self.v.get()), setattr(game_instance, 'time_limit', self.timer_seconds.get()), startTheGame(), self.new_window(GUI_running_window)])
		self.append_window_list(self.frame, self.start_game, self.quitButton)
		self.packer(self.window_list)
		

class GUI_running_window(GUI_base):
	def __init__(self, master):
		GUI_base.__init__(self,master)
		self.cb_var = tk.BooleanVar()
		self.loop_game = tk.Checkbutton(self.frame, text = 'Loop game', width = 25, variable = self.cb_var, onvalue = True, offvalue = False, command=self.change_loop_state)
		self.current_game = tk.Label(self.frame, text=game_instance.game_type)
		self.current_category = tk.Label(self.frame, text=game_instance.category)
		
		try: 
			self.current_player_1 = tk.Label(self.frame, text=game_instance.players[0]["name"])
			self.append_window_list(self.current_player_1)
		except IndexError:
			print("IndexError 1")

		try:
			self.current_player_2 = tk.Label(self.frame, text=game_instance.players[1]["name"])
			self.append_window_list(self.current_player_2)
		except IndexError:
			print("IndexError 2")
		
		self.append_window_list(self.frame, self.loop_game, self.current_game, self.current_category)
		self.packer(self.window_list)
		_thread.start_new_thread(self.play_again, ())

	def change_loop_state(self):
		print ("variable is {0}".format(self.cb_var.get()))
		game_instance.loop_game = self.cb_var.get() #gets the current value of cb_var and puts it into player.flipped

	def play_again(self):
		while True:
			if game_instance.game_is_running == False:
				self.close_window(GUI_game_settings)
				break
			time.sleep(1)
#GUI END



def main():
	root = tk.Tk()
	#root.attributes('-fullscreen',True)
	root.geometry('450x300+0+0')
	GUI_connect_devices(root)
	root.mainloop()


def socket_bind(socket_object, HOST, PORT, numberofclients): # setting up the socket, limitied to a fixed number of cones 
	try:
		print("Binding socket to port: " + str(PORT))
		socket_object.bind((HOST, PORT))
		socket_object.listen(numberofclients) #setting up the socket, limitied to a fixed number of cones
	except socket.error as msg:
		print("Socket binding error: " + str(msg) +"\n" + "Retrying...")
		socket_bind(socket_object, HOST, PORT, numberofclients)

def socket_accept(numberofclients, connections, addresses): # accepting a fixed number of clients/cones
	for conn_list in connections.values():
		for each_connection in conn_list:
			each_connection.close()
		del conn_list[:]
	for addr_list in all_addresses.values():
		del addr_list[:]
	for x in range(numberofclients):
		try:
			conn, address = s.accept()
			conn.setblocking(1)
		except:
			print("Error accepting connections")
		if address[0] in turtlebot_ips:
			all_connections['turtlebots'].append(conn)
			all_addresses['turtlebots'].append(address)
			print("Connected to turtlebot: " +address[0])
		elif address[0] in displayunit_address:
			all_connections['displayunit'].append(conn)
			all_addresses['displayunit'].append(address)
			print("Connected to displayunit: " +address[0])
		elif address[0] in controller_ips:
			all_connections['controllers'].append(conn)
			all_addresses['controllers'].append(address)
			print('Connected to controller: ' + address[0])
		else:
			all_connections['cones'].append(conn)
			all_addresses['cones'].append(address)
			print("Connected to cone: " +address[0])
	print('\nEstablished connections')
	for name in all_connections.keys():
		print(name+': ' + str(len(all_connections[name])))
		

def event_packer(game_event, **kwargs):
	"""Expands the dictionary received from the cones with the passed key-value pairs"""
	for key, value in kwargs.items():
		game_event[key] = value
	return game_event

#Receive information from the cone connections. Event specific dictionaries.
def receive(connection, address):
	while True:
		while True:
			try:
				game_event_raw = connection.recv(1024)
				break
			except TimeoutError:
				print('Timed out')
		times_lock.acquire()
		game_instance.time_tracking['end']=time.time()
		times_lock.release()
		game_event = json.loads(game_event_raw.decode())
		print("Event received: " + str(game_event))
		game_instance.event_list.append(event_packer(game_event, address = address, time = (game_instance.time_tracking['end']-game_instance.time_tracking['start']), category = game_instance.category, game_type = game_instance.game_type, game_nr = game_instance.game_nr, date = time.asctime(), control_mode = 'N/A', player = 'N/A')) # Write to list containing information on all cones that were hit
		print("Current event list: " + str(game_instance.event_list) + " has length: " + str(len(game_instance.event_list)))
	
def recv_from_controller(connection):
	print("we got into recv_from_controller")
	time.sleep(10) #TODO: ask Jakob
	print("just slept 10 seconds")
	while True:
		while True:
			try:
				player_raw = connection.recv(1024)
				player = json.loads(player_raw.decode())
				break
			except:
				print('Was not informed of any player')

		#print("this is the player i loaded", player)

		if len(game_instance.players) < game_instance.nr_of_clients["controllers"]:
			game_instance.players.append(player)
			print("appended", player)

		elif player_is_registered(game_instance.players, player):
			print('player is already registered')


		else:
			for i, person in enumerate(game_instance.players):
				print("person ", i, person, "player", player,)
				if person['robot'] == player['robot']:
					game_instance.players.pop(i)
					print('removed player: ', game_instance.players[i])
					game_instance.players.append(player)
					print('added player: ', player)

def player_is_registered(player_list, player):
	for idx, person in enumerate(player_list):
		print("this is person", person)
		if player['name'] == person['name'] and player['robot'] == person['robot']:
			if player['control_mode'] != person['control_mode']:
				print('updating control mode')
				player_list[idx]['control_mode'] = player['control_mode']
			return True
	return False

def recv_from_turtlebot(connection, address):
	# Lets try to capture all data en event list
	# Lets make a list with the names of all hits
	#print(len(game_instance.players), "first")
	#print(game_instance.nr_of_clients['controllers'], "sammelign")
	while len(game_instance.players) < game_instance.nr_of_clients['controllers']:
		time.sleep(0.1)

	
	while True:
		for player in game_instance.players:
			if player['robot'] == address:
				player_name = player['name']
				control_mode = player['control_mode']
				break
		print("I know of the player ", address, player_name)
		hit = connection.recv(1024)
		game_instance.nr_of_turtle_events += 1 #Using a class attribute because both threads running the function should share the variable
		print(game_instance.nr_of_turtle_events, "Turtle Events ")
		print(len(game_instance.event_list), "Len Event List")
		if game_instance.nr_of_turtle_events == len(game_instance.event_list):
			game_instance.event_list[game_instance.nr_of_turtle_events-1]['player'] = player_name
			game_instance.event_list[game_instance.nr_of_turtle_events-1]['control_mode'] = control_mode

		elif game_instance.nr_of_turtle_events > len(game_instance.event_list): # In case of false positive from a turtlebot that did not hit a cone
			game_instance.nr_of_turtle_events = len(game_instance.event_list)

		elif game_instance.nr_of_turtle_events < len(game_instance.event_list): # In case of false negative
			game_instance.nr_of_turtle_events = len(game_instance.event_list)
			game_instance.event_list[game_instance.nr_of_turtle_events-1]['player'] = player_name
			game_instance.event_list[game_instance.nr_of_turtle_events-1]['control_mode'] = control_mode
			#for entry in range(game_instance.nr_of_turtle_events-1, len(game_instance.event_list)-1):
			#	game_instance.event_list[entry]['player'] = 'NaN'
			

			
def startTheGame():
	global receive_threads_created
	global controller_started
	print ("click!")
	if not receive_threads_created:
		for index, conn in enumerate(all_connections['cones']):
			try:
				_thread.start_new_thread(receive, (conn, all_addresses['cones'][index][0]))
			except:
				print ("Error: unable to start thread")
		receive_threads_created = True	# Only create threads once
	game_instance.game_is_running = True
	#del(game_instance.event_list[:]) #Ensure that correct hits from previous game doesn't carry over



def start_controller_thread():
	test_it = 1
	if all_connections['controllers']:
		print("starting controller threads")
		for conn in all_connections['controllers']:
			print("controller thread number ", test_it)
			try:
				_thread.start_new_thread(recv_from_controller, (conn,))
			except:
				print("Couldn't start thread for controller")

			print("started a controller thread")
			test_it +=1

def start_game():
		
		game_instance.results.to_sql('game_data', con=engine, if_exists='append')
		print("Game data saved in database")

		game_instance.nr_of_events = 0 # Reinitialize nr_of_events since even_list is cleared
		game_instance.nr_of_turtle_events = 0
		print("Cleared event list and turtleevents")

		game_instance.send_info(all_connections['turtlebots'], defaultContent=b'Nothing')


		print ("starting game...")
		game_instance.makeList(game_instance.coneInfo, game_instance.time_limit)
		game_instance.send_info(all_connections['cones'], defaultContent= b"questionmark")
		print("Send question marks is done")
		time.sleep(1)
		game_instance.findCorrectCones(game_instance.nr_true, game_instance.coneInfo)
		print("We found the correct cones")
		game_instance.findContent(game_instance.get_category(game_instance.category), game_instance.coneInfo)
		print("We found the content", game_instance.coneInfo)
		game_instance.send_info(all_connections['cones'], game_instance.coneInfo)
		print("Send cone info is done")
		game_instance.packDUInfo(game_instance.DUInfo, game_instance.coneInfo)
		game_instance.sendDisplayunitInfo(game_instance.DUInfo, all_connections['displayunit'])
		print("Send display unit info is done")
		game_instance.time_tracking['start'] = time.time()

try:
   _thread.start_new_thread( main, ())
except:
	print ("Error: unable to start main thread")

#if game_instance.nr_of_clients['turtlebots']:
while len(all_connections['turtlebots']) < game_instance.nr_of_clients['turtlebots']:
	time.sleep(0.1)

for conn, address in zip(all_connections['turtlebots'], all_addresses['turtlebots']):
	try:
		_thread.start_new_thread( recv_from_turtlebot, (conn, address[0]))
	except:
		print ("Error: unable to start turtlebot thread")

while len(all_connections['controllers']) < game_instance.nr_of_clients['controllers']:
	time.sleep(0.1)
print("Starting the controllers thread")

start_controller_thread()

#start_controller_thread()
print("we passed")

while True:
	
	if game_instance.game_is_running == True:
		start_game()
		print('looking for a game to play')
		print(game_instance.game_type, "game type")
		if game_instance.game_type == 'battle':
			game_instance.battle_game(all_connections['turtlebots'])

		elif game_instance.game_type == 'coop':
			game_instance.coop_game(all_connections['cones'], all_connections['displayunit'], all_connections['turtlebots'], game_instance.time_limit)

	#else:
	#	print("Game instance is false")

	time.sleep(1)



		
		
		