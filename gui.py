from tkinter import *

root = Tk()
#root.attributes('-fullscreen',True)
def Animal_game(event):
	print("Animals")

def Color_game(event):
	print("Colors")	

def Clock_game(event):
	print("Clocks")

def sliderValue(event):
	print(slider.get())


T = Text(root, height=2, width=30)
T.pack(side=RIGHT)
T.insert(END, "Number of cones")


text1 = Text(root, height=15, width=40)
photo=PhotoImage(file='./pylogo.gif')
text1.insert(END,'\n')
text1.image_create(END, image=photo)

text1.pack(side=LEFT)

text2 = Text(root, height=20, width=50)
scroll = Scrollbar(root, command=text2.yview)
text2.configure(yscrollcommand=scroll.set)
text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
text2.tag_configure('big', font=('Verdana', 20, 'bold'))
text2.tag_configure('color', foreground='#476042', 
						font=('Tempus Sans ITC', 12, 'bold'))
text2.tag_bind('follow', '<1>', lambda e, t=text2: t.insert(END, "Not now, maybe later!"))
text2.insert(END,'\nG.O.A.T\n', 'big')
quote = """
For a number of years I have been familiar with the observation that the quality of programmers is a decreasing function of the density of go to statements in the programs they produce.
More recently I discovered why the use of the go to statement has such disastrous effects, and I became convinced that the go to statement should be abolished from all "higher level" programming languages.
"""
text2.insert(END, quote, 'color')
text2.pack(side=LEFT)
scroll.pack(side=RIGHT, fill=Y)


button_1 = Button(root, text="Animals")
button_1.bind("<Button-1>",Animal_game)
button_1.pack()
button_2 = Button(root, text="Colors")
button_2.bind("<Button-1>",Color_game)
button_2.pack()
button_3 = Button(root, text="Clocks")
button_3.bind("<Button-1>", Clock_game)
button_3.pack()
slider = Scale(root, from_=1, to=3, orient=HORIZONTAL)
slider.bind("<ButtonRelease-1>",sliderValue)
slider.pack()
root.mainloop()