from tkinter import *
from tkinter import messagebox
import hashlib
import DatabaseManipulation as dm
import PasswordRecovery as pr
import ToDoList as td
# import NewUserRegistration as nur

def FrameDefination():
	global root
	root=Tk()
	root.geometry('750x450')
	root.title("Todo List")
	root.configure(bg='white')

def Verify(str1,str2):

	c=0
	if len(str1)==0:
		messagebox.showinfo(title="ToDo List",message="Please Enter Username")
		c=1

	if dm.CheckUniqueness(str1,"user_id") and dm.CheckUniqueness(str1,"email") and c==0:
		messagebox.showerror(title="ToDo List",message="Username/E-mail does not exist")
		c=1

	if len(str2)==0 and c==0:
		messagebox.showinfo(title="ToDo List",message="Please Enter Password")
		c=1
		
	elif c==0:
		result=hashlib.md5(str2.encode())
		str3=result.hexdigest()
		if not dm.MatchPassword(str1,str3,"user_id") and not dm.MatchPassword(str1,str3,"email"):
			messagebox.showerror(title="ToDo List",message="Incorrect Password!")
		else:
			if dm.CheckUniqueness(str1,"user_id")==False:
				s1=str1
				s2="user_id"
			if dm.CheckUniqueness(str1,"email")==False:
				s1=str1
				s2="email"
			td.ListInterface(s1,s2)

def CreateHomeScreen():

	root.title("Todo List")
	global label1
	label1=Label(root,text="WELCOME",bg="white",font=("Ubuntu",36))
	label1.grid(row=0,column=0,padx=245)

	global label2
	label2=Label(root,text="Login",bg="white",font=("Ubuntu",30))
	label2.place(relx=0.17,rely=0.3)

	global label3
	label3=Label(root,text="Username/E-mail:",font=("Ubuntu",15),bg="white")
	label3.place(relx=0.018,rely=0.5)

	global entry1
	entry1=Entry(root,width=35,font=("Ubuntu",11),borderwidth=2)
	entry1.place(relx=0.25,rely=0.51)

	global label4
	label4=Label(root,text="Password:",font=("Ubuntu",15),bg="white")
	label4.place(relx=0.10,rely=0.57)

	global entry2
	entry2=Entry(root,width=35,font=("Ubuntu",11),show='*',borderwidth=2)
	entry2.place(relx=0.25,rely=0.58)

	global button1
	button1=Button(root,text="Submit",height = 2, width = 14, font=("Ubuntu",11),command=lambda: Verify(entry1.get(),entry2.get()))
	button1.place(relx=0.445,rely=0.65)

	global label5
	label5=Label(root,text="New User?",font=("Ubuntu",30),bg="white")
	label5.place(relx=0.7,rely=0.3)

	global button2
	button2=Button(root,text="Sign Up!",height = 1, width = 10, font=("Ubuntu",24))
	button2.place(relx=0.7,rely=0.43)

	global button3
	button3=Button(root,text="Forgot Password?",height = 2, width = 14, font=("Ubuntu",11),command=pr.ForgotPassword)
	button3.place(relx=0.25,rely=0.65)





