from tkinter import *
from tkinter import messagebox
from tkcalendar import *
from datetime import date
import Remove as R
import HomeScreen as hs
import DatabaseManipulation as dm
import math, random
import hashlib
import smtplib, ssl
from email.message import EmailMessage

def CancelPasswordRecovery(s):
	response=messagebox.askyesno(title="ToDo List",message="Confirm Cancellation Of Password Recovery?")
	if(response):
		if s=='1':
			R.ClearForgotPassword()
		elif s=='2':
			R.ClearOTP() 
		elif s=='3':
			R.ClearResetPassword()
		hs.CreateHomeScreen()


def generateOTP() : 
  
    digits = "0123456789"
    OTP = "" 

    for i in range(6) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP 

def sendMail(message,email):


	msg = EmailMessage()
	msg.set_content(message)
	msg["Subject"] = "ToDo List Application"
	msg["From"] = "adityaDemo05@gmail.com"
	msg["To"] = email

	context=ssl.create_default_context()

	with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
		smtp.starttls(context=context)
		smtp.login(msg["From"], "Demo@5520")
		smtp.send_message(msg)


def VerifyPassword(s1,s2,str1,str2):
	c=0
	if len(s1)==0 and c==0:
		messagebox.showerror(title="ToDo List",message="Password Cannot Be Empty")
		c=1
	if len(s2)==0 and c==0:
		messagebox.showerror(title="ToDo List",message="Please Confirm Your Password")
		c=1
	if c==0 and s1!=s2:
		messagebox.showerror(title="ToDo List",message="Passwords Do Not Match!")
		c=1
	if c==0 and len(s1)<8:
		messagebox.showerror(title="ToDo List",message="Password Length Should be Greater Than 8")
		c=1
	elif c==0:
		result=hashlib.md5(s1.encode())
		s1=result.hexdigest()
		dm.UpdateValue(str1,str2,s1,"password")
		response=messagebox.showinfo(title="ToDo List",message="Password Updated Successfully!!")
		if response:
			R.ClearResetPassword()
			hs.CreateHomeScreen()


def ResetPassword(str1,str2,dob):
	R.ClearOTP()
	name=dm.getData(str1,str2,"name")
	userid=dm.getData(str1,str2,"user_id")
	email=dm.getData(str1,str2,"email")

	global label1A
	label1A=Label(hs.root,text="Password Recovery Menu",bg="white",font=("Ubuntu",36))
	label1A.grid(row=0,column=0,padx=90)

	global label1B
	label1B=Label(hs.root,text="Name *",bg="white",font=("Ubuntu",13))
	label1B.place(relx=0.05,rely=0.2)

	global entry1B
	entry1B=Entry(hs.root,width=20,borderwidth=2,font=("Ubuntu",15))
	entry1B.insert(0,name)
	entry1B.config(state='disabled')
	entry1B.place(relx=0.05,rely=0.25)

	global label1C
	label1C=Label(hs.root,text="Username *",bg="white",font=("Ubuntu",13))
	label1C.place(relx=0.05,rely=0.35)

	global entry1C
	entry1C=Entry(hs.root,width=20,borderwidth=2,font=("Ubuntu",15))
	entry1C.insert(0,userid)
	entry1C.config(state='disabled')
	entry1C.place(relx=0.05,rely=0.40)

	global label1D
	label1D=Label(hs.root,text="E-mail *",bg="white",font=("Ubuntu",13))
	label1D.place(relx=0.05,rely=0.5)

	global entry1D
	entry1D=Entry(hs.root,width=20,borderwidth=2,font=("Ubuntu",15))
	entry1D.insert(0,email)
	entry1D.config(state='disabled')
	entry1D.place(relx=0.05,rely=0.55)

	global label1E
	label1E=Label(hs.root,text="Date Of Birth *",bg="white",font=("Ubuntu",13))
	label1E.place(relx=0.05,rely=0.65)

	global entry1E
	entry1E=Entry(hs.root,width=20,borderwidth=2,font=("Ubuntu",15))
	entry1E.insert(0,dob)
	entry1E.config(state='disabled')
	entry1E.place(relx=0.05,rely=0.70)

	global label1F
	label1F=Label(hs.root,text="Password *",bg="white",font=("Ubuntu",13))
	label1F.place(relx=0.55,rely=0.2)

	global entry1F
	entry1F=Entry(hs.root,width=20,borderwidth=2,show="*",font=("Ubuntu",15))
	entry1F.place(relx=0.55,rely=0.25)

	global label1G
	label1G=Label(hs.root,text="Confirm Password *",bg="white",font=("Ubuntu",13))
	label1G.place(relx=0.55,rely=0.35)

	global entry1G
	entry1G=Entry(hs.root,width=20,borderwidth=2,show="*",font=("Ubuntu",15))
	entry1G.place(relx=0.55,rely=0.40)

	global button1A
	button1A=Button(hs.root,text="Submit",height = 1, width = 20, font=("Ubuntu",15),command=lambda: VerifyPassword(entry1F.get(),entry1G.get(),str1,str2))
	button1A.place(relx=0.55,rely=0.55)

	global button1B
	button1B=Button(hs.root,text="Cancel",height = 1, width = 20, font=("Ubuntu",15),command=lambda: CancelPasswordRecovery('3'))
	button1B.place(relx=0.55,rely=0.70)

