from tkinter import *
from Attendance import Attendance

# File: run.py
#
# About: This file is still in PlayGround mode.  So the code is definitely not close to being finalized.
#

 #!/usr/bin/env python -W ignore::DeprecationWarning

#window = Tk()
#window.geometry("300x300")
#window.title("Welcome")


#labell=Label(window, text="Welcome to Tkinter", fg="blue" ,bg="yellow",relief="solid",font=("arial", 16, "bold"))
#labell.pack(fill=BOTH, pady=2,padx=2, expand=True)
#labell.place(x=110,y=80)
#labell.grid(row=1,column=1)
#labell.pack()


#button1=Button(window,text="Demo", fg="white" ,bg="brown",relief=GROOVE,font=("arial", 16, "bold"))
#button1.place(x=110,y=110) 	# GROOVE, RIDGE, SUNKEN, RAISED

#-----------------------------------------------------

#root = Tk()

#def leftClick(event):
#	print("Left")

#def middleClick(event):
#	print("Middle")

#def rightClick(event):
#	print("Right")
#frame = Frame(root, width=300, height=250)
#frame.bind("<Button 1>", leftClick)
#frame.bind("<Button 2>", middleClick)
#frame.bind("<Button 3>", rightClick)
#frame.pack()

#----------------------------------------------------

#frame.mainloop() 
SUBMIT_BUTTON_TEXT = "Submit grades"

colors = {
	-1: "grey",
	0: "red",
	1: "orange",
	2: "green",

}
myButtons = []
grader = Attendance()
print("Program has loaded.")
grader.updateJson()

className = grader.getClassName()
currentSection = grader.getSections()[-1]
students = grader.getDefinedGrades(currentSection)

for x in students:
	if students[x] == '':
		students[x] = -1
	else:
		students[x] = int(students[x])

# Updates the attendance number for the current student.
def updateAttendance(event):
	std = event.widget.cget("text")

	if(students[std] == -1):
		students[std] = 2
	
	elif (students[std] == 2):
		students[std] = 1

	elif (students[std] == 1):
		students[std] = 0

	else:
		students[std] = -1

	score = students[std]
	if(score == -1):
		score = ''

	updateScore(std, score)
	event.widget.config(background=colors[students[std]])
	submit.config(fg="red")

def updateScore(std, score):
	grader.addScore(currentSection, std, score)


def submitGrades(event):
	grader.submitScores(currentSection)
	submit.config(fg="green")


#--------------------------------------------------------------------------------------------

root = Tk()
root.title("Attendance Program")
root.resizable(False, False)

#one = Label(root, text="One", bg="red",fg="white")
#one.pack()

# header
header = Label(root, text=className+": "+currentSection, font=("arial", 16, "bold"), height=2)
header.pack(fill=X)

# body
for student in sorted(students.keys()):
	temp = Label(root, text=student, bg = colors[students[student]], fg="black", font=("arial",16))
	temp.config(height=2)
	temp.pack(fill=X)
	temp.bind("<Button 1>", updateAttendance)
	myButtons.append(temp)

# footer
submit = Label(root, text=SUBMIT_BUTTON_TEXT, font=("arial", 16,"bold"), height=2, fg="green")
submit.pack(fill=X)
submit.bind("<Button 1>", submitGrades)


frame = Frame(root, width=300, height=len(students)*2)
frame.pack()
frame.mainloop()




