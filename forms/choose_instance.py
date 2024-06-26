from tkinter import *
from tkinter.font import BOLD
import utils.generic as utils
from hotel.client import instantiateClient
from hotel.user import instantiateUser
from hotel.room import instantiateRoom
from hotel.entry_clients import instantiateEntryClient
from tkinter import messagebox

font = ('Comic Sans MS', 15)

class ChooseInstance():
    
    def choose_intance(self, instance):
        if instance == 'users':
            instantiateUser(role=self.role)
        elif instance == 'clients':
            instantiateClient(role=self.role)
        elif instance == 'rooms':
            instantiateRoom(role=self.role)
        else:
            instantiateEntryClient(role=self.role)

    def __init__(self, window, role):
        self.window = window
        self.role = role
        self.window.title("Inicio")
        self.window.geometry("800x500")
        self.window.config(bg="#fff")
        self.window.resizable(width=0, height=0)
        
        utils.center_window(self.window, 800, 500)
                
        # Frame Form
        frame_form = Frame(self.window, bd=0, relief=SOLID)
        frame_form.grid(row=0, column=0, rowspan=4, sticky=N+S+E+W)
        
        # Button
        usersButton = Button(frame_form, text='Usuarios', bg='#f59e0b', font=font, bd=0, command=lambda: self.choose_intance('users'))
        usersButton.grid(row=0, column=0, sticky=W+E, padx=20, pady=10)
        
        clientsButton = Button(frame_form, text='Clientes', bg='#f59e0b', font=font, bd=0, command=lambda: self.choose_intance('clients'))
        clientsButton.grid(row=1, column=0, sticky=W+E, padx=20, pady=10)
        
        roomsButton = Button(frame_form, text='Habitaciones', bg='#f59e0b', font=font, bd=0, command=lambda: self.choose_intance('rooms'))
        roomsButton.grid(row=2, column=0, sticky=W+E, padx=20, pady=10)
        
        if role < 3:
            entryClientsButton = Button(frame_form, text='Ingresar entrada a hotel', bg='#f59e0b', font=font, bd=0, command=lambda: self.choose_intance('hotel'))
            entryClientsButton.grid(row=3, column=0, sticky=W+E, padx=20, pady=10)
        
        # Configurar pesos para permitir expansión
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        # self.window.grid_columnconfigure(1, weight=1)
        frame_form.grid_rowconfigure(0, weight=1)
        frame_form.grid_rowconfigure(1, weight=1)
        frame_form.grid_rowconfigure(2, weight=1)
        frame_form.grid_rowconfigure(3, weight=1)
        frame_form.grid_columnconfigure(0, weight=1)

def instantiateChooseInstance(role):
    window = Tk()
    ChooseInstance(window, role)
    window.mainloop()
