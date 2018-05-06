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
		
		self.time_limit = 5.0
		self.time_tracking = {'start': 0, 'end': 0}
		self.game_type = ''
		self.coneInfo=[]
		self.DUInfo=[]
		self.event_list = []
		self.nr_of_events = 0
		self.nr_of_correct_hits = 0
		self.makeList(self.nr_cones, self.coneInfo, self.time_limit)
		self.game_is_running = False
		self.allow_sound = False
		
		

	def makeList(self, nrOfCones, coneInformation, coop_time_limit):
		for i in range(nrOfCones):
			coneInformation.append({"Role": 'False', "Content": 'questionmark', 'time_limit': self.time_limit})
	
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
			for i in range(self.nr_true):
				displayunitInfo.append(defaultContent)
		print(displayunitInfo)

	def sendConeInfo(self, all_connections, coneInformation=None, defaultContent=None):
		"""send roles and content to each cone - Every cone receives a dictionary with role and content"""
		if coneInformation:
			for i in range(len(all_connections)):
				enConeInformation = json.dumps(coneInformation[i])
				enConeInformation = enConeInformation.encode()
				all_connections[i].sendall(enConeInformation)
			self.time_tracking['start'] = time.time()
		elif defaultContent:
			for conn in all_connections:
				conn.sendall(defaultContent)
			print(str(defaultContent) + " was sent to " + str(len(all_connections)) + " cones")
		else:
			print("No information to send to cones")

	def sendDisplayunitInfo(self,DUInfo,displayunitconnection): #send information on what corrects answer(s) are on the cones. 
		if not DUInfo:
			print("There is no information to display - list is empty")
		#if type(DUInfo) == str:
		#	enDUInfo = DUInfo.encode()
		else:
			enDUInfo = json.dumps(DUInfo).encode()
			print('send to displayunit', enDUInfo, type(enDUInfo))
		displayunitconnection[0].sendall(enDUInfo) #Send to the one and only display unit

