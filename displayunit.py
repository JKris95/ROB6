#imports needed
import socket
import time
import tkinter as tk
import _thread

#
imageToDisplay = b'Start'


#Setup of root window for the GUI and the different images 
root = tk.Tk()
root.attributes('-fullscreen',True)

image4 = tk.PhotoImage(file="/home/pi/Desktop/wav/questionmark.gif")
questionlabel = tk.Label(image=image4)
answerlabel = tk.Label(image=image4)

#Try to connect to the server untill successfull
HOST = '192.168.1.40'    # The remote host, 
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



while True:
		
		DUInfoUnparsed = s.recv(1024)
		DUInfoParsed = json.loads(DUInfoUnparsed.decode())
		print(DUInfoParsed)

		if len(DUInfoParsed) == 1:
			path = '/home/pi/Desktop/wav/%s.gif' % DUInfoParsed #set the path to this desired image
			left.pack_forget()
			right.pack_forget()
			questionlabel.pack_forget()
			answerlabel.pack_forget()
			answerlabel1.pack_forget()
			answerlabel2.pack_forget()
			#Display the image at the path
			image = tk.PhotoImage(file=path) 
			answerlabel = tk.Label(image=image)
			answerlabel.pack()
			root.update()

		elif len(DUInfoParsed) == 2:
			left = Frame(root, borderwidth=2, relief="solid")
			right = Frame(root, borderwidth=2, relief="solid")
			path1 = '/home/pi/Desktop/wav/%s.gif' % DUInfoParsed[0] #set the path to this desired image
			path2 = '/home/pi/Desktop/wav/%s.gif' % DUInfoParsed[1] #set the path to this desired image
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
			left.pack(side="left", expand=True, fill="both")
			right.pack(side="right", expand=True, fill="both")
			root.update()

