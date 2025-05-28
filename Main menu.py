import tkinter as tk
import sys   #to make the files run by the selected interpreter
import subprocess

def run_admin_module():
    root.destroy()
    subprocess.run([sys.executable, 'Admin.py'])


def run_user_module():
    root.destroy()
    subprocess.run([sys.executable, 'Student.py'])



# Create the main window
root = tk.Tk()
root.title("Main menu")
root.geometry("500x300")

label = tk.Label(root, text="Online Quiz System:", font=("Arial", 14))
label.pack(pady=10)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Add buttons for Admin and User modules
admin_button = tk.Button(button_frame, text="Admin system", command=run_admin_module, width=20, bg="pink")
admin_button.pack(side=tk.LEFT, padx=5)

user_button = tk.Button(button_frame, text="Student system", command=run_user_module, width=20, bg="lightgreen")
user_button.pack(side=tk.LEFT, padx=5)

# Run loop
root.mainloop()


