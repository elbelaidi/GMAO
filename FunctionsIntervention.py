import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime



# Database connection
connection = mysql.connector.connect(host="localhost", user="root", password="", database="gmao")
cursor = connection.cursor()

def show_interventions():
    popup_window = tk.Toplevel()
    popup_window.title("Interventions")
    popup_window.geometry("800x400")


    # Entry for searching by Immatriculation
    search_label = tk.Label(popup_window, text="Search by Immatriculation:")
    search_label.pack(pady=10)

    search_entry = tk.Entry(popup_window, width=25)
    search_entry.pack(pady=5)

    def search_interventions():
        search_value = search_entry.get()
        query = """
        SELECT id, Immatriculation, TypeProb, Prob, DateDebutIntervention, DateFinIntervention 
        FROM intervention 
        WHERE Immatriculation LIKE %s
        """
        cursor.execute(query, ('%' + search_value + '%',)) 
        rows = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert('', tk.END, values=row)

    search_button = tk.Button(popup_window, text="Search", command=search_interventions)
    search_button.pack(pady=10)

    tree = ttk.Treeview(popup_window, columns=(1, 2, 3, 4, 5, 6), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading(1, text="ID")
    tree.heading(2, text="Immatriculation")
    tree.heading(3, text="TypeProb")
    tree.heading(4, text="Prob")
    tree.heading(5, text="Date Debut")
    tree.heading(6, text="Date Fin")

    tree.column(1, width=50)
    tree.column(2, width=150)
    tree.column(3, width=100)
    tree.column(4, width=100)
    tree.column(5, width=100)
    tree.column(6, width=100)

    query = "SELECT id, Immatriculation, TypeProb, Prob, DateDebutIntervention, DateFinIntervention FROM intervention"
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        tree.insert('', tk.END, values=row)

    scrollbar = ttk.Scrollbar(popup_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def treeCamion():
    global tree
    tree = ttk.Treeview(frame1, columns=(1, 2, 3, 4), height=5, show="headings")
    tree.place(x=100, y=90, width=590, height=120)

    tree.heading(1, text="ID", anchor="center")
    tree.heading(2, text="Chauffeur", anchor="center")
    tree.heading(3, text="Immatriculation", anchor="center")
    tree.heading(4, text="Date Entree", anchor="center")

    tree.column(1, width=50)
    tree.column(2, width=100)
    tree.column(3, width=100)
    tree.column(4, width=100)

    scroll1 = ttk.Scrollbar(tree, command=tree.yview)
    tree.configure(yscrollcommand=scroll1.set)
    scroll1.pack(side=tk.RIGHT, fill=tk.Y)

    req = "SELECT id, chauffeur, Immatriculation, DateEntree FROM entréecamion WHERE Panne = 1"
    cursor.execute(req)
    res = cursor.fetchall()

    for row in res:
        tree.insert('', tk.END, values=row)

def Intervention(w):
    global frame1, frame0
    global vidange_var, visite_var, mecanique_var, electrique_var, chaudronnerie_var, pneu_var, ampoule_var

    if 'frame1' in globals():
        frame1.destroy()

    frame1 = tk.Frame(w, width=800, height=700, bg='#262626')
    frame1.place(x=60, y=40)

    l1 = tk.Label(frame1, text="Service de réparation", fg='white', bg='#262626')
    l1.config(font=('Comic Sans MS', 25))
    l1.place(x=200, y=10)


    typeProb_var = tk.StringVar(value="Préventif")
    typeProb_combobox = ttk.Combobox(frame1, textvariable=typeProb_var, font="BahnschriftLight 13", width=20, state="readonly")
    typeProb_combobox['values'] = ["Préventif", "Panne", "Travaux neufs"]
    typeProb_combobox.place(x=300, y=230)

    # Initialize IntVar variables
    vidange_var = tk.IntVar()
    visite_var = tk.IntVar()
    mecanique_var = tk.IntVar()
    electrique_var = tk.IntVar()
    chaudronnerie_var = tk.IntVar()
    pneu_var = tk.IntVar()
    ampoule_var = tk.IntVar()

    def update_checkboxes(event=None):
        global frame0
        if 'frame0' in globals():
            frame0.destroy()

        frame0 = tk.Frame(frame1, width=780, height=100, bg='#262626')
        frame0.place(x=10, y=270)

        vidange_var.set(0)
        visite_var.set(0)
        mecanique_var.set(0)
        electrique_var.set(0)
        chaudronnerie_var.set(0)
        pneu_var.set(0)
        ampoule_var.set(0)

        selected_type = typeProb_var.get()
        if selected_type == "Préventif":
            tk.Checkbutton(frame0, text="Vidange", font="BahnschriftLight 13", bg="#3BD2C1", fg="white", width=20, height=2, variable=vidange_var).place(x=45, y=10)
            tk.Checkbutton(frame0, text="Visite technique", font="BahnschriftLight 13", bg="#3BD2C1", fg="white", width=20, height=2, variable=visite_var).place(x=515, y=10)
        elif selected_type == "Panne":
            tk.Checkbutton(frame0, text="Mécanique", font="BahnschriftLight 13", bg="#3BD2C1", fg="white", width=20, height=2, variable=mecanique_var).place(x=20, y=10)
            tk.Checkbutton(frame0, text="Electrique", font="BahnschriftLight 13", bg="#3BD2C1", fg="white", width=20, height=2, variable=electrique_var).place(x=290, y=10)
            tk.Checkbutton(frame0, text="Chaudronnerie", font="BahnschriftLight 13", bg="#3BD2C1", fg="white", width=20, height=2, variable=chaudronnerie_var).place(x=555, y=10)
        elif selected_type == "Travaux neufs":
            tk.Checkbutton(frame0, text="Changement Pneus", font="BahnschriftLight 13", bg="#3BD2C1", fg="white", width=20, height=2, variable=pneu_var).place(x=45, y=10)
            tk.Checkbutton(frame0, text="Changement Ampoules", font="BahnschriftLight 13", bg="#3BD2C1", fg="white", width=20, height=2, variable=ampoule_var).place(x=515, y=10)

    typeProb_combobox.bind("<<ComboboxSelected>>", update_checkboxes)
    update_checkboxes() 
    
    
    def display_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Veuillez sélectionner une entrée dans la liste.")
            return

        camion_info = tree.item(selected_item[0])['values']
        immatriculation = camion_info[2]
        typeProb = typeProb_var.get()
        problems = []

        if vidange_var.get(): problems.append("Vidange")
        if visite_var.get(): problems.append("Visite technique")
        if mecanique_var.get(): problems.append("Mécanique")
        if electrique_var.get(): problems.append("Electrique")
        if chaudronnerie_var.get(): problems.append("Chaudronnerie")
        if pneu_var.get(): problems.append("Changement Pneus")
        if ampoule_var.get(): problems.append("Changement Ampoules")
        messagebox.showinfo("Information", f"Immatriculation: {immatriculation}\nType de problème: {typeProb}\nProblèmes sélectionnés: {', '.join(problems)}")
        
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        sql = """UPDATE intervention SET TypeProb = %s, Prob = %s, DateFinIntervention = %s  WHERE Immatriculation = %s"""
        prob_string = ', '.join(problems) 
        data = (typeProb, prob_string, current_date_time, immatriculation)

        cursor.execute(sql, data)
        connection.commit()
        
        #Update Camion
        req = "UPDATE camion SET Disponibilité = %s WHERE Immatriculation = %s"
        valeur = ("1",immatriculation)
        cursor.execute(req, valeur)
        connection.commit()
        
        #Update entréecamion
        req = "UPDATE entréecamion SET Panne = %s WHERE Immatriculation = %s"
        valeur = ("0",immatriculation)
        cursor.execute(req, valeur)
        connection.commit()
        treeCamion()

    tk.Button(frame1, width=39, pady=7, text='Valider', bg='#3BD2C1', fg='white', border=0, command=display_selected).place(x=240, y=385)
    treeCamion()    

    
    
    
    
    

