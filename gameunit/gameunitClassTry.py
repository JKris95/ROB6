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

conesInGame = False

chosenGame = ['not chosen', False]

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



#SENDDISPLAYUNITINFO()
def sendToDisplayunit(connectionDU, content):
	for i in range(len(connectionDU)):
		connectionDU[i].sendall(content)
		print("Content was send to display unit:", content)


def Battle_game(event):
	print ("You have chosen the battle game")

def Coop_game(event):
	print ("You have chosen the coop game")	

def Animal_game(event):
	chosenGame[0] = 'animals'
	chosenGame[1] = True
	print (chosenGame)

def Color_game(event):
	chosenGame[0] = 'colors'
	chosenGame[1] = True
	print (chosenGame)	

def Clock_game(event):
	chosenGame[0] = 'clocks'
	chosenGame[1] = True
	print (chosenGame)

def startTheGame():
	print ("click!")	

def guiThread():
	while True:
		root = Tk()

		def sliderValue(event):
			global numberofclients
			print(slider.get())
			numberofclients = slider.get()
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

		b = Button(root, text="Start", command=startTheGame)
		b.pack()

		root.mainloop()



try:
   _thread.start_new_thread( guiThread, ())
except:
   print ("Error: unable to start thread")

while True:
	if conesInGame == True:
		print("moving on")
		break

socket_bind(HOST,PORT,numberofclients+1)
socket_accept(numberofclients,displayunit_address)

while True:
	if chosenGame[1] == True:
		battleGame = GameType(1,1,chosenGame[0])
		break

hum = 1
while True:
	print ("We are in whiel treu",hum)
	time.sleep(7)
	sendToDisplayunit(displayunit_connection, b"questionmark")
	time.sleep(3)
	sendToDisplayunit(all_connections, b"questionmark")
	print("Send question marks is done")
	time.sleep(3)
	battleGame.findCorrectCones(battleGame.nr_cones, battleGame.nr_true, battleGame.coneInfo)
	print("We found the correct cones")
	time.sleep(3)
	battleGame.findContent(battleGame.category, battleGame.nr_cones, battleGame.coneInfo) # takes the return of randomCorrect and stores it in index. 
	print("We found the content", battleGame.coneInfo)
	time.sleep(3)
	battleGame.sendConeInfo(battleGame.coneInfo, all_connections)
	print("Send cone info is done")
	time.sleep(3)
	battleGame.packDUInfo(battleGame.DUInfo, battleGame.coneInfo)
	battleGame.sendDisplayunitInfo(battleGame.DUInfo, displayunit_connection)
	print("Send display unit info is done")
	time.sleep(3)
	