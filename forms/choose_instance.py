from tkinter import *
from tkinter.font import BOLD
import utils.generic as utils
from hotel.client import instantiateClient
from hotel.user import instantiateUser
from hotel.room import instantiateRoom
from hotel.entry_clients import instantiateEntryClient

class ChooseInstance():
    
    def choose_intance(self, instance):
        if instance == 'users':
            self.window.destroy()
            instantiateUser()
        elif instance == 'clients':
            instantiateClient()
        elif instance == 'rooms':
            instantiateRoom()
        else:
            instantiateEntryClient()

    def __init__(self, window):
        self.window = window
        self.window.title("Inicio")
        self.window.geometry("800x500")
        self.window.config(bg="#fcfcfc")
        self.window.resizable(width=0, height=0)
        
        utils.center_window(self.window, 800, 500)
        
        logo = utils.read_image("./images/Hermes.jpg", (200, 200))
        
        # Frame Logo
        frame_logo = Frame(self.window, bd=0, width=300, relief=SOLID, padx=10, pady=10, bg='#3a7ff6')
        frame_logo.pack(side='left', expand=NO, fill=BOTH)
        
        label = Label(frame_logo, image=logo, bg='#3a7ff6')
        label.place(x=0,y=0,relwidth=1, relheight=1)
        
        # Frame Form
        frame_form = Frame(self.window, bd=0, relief=SOLID)
        frame_form.pack(side='right', expand=YES, fill=BOTH)
        
        # Button
        usersButton = Button(frame_form, text='Usuarios', bg='gray', font=('Times', 15, BOLD), bd=0, command=lambda: self.choose_intance('users'))
        usersButton.pack(fill=X, padx=20, pady=20)
        
        clientsButton = Button(frame_form, text='Clientes', bg='gray', font=('Times', 15, BOLD), bd=0, command=lambda: self.choose_intance('clients'))
        clientsButton.pack(fill=X, padx=20, pady=20)
        
        roomsButton = Button(frame_form, text='Habitaciones', bg='gray', font=('Times', 15, BOLD), bd=0, command=lambda: self.choose_intance('clients'))
        roomsButton.pack(fill=X, padx=20, pady=20)
        
        # Entry clients
        entryClientsButton = Button(frame_form, text='Ingresar entrada a hotel', bg='gray', font=('Times', 15, BOLD), bd=0, command=lambda: self.choose_intance('hotel'))
        entryClientsButton.pack(fill=X, padx=20, pady=20)
        
        
def instantiateChooseInstance():
    window = Tk()
    ChooseInstance(window)
    window.mainloop()