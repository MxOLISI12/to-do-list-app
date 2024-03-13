import tkinter as tk
from tkinter import messagebox
import csv
import os


def ensure_csv_exists():
    if not os.path.exists("user_info.csv"):
        with open("user_info.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password"])
            writer.writerow(["admin", "admin"])  


def add_user_to_csv(username, password):
    with open("user_info.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

# Function to handle the signup process


def signup():
    new_username = entry_new_username.get()
    new_password = entry_new_password.get()

    with open("user_info.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and new_username == row[0]:
                messagebox.showerror(
                    "Signup failed", "Username already exists.")
                return

    add_user_to_csv(new_username, new_password)
    messagebox.showinfo("Signup Successful",
                        "You can now login with your details.")
    signup_window.destroy()

def open_signup_window():
    global signup_window, entry_new_username, entry_new_password

    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")
    signup_window.geometry("300x200")

    tk.Label(signup_window, text="New Username:").pack()
    entry_new_username = tk.Entry(signup_window)
    entry_new_username.pack()

    tk.Label(signup_window, text="New Password:").pack()
    entry_new_password = tk.Entry(signup_window, show="*")
    entry_new_password.pack()

    tk.Button(signup_window, text="Register", command=signup).pack()


def login():
    global current_user  
    username = entry_username.get()
    password = entry_password.get()

    with open("user_info.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and username == row[0] and password == row[1]:
                current_user = username
                login_window.destroy()
                open_main_window()
                return
    messagebox.showerror("Login failed", "Incorrect username or password")


def open_login_window():
    global login_window, entry_username, entry_password

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Username:").pack()
    entry_username = tk.Entry(login_window)
    entry_username.pack()

    tk.Label(login_window, text="Password:").pack()
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack()

    tk.Button(login_window, text="Login", command=login).pack()
    tk.Button(login_window, text="Sign Up", command=open_signup_window).pack()
    login_window.mainloop()


def save_tasks(username):
    """Save all tasks to a file specific to the user."""
    with open(f"{username}_tasks.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        tasks = listbox_tasks.get(0, tk.END)  # Get all tasks from the listbox
        for task in tasks:
            writer.writerow([task])

def load_tasks(username):
    """Load tasks from the user's file and add them to the listbox."""
    try:
        with open(f"{username}_tasks.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                listbox_tasks.insert(tk.END, row[0])
    except FileNotFoundError:
        pass


def add_task():
    """Add a task to the list."""
    task = task_entry.get()
    if task != "":
        listbox_tasks.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")


def delete_task():
    """Delete the selected task from the list."""
    try:
        task_index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(task_index)
    except:
        messagebox.showwarning("Warning", "Please select a task to delete.")


def on_app_close(username):
    save_tasks(username)
    app.destroy()


def open_main_window():
    global current_user, app  
    app = tk.Tk()
    app.title("😝To-do-list-App😝")
    app.geometry("400x650+400+100")
    app.resizable(False, False)
    tk.Label(app, text=f"Welcome to To-Do List Application, {current_user}").pack(pady=10)
    global task_entry, listbox_tasks
    task_entry = tk.Entry(app, width=50)
    task_entry.pack(pady=10)
    listbox_tasks = tk.Listbox(app, width=50, height=20)
    listbox_tasks.pack(pady=10)
    
    #todo Load tasks for the current user
    load_tasks(current_user)  
    button_frame = tk.Frame(app)
    button_frame.pack(pady=20)
    add_task_button = tk.Button(button_frame, text="Add Task", command=add_task)
    add_task_button.pack(side=tk.LEFT, padx=10)
    delete_task_button = tk.Button(button_frame, text="Delete Task", command=delete_task)
    delete_task_button.pack(side=tk.RIGHT, padx=10)
    app.protocol("WM_DELETE_WINDOW", lambda: on_app_close(current_user))
    app.mainloop()


def on_app_close(username):
    save_tasks(username)
    app.destroy()



if __name__ == "__main__":
    ensure_csv_exists()
    open_login_window()
