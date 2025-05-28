import tkinter as tk
from tkinter import messagebox
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="question bank"
)
cursor = connection.cursor()

def window(name, title, show_window=True):
    win = tk.Toplevel() if name != "root" else tk.Tk()
    win.geometry("800x700+350+100")
    win.title(title)
    if not show_window:
        win.withdraw()
    return win

def label(window, text, x, y, font=30):
    lbl = tk.Label(window, text=text, font=font)
    lbl.place(x=x, y=y)

def entry(window, y):
    ent = tk.Entry(window)
    ent.place(x=100, y=y, width=600, height=40)
    return ent

def button(window, text, bg, command, x, y, width, height):
    btn = tk.Button(window, text=text, bg=bg, command=command)
    btn.place(x=x, y=y, width=width, height=height)


root = window("root", "Login", show_window=True)
admin_window = window("admin_window", "Admin", show_window=False)
quiz_window = window("quiz_window", "Quiz", show_window=False)
add_user_window = window("add_user_window", "Add User", show_window=False)
delete_user_window = window("delete_user_window", "Delete User", show_window=False)
add_question_window = window("add_question_window", "Add Question", show_window=False)
delete_question_window = window("delete_question_window", "Delete Question", show_window=False)


def login():
    name = entry_login_email.get()
    password = entry_login_password.get()
    cursor.execute("SELECT * FROM `users` WHERE name=%s AND password=%s AND type=1", (name, password))
    user = cursor.fetchall()
    if user:
        root.withdraw()
        admin_window.deiconify()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

def add_user():
    name = entry_add_user_name.get()
    password = entry_add_user_password.get()
    user_type = entry_add_user_type.get()

    cursor.execute("SELECT * FROM `users` WHERE name=%s", (name,))
    if cursor.fetchone():
        messagebox.showwarning("Error", "User already exists")
    else:
        cursor.execute("INSERT INTO `users` (name, password, type) VALUES (%s, %s, %s)", (name, password, user_type))
        connection.commit()
        messagebox.showinfo("Success", "User added successfully")

def delete_user():
    user_id = entry_delete_user_id.get()
    cursor.execute("DELETE FROM `users` WHERE id=%s", (user_id,))
    connection.commit()
    messagebox.showinfo("Success", "User deleted successfully")

def add_question():
    question = entry_add_question_question.get()
    option1 = entry_add_question_option1.get()
    option2 = entry_add_question_option2.get()
    option3 = entry_add_question_option3.get()
    answer = entry_add_question_answer.get()

    cursor.execute(
        "INSERT INTO `question bank` (Question, Choice1, Choice2, Choice3, Answer) VALUES (%s, %s, %s, %s, %s)",
        (question, option1, option2, option3, answer)
    )
    connection.commit()
    messagebox.showinfo("Success", "Question added successfully")

def delete_question():
    question_id = entry_delete_question_id.get()
    cursor.execute("DELETE FROM `question bank` WHERE id=%s", (question_id,))
    connection.commit()
    messagebox.showinfo("Success", "Question deleted successfully")

# Login Window
label(root, "Login", 375, 50)
label(root, "Email", 100, 200)
label(root, "Password", 100, 300)

entry_login_email = entry(root, 250)
entry_login_password = entry(root, 350)

button(root, "Login", "yellow", login, 370, 450, 100, 50)

# Admin Window
button(admin_window, "Add User", "green", lambda: add_user_window.deiconify(), 150, 150, 200, 50)
button(admin_window, "Delete User", "red", lambda: delete_user_window.deiconify(), 450, 150, 200, 50)
button(admin_window, "Add Question", "green", lambda: add_question_window.deiconify(), 150, 350, 200, 50)
button(admin_window, "Delete Question", "red", lambda: delete_question_window.deiconify(), 450, 350, 200, 50)

# Add User Window
label(add_user_window, "Add User", 375, 20)
label(add_user_window, "Name", 100, 100)
label(add_user_window, "Password", 100, 200)
label(add_user_window, "Type", 100, 300)
entry_add_user_name = entry(add_user_window, 150)
entry_add_user_password = entry(add_user_window, 250)
entry_add_user_type = entry(add_user_window, 350)

button(add_user_window, "Add", "yellow", add_user, 375, 500, 70, 50)

# Delete User Window
label(delete_user_window, "Delete User", 360, 50)
label(delete_user_window, "User ID", 100, 200)
entry_delete_user_id = entry(delete_user_window, 250)

button(delete_user_window, "Delete", "yellow", delete_user, 375, 400, 70, 50)

# Add Question Window
label(add_question_window, "Add Question", 350, 20)
label(add_question_window, "Question", 100, 100)
label(add_question_window, "Choice 1", 100, 200)
label(add_question_window, "Choice 2", 100, 300)
label(add_question_window, "Choice 3", 100, 400)
label(add_question_window, "Answer", 100, 500)
entry_add_question_question = entry(add_question_window, 150)
entry_add_question_option1 = entry(add_question_window, 250)
entry_add_question_option2 = entry(add_question_window, 350)
entry_add_question_option3 = entry(add_question_window, 450)
entry_add_question_answer = entry(add_question_window, 550)

button(add_question_window, "Add", "yellow", add_question, 375, 600, 70, 50)

# Delete Question Window
label(delete_question_window, "Delete Question", 360, 50)
label(delete_question_window, "Question ID", 100, 200)
entry_delete_question_id = entry(delete_question_window, 250)

button(delete_question_window, "Delete", "yellow", delete_question, 375, 400, 70, 50)

root.mainloop()

