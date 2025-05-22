import sqlite3 as sq
connection=sq.connect("student.db")
cursor=connection.cursor()
std_table="""create table student(name char(30),branch char(20),section char(5),marks int);"""
cursor.execute(std_table)
cursor.execute('''insert into student values('Sowjanya','IT','B',98)''')
cursor.execute('''insert into student values('Bala','CSE','A',89)''')
cursor.execute('''insert into student values('Sree','AIML','C',100)''')
cursor.execute('''insert into student values('Hari','AI&DS','B',50)''')
cursor.execute('''insert into student values('Yamini','CYBER','A',35)''')

data=cursor.execute('''select * from student''')
for i in data:
    print(i)
connection.commit()
connection.close()