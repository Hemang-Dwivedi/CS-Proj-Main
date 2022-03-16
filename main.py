#https://github.com/TomSchimansky
import keyboard
import time
import customtkinter
from tkinter import messagebox
from customtkinter import *
from tkinter import *
import mysql.connector
from PIL import ImageTk, Image

db = mysql.connector.connect(host="localhost", user="root", passwd="Pass", database="cs_proj",)
cursor = db.cursor(buffered=True)

# geting all user details
cursor.execute("select * from users;")
all_user = cursor.fetchall()
customtkinter.set_appearance_mode('dark_blue')
root = CTk()
root.attributes("-fullscreen", True)

cursor.execute("select * from tests")
all_tests = cursor.fetchall()
# making a CTkFrame for the login screen
loginCTkFrame = CTkFrame(root, )
loginCTkFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
# CTkFrame for admin login
adminlogin = CTkFrame(root, width=1920, height=1080)
adminlogin.place_forget()


# CTkFrame for user login
userlogin = CTkFrame(root, width=1920, height=1080)
userlogin.place_forget()


header = CTkFrame(root)
header.place_forget()

# place to enter user name
userid = CTkLabel(loginCTkFrame, text="Login ID:")
userid.grid(row=2, column=0, pady=(20, 10))
user = CTkEntry(loginCTkFrame, placeholder_text="Enter your User ID " )
user.grid(row=2, column=1, pady=(20, 10))


# place to enter pass
passtxt = CTkLabel(loginCTkFrame, text="Password")
passtxt.grid(row=3, column=0, pady=(10, 10))
password = CTkEntry(loginCTkFrame, placeholder_text="Enter Password",  show="*")
password.grid(row=3, column=1)

# checking credentials
def login():
    global stud_CTkFrame
    stud_CTkFrame = CTkFrame(adminlogin, width=1920, height=1080)
    stud_CTkFrame.grid_forget()
    recs_searched = 0

    for a in all_user:
        if a[1] == user.get():
            namelable = CTkLabel(header, text="Welcome %s!" % (all_user[recs_searched][1])).grid(row=0, column=99)
            if a[2] == password.get():
                if a[3] == 1:
                    adminlogin.place(x=0, y=0,anchor=NW, width=1920, height=1080)
                    loginCTkFrame.place_forget()
                    header.place(relx=1, anchor=NE)
                    stud_CTkFrame.grid(row=0, column=0, sticky=NW)
                    global user_id
                    user_id = a[0]
                    admin_login()
                    break
                elif a[3] == 0:
                    userlogin.place(x=0, y=0,anchor=NW, width=1920, height=1080)
                    loginCTkFrame.place_forget()
                    header.place(relx=1, anchor="ne")
                    user_id = a[0]
                    User_login()
                    break
            else:
                response = CTkLabel(loginCTkFrame, text="Password is Incorrect", fg="Red", bg="White", width=200)
                response.grid(row=0, column=1)
                break
        recs_searched += 1
    if recs_searched == len(all_user):
        response = CTkLabel(loginCTkFrame, text="No User with that ID found", fg="Red", bg="White", width=200)
        response.grid(row=0, column=1)


# login CTkButton
loginCTkButton = CTkButton(master=loginCTkFrame, text="Login", command=login, ).grid(row=4, column=1)

# -------->>Login screen end
def logout():
    cursor.close()
    db.close()
    root.quit()

# logout CTkButton (ends program)
logoutimage = ImageTk.PhotoImage(Image.open("logoutButton.png"))
logoutCTkButton = CTkButton(header, image=logoutimage, text="Logout", command=logout,  compound=TOP,)
logoutCTkButton.grid(row=0, column=100)


