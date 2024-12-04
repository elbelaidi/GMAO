import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning
import mysql.connector
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import datetime


ImmatriculationCam = None
Modele = None

# Database
connection = mysql.connector.connect(host="localhost", user="root", password="", database="gmao")
cursor = connection.cursor()

#Immatriculation camion
def on_entry4(e):
    ImmatriculationCam.delete(0, 'end')

def on_leave4(e):
    if ImmatriculationCam.get() == '':
        ImmatriculationCam.insert(0, 'Immatriculation Camion')
        
#Modele
def on_entry5(e):
    Modele.delete(0, 'end')

def on_leave5(e):
    if Modele.get() == '':
        Modele.insert(0, 'Modèle')


#Ajout camion
def AjoutCamion(w):

    global frame2
    global ImmatriculationCam , Modele
    if 'f1' in globals():
        f1.destroy()
        
    frame2 = Frame(w, width=800, height=450, bg='#262626')
    frame2.place(x=60, y=40)
    l1 = Label(frame2, text="Ajout Camion", fg='white', bg='#262626')
    l1.config(font=('Comic Sans MS', 25))
    l1.place(x=270, y=30)

    ImmatriculationCam = Entry(frame2, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11, 'bold'))
    ImmatriculationCam.place(x=30, y=150)
    ImmatriculationCam.insert(0, 'Immatriculation Camion')
    ImmatriculationCam.bind('<FocusIn>', on_entry4)
    ImmatriculationCam.bind('<FocusOut>', on_leave4)


    Modele = Entry(frame2, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11, 'bold'))
    Modele.place(x=500, y=150)
    Modele.insert(0, 'Modèle')
    Modele.bind('<FocusIn>', on_entry5)
    Modele.bind('<FocusOut>', on_leave5)

    Button(frame2, width=39, pady=7, text='Ajouter', bg='#3BD2C1', fg='white', border=0,command=AddCamionBDD).place(x=240, y=290)
    
#Ajout camion BDD
def AddCamionBDD():

    if ImmatriculationCam.get() == "" or  Modele.get() == "" :
        messagebox.showerror("Error","Veuillez remplir tous les champs !")

    else:
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        req = "INSERT INTO camion (Immatriculation,Modele,DateAjoutCamion) VALUES (%s,%s,%s)"
        val = (ImmatriculationCam.get(), Modele.get(),current_date_time)
        cursor.execute(req, val)
        connection.commit()
        ImmatriculationCam.delete(0, 'end')
        ImmatriculationCam.insert(0, 'Immatriculation Camion')
        Modele.delete(0, 'end')
        Modele.insert(0, 'Modèle')
        messagebox.showinfo("Information !", "Camion ajouté avec succes")