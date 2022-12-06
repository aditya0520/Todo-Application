from tkinter import * 
from tkinter import ttk 
import Remove as R
import HomeScreen as hs
import time
import datetime
from datetime import date
from tkcalendar import *
import DatabaseManipulation as dm

def Logout():
	response=messagebox.askyesno(title="ToDo List",message="Confirm Logout?")
	if response:
		R.ClearTodoList()
		hs.CreateHomeScreen()

def UpdateLabels(user_id):
	query=query="SELECT * FROM "+user_id+" ORDER BY duedate ASC"
	records=dm.GetTask(query)
	count=len(records)
	k=-1
	if len(records)>0:
		d=records[0][2]
		today=datetime.datetime.today().strftime('%Y/%m/%d')
		d0=date(int(d[0:4]),int(d[5:7]),int(d[8:10]))
		d1=date(int(today[0:4]),int(today[5:7]),int(today[8:10]))
		delta=d0-d1
		k=delta.days
	#print(today)
	if count==0:
		label3.config(text="")
		label2.config(text="You Have No Task\n Remaining To\n Complete",font=("italic",15))

	elif count==1:
		label2.config(text="You Have 1 Task\n Remaining To\n Complete",font=("italic",15))
		label2.place(relx=0.08,rely=0.33)
	elif count>1:
		label2.config(text="You Have "+str(count)+" Tasks\n Remaining To\n Complete",font=("italic",15))
		label2.place(relx=0.07,rely=0.33)
	if k==0:
		label3.config(text="You Have a Task \nDue Today",)
		label3.place(relx=0.07,rely=0.54)
	elif k==1:
		label3.config(text="Next Task Due\n In 1 Day")
		label3.place(relx=0.1,rely=0.54)
	elif k>1:
		label3.config(text="Next Task Due\n In "+str(k)+" Days")
		label3.place(relx=0.1,rely=0.54)

def ShowRecord(user_id):
	labelA.place_forget()
	query="SELECT * FROM "+user_id
	tasks=dm.GetTask(query)
	count=1
	for task in tasks:
		treev.insert("", 'end', text ="",values =(count, task[0][:len(task[0])-1], task[1],task[2])) 
		count=int(count)+1
	UpdateLabels(user_id)

def RemoveAll():
	for i in treev.get_children():
		treev.delete(i)

def RemoveFilter(user_id):
	RemoveAll()
	button1.config(state='active')
	button2.config(state='active')
	button4.config(state='active')
	button5.config(state='active')
	button3.config(text="Filter",width=15,height=1,font=("Ubuntu",11),command=lambda: AddFilter(user_id))
	button3.place(relx=0.02,rely=0.8)
	ShowRecord(user_id)
	top1.destroy()

def RemoveSelected(user_id):
	selected=treev.selection()
	if len(selected)==0:
		messagebox.showerror(title="Remove Task",message="Please Select A Task To Remove")
	for i in selected:
		it=treev.item(i,"values")
		treev.delete(i)
		query="DELETE FROM "+user_id+" where task=?"
		dm.DeleteTask(it[1]+"\n",query)
	RemoveAll()
	ShowRecord(user_id)

def ValidateNAddTask(user_id,txt,drp,cal):
	c=0
	if len(txt)==1:
		messagebox.showerror(title="Add Task",message="Please Mention The Task")
		c=1
	elif c==0:
		response=messagebox.showinfo(title="Add Task",message="Task Added Successfully!")
		top.destroy()
		dm.Addtask(user_id,txt,drp,cal)
		RemoveAll()
		ShowRecord(user_id)

def InsertFiltered(tasks):
	RemoveAll()
	count=1
	for task in tasks:
		treev.insert("", 'end', text ="",values =(count, task[0][:len(task[0])-1], task[1],task[2])) 
		count=int(count)+1
	labelA.config(text="Showing Filtered \nResults",fg="red",bg="white",font=("italic",18))
	labelA.place(relx=0.06,rely=0.38)
	button1.config(state='disable')
	button2.config(state='disable')
	button4.config(state='disable')
	button5.config(state='disable')
	label2.config(text="")
	label3.config(text="")