def ValidateOTP(s1,s2,str1,str2,dob,otp):#str1=The value of column,str2=The name of column
	ans=dm.getData(str1,str2,"answer")
	c=0
	if c==0 and len(s1)==0:
		messagebox.showerror(title="ToDo List",message="Enter OTP!")
		c=1
	if c==0 and len(s2)==0:
		messagebox.showerror(title="ToDo List",message="Enter Answer!")
		c=1
	if c==0 and s1!=otp:
		messagebox.showerror(title="ToDo List",message="Invalid OTP!")
		c=1
	if c==0 and ans!=s2:
		messagebox.showerror(title="ToDo List",message="Incorrect Answer!")
		c=1
	elif c==0:
		response=messagebox.showinfo(title="ToDo List",message="Validated Successfully!")
		if response:
			ResetPassword(str1,str2,dob)

def OTP(str1,str2,str3):

	otp=generateOTP()
	email=dm.getData(str1,str2,"email")
	message="Your One Time Password For Account Recovery is "+otp
	sendMail(message,email)
	dob=str3
	sq=dm.getData(str1,str2,"secret_Q")

	global labelA
	labelA=Label(hs.root,text="Password Recovery Menu",bg="white",font=("Ubuntu",36))
	labelA.grid(row=0,column=0,padx=90)

	global labelB
	labelB=Label(hs.root,text="OTP Verification",bg="white",font=("Ubuntu",30))
	labelB.place(relx=0.32,rely=0.17)

	global labelC
	labelC=Label(hs.root,text="Enter OTP*",font=("Ubuntu",15),bg="white")
	labelC.place(relx=0.275,rely=0.32)

	global entryA
	entryA=Entry(hs.root,width=20,font=("Ubuntu",15),borderwidth=2)
	entryA.place(relx=0.28,rely=0.40)

	global labelD
	labelD=Label(hs.root,text="Secret Question:",font=("Ubuntu",15),bg="white")
	labelD.place(relx=0.275,rely=0.50)

	global entryB
	entryB=Entry(hs.root,width=20,font=("Ubuntu",15),borderwidth=2)
	entryB.insert(0,sq)
	entryB.config(state='disabled')
	entryB.place(relx=0.28,rely=0.58)

	global labelE
	labelE=Label(hs.root,text="Answer*:",font=("Ubuntu",15),bg="white")
	labelE.place(relx=0.275,rely=0.68)

	global entryC
	entryC=Entry(hs.root,width=20,font=("Ubuntu",15),borderwidth=2)
	entryC.place(relx=0.28,rely=0.76)

	global buttonA
	buttonA=Button(hs.root,text="Validate",height=1,width=20,font=("Ubuntu",16),command=lambda: ValidateOTP(entryA.get(),entryC.get(),str1,str2,dob,otp))
	buttonA.place(relx=0.65,rely=0.74)

	global buttonB
	buttonB=Button(hs.root,text="Cancel",height=1,width=20,font=("Ubuntu",16),command=lambda: CancelPasswordRecovery('2'))
	buttonB.place(relx=0.65,rely=0.62)

