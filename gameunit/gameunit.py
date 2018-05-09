import socket
from random import randrange
import time
from tkinter import *
import _thread
from gameClass import GameType
import json

#Global variables
all_connections = {'cones': [], 'displayunit': [], 'turtlebots': []}
all_addresses = {'cones': [], 'displayunit': [], 'turtlebots': []}
nr_of_clients = {'cones': 3, 'displayunit': 1, 'turtlebots': 1}
turtlebot_ips = ['192.168.1.38', '192.168.1.39', '192.168.1.36']
displayunit_address = ['192.168.1.44']
HOST=''
PORT=50007
conesInGame = False
receive_threads_created = False
times_lock = _thread.allocate_lock()
game_instance = GameType()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
			print("Connected to turtlebot:" +address[0])
		elif address[0] in displayunit_address:
			all_connections['displayunit'].append(conn)
			all_addresses['displayunit'].append(address)
			print("Connected to displayunit:" +address[0])
		else:
			all_connections['cones'].append(conn)
			all_addresses['cones'].append(address)
			print("Connected to cone:" +address[0])
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
		game_instance.event_list.append(event_packer(game_event, address = address, time = game_instance.time_tracking['end']-game_instance.time_tracking['start'])) # Write to list containing information on all cones that were hit
		print("Current event list: " + str(game_instance.event_list) + " has length: " + str(len(game_instance.event_list)))
	
def Battle_game(event):
	print ("You have chosen the battle game")
	game_instance.nr_true = 1
	game_instance.nr_cones = nr_of_clients['cones']
	game_instance.game_type = 'battle'

def Coop_game(event):
	print ("You have chosen the coop game")
	game_instance.nr_true = 2
	game_instance.nr_cones = nr_of_clients['cones']
	game_instance.game_type = 'coop'

def Animal_game(event):
	game_instance.category = 'animals'
	print (game_instance.category)

def Color_game(event):
	game_instance.category = 'colors'
	print (game_instance.category)

def Clock_game(event):
	game_instance.category = 'clocks'
	print (game_instance.category)

def startTheGame():
	global receive_threads_created
	print ("click!")
	if not receive_threads_created:
		for index, conn in enumerate(all_connections['cones']):
			try:
				_thread.start_new_thread(receive, (conn, all_addresses['cones'][index][0]))
			except:
				print ("Error: unable to start thread")
		receive_threads_created = True	# Only create threads once
	game_instance.game_is_running = True
	del(game_instance.event_list[:]) #Ensure that correct hits from previous game doesn't carry over
	game_instance.nr_of_events = 0 # Reinitialize nr_of_events since even_list is cleared
	start_game()

def startConnection():
	global conesInGame
	conesInGame = True

def guiThread():
	while True:
		root = Tk()

		def sliderValue(event):
			print(slider.get())
			nr_of_clients['cones'] = slider.get()

		text1 = Text(root, height=15, width=40)
		photo=PhotoImage(file='gameunit/pylogo.gif')
		text1.insert(END,'\n')
		text1.image_create(END, image=photo)

		text1.pack(side=LEFT)


		GAMETYPES = [
		("Battle", Battle_game),
		("Coop", Coop_game),
		]

		for text, callback in GAMETYPES:
			b = Radiobutton(root, text=text)
			b.bind("<Button-1>", callback)
			b.pack(anchor=W)


		MODES = [
		("Animals", Animal_game),
		("Colors", Color_game),
		("Clocks", Clock_game),
		("New category", Animal_game),
		]

		for text, callback in MODES:
			b = Radiobutton(root, text=text)
			b.bind("<Button-1>", callback)
			b.pack(anchor=W)

		slider = Scale(root, from_=1, to=3, orient=HORIZONTAL, label="Number of cones",)
		slider.bind("<ButtonRelease-1>",sliderValue)
		slider.pack()

		start_button = Button(root, text="Start", command=startTheGame)
		start_button.pack()

		connect_button = Button(root, text="Connect", command=startConnection)
		connect_button.pack()

		root.mainloop()
			
def start_game():
		print ("starting game...")
		game_instance.makeList(game_instance.nr_cones, game_instance.coneInfo, game_instance.time_limit)
		game_instance.send_info(all_connections['cones'], defaultContent= b"questionmark")
		print("Send question marks is done")
		time.sleep(1)
		game_instance.findCorrectCones(game_instance.nr_cones, game_instance.nr_true, game_instance.coneInfo)
		print("We found the correct cones")
		game_instance.findContent(game_instance.category, game_instance.nr_cones, game_instance.coneInfo)
		print("We found the content", game_instance.coneInfo)
		game_instance.send_info(all_connections['cones'], game_instance.coneInfo)
		print("Send cone info is done")
		game_instance.packDUInfo(game_instance.DUInfo, game_instance.coneInfo)
		game_instance.sendDisplayunitInfo(game_instance.DUInfo, all_connections['displayunit'])
		print("Send display unit info is done")
		time.sleep(7)

try:
   _thread.start_new_thread( guiThread, ())
except:
   print ("Error: unable to start thread")

#tilføj knap og lad dem slide
while True:
	if conesInGame == True:
		print("moving on")
		break

#Establish connection to all units
socket_bind(s, HOST, PORT, sum(nr_of_clients.values()))
socket_accept(sum(nr_of_clients.values()), all_connections, all_addresses)

while True:
	if game_instance.game_is_running == True:
		print('looking for a game to play')
		if game_instance.game_type == 'battle':
			game_instance.battle_game(all_connections['turtlebots'])
		elif game_instance.game_type == 'coop':
			game_instance.coop_game(all_connections['cones'], all_connections['displayunit'], all_connections['turtlebots'], game_instance.time_limit)
	time.sleep(0.2)


		
		
		