###COOP SPECIFIC###

	def determine_coop_outcome(self, time_limit, consecutive_corrects):
		""" Returns True if the coop game was won under the conditions of param "time_limit" and param "consecutive_corrects".
		Returns False in case the game was lost. """
		elapsed_time = 0
		correct_hit_time = None
		nr_of_correct_hits = 0
		self.nr_of_events = 0
		del(self.event_list[:])
		print('Determining the outcome..')
		while elapsed_time < time_limit: # wait for event
			if len(self.event_list) > self.nr_of_events: # A new event has happened
				print("A new cone was hit")
				self.nr_of_events = len(self.event_list) # Keep track of how many events have happened
				recent_event = self.event_list[-1] # last element of event_list - a dictionary with role, address and time keys 
				if recent_event['role'] == True:
					nr_of_correct_hits += 1
					print("it was correct")
					if nr_of_correct_hits == 1: #The timer should start when the first correct cone is hit
						correct_hit_time = time.time()
						print("Time of first hit", correct_hit_time)
						self.allow_sound = True
						threading._start_new_thread(self.start_counter, (self.time_limit,)) #A new thread informs of the time available for the remaining correct hits
					elif nr_of_correct_hits == consecutive_corrects:
						self.allow_sound = False
						return (True, 0, elapsed_time) 
				else:
					print("A wrong cone was hit")
					self.allow_sound = False
					if nr_of_correct_hits == 0:
						return (False, 2, elapsed_time) # Fail condition 2: Wrong cone hit first
					elif nr_of_correct_hits == 1:
						return (False, 3, elapsed_time) # Fail condition 3: Wrong cone hit after correct cone
			if correct_hit_time: # We only want track time if a correct cone has been hit, otherwise keep elapsed time at 0
				elapsed_time = time.time()-correct_hit_time
				#print("elapsed time: ", elapsed_time)
 		# We broke the loop because time_elapsed exceeded time_limit
		print("Time ran out")
		self.allow_sound = False
		return (False, 1, elapsed_time) # Fail condition 1: Time expired
	
	
	def start_counter(self, time_limit):
		start_pos = 20 - time_limit
		while self.allow_sound:	
			path = 'gameunit/countdown.mp3'  #ændre path alt efter hvor scriptet kører fra, denne virker hvis det køres fra /gameunit.
			pygame.mixer.music.load(path)
			pygame.mixer.music.play(0,start_pos)
			time.sleep(time_limit)
		pygame.mixer.music.stop() #this is after the while loop, if the while loop breaks from change in bool value, 
			

	def coop_game(self, cone_connections, DU_connection, time_limit=5.0, consecutive_corrects=2):
		while True:
			print('playing coop')	
			outcome = self.determine_coop_outcome(time_limit, consecutive_corrects) #outcome = (game_outcome(bool), game_state(int), and elapsed_time(float))
			print(outcome)
			if outcome[0] == True:
				print("Congratulation, you won")
				self.game_is_running = False
				#self.packDUInfo(self.DUInfo, defaultContent='victory')
				#self.sendDisplayunitInfo(self.DUInfo, DU_connection)
				return
			else:
				print("You lost")
				self.reroll(cone_connections, outcome[1], outcome[2])

	def reroll(self, connections, fail_condition, elapsed_time):
		if fail_condition == 2:
			time.sleep(5) #Necessary because the cones utilize a 5 second sleep to show correct/wrong sign
			shuffle(self.coneInfo)
			self.sendConeInfo(connections, defaultContent=b'questionmark')
			time.sleep(1)
			self.sendConeInfo(connections, self.coneInfo)
		elif fail_condition == 1:
			time.sleep(5) #Necessary because the cones utilize a 5 second sleep to show correct/wrong sign
			shuffle(self.coneInfo)
			self.sendConeInfo(connections, defaultContent=b'questionmark')
			time.sleep(1)
			self.sendConeInfo(connections, self.coneInfo)
		elif fail_condition == 3:
			time.sleep(self.time_limit-elapsed_time + 5) #Necessary because the cones utilize a 5 second sleep to show correct/wrong sign
			shuffle(self.coneInfo)
			self.sendConeInfo(connections, defaultContent=b'questionmark')
			time.sleep(1)
			self.sendConeInfo(connections, self.coneInfo)


"""
	def correct_hit(self, time_limit):
		#Returns True if a new "correct cone hit" is found. Returns False in all other cases
		nonlocal elapsed_time
		nonlocal correct_hit_at
		while True: #Wait for a new event
			while elapsed_time < time_limit:
				if len(self.event_list) > self.nr_of_events: # A new event has happened
					self.nr_of_events = len(self.event_list)
					recent_event = self.event_list[-1] # last element of event_list - a dictionary with role, address and time keys 
					if recent_event['role'] == True:
						self.correct_hits.append(recent_event['time'])
						correct_hit_at = time.time()
						return True
					else:
						print("A wrong cone was hit")
						return False
				if correct_hit_at > 0: # We only want track time if a correct cone has been hit, otherwise keep elapsed time at 0
					elapsed_time = time.time()-correct_hit_at
			print("Time ran out")
			return False

	

	def coop_game(self, time_limit, consecutive_corrects):
		elapsed_time = 0 # May need to be changed to a mutable type and passed to correct_hit()
		correct_hit_at = 0 # May need to be changed to a mutable type and passed to correct_hit()
		for hit in range(consecutive_corrects): #Maybe include the for loop in correct hit to avoid potential scope issues
			if not self.correct_hit(time_limit):
				print("you lost")
				self.reroll()
				break
			else:
				pass #Do some displayunit work to indicate the state of the game
		self.game_is_running = False
	
	def remaining(self, condition):
		remainer = condition-consecutive_corrects
		if remainer == 0:
			return 0 # consecutive_correct cones have been hit in a sequence and the game is won
		else: #Only one correct cone has been hit, which indicates the start of the counter
			return 1
			
	


	def coop_won(self, time_limit=5.0):
		if len(self.correct_hits) % 2 == 0:
			last_two = self.event_list[-2:]
			return self.correct_hits[-1]-self.correct_hits[-2] < time_limit
		else:
			print("Only one correct cone has been hit")
"""