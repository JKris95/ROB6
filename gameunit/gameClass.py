from random import randrange
import json

colors = ['red', 'green','blue','orange','purple','yellow']
animals = ['cow','dog','chicken','cat','zebra']
times = ['0100','0200','0300','0400','0500','0600','0700','0800','0900','1000','1100','1200']


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
		self.game_type = ''
		self.coneInfo=[]
		self.DUInfo=[]
		self.event_list = []
		self.makeList(self.nr_cones, self.coneInfo)
		

	def makeList(self, nrOfCones, coneInformation):
		for i in range(nrOfCones):
			coneInformation.append({"Role": 'False', "Content": 'questionmark'})
	
	def findCorrectCones(self, nrOfCones, nrOfTrue, coneInformation):
		pickedNumbers = []
		#Clean cone information
		for entry in coneInformation:
			entry['Role']='False'
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
	def packDUInfo(self, displayunitInfo, coneInformation=None, defaultContent=None):
		if not coneInformation:
			print("Content information is empty")
		del displayunitInfo[:]
		if coneInformation:
			for i in range(len(coneInformation)):
				if coneInformation[i]["Role"] == 'True':
					displayunitInfo.append(coneInformation[i]["Content"])
		if defaultContent:
			for i in range(self.nr_true):
				displayunitInfo.append(defaultContent)
		print(displayunitInfo)


	#send roles and content to each cone - Every cone receives a dictionary with role and content
	def sendConeInfo(self, all_connections, coneInformation=None, defaultContent=None):
		if coneInformation:
			for i in range(len(all_connections)):
				enConeInformation = json.dumps(coneInformation[i])
				enConeInformation = enConeInformation.encode()
				all_connections[i].sendall(enConeInformation)
		elif defaultContent:
			for conn in all_connections:
				conn.sendall(defaultContent)
			print(str(defaultContent) + " was sent to " + str(len(all_connections)) + " cones")
		else:
			print("No information to send to cones")

	def sendDisplayunitInfo(self,DUInfo,displayunitconnection): #send information on what corrects answer(s) are on the cones. 
		if not DUInfo:
			print("There is no information to display - list is empty")
		if type(DUInfo) == str:
			enDUInfo = DUInfo.encode()
		else:
			enDUInfo = json.dumps(DUInfo).encode()
		displayunitconnection[0].sendall(enDUInfo) #Send to the one and only display unit
