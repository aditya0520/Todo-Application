import sqlite3
import os.path

def CreateLoginTable():
	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	c.execute(""" CREATE TABLE IF NOT EXISTS registration_details (
		name text,
		user_id text,
		email text,
		DOB text,
		password text,
		secret_Q text,
		answer text
		)""")
	con.commit()
	con.close()

def CreateUserTable(st):
	con1=sqlite3.connect('User_Details.db',timeout=10)
	c1=con1.cursor()
	s="CREATE TABLE IF NOT EXISTS "+st+" (task text,type text,duedate date)"
	c1.execute(s)
	con1.commit()
	con1.close()

def CheckUniqueness(str1,s1): # Returns true if str1 is unique

	if not os.path.isfile('User_Details.db'):
		return True
	else:
		var=0
		con=sqlite3.connect('User_Details.db')
		c=con.cursor()
		query="SELECT "+s1+" FROM registration_details"
		c.execute(query)
		rows=c.fetchall()
		for row in rows:
			if str1==row[0]:
				var=1
				break
		if var==1:
			return False
		else:
			return True
	con.close()

def getData(str1,str2,str3): #str3=column to select, str2=the attribute on the basis of which search will happen,str1=value of that attribute
	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	query="SELECT "+str3+" FROM registration_details WHERE "+str2+"=?"
	c.execute(query,(str1,))
	res=c.fetchone()
	con.close()
	return res[0]

def UpdateValue(str1,str2,s1,s2):#s2=attribute/column name to update s1=new value,str2=column name,str1=value of that column
	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	query="UPDATE registration_details SET "+s2+"=?"+" WHERE "+str2+"=?"
	c.execute(query,(s1,str1))
	con.commit()
	con.close()

def MatchDOB(s1,s2,s3):#Returns True if DOB matches with either userid or email
	v1=CheckUniqueness(s1,"user_id")
	v2=CheckUniqueness(s2,"email")
	if v1==False:
		st="user_id"
		s=s1
	if v2==False:
		st="email"
		s=s2
	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	query="SELECT DOB FROM registration_details WHERE "+st+"=?"
	c.execute(query,(s,))
	res=c.fetchone()
	con.close()
	if s3==res[0]:
		return True
	else:
		return False

def MatchPassword(str1,str3,s): #returns true if password matches

	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	query="SELECT password FROM registration_details WHERE "+s+"=?"
	c.execute(query,(str1,))
	res=c.fetchone()
	con.close()
	if res is None:
		return False
	if str3==res[0]:
		return True
	else:
		return False

def Addtask(user_id,txt,drp,cal):
	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	query="INSERT INTO "+user_id+" (task,type,duedate) VALUES (?,?,?)"
	c.execute(query,(txt,drp,cal))
	con.commit()
	con.close()

def GetTask(query):
	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	c.execute(query)
	rows=c.fetchall()
	con.commit()
	con.close()
	return rows

def Update(query):
	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	c.execute(query)
	con.commit()
	con.close()

def DeleteTask(txt,query):
	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	c.execute(query,(txt,))
	con.commit()
	con.close()

def AddtoDB(str1,str2,str3,str4,str5,str7,str8):
	print(str1,"  ",str2,"  ",str3,"  ",str4,"  ",str5,"  ",str7,"  ",str8)

	CreateLoginTable()

	con=sqlite3.connect('User_Details.db')
	c=con.cursor()
	c.execute("INSERT INTO registration_details (name,user_id,email,DOB,password,secret_Q,answer) VALUES (?,?,?,?,?,?,?)", (str1,str2,str3,str4,str5,str7,str8))
	c.execute("SELECT * FROM registration_details")

	con.commit()
	con.close()


	CreateUserTable(str2)
	#rows = c.fetchall()

	# for row in rows:
	# 	print(row)

	
