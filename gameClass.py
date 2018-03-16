from random import randrange



colors = [b'red', b'green',b'blue',b'orange',b'purple',b'yellow']
animals = [b'cow',b'dog',b'chicken',b'cat',b'zebra']
times = [b'0100',b'0200',b'0300',b'0400',b'0500',b'0600',b'0700',b'0800',b'0900',b'1000',b'1100',b'1200']


class GameType():


	def __init__(self):
		self.category = ''
		self.nr_cones = 0
		self.nr_true = 0 #will be dependent on type of game and not changed bu user.
		self.coneInfo=[]
		self.DUInfo=[]

	def makeList(self, nrOfCones,x):
		for i in range(nrOfCones):
			x.append({"Role": "False", "Content": "questionmark"})
	
	def findCorrectCones(self, nrOfCones, nrOfTrue, coneInformation):
		pickedNumbers = []
		for i in range(nrOfTrue):
			while True:
				x = randrange(0, nrOfCones)
				if x not in pickedNumbers:
					coneInformation[x]["Role"] = "True"
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


	def sendConeInfo(self,coneInformation, all_connections): #send roles and content to the connected cones found in all_connections. Can be send as one 'packet' if possible.
		pass

	def sendDisplayunitInfo(self,DUInfo,displayunitconnection): #send information on what corrects answer(s) are on the cones. 
		pass

	
 
Battle = GameType()
Battle.category = 'colors'
#print(Battle.category)
Battle.nr_cones = 3
Battle.nr_true = 1
#print(Battle.coneInfo)
Battle.makeList(Battle.nr_cones,Battle.coneInfo)
print(Battle.coneInfo)
Battle.findCorrectCones(Battle.nr_cones, Battle.nr_true, Battle.coneInfo)
print(Battle.coneInfo)
Battle.findContent(Battle.category,Battle.nr_cones, Battle.coneInfo)
print(Battle.coneInfo)