#https://github.com/TomSchimansky

import tkinter
from tkinter import *
import mysql.connector
from PIL import ImageTk, Image

db = mysql.connector.connect(host="localhost", user="root", passwd="Pass", database="cs_proj",)
cursor = db.cursor(buffered=True)

# geting all user details
cursor.execute("select * from users;")
all_user = cursor.fetchall()

root = Tk()
root.attributes("-fullscreen", True)

# making a frame for the login screen
loginFrame = Frame(root, bg="White", )
loginFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

# frame for admin login
adminlogin = Frame(root)
adminlogin.place_forget()


# frame for user login
userlogin = Frame(root)
userlogin.place_forget()


header = Frame(root)
header.place_forget()

# place to enter user name
userid = Label(loginFrame, text="Login ID:")
userid.grid(row=2, column=0, pady=(20, 10))
user = Entry(loginFrame, text="Enter your User ID " )
user.grid(row=2, column=1, pady=(20, 10))


# place to enter pass
passtxt = Label(loginFrame, text="Password")
passtxt.grid(row=3, column=0, pady=(10, 10))
password = Entry(loginFrame,text="Enter Password",  show="*")
password.grid(row=3, column=1)

# checking credentials
def login():
    recs_searched = 0

    for a in all_user:
        if a[1] == user.get():
            namelable = Label(header, text="Welcome %s!" % (all_user[recs_searched][1])).grid(row=0, column=99)
            if a[2] == password.get():
                if a[3] == 1:
                    adminlogin.place(x=0, y=0,anchor=NW, width=1000)
                    loginFrame.place_forget()
                    header.place(relx=1, anchor=NE)
                    stud_frame.grid(row=0, column=0, sticky=NW)
                    break
                elif a[3] == 0:
                    userlogin.place(relx=0.5, rely=0.5, anchor=CENTER,  )
                    loginFrame.place_forget()
                    stud_view_tests.grid(row=0, column=0)
                    header.place(relx=1, anchor="ne")
                    break
            else:
                response = Label(loginFrame, text="Password is Incorrect", fg="Red", bg="White", )
                response.grid(row=0, column=1)
                break
        recs_searched = + 1
    cursor.execute("Select * from users;")
    cursor.fetchall()
    if recs_searched == cursor.rowcount-1:
        response = Label(loginFrame, text="No User with that ID found", fg="Red", bg="White", )
        response.grid(row=0, column=1)


# login button
loginbutton = Button(master=loginFrame, text="Login", command=login, ).grid(row=4, column=1)

# -------->>Login screen end


# logout button (ends program)
logoutimage = ImageTk.PhotoImage(Image.open("logoutbutton.png"))
logoutbutton = Button(header, image=logoutimage, text="Logout", command=root.quit,  compound=TOP,)
logoutbutton.grid(row=0, column=100)

# -------->> Admin Screen start

# ------->Student Frame
stud_frame = Frame(adminlogin, )
stud_frame.grid_forget()


test_frame = Frame(adminlogin, )


def studshow():
    stud_frame.grid(row=0, column=0)
    test_frame.grid_forget()


def testshow():
    test_frame.grid(row=0, column=0,)
    stud_frame.grid_forget()


stud_button = Button(adminlogin, text="Students", command=studshow)
stud_button.place(anchor="nw")

test_button = Button(adminlogin, text="Tests", command=testshow)
test_button.place(anchor="nw", x=70)


# --------------------------------------------> Student Frame
no_of_stud = 1
name = "user%s" % no_of_stud
for a in all_user:
    if a[3] == 0:
        placeholder = Label(stud_frame, text="  ", ).grid(row=0, column=2)
        name = Button(stud_frame, text="%s| %s" % ( no_of_stud, a[1]),)
        name.grid(row=no_of_stud+1, column=2, pady=10, sticky="w", columnspan=3)
        no_of_stud += 1

# ----------------------------------> Test frame
cursor.execute("select * from tests")
all_tests = cursor.fetchall()

test_create_frame = Frame(adminlogin, )

def createnew():
    test_create_frame.grid(row=1, column=0, columnspan=3)
    test_frame.grid_forget()
    stud_button.place_forget()
    test_button.place_forget()

no_of_tests = 1
testname = "test%s" % no_of_tests
placeholdertest = Label(test_frame, text="   ",).grid(row=0, column=2)
createtest = Button(test_frame, text="Create New Test", command=createnew)
createtest.grid(row=no_of_tests + 1, column=2, pady=10, sticky="w", columnspan=3)
for a in all_tests:
    testname = Button(test_frame, text="%s| %s" % (no_of_tests, a[1]),)
    testname.grid(row=no_of_tests + 2, column=2, pady=10, sticky="w", columnspan=3)
    no_of_tests += 1

# ---------------------------------> Test create frame
def test_create_back():
    test_create_frame.grid_forget()
    test_frame.grid()
    stud_button.place(anchor="nw")
    test_button.place(anchor="nw", x=200)


back_button = Button(test_create_frame, text="Back", command=test_create_back).grid(row=0, column=0, sticky="w")