# -------->> Admin Screen start
def admin_login():
    test_CTkFrame = CTkFrame(adminlogin, width=1920, height=1080 )

    def studshow():
        stud_CTkFrame.grid(row=0, column=0)
        test_CTkFrame.grid_forget()

    def testshow():
        test_CTkFrame.grid(row=0, column=0,)
        stud_CTkFrame.grid_forget()

    stud_CTkButton = CTkButton(adminlogin, text="Students", command=studshow, text_font=("", 36))
    stud_CTkButton.place(anchor="nw")
    test_CTkButton = CTkButton(adminlogin, text="Tests", command=testshow, text_font=("", 36))
    test_CTkButton.place(anchor="nw", x=300)
    # --------------------------------------------> Student CTkFrame
    cursor.execute("select * from results;")
    all_result = cursor.fetchall()
    message = StringVar()

    def show_student_result(x):
        stud_result = "Result of %s:"%all_user[x][1]
        for a in all_tests:
            for f in all_result:
                if a[0] == f[2]:
                    if f[1] == all_user[x][0]:
                        stud_result += "\n Test Name: %s, Marks: %s"%(a[1],f[3])
                    else:
                        stud_result = "Student hasn't attempted any tests"
        message.set(stud_result)
        messagebox.showinfo("%s Result" % all_user[x][1], message=message.get())
    no_of_stud = 1
    name = "user%s" % no_of_stud
    for a in all_user:
        if a[3] == 0:
            placeholder = CTkLabel(stud_CTkFrame, text="  ", text_font=("", 36) ).grid(row=0, column=2)
            name = CTkButton(stud_CTkFrame, text="%s. %s" % ( no_of_stud, a[1]), command=lambda z=no_of_stud: show_student_result(z), text_font=("", 36))
            name.grid(row=no_of_stud+1, column=2, pady=10, sticky="w", columnspan=3)
            no_of_stud += 1
    # ----------------------------------> Test CTkFramez
    test_create_CTkFrame = CTkFrame(adminlogin, width=1920, height=1080, )

    def createnew():
        test_create_CTkFrame.grid( stick="nw")
        test_CTkFrame.grid_forget()
        stud_CTkButton.place_forget()
        test_CTkButton.place_forget()

    no_of_tests = 1
    placeholdertest = CTkLabel(test_CTkFrame, text="   ", text_font=("", 36)).grid(row=0, column=2)
    createtest = CTkButton(test_CTkFrame, text="Create New Test", command=createnew, text_font=("", 36))
    createtest.grid(row=no_of_tests + 1, column=2, pady=10, sticky="w", columnspan=3)
    CTkLabel(test_CTkFrame, text="Tests Available:-", text_font=("", 36)).grid(row=no_of_tests + 2, column=2,sticky="w", columnspan=3, pady =10)
    for a in all_tests:
        testname = CTkLabel(test_CTkFrame, text="%s| %s" % (no_of_tests, a[1]), text_font=("", 36))
        testname.grid(row=no_of_tests + 3, column=2, pady=10, sticky="w", columnspan=3)
        no_of_tests += 1

    # ---------------------------------> Test create CTkFrame
    def test_create_back():
        test_create_CTkFrame.grid_forget()
        test_CTkFrame.grid()
        stud_CTkButton.place(anchor="nw")
        test_CTkButton.place(anchor="nw", x=200)

    back_CTkButton = CTkButton(test_create_CTkFrame, text="Back", command=test_create_back).grid(row=0, column=0, sticky="w")
    test_name = CTkEntry(test_create_CTkFrame, placeholder_text="Enter Test Name", width=1550 )
    test_name.grid(row=2, column=0, pady=10, columnspan=4, sticky="w")
    test_dur = CTkEntry(test_create_CTkFrame, placeholder_text="Enter Duration of test in minutes", width=1550 )
    test_dur.grid(row=3, column=0, pady=10, sticky="w", columnspan=4, padx=10)
    question = CTkEntry(test_create_CTkFrame, placeholder_text="Enter Question", width=1550)
    question.grid(row=4, column=0, pady=10, columnspan=4, sticky="w")
    checkvar = StringVar()
    rightoption1 = CTkRadioButton(test_create_CTkFrame, text="Option A is correct", variable=checkvar, value="A")
    rightoption1.grid(row=5, column=0, pady=10,padx=0)
    option1 = CTkEntry(test_create_CTkFrame, placeholder_text="Enter Option A",width=500)
    option1.grid(row=5, column=1, pady=10)
    rightoption2 = CTkRadioButton(test_create_CTkFrame, text="Option B is correct", variable=checkvar, value="B")
    rightoption2.grid(row=5, column=2, pady=10,padx=0)
    option2 = CTkEntry(test_create_CTkFrame, placeholder_text="Enter Option B",width=500)
    option2.grid(row=5, column=3, pady=10)
    rightoption3 = CTkRadioButton(test_create_CTkFrame, text="Option C is correct", variable=checkvar, value="C")
    rightoption3.grid(row=6, column=0, pady=10,padx=0)
    option3 = CTkEntry(test_create_CTkFrame, placeholder_text="Enter Option C",width=500)
    option3.grid(row=6, column=1, pady=10)
    rightoption4 = CTkRadioButton(test_create_CTkFrame, text="Option D is correct", variable=checkvar, value="D")
    rightoption4.grid(row=6, column=2, pady=10,padx=0)
    option4 = CTkEntry(test_create_CTkFrame, placeholder_text="Enter Option D",width=500)
    option4.grid(row=6, column=3, pady=10)
    global question_no
    question_no = 0

    def create_table():
        cursor.execute("create table %s(Question_No int primary key auto_increment,Questions varchar(3000),Option_A varchar(1000),Option_B varchar(1000),Option_C varchar(1000),Option_D varchar(1000),Correct_option char(5));" % (test_name.get().replace(" ", "_")))
        cursor.execute("INSERT INTO tests(name, max_dur_min) VALUES('%s',%s);" % (test_name.get().replace(" ", "_"), test_dur.get()))
        db.commit()

    def add_ques():
        global question_no
        question_no += 1
        if question_no == 1:
            create_table()
        cursor.execute("INSERT INTO %s VALUES(%s" %(test_name.get().replace(" ", "_"), question_no) + ",'" + question.get() + "','" + option1.get() + "','" + option2.get() + "','" + option3.get() + "','" + option4.get()+"','" + checkvar.get() + "');")
        db.commit()
        question.delete(0, tkinter.END)
        option1.delete(0, tkinter.END)
        option2.delete(0, tkinter.END)
        option3.delete(0, tkinter.END)
        option4.delete(0, tkinter.END)

    add_question_CTkButton = CTkButton(test_create_CTkFrame, text="Add Another\nQuestion", command=add_ques).grid(row=7, column=4)
    finish_making_test = CTkButton(test_create_CTkFrame, text="Finish Making Test", command=lambda: [test_creaYte_back, add_ques]).grid(row=8, column=4, pady=10)


