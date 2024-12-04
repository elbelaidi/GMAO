import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk
from datetime import datetime


# Database connection
connection = mysql.connector.connect(host="localhost", user="root", password="", database="gmao")
cursor = connection.cursor()

# Immatriculation camion
def on_entry4(e):
    ImmatriculationCam.delete(0, 'end')

def on_leave4(e):
    if ImmatriculationCam.get() == '':
        ImmatriculationCam.insert(0, 'Immatriculation Camion')

# Modele
def on_entry5(e):
    Modele.delete(0, 'end')

def on_leave5(e):
    if Modele.get() == '':
        Modele.insert(0, 'Modèle')

def treeCamions(): 
    global tree
    tree = ttk.Treeview(frame1, columns=(1, 2, 3, 4), height=5, show="headings")
    tree.place(x=100, y=90, width=590, height=120)

    tree.heading(1, text="ID", anchor="center")
    tree.heading(2, text="Modele", anchor="center")
    tree.heading(3, text="Immatriculation", anchor="center")
    tree.heading(4, text="Date Ajout", anchor="center") 

    tree.column(1, width=50)
    tree.column(2, width=100)
    tree.column(3, width=100)
    tree.column(4, width=100) 

    scroll1 = ttk.Scrollbar(tree, command=tree.yview)
    tree.configure(yscrollcommand=scroll1.set)
    scroll1.pack(side=tk.RIGHT, fill=tk.Y)

    req = "SELECT id, Modele, Immatriculation, DateAjoutCamion FROM camion WHERE Disponibilité = 1"
    cursor.execute(req)
    res = cursor.fetchall()

    for row in res:
        tree.insert('', tk.END, values=row)

    tree.bind('<<TreeviewSelect>>', autofill_entries)

def autofill_entries(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        values = item['values']

        ImmatriculationCam.delete(0, 'end')
        ImmatriculationCam.insert(0, values[2]) 
        Modele.delete(0, 'end')
        Modele.insert(0, values[1])  

def update_camion():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Sélectionnez un camion", "Veuillez sélectionner un camion à modifier.")
        return

    item = tree.item(selected_item)
    camion_id = item['values'][0]  
    new_immat = ImmatriculationCam.get().strip()  
    new_modele = Modele.get().strip() 
    
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    update_query = "UPDATE camion SET Immatriculation = %s, Modele = %s ,DateAjoutCamion = %s WHERE id = %s"
    cursor.execute(update_query, (new_immat, new_modele, current_date_time,camion_id))
    connection.commit()

    tree.delete(*tree.get_children())
    treeCamions()

def delete_camion():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Sélectionnez un camion", "Veuillez sélectionner un camion à supprimer.")
        return

    item = tree.item(selected_item)
    camion_id = item['values'][0]  

    delete_query = "DELETE FROM camion WHERE id = %s"
    cursor.execute(delete_query, (camion_id,))
    connection.commit()

    tree.delete(*tree.get_children())
    treeCamions()



def GererCamion(w):
    global frame1, tree, ImmatriculationCam, Modele

    if 'frame1' in globals():
        frame1.destroy()

    frame1 = tk.Frame(w, width=800, height=700, bg='#262626')
    frame1.place(x=60, y=40)

    l1 = tk.Label(frame1, text="Gérer Camion", fg='white', bg='#262626')
    l1.config(font=('Comic Sans MS', 25))
    l1.place(x=270, y=10)
    
    ImmatriculationCam = tk.Entry(frame1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    ImmatriculationCam.place(x=30, y=270)
    ImmatriculationCam.insert(0, 'Immatriculation Camion')
    ImmatriculationCam.bind('<FocusIn>', on_entry4)
    ImmatriculationCam.bind('<FocusOut>', on_leave4)

    Modele = tk.Entry(frame1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    Modele.place(x=500, y=270)
    Modele.insert(0, 'Modèle')
    Modele.bind('<FocusIn>', on_entry5)
    Modele.bind('<FocusOut>', on_leave5)

    treeCamions()

    tk.Button(frame1, width=39, pady=7, text='Modifier', bg='#3BD2C1', fg='white', border=0, command=update_camion).place(x=240, y=340)
    tk.Button(frame1, width=39, pady=7, text='Supprimer', bg='#3BD2C1', fg='white', border=0,command=delete_camion).place(x=240, y=390)