def  CheckandApplyFilter(user_id,txt,typ,date):
	c=0
	
	if len(txt)==0 and typ=="Select" and date=="Select":
		messagebox.showerror(title="Apply Filter",message="Please Select Atleast One Option")
		c=1
	elif c==0:
		if len(txt)!=0 and typ!="Select" and date!="Select":
			global rows
			query="SELECT * FROM "+user_id+" WHERE type='"+typ+"' AND task LIKE '%"+txt+"%' ORDER BY duedate "+date[6:]
			rows=dm.GetTask(query)
		elif len(txt)!=0 and typ=="Select" and date=="Select":
			query="SELECT * FROM "+user_id+" WHERE task LIKE '%"+txt+"%'"
			rows=dm.GetTask(query)
		elif len(txt)!=0 and typ!="Select" and date=="Select":
			query="SELECT * FROM "+user_id+" WHERE type='"+typ+"' AND task LIKE '%"+txt+"%'"
			rows=dm.GetTask(query)
		elif len(txt)==0 and typ=="Select" and date!="Select":
			query="SELECT * FROM "+user_id+" ORDER BY duedate "+date[6:]
			rows=dm.GetTask(query)
		elif len(txt)==0 and typ!="Select" and date!="Select":
			query="SELECT * FROM "+user_id+" WHERE type='"+typ+"' ORDER BY duedate "+date[6:]
			rows=dm.GetTask(query)
		elif len(txt)==0 and typ!="Select" and date=="Select":
			query="SELECT * FROM "+user_id+" WHERE type='"+typ+"'"
			rows=dm.GetTask(query)
		elif len(txt)!=0 and typ=="Select" and date!="Select":
			query="SELECT * FROM "+user_id+" WHERE task LIKE '%"+txt+"%' ORDER BY duedate "+date[6:]
			rows=dm.GetTask(query)
		InsertFiltered(rows)
		top1.destroy() 
		button3.config(text="Remove Filter",width=15,height=1,font=("Ubuntu",11),command=lambda: RemoveFilter(user_id))
		button3.place(relx=0.02,rely=0.8)

def AddFilter(user_id):
	global top1
	top1=Toplevel()
	top1.geometry("600x170")
	top1.configure(bg='white')
	top1.title("Filter")
	label1=Label(top1,text="Task Description",bg="white",font=("Ubuntu",11))
	label1.place(relx=0.01,rely=0.1)

	entry=Entry(top1,width=20,font=("Ubuntu",11),borderwidth=2)
	entry.place(relx=0.01,rely=0.25)

	label2=Label(top1,text="Task Type",bg="white",font=("Ubuntu",11))
	label2.place(relx=0.33,rely=0.1)

	store=StringVar(top1)
	store.set("Select")
	drop=OptionMenu(top1,store,"Select","Important","Planned","My Day","Assigned To You")
	drop.config(width=18,font=("Ubuntu",11),bg="white")
	drop.place(relx=0.33,rely=0.25)

	label2=Label(top1,text="Due Date",bg="white",font=("Ubuntu",11))
	label2.place(relx=0.68,rely=0.1)

	store1=StringVar(top1)
	store1.set("Select")
	drop1=OptionMenu(top1,store1,"Select","Date: ASC","Date: DESC")
	drop1.config(width=18,font=("Ubuntu",11),bg="white")
	drop1.place(relx=0.68,rely=0.26)

	button1=Button(top1,text="Apply",height=1,width=14,font=("Ubuntu",11),command=lambda: CheckandApplyFilter(user_id,entry.get(),store.get(),store1.get()))
	button1.place(relx=0.38,rely=0.65)

