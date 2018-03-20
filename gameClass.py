from random import randrange
import json


colors = [b'red', b'green',b'blue',b'orange',b'purple',b'yellow']
animals = [b'cow',b'dog',b'chicken',b'cat',b'zebra']
times = [b'0100',b'0200',b'0300',b'0400',b'0500',b'0600',b'0700',b'0800',b'0900',b'1000',b'1100',b'1200']


class GameType():


	def __init__(self, nrOfCones=None, nrOfTrue=None, category=None):
		if category == None:
			self.category = ''
		else:	
			self.category = category
		if nrOfCones == None:
			self.nr_cones = 0
		else:
			self.nr_cones = nrOfCones
		if nrOfTrue == None:
			self.nr_true = 0
		else:
			self.nr_true = nrOfTrue #will be dependent on type of game and not changed by user.
		self.coneInfo=[]
		self.DUInfo=[]
		self.makeList(self.nr_cones, self.coneInfo)

	def makeList(self, nrOfCones,x):
		for i in range(nrOfCones):
			x.append({"Role": 'False', "Content": 'questionmark'})
	
	def findCorrectCones(self, nrOfCones, nrOfTrue, coneInformation):
		pickedNumbers = []
		for i in range(nrOfTrue):
			while True:
				x = randrange(0, nrOfCones)
				if x not in pickedNumbers:
					coneInformation[x]["Role"] = 'True'
					pickedNumbers.append(x)
					break

	def findContent(self, categoryName, nrOfCones,coneInformation): # lets the gamemaster chose what game category the questions should come from. 
		pickedNumbers = []

		for category, contents in [
			('animals', animals),
			('colors', colors),
			('clocks', times)
		]:
			if categoryName==category:
				for i in range(nrOfCones):
					while True:
						pick = randrange(0,len(contents)) 
						if pick not in pickedNumbers:
							pickedNumbers.append(pick)
							break
					coneInformation[i]["Content"] = contents[pickedNumbers[i]]

	# A function to pack all info content to be send to the display unit, i.e all correct coneinfo
	def packDUInfo(self, displayuitInfo, coneInformation=None, defaultContent=None):
		if not coneInformation:
			print("Content information is empty")
		if coneInformation:
			for i in range(len(coneInformation)):
				if coneInformation[i]["Role"] == 'True':
					displayuitInfo.append(coneInformation[i]["Content"])
		if defaultContent:
			for i in range(self.nr_true):
				displayuitInfo.append(defaultContent)



	#send roles and content to each cone - Every cone receives a dictionary with role and content
	def sendConeInfo(self,coneInformation, all_connections):
		if not coneInformation:
			print("Content information is empty")
		enConeInformation = json.dumps(coneInformation.encode())
		for i in range(len(all_connections)):
			all_connections[i].sendall(enConeInformation[i])

	def sendDisplayunitInfo(self,DUInfo,displayunitconnection): #send information on what corrects answer(s) are on the cones. 
		if not DUInfo:
			print("There is no information to display - list is empty")
		enDUInfo = json.dumps(DUInfo.encode())
		for i in range(len(displayunitconnection)):
			displayunitconnection[i].sendall(enDUInfo)

	
 
Battle = GameType() # Parameters: 'category', nrCones, nrTrue
#Battle.category = 'colors'
#print(Battle.category)
#Battle.nr_cones = 3
#Battle.nr_true = 2
#print(Battle.coneInfo)
#Battle.makeList(Battle.nr_cones,Battle.coneInfo)
print(Battle.coneInfo)
Battle.findCorrectCones(Battle.nr_cones, Battle.nr_true, Battle.coneInfo)
print(Battle.coneInfo)
Battle.findContent(Battle.category,Battle.nr_cones, Battle.coneInfo)
print(Battle.coneInfo)
Battle.packDUInfo(Battle.coneInfo, Battle.DUInfo)
print(Battle.DUInfo)