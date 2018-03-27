#imports needed
import socket
import RPi.GPIO as GPIO
import time
import tkinter as tk
import pygame
import _thread
import json
#
role = b'Start'
imageToDisplay = b'Start'  
buttonstate = False
imageIsUpdated = False

#Setup of GPIO pin for buttons used as bumpers
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pin 36 = GPIO16

#Setup of root window for the GUI and the different images 
root = tk.Tk()
#root.attributes('-fullscreen',True)

image6 = tk.PhotoImage(file="/home/pi/Desktop/wav/wrong.gif")
incorrectlabel = tk.Label(image=image6)

image5 = tk.PhotoImage(file="/home/pi/Desktop/wav/correct.gif")
correctlabel = tk.Label(image=image5)

image4 = tk.PhotoImage(file="/home/pi/Desktop/wav/questionmark.gif")
questionlabel = tk.Label(image=image4)

answerlabel = tk.Label(image=image4)

#Initialise pygame to be able to play sounds
pygame.init() 

#Setup of the different sounds to use in the project
correctsound = pygame.mixer.Sound('/home/pi/Desktop/wav/correct.wav')
incorrectsound = pygame.mixer.Sound('/home/pi/Desktop/wav/wrong.wav')

#Try to connect to the server untill successfull
HOST = '192.168.1.34'    # The remote host, 
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try: 
	s.connect((HOST, PORT))

except:
	print("FAILED. Sleep briefly & try again")
	time.sleep(10)

#Display the questionmark on the screen
questionlabel.pack()
root.update()

#Loop of the game 
def receiveThread():
	i=1
	while True:
		global imageToDisplay
		imageToDisplay = s.recv(1024) #receive information on what image to display. 
		imageToDisplay = imageToDisplay.decode()
		print(imageToDisplay)
		global imageIsUpdated
		imageIsUpdated = True
		
		coneInfoUnparsed = s.recv(1024)
		coneInfoParsed = json.loads(coneInfoUnparsed.decode())
		print(coneInfoParsed)
		global role 
		role = coneInfoParsed["Role"]
		print("role is", role)
		imageToDisplay = coneInfoParsed["Content"]
		print("image to display", imageToDisplay)
		imageIsUpdated = True
		print(i)
		i+1

def buttonThread():
	while True:
		global buttonstate
		buttonstate = GPIO.input(36) #When of of the buttons is actuated GPIO.input(36) will turn TRUE. 

try:
   _thread.start_new_thread( receiveThread, ())
   _thread.start_new_thread( buttonThread, ())
except:
   print ("Error: unable to start thread")


while True:
	if imageIsUpdated == True:
		path = '/home/pi/Desktop/wav/%s.gif' % imageToDisplay #set the path to this desired image
		questionlabel.pack_forget()
		answerlabel.pack_forget()
		#Display the image at the path
		image1 = tk.PhotoImage(file=path) 
		answerlabel = tk.Label(image=image1)
		answerlabel.pack()
		root.update()
		imageIsUpdated = False

	if buttonstate == True:
		if role == b'True':
			answerlabel.pack_forget()
			correctlabel.pack()
			root.update()
			correctsound.play()
			s.sendall(b'{"role": "True", "time": 5}')
			time.sleep(5) #Leave the correct label on the screen for 5 seconds before displaying the question mark again. 
			correctlabel.pack_forget()
			questionlabel.pack()
			root.update()

		if role == b'False':
			answerlabel.pack_forget()
			incorrectlabel.pack()
			root.update()
			incorrectsound.play()
			s.sendall(b'{"role": "False", "time": 5}')
			time.sleep(5) #Leave the incorrect label on the screen for 5 seconds before displaying the question mark again.
			incorrectlabel.pack_forget()
			questionlabel.pack()
			root.update()