def ValidateUser(s1,s2,s3):
	c=0
	dob=s3
	result=hashlib.md5(s3.encode())
	s3=result.hexdigest()
	if len(s1)==0 and len(s2)==0 and c==0:
		messagebox.showerror(title="ToDo List",message="Please Enter Username Or Email")
		c=1
	if c==0 and dm.CheckUniqueness(s1,"user_id") and dm.CheckUniqueness(s2,"email"):
		messagebox.showerror(title="ToDo List",message="Invalid Credentials")
		c=1
	if c==0 and not dm.MatchDOB(s1,s2,s3):
		messagebox.showerror(title="ToDo List",message="Invalid Credentials")
		c=1
	elif c==0:
		response=messagebox.showinfo(title="ToDo List",message="A One Time Password Has Been Sent To Your Email")
		if response:
			R.ClearForgotPassword()
			v1=dm.CheckUniqueness(s1,"user_id")
			v2=dm.CheckUniqueness(s2,"email")
			if v1==False:
				st="user_id"
				s=s1
			if v2==False:
				st="email"
				s=s2
			OTP(s,st,dob)

def ForgotPassword():

	R.Removemain()

	hs.root.title("Password Recovery")

	global label1
	label1=Label(hs.root,text="Password Recovery Menu",bg="white",font=("Ubuntu",36))
	label1.grid(row=0,column=0,padx=90)

	global label2
	label2=Label(hs.root,text="User Authentication",bg="white",font=("Ubuntu",30))
	label2.place(relx=0.27,rely=0.17)

	global label3
	label3=Label(hs.root,text="Username:",font=("Ubuntu",15),bg="white")
	label3.place(relx=0.275,rely=0.32)

	global entry1
	entry1=Entry(hs.root,width=20,font=("Ubuntu",15),borderwidth=2)
	entry1.place(relx=0.28,rely=0.40)

	global label4
	label4=Label(hs.root,text="OR",font=("Ubuntu",20),bg="white")
	label4.place(relx=0.40,rely=0.49)

	global label5
	label5=Label(hs.root,text="Email:",font=("Ubuntu",15),bg="white")
	label5.place(relx=0.275,rely=0.58)

	global entry2
	entry2=Entry(hs.root,width=20,font=("Ubuntu",15),borderwidth=2)
	entry2.place(relx=0.28,rely=0.66)

	global label6
	label6=Label(hs.root,text="Date Of Birth*:",font=("Ubuntu",15),bg="white")
	label6.place(relx=0.275,rely=0.76)

	global cal
	cal=DateEntry(hs.root,width=19,year=2019,month=6,day=22,background='darkblue',font=("Ubuntu",15),foreground='white',date_pattern='mm/dd/yyyy',borderwidth=4,maxdate=date.today())
	cal.place(relx=0.28,rely=0.84)

	global button1
	button1=Button(hs.root,text="Validate",height=1,width=20,font=("Ubuntu",16),command=lambda: ValidateUser(entry1.get(),entry2.get(),cal.get()))
	button1.place(relx=0.65,rely=0.84)

	global button2
	button2=Button(hs.root,text="Cancel",height=1,width=20,font=("Ubuntu",16),command=lambda: CancelPasswordRecovery('1'))
	button2.place(relx=0.65,rely=0.72)
