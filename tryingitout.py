import sys
import json

allow sound = False

    def determine_coop_outcome(self, time_limit, consecutive_corrects):
		""" Returns True if the coop game was won under the conditions of param "time_limit" and param "consecutive_corrects".
        Returns False in case the game was lost. """
		elapsed_time = 0
		correct_hit_at = 0
		while True: #Wait for a new event
        for hit in range(consecutive_corrects):
			while elapsed_time < time_limit: # wait for event
				if len(self.event_list) > self.nr_of_events: # A new event has happened
					self.nr_of_events = len(self.event_list) # Keep track of how many events have happened
					recent_event = self.event_list[-1] # last element of event_list - a dictionary with role, address and time keys 
					if recent_event['role'] == True:
						self.correct_hits.append(recent_event['time'])
						correct_hit_at = time.time()
                        indicate_game_state(len(self.correct_hits))
						break
					else:
						print("A wrong cone was hit")
						return False
				if correct_hit_at > 0: # We only want track time if a correct cone has been hit, otherwise keep elapsed time at 0
					elapsed_time = time.time()-correct_hit_at
            if elapsed_time < time_limit: # We simply broke the loop because a correct cone was hit and want to look for another hit
                break
            else: # We broke the loop because time_elapsed exceeded time_limit
			    print("Time ran out")
			    return False

    def indicate_game_state(self, condition):
        remainer = condition-consecutive_corrects
        if remainer == 0:
            return True # consecutive_correct cones have been hit in a sequence and the game is won
        else:
            start_counter()
    
    def start_counter(self, time_limit):


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

