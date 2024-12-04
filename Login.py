import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning
import mysql.connector
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import datetime
from Accueil import MainMenu

def get_user_connected():
    return User_connected

def login_user(username):
    global User_connected
    User_connected = username

# Database connection
connection = mysql.connector.connect(host="localhost", user="root", password="", database="gmao")
cursor = connection.cursor()

def CheckLogin():
    global User_connected
    cursor.execute("SELECT * FROM login")
    res = cursor.fetchall()

    for user in res:
        if User.get() == user[1] and Password.get() == user[2]:
            User_connected = user[1]  
            window.destroy()  
            MainMenu()
            return  

    messagebox.showerror("Error Connection", "Invalid username or password.")

# Username
def on_entry0(e):
    User.delete(0, 'end')

def on_leave0(e):
    name = User.get()
    if name == '':
        User.insert(0, 'Username')

# Password
def on_entry1(e):
    Password.delete(0, 'end')
    Password.configure(show='*')

def on_leave1(e):
    name = Password.get()
    if name == '':
        Password.insert(0, 'Password')

window = Tk()
# Window Titre
window.title('Menara Holding')
window_width = 925
window_height = 500
window.configure(bg="#fff")
window.resizable(False,False)
img = PhotoImage(file='icon.png')
window.iconphoto(False, img)

# Ajout image login
img = ImageTk.PhotoImage(Image.open("login-img.png"))
label = Label(window, image = img,bg="white",width=img.width(), height=img.height(),highlightthickness=0)
label.place(x=0,y=0)
# Emplacement window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
frame = Frame(window,width=350,height=400,bg='white')
frame.place(x=550,y=40)

# Titre Sign up
Titre = Label(frame,text='Sign up',fg='#3BD2C1',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
Titre.place(x=125,y=5)

#Username
User = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11,'bold'))
User.place(x=30,y=130)
User.insert(0,'Username')
User.bind('<FocusIn>',on_entry0)
User.bind('<FocusOut>',on_leave0)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=157)

#Password
Password = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11,'bold'))
Password.place(x=30,y=200)
Password.insert(0,'Password')
Password.bind('<FocusIn>',on_entry1)
Password.bind('<FocusOut>',on_leave1)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=227)

#Button
Button(frame,width=39,pady=7,text='Sign in',bg='#3BD2C1',fg='white',border=0,command=CheckLogin).place(x=35,y=290)

window.mainloop()