def UpdateToDB(user_id,s,text1,store,cal):
	msg="UPDATE "+user_id+" SET task='"+text1+"', type='"+store+"', duedate='"+cal+"' WHERE task='"+s+"'"
	dm.Update(msg)
	RemoveAll()
	ShowRecord(user_id)
	top2.destroy()

def UpdateTask(user_id):
	selected=treev.selection()
	if len(selected)==0:
		messagebox.showerror(title="Remove Task",message="Please Select A Task To Update")
	elif len(selected)>1:
		messagebox.showerror(title="Remove Task",message="Please Update One Task At A Time")
	else:
		i=selected[0]
		it=treev.item(i,"values")
		s=it[1]+"\n"
		#print(it[0],it[1],it[2],it[3])
		global top2
		top2=Toplevel()
		top2.geometry("600x170")
		top2.configure(bg='white')
		top2.title("Update Task")
		label1=Label(top2,text="Task Description",bg="white",font=("Ubuntu",11))
		label1.place(relx=0.01,rely=0.1)

		text1=Text(top2,width=20,height=3,font=("Ubuntu",11),borderwidth=2)
		text1.insert(END,it[1])
		text1.place(relx=0.01,rely=0.25)

		label2=Label(top2,text="Task Type",bg="white",font=("Ubuntu",11))
		label2.place(relx=0.33,rely=0.1)

		store=StringVar(top2)
		store.set(it[2])
		drop=OptionMenu(top2,store,"Important","Planned","My Day","Assigned To You")
		drop.config(width=18,font=("Ubuntu",11),bg="white")
		drop.place(relx=0.33,rely=0.25)

		label2=Label(top2,text="Due Date",bg="white",font=("Ubuntu",11))
		label2.place(relx=0.68,rely=0.1)

		cal=DateEntry(top2,width=13,year=int(it[3][0:4]),month=int(it[3][5:7]),day=int(it[3][8:10]),background='darkblue',font=("Ubuntu",15),foreground='white',borderwidth=4, date_pattern='yyyy/mm/dd',mindate=date.today())
		cal.place(relx=0.68,rely=0.26)

		button1=Button(top2,text="Update",height=1,width=14,font=("Ubuntu",11),command=lambda: UpdateToDB(user_id,s,text1.get("1.0",END),store.get(),cal.get()))
		button1.place(relx=0.38,rely=0.65)

def AddTask(value,column_name):
	global top
	user_id=dm.getData(value,column_name,"user_id")
	top=Toplevel()
	top.geometry("600x170")
	top.configure(bg='white')
	top.title("Add Task")
	label1=Label(top,text="Task Description",bg="white",font=("Ubuntu",11))
	label1.place(relx=0.01,rely=0.1)

	text1=Text(top,width=20,height=3,font=("Ubuntu",11),borderwidth=2)
	text1.place(relx=0.01,rely=0.25)

	label2=Label(top,text="Task Type",bg="white",font=("Ubuntu",11))
	label2.place(relx=0.33,rely=0.1)

	store=StringVar(top)
	store.set("Planned")
	drop=OptionMenu(top,store,"Important","Planned","My Day","Assigned To You")
	drop.config(width=18,font=("Ubuntu",11),bg="white")
	drop.place(relx=0.33,rely=0.25)

	label2=Label(top,text="Due Date",bg="white",font=("Ubuntu",11))
	label2.place(relx=0.68,rely=0.1)

	cal=DateEntry(top,width=13,year=2019,month=6,day=22,background='darkblue',font=("Ubuntu",15),foreground='white',borderwidth=4, date_pattern='yyyy/mm/dd',mindate=date.today())
	cal.place(relx=0.68,rely=0.26)

	button1=Button(top,text="Add",height=1,width=14,font=("Ubuntu",11),command=lambda: ValidateNAddTask(user_id,text1.get("1.0",END),store.get(),cal.get()))
	button1.place(relx=0.38,rely=0.65)