test_name = Entry(test_create_frame, text="Enter Test Name", )
test_name.grid(row=2, column=0, pady=10, columnspan=4)
max_marks = Entry(test_create_frame, text="Enter max marks of test", )
max_marks.grid(row=3, column=0, pady=10)
test_dur = Entry(test_create_frame, text="Enter Duration of test in minutes", )
test_dur.grid(row=3, column=1, pady=10)
question = Entry(test_create_frame, text="Enter Question", )
question.grid(row=4, column=0, pady=10, columnspan=4)


check1var = Variable()
check2var = Variable()
check3var = Variable()
check4var = Variable()

def opt1():
    check2var.set(0)
    check3var.set(0)
    check4var.set(0)
    global rightopt
    rightopt = "A"



def opt2():
    check1var.set(0)
    check3var.set(0)
    check4var.set(0)
    global rightopt
    rightopt = "B"


def opt3():
    check1var.set(0)
    check2var.set(0)
    check4var.set(0)
    global rightopt
    rightopt = "C"


def opt4():
    check1var.set(0)
    check2var.set(0)
    check3var.set(0)
    global rightopt
    rightopt = "D"


rightoption1 = tkinter.Checkbutton(test_create_frame, text="Option A is correct", variable=check1var, command=opt1, onvalue=1, offvalue=0, bg="#192026", fg="gray75", selectcolor="#395E9C")
rightoption1.grid(row=5, column=0, pady=10)
option1 = Entry(test_create_frame, text="Enter Option A",  )
option1.grid(row=5, column=1, pady=10)
rightoption2 = tkinter.Checkbutton(test_create_frame, text="Option B is correct", variable=check2var, command=opt2, onvalue=1, offvalue=0, bg="#192026", fg="gray75", selectcolor="#395E9C")
rightoption2.grid(row=5, column=2, pady=10)
option2 = Entry(test_create_frame, text="Enter Option B",  )
option2.grid(row=5, column=3, pady=10)
rightoption3 = tkinter.Checkbutton(test_create_frame, text="Option C is correct", variable=check3var, command=opt3, onvalue=1, offvalue=0, bg="#192026", fg="gray75", selectcolor="#395E9C")
rightoption3.grid(row=6, column=0, pady=10)
option3 = Entry(test_create_frame, text="Enter Option C",  )
option3.grid(row=6, column=1, pady=10)
rightoption4 = tkinter.Checkbutton(test_create_frame, text="Option D is correct", variable=check4var, command=opt4, onvalue=1, offvalue=0, bg="#192026", fg="gray75", selectcolor="#395E9C")
rightoption4.grid(row=6, column=2, pady=10)
option4 = Entry(test_create_frame, text="Enter Option D",  )
option4.grid(row=6, column=3, pady=10)
question_no = 0


def create_table():
    cursor.execute("create table %s(Question_Num int primary key auto_increment,Questions varchar(3000),Option_A varchar(1000),Option_B varchar(1000),Option_C varchar(1000),Option_D varchar(1000),Correct_option char(5), Test_duration(mins) int(6));" % (test_name.get().replace(" ", "_")))
    cursor.execute("INSERT INTO tests('name', 'max_marks') VALUES('%s',%s)" % (test_name.get(), max_marks.get()))
    db.commit()


def add_ques():
    global question_no
    question_no += 1
    print(rightopt)
    if question_no == 1:
        create_table()
    cursor.execute("INSERT INTO %s VALUES(%s" %(test_name.get().replace(" ", "_"), question_no) + ",'" + question.get() + "','" + option1.get() +"','" + option2.get() +"','" + option3.get() +"','" + option4.get()+"','" + rightopt+ "');")
    db.commit()
    question.delete(0, tkinter.END)
    option1.delete(0, tkinter.END)
    option2.delete(0, tkinter.END)
    option3.delete(0, tkinter.END)
    option4.delete(0, tkinter.END)


add_question_button = Button(test_create_frame, text="Add Another\nQuestion", command=add_ques).grid(row=7, column=4)
finish_making_test = Button(test_create_frame, text="Finish Making Test", command=test_create_back).grid(row=8, column=4, pady=10)
# -------------------------------> User Framed
studtestname= []
stud_view_tests = Frame(userlogin, )
stud_view_tests.grid_forget()
no_of_stud_tests = 1




for b in range(len(all_tests)):
    studtestname.append("test%s"%b)
test_stud_button_give = "button%s"%no_of_stud_tests
placeholderstudenttext = Label(stud_view_tests, text="   ", ).grid(row=0, column=4)
for a in all_tests:
    def give_exam(x=no_of_stud_tests):
        print(x)

    studtestname[no_of_stud_tests-1] = Button(stud_view_tests, text="%s| %s" % (no_of_stud_tests, a[1]), command=lambda: give_exam())
    studtestname[no_of_stud_tests-1].grid(row=no_of_stud_tests + 1, column=0, pady=10, sticky="w", columnspan=3)
    '''
    if user.get() in a[4:len(a)-1]:
        test_stud_button = Button(stud_view_tests, text="View Result", 0, 0)
        test_stud_button.grid(row=no_of_stud_tests + 1, column=5, pady=10, sticky="w")
    else:
        print("else")
        test_stud_button_give = Button(stud_view_tests, text="Give Test",  0, 0, command=give_exam)
        test_stud_button_give.grid(row=no_of_stud_tests + 1, column=5, pady=10, sticky="w")
    '''
    no_of_stud_tests += 1
root.mainloop()
