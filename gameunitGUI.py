import socket
from random import randrange
import time
from tkinter import *
import _thread
all_connections = []
all_addresses = []
displayunit_connection = []
displayunit_address = '192.168.1.43' 
HOST=''
PORT=50007

conesInGame = False

chosenGame = ['not chosen', False]
#The images availible in the different categories. 
colors = [b'red', b'green',b'blue',b'orange',b'purple',b'yellow']
animals = [b'cow',b'dog',b'chicken',b'cat',b'zebra']
times = [b'0100',b'0200',b'0300',b'0400',b'0500',b'0600',b'0700',b'0800',b'0900',b'1000',b'1100',b'1200']



sendList = [b'False', b'False', b'False']
index = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def socket_bind(HOST,PORT,numberofclients): #setting up the socket, limitied to a fixed number of cones
	try:
		print("Binding socket to port: " + str(PORT))
		s.bind((HOST, PORT))
		s.listen(numberofclients) #setting up the socket, limitied to a fixed number of cones
	except socket.error as msg:
		print("Socket binding error: " + str(msg) +"\n" + "Retrying...")
		socket_bind()

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

def chooseGame(correctCone, gametoplay): # lets the gamemaster chose what game catagory the questions should come from. 
	contentList = []
	pickedNumbers = []

	for catagory, contents in [
		('animals', animals),
		('colors', colors),
		('clocks', clocks)
	]:
		if gametoplay[0]==catagory:
			print(catagory)
			for i in range(numberofclients):
				while True:
					pick = randrange(0,len(contents)) 
					if pick not in pickedNumbers:
						pickedNumbers.append(pick)
						break
				contentList.append(contents[pickedNumbers[i]])

	contentOnCorrectCone = contentList[correctCone]
	#print(contentList)
	#print ("{} {}".format("\n Kør til keglen som viser:", contentOnCorrectCone))
	return {"coneContent":contentList, "DUcontent":contentOnCorrectCone}


def sendGameContent(contentList,cones,numberofclients): #sends the content to the cones

	for i in range(numberofclients):
		cones[i].sendall(contentList[i])
	print("{} {}".format("\n Information sent to this many connections:", numberofclients))

def randomCorrect(foo): #takes the array with the default false, and assigns a random correct cone and saves that chosen correct cone.
	y = randrange(0,len(foo))
	#print("{} {}".format("\n Random index chosen:", y))
	#print ("{} {}".format("\n What object is at this index:", foo[y]))
	return y

def sendTrueFalse(x,z,numberofclients): # sends True to the correct cone and false to the rest of the cones
	y = [b'False', b'False', b'False']
	print ("{} {}".format("\n Send list before adding the true cone", y))
	y[x] = b'True'
	print ("{} {}".format("\n Send list after adding the true cone", y))
	for i in range(numberofclients):
		z[i].sendall(y[i])
	print("{} {}".format("\n TRUE/FALSE Information sent to this many connections:", numberofclients))

def sendToDisplayunit(connectionDU, content):
	for i in range(len(connectionDU)):
		connectionDU[i].sendall(content)
		print("Content was send to display unit:", content)




def Animal_game(event):
	print("Animals")
	chosenGame[0] = 'animals'
	chosenGame[1] = True
	print (chosenGame)

def Color_game(event):
	print("Colors")
	chosenGame[0] = 'colors'
	chosenGame[1] = True
	print (chosenGame)	

def Clock_game(event):
	print("Clocks")	
	chosenGame[0] = 'clocks'
	chosenGame[1] = True
	print (chosenGame)

def guiThread():
	while True:
		root = Tk()
		T = Text(root, height=2, width=30)
		T.pack(side=RIGHT)
		T.insert(END, "Number of cones")
		
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

		text2 = Text(root, height=20, width=50)
		scroll = Scrollbar(root, command=text2.yview)
		text2.configure(yscrollcommand=scroll.set)
		text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
		text2.tag_configure('big', font=('Verdana', 20, 'bold'))
		text2.tag_configure('color', foreground='#476042', 
								font=('Tempus Sans ITC', 12, 'bold'))
		text2.tag_bind('follow', '<1>', lambda e, t=text2: t.insert(END, "Not now, maybe later!"))
		text2.insert(END,'\nRobot Game\n', 'big')
		quote = """
		This is the user interface to the platform.
		Needs some design update.
		"""
		text2.insert(END, quote, 'color')
		text2.pack(side=LEFT)
		scroll.pack(side=RIGHT, fill=Y)


		button_1 = Button(root, text="Animals")
		button_1.bind("<Button-1>",Animal_game)
		button_1.pack()
		button_2 = Button(root, text="Colors")
		button_2.bind("<Button-1>",Color_game)
		button_2.pack()
		button_3 = Button(root, text="Clocks")
		button_3.bind("<Button-1>", Clock_game)
		button_3.pack()
		slider = Scale(root, from_=1, to=3, orient=HORIZONTAL)
		slider.bind("<ButtonRelease-1>",sliderValue)
		slider.pack()
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




hum = 1
while True:
	print (hum)
	time.sleep(7)
	sendToDisplayunit(displayunit_connection, b"questionmark")
	time.sleep(3)
	sendToDisplayunit(all_connections, b"questionmark")
	index = randomCorrect(all_connections) # takes the return of randomCorrect and stores it in index. 
	sendTrueFalse(index, all_connections,numberofclients)
	hum+=1
	while True:
		if chosenGame[1] == True:
			content = chooseGame(index, chosenGame)
			sendGameContent(content["coneContent"],all_connections,numberofclients)
			sendToDisplayunit(displayunit_connection, content["DUcontent"])
			print(all_connections[index].recv(1024))
			chosenGame[1] = False
			hum += 1000
			time.sleep(5)
			break