def ListInterface(value,column_name):
	#print(str1,"  ",str2)
	user_id=dm.getData(value,column_name,"user_id")
	R.Removemain()
	hs.root.title("Tasks")
	name=dm.getData(value,column_name,"name")

	currentTime = int(time.strftime('%H')) 
	global label1
	if currentTime < 12 :
		label1=Label(hs.root,text="Good Morning, "+name,bg="white",font=("Arial",36))
	elif currentTime >= 18 :
		label1=Label(hs.root,text="Good Evening, "+name,bg="white",font=("Arial",36))
	elif currentTime >= 12 :
		label1=Label(hs.root,text="Good Afternoon, "+name,bg="white",font=("Arial ",36))
	label1.grid(row=0,column=0)

	global label2
	label2=Label(hs.root,text="You Have No Task\n Remaining To\n Complete")
	label2.config(bg='white',fg="red",font=("italic",15))
	label2.place(relx=0.05,rely=0.33)

	global label3
	label3=Label(hs.root,text="")
	label3.config(bg='white',fg="red",font=("italic",15))
	label3.place(relx=0.09,rely=0.54)

	global labelA
	labelA=Label(hs.root,text="",fg="red",bg="white",font=("italic",18))
	labelA.place(relx=0.1,rely=0.1)

	def clock():
		hour=time.strftime("%I")
		minute=time.strftime("%M")
		day=time.strftime("%A")
		am_pm=time.strftime("%p")
		date=time.strftime("%d")
		month=time.strftime("%B")
		year=time.strftime("%Y")
		label4.config(bg="white",fg="blue",text=date+" "+month+" "+year+" \n "+hour+":"+minute+am_pm)
		label4.after(1000,clock)

	global label4
	label4=Label(hs.root,text="",font=("Helvetica",20))
	label4.place(relx=0.07,rely=0.15)
	clock()

	global button1
	button1=Button(hs.root,text="Add Task",width=15,height=1,font=("Ubuntu",11),command=lambda: AddTask(value,column_name))
	button1.place(relx=0.02,rely=0.7)

	global button2
	button2=Button(hs.root,text="Remove Task",width=15,height=1,font=("Ubuntu",11),command=lambda: RemoveSelected(user_id))
	button2.place(relx=0.23,rely=0.7)

	global button3
	button3=Button(hs.root,text="Filter",width=15,height=1,font=("Ubuntu",11),command=lambda: AddFilter(user_id))
	button3.place(relx=0.02,rely=0.8)

	global button4
	button4=Button(hs.root,text="Update Task",width=15,height=1,font=("Ubuntu",11),command=lambda: UpdateTask(user_id))
	button4.place(relx=0.23,rely=0.8)

	global button5
	button5=Button(hs.root,text="Log Out",width=33,height=1,font=("Ubuntu",11),command=Logout)
	button5.place(relx=0.02,rely=0.9)

	global treev
	treev = ttk.Treeview(hs.root)
	treev.place(x=340,y=80)

	global vsb
	vsb = ttk.Scrollbar(hs.root, orient="vertical", command=treev.yview)
	vsb.place(x=723, y=80, height=348)

	treev.configure(yscrollcommand=vsb.set)

	s = ttk.Style()
	s.configure('Treeview', rowheight=32)

	treev["columns"] = ("1", "2", "3","4") 
	treev.column("#0", width = 0, anchor ='c') 
	treev.column("1", width = 40,minwidth=40, anchor ='c') 
	treev.column("2", width = 150,minwidth=150, anchor ='c') 
	treev.column("3", width = 100,minwidth=90, anchor ='c')
	treev.column("4", width = 90,minwidth=90, anchor ='c')

	treev['show'] = 'headings'
	treev.heading("1", text ="Index") 
	treev.heading("2", text ="Task") 
	treev.heading("3", text ="Type") 
	treev.heading("4", text ="Due Date")

	ShowRecord(user_id)
