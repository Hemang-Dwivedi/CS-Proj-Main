from customtkinter import *
import mysql.connector
root = CTk()
db = mysql.connector.connect(host="localhost", user="root", passwd="Pass", database="cs_proj",)
cursor = db.cursor(buffered=True)
cursor.execute("select * from results;")
for i in cursor.fetchall():
    print(i[1])
