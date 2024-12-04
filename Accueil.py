import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from PIL import *
from FunctionsAjoutChauffeur import *
from FunctionsAjoutCamion import *
from FunctionsSortieCamion import *
from FunctionsEntreeCamion import * 
from FunctionsIntervention import *
from FunctionsGererCamion import * 
from FunctionsGererChauffeur import * 

def get_camion_count():
    cursor.execute("SELECT COUNT(*) FROM camion WHERE Disponibilité = 1")
    available_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM camion")
    total_count = cursor.fetchone()[0]
    
    return f"{available_count}/{total_count}"

def get_chauffeur_count():
    cursor.execute("SELECT COUNT(*) FROM chauffeur WHERE Disponibilité = 1")
    available_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM chauffeur")
    total_count = cursor.fetchone()[0]
    
    return f"{available_count}/{total_count}"

def get_Intervention_count():
   
    cursor.execute("SELECT COUNT(*) FROM entréecamion WHERE Panne=1")
    total_count = cursor.fetchone()[0]
    
    return f"{total_count}"

def LogOut(w):
    w.destroy()

def toggle_win(w):
    global f1
    f1 = Frame(w, width=300, height=500, bg='#12c4c0')
    f1.place(x=0, y=0)

    def bttn(x, y, text, bcolor, fcolor, cmd, close_toggle=False):
        def on_entera(e):
            myButton1['background'] = bcolor
            myButton1['foreground'] = '#262626'
        def on_leavea(e):
            myButton1['background'] = fcolor 
            myButton1['foreground'] = '#262626' 

        myButton1 = Button(f1, text=text, width=42, height=2, fg='#262626', border=0, bg=fcolor, 
                           activeforeground='#262626', activebackground=bcolor,
                           command=lambda: handle_command(cmd, close_toggle))

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)
        myButton1.place(x=x, y=y)

    def handle_command(cmd, close_toggle):
        if close_toggle:
            f1.destroy()   
        cmd()  

    bttn(0, 80, 'Ajout Camion', '#0f9d9a', '#12c4c0', lambda: AjoutCamion(w), close_toggle=True)
    bttn(0, 117, 'Ajout Chauffeur', '#0f9d9a', '#12c4c0', lambda: AjoutChauffeur(w), close_toggle=True)
    bttn(0, 154, 'Sortie de camions', '#0f9d9a', '#12c4c0', lambda: SortieCamion(w), close_toggle=True)
    bttn(0, 191, 'Entrée de camions', '#0f9d9a', '#12c4c0', lambda: EntreCamion(w), close_toggle=True)
    bttn(0, 228, 'Service de réparation', '#0f9d9a', '#12c4c0', lambda: Intervention(w), close_toggle=True)
    bttn(0, 265, 'Gérer Camion', '#0f9d9a', '#12c4c0', lambda: GererCamion(w), close_toggle=True)
    bttn(0, 302, 'Gérer Chauffeur', '#0f9d9a', '#12c4c0', lambda: GererChauffeur(w), close_toggle=True)
    bttn(0, 339, 'Historique Interventions', '#0f9d9a', '#12c4c0', lambda: show_interventions(), close_toggle=True)  
    bttn(0, 377, 'Historique Trajet', '#0f9d9a', '#12c4c0', lambda: show_camion_details(), close_toggle=True)
    bttn(0, 463, 'Déconnexion', '#0f9d9a', '#12c4c0', lambda: LogOut(w))

    global img2
    img2 = PhotoImage(file='close.png')
    Button(f1, image=img2, border=0, command=f1.destroy, bg='#12c4c0', activebackground='#12c4c0').place(x=5, y=10)

def MainMenu():
    global w
    camion_count = get_camion_count()
    chauffeur_count = get_chauffeur_count ()
    intervention_count = get_Intervention_count()
   
    w = Tk()
    w.geometry('900x500')
    w.configure(bg='#262626')
    w.resizable(0, 0)
    w.title('Menara Holding')
    img = PhotoImage(file='icon.png')
    w.iconphoto(False, img)


    screen_width = w.winfo_screenwidth()
    screen_height = w.winfo_screenheight()
    center_x = int(screen_width / 2 - 900 / 2)
    center_y = int(screen_height / 2 - 500 / 2)
    w.geometry(f'{900}x{500}+{center_x}+{center_y}')
    
    global frame0
    frame0 = Frame(w, width=800, height=450, bg='#262626')
    frame0.place(x=60, y=40)
    
    l1 = Label(frame0, text="Gestion de Maintenance", fg='white', bg='#262626', font=('Comic Sans MS', 25))
    l1.place(x=235, y=0)

    Button(frame0, height=3, width=30, text=f'Nombre de Camions : {camion_count}',bg='#3BD2C1', fg='white', border=1, font=('Comic Sans MS', 15)).place(x=235, y=90)

    Button(frame0, height=3, width=30, text=f'Nombre de Chauffeurs : {chauffeur_count}',bg='#3BD2C1', fg='white', border=1, font=('Comic Sans MS', 15)).place(x=235, y=210)  

    Button(frame0, height=3, width=30, text=f'Nombre d\'Interventions : {intervention_count}',bg='#3BD2C1', fg='white', border=1, font=('Comic Sans MS', 15)).place(x=235, y=330)  

    global img1
    img1 = PhotoImage(file='open.png')
    Button(w,image=img1,command=lambda:toggle_win(w),border=0,bg='#262626',activebackground='#262626').place(x=5, y=10)
    
    w.mainloop()