# -------------------------------> User CTkFramed
def User_login():
    stud_view_tests = CTkFrame(userlogin, width=1920, height=1080 )
    stud_view_tests.grid(row=0, column=0)
    no_of_stud_tests = 1

    def stopkeyboard(x):
        for z in range(150):
            keyboard.block_key(z)
        time.sleep(x * 60)

    give_test_CTkFrame = CTkFrame(userlogin, width=1920, height=1080)
    test_time = CTkLabel(give_test_CTkFrame, text="Not updated", text_font=("", 36))
    test_time.place(x=1500)
    sec = StringVar()
    mins = StringVar()
    hrs = StringVar()
    
    def countdowntimer(x):
        times = x*60
        while times > -1:
            minute, second = (times // 60, times % 60)
            hour = 0
            if minute > 60:
                hour, minute = (minute // 60, minute % 60)
            sec.set(second)
            mins.set(minute)
            hrs.set(hour)
            # Update the time
            test_time.update()
            time.sleep(1)
            if (times == 0):
                sec.set('00')
                mins.set('00')
                hrs.set('00')
            times -= 1
            test_time.configure(text="%s:%s:%s" % (hrs.get(), mins.get(), sec.get()))

    def give_exam(x):
        header.place_forget()
        global marks_obt
        marks_obt = 0
        stud_view_tests.grid_forget()
        give_test_CTkFrame.grid(row=0, column=0)
        test_give = all_tests[x-1][1]
        test_duration = all_tests[x-1][2]
        stopkeyboard(test_duration)
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        countdowntimer(test_duration)
        for i in tables:
            if i[0] == test_give.lower():
                cursor.execute("select * from %s" % i)
                questions = cursor.fetchall()
                ques_no = 0
                vari = 0
                ans = {}
                val = 0
                variables = {}
                for i in range(len(questions)):
                    variables[i] = IntVar()
                for d in questions:
                    ques = CTkLabel(give_test_CTkFrame, text="Q%s. %s" % (d[0], d[1]), width=1000, text_font=("", 50))
                    ques.grid(row=ques_no, column=0, columnspan=2, sticky="w")
                    opt_a = CTkRadioButton(give_test_CTkFrame, text="A. %s" % d[2], value=1+val, variable=variables[vari], text_font=("", 36))
                    opt_a.grid(row=ques_no + 1, column=0, sticky="w")
                    opt_b = CTkRadioButton(give_test_CTkFrame, text="B. %s" % d[3], value=2+val, variable=variables[vari], text_font=("", 36))
                    opt_b.grid(row=ques_no + 1, column=1, sticky="w")
                    opt_c = CTkRadioButton(give_test_CTkFrame, text="C. %s" % d[4], value=3+val, variable=variables[vari], text_font=("", 36))
                    opt_c.grid(row=ques_no + 2, column=0, sticky="w")
                    opt_d = CTkRadioButton(give_test_CTkFrame, text="D. %s" % d[5], value=4+val, variable=variables[vari], text_font=("", 36))
                    opt_d.grid(row=ques_no + 2, column=1, sticky="w")
                    ques_no += 3
                    vari += 1
                    val += 4

                def next():
                    print("Next called")
                    global marks_obt
                    for a in range(len(questions)):
                        if variables[a].get() - 4 * a == 1:
                            ans[a] = "A"
                            if ans[a] == questions[a][6]:
                                marks_obt =+1
                        elif variables[a].get() - 4 * a == 2:
                            ans[a] = "B"
                            if ans[a] == questions[a][6]:
                                marks_obt =+1
                        elif variables[a].get() - 4 * a == 3:
                            ans[a] = "C"
                            if ans[a] == questions[a][6]:
                                marks_obt =+1
                        elif variables[a].get() - 4 * a == 4:
                            ans[a] = "D"
                            if ans[a] == questions[a][6]:
                                marks_obt =+1
                    print("")
                    cursor.execute("INSERT INTO results(UserID,Test_ID,marks_scored) VALUE (%s,%s,%s);" % (int(user_id), int(all_tests[x-1][0]), int(marks_obt)))
                    db.commit()
                    print(cursor)
                    print(marks_obt)
                    give_test_CTkFrame.grid_forget()
                    stud_view_tests.update()
                    stud_view_tests.grid(row=0, column=0)
                    header.place(relx=1, anchor=NE)
                next_q_test = CTkButton(give_test_CTkFrame, text="Finish Exam>", command=next)
                next_q_test.grid(row=ques_no+1, column=1, sticky="e")

    cursor.execute("select * from results;")
    all_result = cursor.fetchall()

    def show_result(x):
        for v in all_result:
            if v[1] == user_id:
                if v[2] == all_tests[x-1][0]:
                    messagebox.showinfo("Test", message="You Scored %s in this test" % v[3])

    placeholderstudenttext = CTkLabel(stud_view_tests, text="   ", ).grid(row=0, column=4)
    for a in all_tests:
        studtestname = CTkLabel(stud_view_tests, text="%s| %s" % (no_of_stud_tests, a[1]))
        studtestname.grid(row=no_of_stud_tests + 1, column=0, pady=10, sticky="w", columnspan=3)

        for c in all_result:
            if c[1] == user_id:
                if int(c[2]) == int(all_tests[no_of_stud_tests-1][0]):
                    print("A")
                    test_stud_CTkButton = customtkinter.CTkButton(stud_view_tests, text="View Result", command=lambda x=no_of_stud_tests: show_result(x))
                    test_stud_CTkButton.grid(row=no_of_stud_tests + 1, column=5, pady=10, sticky="w")
                    break
                else:
                    test_stud_CTkButton_give = customtkinter.CTkButton(stud_view_tests, text="Give Test", command=lambda x=no_of_stud_tests: give_exam(x))
                    test_stud_CTkButton_give.grid(row=no_of_stud_tests + 1, column=5, pady=10, sticky="w")
            else:
                test_stud_CTkButton_give = customtkinter.CTkButton(stud_view_tests, text="Give Test", command=lambda x=no_of_stud_tests: give_exam(x))
                test_stud_CTkButton_give.grid(row=no_of_stud_tests + 1, column=5, pady=10, sticky="w")
        else:
            test_stud_CTkButton_give = customtkinter.CTkButton(stud_view_tests, text="Give Test", command=lambda x=no_of_stud_tests: give_exam(x))
            test_stud_CTkButton_give.grid(row=no_of_stud_tests + 1, column=5, pady=10, sticky="w")
        no_of_stud_tests += 1

        
root.mainloop()
