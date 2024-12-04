import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning
import mysql.connector
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import datetime
import tkinter as tk


Immatriculation = None
Km = None


# Database
connection = mysql.connector.connect(host="localhost", user="root", password="", database="gmao")
cursor = connection.cursor()

def fill_Immatriculation(tree):
    selected_item = tree.focus()
    values = tree.item(selected_item, 'values')
    if values:
        Immatriculation.delete(0, 'end')
        Immatriculation.insert(0, values[2]) 
        global selected_id  
        selected_id = values[0]


def show_camion_details():
    popup_window = tk.Toplevel()
    popup_window.title("Détails Trajets")
    popup_window.geometry("800x400")

    label_chauffeur = tk.Label(popup_window, text="Chauffeur:")
    label_chauffeur.pack(pady=5)
    entry_chauffeur = tk.Entry(popup_window)
    entry_chauffeur.pack(pady=5)

    label_immat = tk.Label(popup_window, text="Immatriculation:")
    label_immat.pack(pady=5)
    entry_immat = tk.Entry(popup_window)
    entry_immat.pack(pady=5)

    def filter_trajets():
        chauffeur_filter = entry_chauffeur.get()
        immatriculation_filter = entry_immat.get()

        query = """
            SELECT s.id, s.Chauffeur, s.Immatriculation, e.Kilométrage, 
                s.DateSortie, e.DateEntree 
            FROM sortiecamion s 
            LEFT JOIN entréecamion e ON s.id = e.id
            WHERE (%s = '' OR s.Chauffeur LIKE %s)
            AND (%s = '' OR s.Immatriculation LIKE %s)
        """
        
        cursor.execute(query, (chauffeur_filter, '%' + chauffeur_filter + '%', 
                                immatriculation_filter, '%' + immatriculation_filter + '%'))
        rows = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert('', tk.END, values=row)

    filter_button = tk.Button(popup_window, text="Filter", command=filter_trajets)
    filter_button.pack(pady=10)

    tree = ttk.Treeview(popup_window, columns=(1, 2, 3, 4, 5, 6), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading(1, text="ID")
    tree.heading(2, text="Chauffeur")
    tree.heading(3, text="Immatriculation")
    tree.heading(4, text="Kilométrage")
    tree.heading(5, text="Date Sortie")
    tree.heading(6, text="Date Entree")

    tree.column(1, width=100)
    tree.column(2, width=100)
    tree.column(3, width=100)
    tree.column(4, width=100)
    tree.column(5, width=100)
    tree.column(6, width=100)

    filter_trajets()  

    scrollbar = ttk.Scrollbar(popup_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)




#Km
def on_entry2(e):
    Km.delete(0, 'end')

def on_leave2(e):
    if Km.get() == '':
        Km.insert(0, 'kilométrage')
        
#Immatriculation
def on_entry1(e):
    Immatriculation.delete(0, 'end')

def on_leave1(e):
    if Immatriculation.get() == '':
        Immatriculation.insert(0, 'Immatriculation')

#Update BDD      
def SignalerProb():
    
    global selected_id
    #recuperer Nom chauffeur
    req = "Select Chauffeur from sortiecamion where Immatriculation = %s "
    valeur =(Immatriculation.get(),)
    cursor.execute(req,valeur)
    res = cursor.fetchall()
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    #Ajout
    x = "INSERT INTO entréecamion (id,chauffeur,Immatriculation,Disponibilité,kilométrage,DateEntree,Panne) values (%s,%s,%s,%s,%s,%s,%s)"
    val = (selected_id,res[0][0], Immatriculation.get(),'1',Km.get(),current_date_time,True)
    cursor.execute(x, val)
    connection.commit()
    
    y = "INSERT INTO intervention (Immatriculation,DateDebutIntervention) VALUES (%s, %s)"
    z = (Immatriculation.get(),current_date_time)
    cursor.execute(y, z)
    connection.commit()


    #Update disponibilité chauffeur
    req = "UPDATE chauffeur SET Disponibilité = %s WHERE Nom = %s"
    valeur = ("1",res[0][0])
    cursor.execute(req, valeur)
    connection.commit()
    #Update disponibilité camion
    req = "UPDATE camion SET Disponibilité = %s WHERE Immatriculation = %s"
    valeur = ("0",Immatriculation.get())
    cursor.execute(req, valeur)
    connection.commit()

    #Update disponibilité SortieCamion
    req = "UPDATE sortiecamion SET Disponibilité = %s WHERE Immatriculation = %s"
    valeur = ("0", Immatriculation.get())
    cursor.execute(req, valeur)
    connection.commit()


    Immatriculation.delete(0, 'end')
    Immatriculation.insert(0, 'Immatriculation camion ')
    Km.delete(0, 'end')
    Km.insert(0, 'kilométrage')
    treeEntreeC()
    messagebox.showinfo("Information !", "Ajouté avec succes")
        
#Ajout BDD
def EntreeCamionBDD():

    global selected_id
    #recuperer Nom chauffeur
    req = "Select Chauffeur from sortiecamion where Immatriculation = %s "
    valeur =(Immatriculation.get(),)
    cursor.execute(req,valeur)
    res = cursor.fetchall()
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    #Ajout
    x = "INSERT INTO entréecamion (id,chauffeur,Immatriculation,Disponibilité,kilométrage,DateEntree,Panne) values (%s,%s,%s,%s,%s,%s,%s)"
    val = (selected_id , res[0][0], Immatriculation.get(),'1',Km.get(),current_date_time,False)
    cursor.execute(x, val)
    connection.commit()
    #Update disponibilité chauffeur
    req = "UPDATE chauffeur SET Disponibilité = %s WHERE Nom = %s"
    valeur = ("1",res[0][0])
    cursor.execute(req, valeur)
    connection.commit()
    #Update disponibilité camion
    req = "UPDATE camion SET Disponibilité = %s WHERE Immatriculation = %s"
    valeur = ("1",Immatriculation.get())
    cursor.execute(req, valeur)
    connection.commit()

    #Update disponibilité SortieCamion
    req = "UPDATE sortiecamion SET Disponibilité = %s WHERE Immatriculation = %s"
    valeur = ("0", Immatriculation.get())
    cursor.execute(req, valeur)
    connection.commit()


    Immatriculation.delete(0, 'end')
    Immatriculation.insert(0, 'Immatriculation camion ')
    Km.delete(0, 'end')
    Km.insert(0, 'kilométrage')
    treeEntreeC()
    messagebox.showinfo("Information !", "Ajouté avec succes")
                
                
#tree view
def treeEntreeC():
    treeEntrée = ttk.Treeview(frame4, columns=(1, 2, 3, 4), height=5, show="headings")
    treeEntrée.place(x=100, y=110, width=590, height=70)
    treeEntrée.heading(1, text="Id", anchor="center")
    treeEntrée.heading(2, text="Nom chauffeur", anchor="center")
    treeEntrée.heading(3, text="Immatriculation", anchor="center")
    treeEntrée.heading(4, text="Date de sortie", anchor="center")
    treeEntrée.column(1, width=80)
    treeEntrée.column(2, width=170)
    treeEntrée.column(3, width=170)
    treeEntrée.column(4, width=170)

    scroll1 = ttk.Scrollbar(treeEntrée, command=treeEntrée.yview)
    treeEntrée.configure(yscrollcommand=scroll1.set)
    scroll1.pack(side=RIGHT, fill=Y)
    treeEntrée.bind('<<TreeviewSelect>>', lambda event: fill_Immatriculation(treeEntrée))




    req = "select Id,Chauffeur,Immatriculation,DateSortie from sortiecamion where Disponibilité = 1 "
    cursor.execute(req)
    res = cursor.fetchall()
    for row in res:
        treeEntrée.insert('', END, values=row)



#Entrée camion
def EntreCamion(w) :
    
    global Immatriculation , Km
        
    if 'f1' in globals():
        f1.destroy()


    global frame4
    frame4 = Frame(w, width=800, height=450, bg='#262626')
    frame4.place(x=60, y=40)

    l1 = Label(frame4, text="Entrée de camion", fg='white', bg='#262626')
    l1.config(font=('Comic Sans MS', 25))
    l1.place(x=270, y=30)


    Immatriculation = Entry(frame4, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11, 'bold'))
    Immatriculation.place(x=40, y=250)
    Immatriculation.insert(0, 'Immatriculation')
    Immatriculation.bind('<FocusIn>', on_entry1)
    Immatriculation.bind('<FocusOut>', on_leave1)


    Km = Entry(frame4, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11, 'bold'))
    Km.place(x=510, y=250)
    Km.insert(0, 'kilométrage')
    Km.bind('<FocusIn>', on_entry2)
    Km.bind('<FocusOut>', on_leave2)

    Button(frame4, width=39, pady=7, text='Valider', bg='#3BD2C1', fg='white', border=0,command=EntreeCamionBDD).place(x=240, y=330)
    Button(frame4, width=39, pady=7, text='Signaler un problème', bg='#3BD2C1', fg='white', border=0,command=SignalerProb).place(x=240, y=380)

    treeEntreeC()
