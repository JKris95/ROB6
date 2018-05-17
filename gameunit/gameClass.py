from random import randrange, shuffle
import json
import time
import threading
import pygame

pygame.mixer.init()

colors = ['red', 'green','blue','orange','purple','yellow']
animals = ['cow','dog','chicken','cat','zebra']
times = ['0100','0200','0300','0400','0500','0600','0700','0800','0900','1000','1100','1200']


class GameType():
	def __init__(self, nrOfCones=None, nrOfTrue=None, category=None):
		self.nr_of_clients = {'cones': 3, 'displayunit': 1, 'turtlebots': 1, 'controllers': 1}
		if category == None:
			self.category = ''
		else:	
			self.category = category
		if nrOfCones == None:
			self.nr_cones = 0
		else:
			self.nr_of_clients['cones'] = nrOfCones
		if nrOfTrue == None:
			self.nr_true = 1
		else:
			self.nr_true = nrOfTrue #will be dependent on type of game and not changed by user.
		
		self.time_limit = 8.0
		self.time_tracking = {'start': 0, 'end': 0}
		self.game_type = ''
		self.coneInfo=[]
		self.DUInfo=[]
		self.event_list = []
		self.hit_by_player = []
		self.nr_of_events = 0
		self.nr_of_turtle_events = 0
		self.nr_of_correct_hits = 0 #Not used
		self.makeList(self.coneInfo, self.time_limit)
		self.game_is_running = False
		self.allow_sound = False
		self.loop_game = False
		self.category_names = ['colors', 'animals', 'times']
		self.players = []
		
		

	def makeList(self, coneInformation, coop_time_limit):
		if len(self.coneInfo) < 3: # Added to avoid that coneinfo increases in length every time a game starts
			for i in range(self.nr_of_clients['cones']):
				coneInformation.append({"Role": 'False', "Content": 'questionmark', 'time_limit': self.time_limit})
	
	def findCorrectCones(self, nrOfTrue, coneInformation):
		pickedNumbers = []
		#Clean cone information
		for entry in coneInformation:
			entry['Role']='False'
		for i in range(nrOfTrue):
			while True:
				x = randrange(0, self.nr_of_clients['cones'])
				if x not in pickedNumbers:
					coneInformation[x]["Role"] = 'True'
					pickedNumbers.append(x)
					break

	def get_category(self, category_name):
		if category_name in self.category_names:
			return category_name
		elif category_name == 'random':
			return self.category_names[randrange(0,len(self.category_names))]


	def findContent(self, categoryName, coneInformation): # lets the gamemaster chose what game category the questions should come from. 
		pickedNumbers = []

		for category, contents in [
			('animals', animals),
			('colors', colors),
			('times', times)
		]:
			if categoryName==category:
				for i in range(self.nr_of_clients['cones']):
					while True:
						pick = randrange(0,len(contents)) 
						if pick not in pickedNumbers:
							pickedNumbers.append(pick)
							break
					coneInformation[i]["Content"] = contents[pickedNumbers[i]]

	def packDUInfo(self, displayunitInfo, coneInformation=None, defaultContent=None):
		"""A function to pack all info content to be send to the display unit, i.e all correct coneinfo"""
		if not coneInformation:
			print("Content information is empty")
		del displayunitInfo[:]
		if coneInformation:
			for i in range(len(coneInformation)):
				if coneInformation[i]["Role"] == 'True':
					displayunitInfo.append(coneInformation[i]["Content"])
		if defaultContent:
			displayunitInfo.append(defaultContent)
		print(displayunitInfo)

	def send_info(self, connections, coneInformation=None, defaultContent=None):
		"""send roles and content to each cone - Every cone receives a dictionary with role and content"""
		if connections:
			if coneInformation:
				for i in range(len(connections)):
					enConeInformation = json.dumps(coneInformation[i])
					enConeInformation = enConeInformation.encode()
					connections[i].sendall(enConeInformation)
					print(str(enConeInformation) + 'was sent')
				self.time_tracking['start'] = time.time()
			elif defaultContent:
				for conn in connections:
					conn.sendall(defaultContent)
				print(str(defaultContent) + " was sent to " + str(len(connections)) + " connections")
			else:
				print("No information to send to cones")
		else:
			print('No connections to send to')

	def sendDisplayunitInfo(self,DUInfo,displayunit_connection): #send information on what corrects answer(s) are on the cones. 
		if not DUInfo:
			print("There is no information to display - list is empty")
		#if type(DUInfo) == str:
		#	enDUInfo = DUInfo.encode()
		else:
			enDUInfo = json.dumps(DUInfo).encode()
			print('send to displayunit', enDUInfo, type(enDUInfo))
		displayunit_connection[0].sendall(enDUInfo) #Send to the one and only display unit

	def battle_game(self, turtle_conns):
		self.nr_of_events = len(self.event_list)
		while True:
			if len(self.event_list) > self.nr_of_events:
				
				self.nr_of_events +=1
				recent_event = self.event_list[self.nr_of_events-1]
				if recent_event['role'] == True:
					winner = recent_event['player']
					print(winner + "won")
					if not self.loop_game:
						self.game_is_running = False
					self.send_info(turtle_conns, defaultContent=b'go back') #Send signal to turtlebots telling them to go back to start 
					return
				self.send_info(turtle_conns, defaultContent=b'hit')
