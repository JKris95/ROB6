import pygame
import time


#Enabling pygame to play sounds
pygame.mixer.init()


def start_countdowm_music(length_countdown):
    start_pos = 20 - length_countdown
    
     #TODO: add while loop with the boolean variable here that tells when the countdown stops. 
    #while play_okay == True:
    path = 'countdown.mp3'  #ændre path alt efter hvor scriptet kører fra, denne virker hvis det køres fra /gameunit.
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(0,start_pos)
    time.sleep(length_countdown)


    pygame.mixer.music.stop() #this is after the while loop, if the while loop breaks from change in bool value, 

start_countdowm_music(3)