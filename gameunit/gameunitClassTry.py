import socket
from random import randrange
import time
from tkinter import *
import _thread
from gameClass import GameType
all_connections = []
all_addresses = []
displayunit_connection = []
displayunit_address = '192.168.1.44' 
HOST=''
PORT=50007

game_is_running = False
conesInGame = False

chosenGame = ['not chosen', False]
game_instance = GameType()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def socket_bind(HOST,PORT,numberofclients): # SHOULD NUMBEROFCLIENTS COME FROM OBJECT // setting up the socket, limitied to a fixed number of cones 
	try:
		print("Binding socket to port: " + str(PORT))
		s.bind((HOST, PORT))
		s.listen(numberofclients) #setting up the socket, limitied to a fixed number of cones
	except socket.error as msg:
		print("Socket binding error: " + str(msg) +"\n" + "Retrying...")
		socket_bind(HOST, PORT, numberofclients+1)

def socket_accept(numberofclients,displayunit_address): # accepting a fixed number of clients/cones
	for c in all_connections:
		c.close()
	del all_connections[:]
	del all_addresses[:]
	for x in range(numberofclients+1):
		try:
			conn, address = s.accept()
			conn.setblocking(1)
			#print(type(address))
			#print(address)
			if address[0] == displayunit_address:
				print("Display unit appended")
				displayunit_connection.append(conn)
			else:
				print("Cone appended") 
				all_connections.append(conn)
				all_addresses.append(address)
			print("\n Connection has been established:" +address[0])
			print(len(all_connections))
		except:
			print("Error accepting connections")

def event_packer(game_event, adresss):
	#needs to pack the dictionary. 

	pass

#Receive information from the cone connections. Event specific dictionaries.
def receive(connection):
	game_event_raw = connection.recv(1024)
	game_event = json.loads(game_event_raw.decode())
	game_instance.event_list.append(event_packer(game_event,connection.address)) #does connections have an address

#SENDDISPLAYUNITINFO()
def sendToDisplayunit(connectionDU, content):
	for i in range(len(connectionDU)):
		connectionDU[i].sendall(content)
		print("Content was send to display unit:", content)

def Battle_game(event):
	print ("You have chosen the battle game")
	game_instance = GameType(numberofclients,1)

def Coop_game(event):
	print ("You have chosen the coop game")
	game_instance = GameType(numberofclients,2)	

def Animal_game(event):
	chosenGame[0] = 'animals'
	print (chosenGame)

def Color_game(event):
	chosenGame[0] = 'colors'
	print (chosenGame)	

def Clock_game(event):
	chosenGame[0] = 'clocks'
	print (chosenGame)

def startTheGame():
	global game_is_running
	print ("click!")
	for x in all_connections:
		try:
			_thread.start_new_thread( receive, (x.address))
		except:
			print ("Error: unable to start thread")
	game_instance.category = chosenGame[0] 
	game_is_running = True			

def guiThread():
	while True:
		root = Tk()

		def sliderValue(event):
			global numberofclients
			print(slider.get())
			numberofclients = slider.get()

		def startConnection(event):
			global conesInGame
			conesInGame = True



		text1 = Text(root, height=15, width=40)
		photo=PhotoImage(file='./pylogo.gif')
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

def battle_game_over(Battle_events):
	#if battle events contains a true set game is running = false
	global game_is_running
	for x in Battle_events:
		if x["role"] == True:
			game_is_running = False
			print("Found a try hit in event list")
			break

def start_game():
		print ("starting game...")
		game_instance.packDUInfo(game_instance.DUInfo, defaultContent = "questionmark")
		game_instance.sendDisplayunitInfo(game_instance.DUInfo, displayunit_connection)
		print("Send question marks is done")
		game_instance.findCorrectCones(game_instance.nr_cones, game_instance.nr_true, game_instance.coneInfo)
		print("We found the correct cones")
		game_instance.findContent(game_instance.category, game_instance.nr_cones, game_instance.coneInfo) # takes the return of randomCorrect and stores it in index. 
		print("We found the content", game_instance.coneInfo)
		game_instance.sendConeInfo(game_instance.coneInfo, all_connections)
		print("Send cone info is done")
		game_instance.packDUInfo(game_instance.DUInfo, game_instance.coneInfo)
		game_instance.sendDisplayunitInfo(game_instance.DUInfo, displayunit_connection)
		print("Send display unit info is done")

try:
   _thread.start_new_thread( guiThread, ())
except:
   print ("Error: unable to start thread")

#tilføj knap og lad dem slide
while True:
	if conesInGame == True:
		print("moving on")
		break

socket_bind(HOST,PORT,numberofclients+1)
socket_accept(numberofclients,displayunit_address)

while True:
	if game_is_runnning == True:
		start_game()
		
		