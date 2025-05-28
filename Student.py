import tkinter as tk
from tkinter import messagebox
import mysql.connector
from threading import Thread, Lock
import subprocess
import sys
# Lock for thread safety
lock = Lock()
scores = []

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="question bank"
)
cursor = connection.cursor()

#Get all questions from the database
cursor.execute("""SELECT * FROM `question bank`""")
questions = cursor.fetchall()

# Get all students from the database where type=2 (student users)
cursor.execute("""SELECT * FROM `users` WHERE type=2""")
students_data = cursor.fetchall()

def create_student_window(student_number):
    def submit_answer(question, answer):
        lock.acquire()  #lock for thread safety
        if answer == question[5]:  # Compare answer with correct answer
            scores[student_number] += 1
        lock.release()

    # Create the quiz window
    win = tk.Tk()
    win.geometry("800x600+350+100")
    win.title(f"{students_data[student_number][1]}'s Quiz")

    question_index = 0

    # Display the score
    label_score = tk.Label(win, text=f"Score: 0", font=20)
    label_score.pack(pady=10)

    def display_question():
        if question_index < len(questions):
            question = questions[question_index]
            label_question.config(text=f"Question {question_index + 1}: {question[1]}")
            label_choices.config(text=f"{question[2]} | {question[3]} | {question[4]}")
            entry_answer.delete(0, tk.END)

    def next_question():
        nonlocal question_index
        answer = entry_answer.get()  # Get the student's answer
        submit_answer(questions[question_index], answer)  # Check the answer
        question_index += 1  # Move to the next question
        label_score.config(text=f"Score: {scores[student_number]}")  # Update the score display
        if question_index < len(questions):
            display_question()  # Display the next question
        else:
            win.destroy()  # Close the window if all questions are completed

    # GUI shape
    label_question = tk.Label(win, font=30)
    label_question.pack(pady=20)

    label_choices = tk.Label(win, font=20)
    label_choices.pack(pady=10)

    entry_answer = tk.Entry(win, font=20)
    entry_answer.pack(pady=20)

    button_submit = tk.Button(win, text="Submit Answer", font=20, command=next_question)
    button_submit.pack(pady=20)

    display_question()  # Display the first question
    win.mainloop()

def login(student_number,Error):
    def Check():
        username = entry_username.get()
        password = entry_password.get()
        cursor.execute("SELECT * FROM `users` WHERE `type`=2 AND `name`=%s AND `password`=%s", (username, password))
        user = cursor.fetchone()
        if user and user[0] == students_data[student_number][0]:
            login_win.destroy()
            create_student_window(student_number)
        else:
            login_win.destroy()
            login(student_number,"Wrong name or password try Again") #if wrong data is enterd Error text have a value
    login_win = tk.Tk()
    login_win.geometry("800x600+500+200")
    login_win.title(f"Login for Student {students_data[student_number][1]}")

    label_title = tk.Label(login_win, text="Student Login", font=("Arial", 18))
    label_title.pack(pady=20)

    label_username = tk.Label(login_win, text="Username:", font=("Arial", 12))
    label_username.pack(pady=5)
    entry_username = tk.Entry(login_win, font=("Arial", 12))
    entry_username.pack(pady=5)

    label_password = tk.Label(login_win, text="Password:", font=("Arial", 12))
    label_password.pack(pady=5)
    entry_password = tk.Entry(login_win, show="*", font=("Arial", 12))
    entry_password.pack(pady=5)
    label_title.config(text=Error,fg="red")    # print Error Message

    button_login = tk.Button(login_win, text="Login", font=("Arial", 12), command=Check)
    button_login.pack(pady=20)

    login_win.mainloop()

def online_quiz_system():
    root = tk.Tk()
    root.geometry("800x600+350+100")
    root.title("Main Menu")

    # GUI shape
    label_main = tk.Label(root, text="Online Quiz System", font=40)
    label_main.pack(pady=100)

    label = tk.Label(root, text="Number of Students", font=20)
    label.pack(pady=20)

    Number_of_students = tk.Entry(root, font=20)
    Number_of_students.pack(pady=10)

    def quiz():
        number = int(Number_of_students.get())
        root.destroy()
        global scores
        scores = [0] * number  # Initialize scores
        if number <= len(students_data):
            Students = []
            for i in range(number):
                # Create threads for each student's login
                Student = Thread(target=login, args=(i, "",))
                Students.append(Student)
                Student.start()

            for Student in Students:
                Student.join()

            final_scores()  # Display final scores
        else:
            messagebox.showerror("Error", f"There are only {len(students_data)} students in the class")

    button_start_quiz = tk.Button(root, text="Start Quiz", font=20, command=quiz)
    button_start_quiz.pack(pady=20)

    root.mainloop()

def final_scores():
    scores_win = tk.Tk()
    scores_win.geometry("800x600+350+100")
    scores_win.title("Final Scores")

    label_scores = tk.Label(scores_win, text="Final Scores", font=40)
    label_scores.pack(pady=50)

    # Display each student's name and score
    for i in range(len(scores)):
        name = students_data[i][1]
        score = scores[i]
        score_label = tk.Label(scores_win, text=f"{name}: {score}", font=20)
        score_label.pack(pady=5)

    scores_win.mainloop()

# Start the GUI in a separate thread
gui_thread = Thread(target=online_quiz_system)
gui_thread.start()
gui_thread.join()
subprocess.run([sys.executable, 'Main menu.py'])

