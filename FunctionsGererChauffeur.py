import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk
from datetime import datetime

# Database connection
connection = mysql.connector.connect(host="localhost", user="root", password="", database="gmao")
cursor = connection.cursor()

chauffeur = None
tel = None
Adresse = None
selected_chauffeur_id = None  

def treeChauffeurs(): 
    global tree_chauffeurs
    tree_chauffeurs = ttk.Treeview(frame1, columns=(1, 2, 3, 4, 5), height=5, show="headings")
    tree_chauffeurs.place(x=100, y=90, width=590, height=120)

    tree_chauffeurs.heading(1, text="ID", anchor="center")
    tree_chauffeurs.heading(2, text="Nom", anchor="center")
    tree_chauffeurs.heading(3, text="Tel", anchor="center")
    tree_chauffeurs.heading(4, text="Adresse", anchor="center")
    tree_chauffeurs.heading(5, text="Date Ajout", anchor="center") 

    tree_chauffeurs.column(1, width=50)
    tree_chauffeurs.column(2, width=100)
    tree_chauffeurs.column(3, width=100)
    tree_chauffeurs.column(4, width=100)
    tree_chauffeurs.column(5, width=100)

    scroll1 = ttk.Scrollbar(tree_chauffeurs, command=tree_chauffeurs.yview)
    tree_chauffeurs.configure(yscrollcommand=scroll1.set)
    scroll1.pack(side=tk.RIGHT, fill=tk.Y)

    req = "SELECT id, Nom, Tel, Adresse, DateAjoutChauffeur FROM chauffeur WHERE Disponibilité = 1"
    cursor.execute(req)
    res = cursor.fetchall()

    for row in res:
        tree_chauffeurs.insert('', tk.END, values=row)

    tree_chauffeurs.bind('<<TreeviewSelect>>', on_tree_select)

def on_entry1(e):
    chauffeur.delete(0, 'end')

def on_leave1(e):
    if chauffeur.get() == '':
        chauffeur.insert(0, 'Nom chauffeur')

def on_entry2(e):
    tel.delete(0, 'end')

def on_leave2(e):
    if tel.get() == '':
        tel.insert(0, 'Telephone')

def on_entry3(e):
    Adresse.delete(0, 'end')

def on_leave3(e):
    if Adresse.get() == '':
        Adresse.insert(0, 'Adresse')

def on_tree_select(event):
    global selected_chauffeur_id
    selected_item = tree_chauffeurs.selection()
    if not selected_item:
        return
    
    item = tree_chauffeurs.item(selected_item)
    selected_chauffeur_id, nom, tel_val, adresse, _ = item['values']
    
    chauffeur.delete(0, 'end')
    chauffeur.insert(0, nom)
    
    tel.delete(0, 'end')
    tel.insert(0, tel_val)
    
    Adresse.delete(0, 'end')
    Adresse.insert(0, adresse)
    
def delete_chauffeur():
    selected_item = tree_chauffeurs.selection() 
    if not selected_item:
        messagebox.showwarning("Sélectionnez un chauffeur", "Veuillez sélectionner un chauffeur à supprimer.")
        return

    item = tree_chauffeurs.item(selected_item)
    chauffeur_id = item['values'][0]  

    delete_query = "DELETE FROM chauffeur WHERE id = %s"
    cursor.execute(delete_query, (chauffeur_id,))
    connection.commit()

    tree_chauffeurs.delete(*tree_chauffeurs.get_children())
    treeChauffeurs() 




def update_chauffeur():
    selected_item = tree_chauffeurs.selection()
    if not selected_item:
        messagebox.showwarning("Sélectionnez un camion", "Veuillez sélectionner un camion à modifier.")
        return
    
    new_nom = chauffeur.get().strip()
    new_tel = tel.get().strip()
    new_adresse = Adresse.get().strip()
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    update_query = """UPDATE chauffeur SET Nom = %s, Tel = %s, Adresse = %s, DateAjoutChauffeur = %s WHERE id = %s"""
    cursor.execute(update_query, (new_nom, new_tel, new_adresse, current_date_time, selected_chauffeur_id))
    connection.commit()
    
    tree_chauffeurs.delete(*tree_chauffeurs.get_children())
    treeChauffeurs()



def GererChauffeur(w):
    global frame1, chauffeur, tel, Adresse  

    if 'frame1' in globals():
        frame1.destroy()

    frame1 = tk.Frame(w, width=800, height=700, bg='#262626')
    frame1.place(x=60, y=40)

    l1 = tk.Label(frame1, text="Gérer Chauffeur", fg='white', bg='#262626')
    l1.config(font=('Comic Sans MS', 25))
    l1.place(x=270, y=10)
    
    chauffeur = tk.Entry(frame1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    chauffeur.place(x=30, y=245)
    chauffeur.insert(0, 'Nom chauffeur')
    chauffeur.bind('<FocusIn>', on_entry1)
    chauffeur.bind('<FocusOut>', on_leave1)

    tel = tk.Entry(frame1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    tel.place(x=500, y=245)
    tel.insert(0, 'Telephone')
    tel.bind('<FocusIn>', on_entry2)
    tel.bind('<FocusOut>', on_leave2)

    Adresse = tk.Entry(frame1, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11, 'bold'))
    Adresse.place(x=270, y=290)
    Adresse.insert(0, 'Adresse')
    Adresse.bind('<FocusIn>', on_entry3)
    Adresse.bind('<FocusOut>', on_leave3)
    
    treeChauffeurs()

    tk.Button(frame1, width=39, pady=7, text='Modifier', bg='#3BD2C1', fg='white', border=0, command=update_chauffeur).place(x=240, y=340)
    tk.Button(frame1, width=39, pady=7, text='Supprimer', bg='#3BD2C1', fg='white', border=0,command=delete_chauffeur).place(x=240, y=390)