###COOP SPECIFIC###

	def determine_coop_outcome(self, turtle_conns, time_limit, consecutive_corrects):
		""" Returns True if the coop game was won under the conditions of param "time_limit" and param "consecutive_corrects".
		Returns False in case the game was lost. """
		elapsed_time = 0
		correct_hit_time = None
		nr_of_correct_hits = 0
		self.nr_of_events = len(self.event_list)
		cones_hit = []
		print('Determining the outcome..')
		while elapsed_time < time_limit: # wait for event
			if len(self.event_list) > self.nr_of_events: # A new event has happened
				print("A new cone was hit")
				self.nr_of_events += 1 # Keep track of how many events have happened
				recent_event = self.event_list[self.nr_of_events-1] # last element of event_list - a dictionary with role, address and time keys 
				if recent_event['role'] == True and recent_event['address'] not in cones_hit:
					nr_of_correct_hits += 1
					cones_hit.append(recent_event['address'])
					print("it was correct")
					if nr_of_correct_hits == 1: #The timer should start when the first correct cone is hit
						correct_hit_time = time.time()
						print("Time of first hit", correct_hit_time)
						threading._start_new_thread(self.start_counter, (self.time_limit,)) #A new thread informs of the time available for the remaining correct hits
						self.send_info(turtle_conns, defaultContent=b'hit')
					elif nr_of_correct_hits == consecutive_corrects:
						#pygame.mixer.music.stop()
						return (True, 0, elapsed_time)
				elif recent_event['role'] == False:
					print("A wrong cone was hit")
					self.allow_sound = False
					if nr_of_correct_hits == 0:
						self.send_info(turtle_conns, defaultContent=b'hit')
						return (False, 2, elapsed_time) # Fail condition 2: Wrong cone hit first
					elif nr_of_correct_hits == 1:
						self.send_info(turtle_conns, defaultContent=b'hit')
						pygame.mixer.music.stop()
						return (False, 3, elapsed_time) # Fail condition 3: Wrong cone hit after correct cone
			if correct_hit_time: # We only want to track time if a correct cone has been hit, otherwise keep elapsed time at 0
				elapsed_time = time.time()-correct_hit_time
				#print("elapsed time: ", elapsed_time)
 		# We broke the loop because time_elapsed exceeded time_limit
		print("Time ran out")
		return (False, 1, elapsed_time) # Fail condition 1: Time expired
	
	
	def start_counter(self, time_limit):
		start_pos = 20 - time_limit
		path = 'gameunit/countdown.mp3'  #ændre path alt efter hvor scriptet kører fra, denne virker hvis det køres fra /gameunit.
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(0,start_pos)
		time.sleep(time_limit)
		 #this is after the while loop, if the while loop breaks from change in bool value, 
			

	def coop_game(self, cone_connections, DU_connection, turtle_conns, time_limit=5.0, consecutive_corrects=2):
		while True:
			print('playing coop')	
			outcome = self.determine_coop_outcome(turtle_conns, time_limit, consecutive_corrects) #outcome = (game_outcome(bool), game_state(int), and elapsed_time(float))
			print(outcome)
			if outcome[0] == True:
				print("Congratulation, you won")
				if not self.loop_game:
					self.game_is_running = False
				self.packDUInfo(self.DUInfo, defaultContent='victory')
				self.sendDisplayunitInfo(self.DUInfo, DU_connection)
				self.send_info(turtle_conns, defaultContent=b'go back')
				pygame.mixer.music.stop()
				return
			else:
				print("You lost")
				self.reroll(cone_connections, outcome[1], outcome[2])

	def reroll(self, connections, fail_condition, elapsed_time):
		if fail_condition == 2:
			print('Game lost because the first cone hit was wrong')
			print('elapsed time: ', elapsed_time)
			print('Sleeping for ', 6)
			time.sleep(6) #Necessary because the cones utilize a 5 second sleep to show correct/wrong sign
			print('coneinfo before shuffle', self.coneInfo)
			shuffle(self.coneInfo)
			self.send_info(connections, defaultContent=b'questionmark')
			time.sleep(3)
			print('coneinfo to be send after shuffling', self.coneInfo)
			self.send_info(connections, self.coneInfo)
		elif fail_condition == 1:
			print('Game lost because time expired')
			print('elapsed time: ', elapsed_time)
			print('Sleeping for ', 2)
			time.sleep(2) #Necessary because the cones utilize a 5 second sleep to show correct/wrong sign
			print('coneinfo before shuffle', self.coneInfo)
			shuffle(self.coneInfo)
			self.send_info(connections, defaultContent=b'questionmark')
			time.sleep(3)
			print('coneinfo to be send after shuffling', self.coneInfo)
			self.send_info(connections, self.coneInfo)
		elif fail_condition == 3:
			print('Game lost because wrong cone was hit after correct')
			print('elapsed time: ', elapsed_time)
			print('Sleeping for ', (self.time_limit-elapsed_time) + 5)
			time.sleep((self.time_limit-elapsed_time) + 5) #Necessary because the cones utilize a 5 second sleep to show correct/wrong sign
			print('coneinfo before shuffle', self.coneInfo)
			shuffle(self.coneInfo)
			self.send_info(connections, defaultContent=b'questionmark')
			time.sleep(3)
			print('coneinfo to be send after shuffling', self.coneInfo)
			self.send_info(connections, self.coneInfo)

