#imports needed
import socket
import time
import tkinter as tk 
import json

#
imageToDisplay = b'Start'


#Setup of root window for the GUI and the different images 
root = tk.Tk()
root.attributes('-fullscreen',True)

image4 = tk.PhotoImage(file="./gifs/questionmark.gif")

#Declare and initialize all labels
questionlabel = tk.Label(image=image4)
answerlabel = tk.Label(image=image4)
answerlabel1 = tk.Label(image=image4)
answerlabel2 = tk.Label(image=image4)



HOST = '192.168.1.34'    # The remote host, remember to change when switching game unit
PORT = 50007              # The same port as used by the server(gameunit) - specifies application
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(socket_object, host, port):
	while True:
		try: 
			socket_object.connect((host, port))
			break
		except:
			print("FAILED. Sleep briefly & try again")
			time.sleep(5)

connect(s, HOST, PORT)

#Display the questionmark on the screen
questionlabel.pack()
root.update()

left = tk.Frame(root, borderwidth=2, relief="solid")
right = tk.Frame(root, borderwidth=2, relief="solid")


while True:
		DUInfoUnparsed = s.recv(1024) # Receive questions / correct answers
		print(DUInfoUnparsed)
		DUInfoParsed = json.loads(DUInfoUnparsed.decode()) #Recover a list from the bytes that were sent
		print(DUInfoParsed)


		# This condition is true when battle game is played (1 correct answer)
		if len(DUInfoParsed) == 1: 
			path = './gifs/%s.gif' % DUInfoParsed[0] #set the path to this desired image
			questionlabel.pack_forget()
			answerlabel.pack_forget()
			answerlabel1.pack_forget()
			answerlabel2.pack_forget()
			left.pack_forget()
			right.pack_forget()
			#Display the image at the path
			image = tk.PhotoImage(file=path) 
			answerlabel = tk.Label(image=image)
			answerlabel.pack()
			root.update()

		# This condition is true when co-op is played (2 correct answers)
		elif len(DUInfoParsed) == 2:
			left.pack(side="left", expand=True, fill="both")
			right.pack(side="right", expand=True, fill="both")
			path1 = './gifs/%s.gif' % DUInfoParsed[0] #set the path to this desired image
			path2 = './gifs/%s.gif' % DUInfoParsed[1] #set the path to this desired image
			questionlabel.pack_forget()
			answerlabel.pack_forget()
			answerlabel1.pack_forget()
			answerlabel2.pack_forget()
			#Display the images at the paths
			image1 = tk.PhotoImage(file=path1) 
			answerlabel1 = tk.Label(left, image=image1)
			answerlabel1.pack() #SPECIAL PACK IS NEEDED
			image2 = tk.PhotoImage(file=path2) 
			answerlabel2 = tk.Label(right, image=image2)
			answerlabel2.pack() #SPECIAL PACK IS NEEDED
			root.update()

