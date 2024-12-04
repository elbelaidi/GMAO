import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning
import mysql.connector
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import datetime


chauffeur = None
tel = None
Adresse = None

# Database
connection = mysql.connector.connect(host="localhost", user="root", password="", database="gmao")
cursor = connection.cursor()


#chauffeur
def on_entry1(e):
    chauffeur.delete(0, 'end')

def on_leave1(e):
    if chauffeur.get() == '':
        chauffeur.insert(0, 'Nom chauffeur')
        
#tél
def on_entry2(e):
                tel.delete(0, 'end')

def on_leave2(e):
    if tel.get() == '':
        tel.insert(0, 'Telephone')

#Adresse
def on_entry3(e):
    Adresse.delete(0, 'end')

def on_leave3(e):
    if Adresse.get() == '':
        Adresse.insert(0, 'Adresse')
        

def AjoutChauffeur(w):
    
    global frame3
    global chauffeur, tel, Adresse
    
    if 'f1' in globals():
        f1.destroy() 

    frame3 = Frame(w, width=800, height=450, bg='#262626')
    frame3.place(x=60, y=40)

    l1 = Label(frame3, text="Ajout chauffeur", fg='white', bg='#262626')
    l1.config(font=('Microsoft YaHei UI Light', 25))
    l1.place(x=270, y=30)

    chauffeur = Entry(frame3, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    chauffeur.place(x=30, y=150)
    chauffeur.insert(0, 'Nom chauffeur')
    chauffeur.bind('<FocusIn>', on_entry1)
    chauffeur.bind('<FocusOut>', on_leave1)

    tel = Entry(frame3, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    tel.place(x=500, y=150)
    tel.insert(0, 'Telephone')
    tel.bind('<FocusIn>', on_entry2)
    tel.bind('<FocusOut>', on_leave2)

    Adresse = Entry(frame3, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    Adresse.place(x=270, y=240)
    Adresse.insert(0, 'Adresse')
    Adresse.bind('<FocusIn>', on_entry3)
    Adresse.bind('<FocusOut>', on_leave3)

    Button(frame3, width=39, pady=7, text='Ajouter', bg='#3BD2C1', fg='white', border=0,command=AddChauffeurBDD).place(x=240, y=330)

def AddChauffeurBDD():
    if chauffeur.get() == "" or tel.get() == "" or Adresse.get() == "":
        messagebox.showerror("Error", "Veuillez remplir tous les champs !")
    else:
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        req = "INSERT INTO chauffeur (Nom,Tel,Adresse,DateAjoutChauffeur) VALUES (%s,%s,%s,%s)"
        val = (chauffeur.get(), tel.get(), Adresse.get(),current_date_time)
        cursor.execute(req, val)
        connection.commit()

        chauffeur.delete(0, 'end')
        chauffeur.insert(0, 'Nom chauffeur')
        tel.delete(0, 'end')
        tel.insert(0, 'Telephone')
        Adresse.delete(0, 'end')
        Adresse.insert(0, 'Adresse')
        messagebox.showinfo("Information !", "Chauffeur ajouté avec succès")

