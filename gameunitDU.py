import socket
from random import randrange
import time
all_connections = []
all_addresses = []
displayunit_connection = []
displayunit_address = '192.168.1.43' 
HOST=''
PORT=50007


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
			print(type(address))
			print(address)
			if address[0] == displayunit_address:
				print("DIsplay unit appednd")
				displayunit_connection.append(conn)
			else:
				print("cone appended") 
				all_connections.append(conn)
				all_addresses.append(address)
			print("\n Connection has been established:" +address[0])
			print(len(all_connections))
		except:
			print("Error accepting connections")

def chooseGame(correctCone): # lets the gamemaster chose what game catagory the questions should come from. 
	contentList = []
	pickedNumbers = []

	choice = input('Hvilket spil skal spilles?')
	if choice=='Dyre spil':
		print('Dyre spil valgt')
		for i in range(numberofclients):
			while True:
				pick = randrange(0,len(animals)) 
				if pick not in pickedNumbers:
					pickedNumbers.append(pick)
					break
			contentList.append(animals[pickedNumbers[i]])


	if choice=='Farve spil':
		print('Farve spil valgt')
		for i in range(numberofclients):
			while True:
				pick = randrange(0,len(colors)) 
				if pick not in pickedNumbers:
					pickedNumbers.append(pick)
					break
			contentList.append(colors[pickedNumbers[i]])


	if choice=='Ur spil':
		print('Ur spil valgt')
		for i in range(numberofclients):
			while True:
				pick = randrange(0,len(times)) 
				if pick not in pickedNumbers:
					pickedNumbers.append(pick)
					break
			contentList.append(times[pickedNumbers[i]])

	contentOnCorrectCone = contentList[correctCone]
	print(contentList)
	print ("{} {}".format("\n Kør til keglen som viser:", contentOnCorrectCone))
	return {"coneContent":contentList, "DUcontent":contentOnCorrectCone}


def sendGameContent(contentList,cones,numberofclients): #sends the content to the cones

	for i in range(numberofclients):
		cones[i].sendall(contentList[i])
	print("{} {}".format("\n Information sent to this many connections:", numberofclients))

def randomCorrect(foo): #takes the array with the default false, and assigns a random correct cone and saves that chosen correct cone.
	y = randrange(0,len(foo))
	print("{} {}".format("\n Random index chosen:", y))
	print ("{} {}".format("\n What object is at this index:", foo[y]))
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

numberofclients = int(input("Hvor mange kegler er med i spillet? "))
print(numberofclients)
socket_bind(HOST,PORT,numberofclients+1)
socket_accept(numberofclients,displayunit_address)
time.sleep(10)
while True:
	sendToDisplayunit(displayunit_connection, b"questionmark")
	sendToDisplayunit(all_connections, b"questionmark")
	index = randomCorrect(all_connections) # takes the return of randomCorrect and stores it in index. 
	sendTrueFalse(index, all_connections,numberofclients)
	content = chooseGame(index)
	sendGameContent(content["coneContent"],all_connections,numberofclients)
	sendToDisplayunit(displayunit_connection, content["DUcontent"])
	print(all_connections[index].recv(1024))
	time.sleep(5)