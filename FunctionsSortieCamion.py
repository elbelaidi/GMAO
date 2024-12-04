import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning
import mysql.connector
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import datetime

Nom_chauffeur = None
Immatriculation = None

# Database
connection = mysql.connector.connect(host="localhost", user="root", password="", database="gmao")
cursor = connection.cursor()

# Immatriculation
def on_entry2(e):
    Immatriculation.delete(0, 'end')

def on_leave2(e):
    if Immatriculation.get() == '':
        Immatriculation.insert(0, 'Immatriculation camion')

# Nom chauffeur
def on_entry1(e):
    Nom_chauffeur.delete(0, 'end')

def on_leave1(e):
    if Nom_chauffeur.get() == '':
        Nom_chauffeur.insert(0, 'Nom chauffeur')
        
# AjoutSortieCamion BDD
def SortieCamionBDD():
    if Immatriculation.get() == "Immatriculation camion" or Nom_chauffeur.get() == "Nom chauffeur":
        messagebox.showerror("Error", "Veuillez remplir tous les champs !")
    else:
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

        # Ajout
        req = "INSERT INTO sortiecamion (Immatriculation, Chauffeur, Disponibilité, DateSortie) VALUES (%s, %s, %s, %s)"
        val = (Immatriculation.get(), Nom_chauffeur.get(), "1", current_date_time)
        cursor.execute(req, val)
        connection.commit()

        # Modification disponibilité chauffeur
        req = "UPDATE chauffeur SET Disponibilité = %s WHERE Nom = %s"
        valeur = ("0", Nom_chauffeur.get())
        cursor.execute(req, valeur)
        connection.commit()

        # Modification disponibilité camion
        req = "UPDATE camion SET Disponibilité = %s WHERE Immatriculation = %s"
        valeur = ("0", Immatriculation.get())
        cursor.execute(req, valeur)
        connection.commit()

        Immatriculation.delete(0, 'end')
        Immatriculation.insert(0, 'Immatriculation camion')
        Nom_chauffeur.delete(0, 'end')
        Nom_chauffeur.insert(0, 'Nom chauffeur')
        treeCamion()
        treeChauffeur()
        messagebox.showinfo("Information !", "Ajouté avec succès")


# TreeView Chauffeur
def treeChauffeur():
    treeChauffeur = ttk.Treeview(frame1, columns=(1, 2), height=5, show="headings")
    treeChauffeur.place(x=30, y=130, width=250, height=100)
    treeChauffeur.heading(1, text="Id chauffeur", anchor="center")
    treeChauffeur.heading(2, text="Nom chauffeur", anchor="center")
    treeChauffeur.column(1, width=80)
    treeChauffeur.column(2, width=170)

    scroll1 = ttk.Scrollbar(treeChauffeur, command=treeChauffeur.yview)
    treeChauffeur.configure(yscrollcommand=scroll1.set)
    scroll1.pack(side=RIGHT, fill=Y)

    req = "select Id,Nom from chauffeur where Disponibilité = 1"
    cursor.execute(req)
    res = cursor.fetchall()
    for row in res:
        treeChauffeur.insert('', END, values=row)

    treeChauffeur.bind('<<TreeviewSelect>>', lambda event: fill_chauffeur_entry(treeChauffeur))


def fill_chauffeur_entry(tree):
    selected_item = tree.focus()
    values = tree.item(selected_item, 'values')
    if values:
        Nom_chauffeur.delete(0, 'end')
        Nom_chauffeur.insert(0, values[1]) 


# TreeView Camion
def treeCamion():
    treeCamion = ttk.Treeview(frame1, columns=(1, 2), height=5, show="headings")
    treeCamion.place(x=500, y=130, width=250, height=100)
    treeCamion.heading(2, text="Immatriculation", anchor="center")
    treeCamion.heading(1, text="Modele", anchor="center")
    treeCamion.column(1, width=80)
    treeCamion.column(2, width=170)

    scroll1 = ttk.Scrollbar(treeCamion, command=treeCamion.yview)
    treeCamion.configure(yscrollcommand=scroll1.set)
    scroll1.pack(side=RIGHT, fill=Y)

    req = "select Modele,Immatriculation from camion where Disponibilité = 1"
    cursor.execute(req)
    res = cursor.fetchall()
    for row in res:
        treeCamion.insert('', END, values=row)

    treeCamion.bind('<<TreeviewSelect>>', lambda event: fill_camion_entry(treeCamion))


def fill_camion_entry(tree):
    selected_item = tree.focus()
    values = tree.item(selected_item, 'values')
    if values:
        Immatriculation.delete(0, 'end')
        Immatriculation.insert(0, values[1])  


# Sortie camion
def SortieCamion(w):

    global frame1
    global Nom_chauffeur, Immatriculation

    if 'f1' in globals():
        f1.destroy()

    frame1 = Frame(w, width=800, height=450, bg='#262626')
    frame1.place(x=60, y=40)

    l1 = Label(frame1, text="Sortie de camion", fg='white', bg='#262626')
    l1.config(font=('Comic Sans MS', 25))
    l1.place(x=270, y=30)

    treeCamion()
    treeChauffeur()

    Nom_chauffeur = Entry(frame1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    Nom_chauffeur.place(x=40, y=270)
    Nom_chauffeur.insert(0, 'Nom chauffeur')
    Nom_chauffeur.bind('<FocusIn>', on_entry1)
    Nom_chauffeur.bind('<FocusOut>', on_leave1)

    Immatriculation = Entry(frame1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    Immatriculation.place(x=510, y=270)
    Immatriculation.insert(0, 'Immatriculation camion')
    Immatriculation.bind('<FocusIn>', on_entry2)
    Immatriculation.bind('<FocusOut>', on_leave2)

    Button(frame1, width=39, pady=7, text='Valider', bg='#3BD2C1', fg='white', border=0,command=SortieCamionBDD).place(x=240, y=330)

