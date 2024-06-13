from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import utils.generic as utils
from forms.choose_instance import instantiateChooseInstance

font = ('Times', 14)

class App:
    
    def validate(self):
        user = self.username.get()
        password = self.password.get()
        if user == 'root' and password == 'root':
            self.window.destroy()
            instantiateChooseInstance()
        else:
            messagebox.showerror(message='Usuario o contraseña incorrectos', title='Error')
    
    def __init__(self):
        self.window = Tk()
        self.window.title("Inicio de sesion")
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
        
        # Frame Form Top
        frame_form_top = Frame(frame_form, height=50, bd=0, relief=SOLID, bg='black')
        frame_form_top.pack(side='top', fill=X)
        title = Label(frame_form_top, text='Inicio de sesion', font=('Times', 30), fg='#fff', pady=50)
        title.pack(expand=YES, fill=BOTH)
        
        # Frame Form Inputs
        frame_form_fill = Frame(frame_form, height=50, bd=0, relief=SOLID)
        frame_form_fill.pack(side='bottom', expand=YES, fill=BOTH)
        
        user_label = Label(frame_form_fill, text="Usuario", font=font, fg='#fff', anchor=W)
        user_label.pack(fill=X, padx=20, pady=5)
        self.username = Entry(frame_form_fill, font=font, bd=0, )
        self.username.pack(fill=X, padx=20, pady=10)
        
        password_label = Label(frame_form_fill, text='Contraseña', font=font, fg='#fff', anchor=W)
        password_label.pack(fill=X, padx=20, pady=5)
        self.password = Entry(frame_form_fill, font=font, bd=0,)
        self.password.pack(fill=X, padx=20, pady=10)
        self.password.config(show="*")
        
        # Button
        loginButton = Button(frame_form_fill, text='Iniciar sesion', bg='red', font=('Times', 15, BOLD), bd=0, command=self.validate)
        loginButton.pack(fill=X, padx=20, pady=20)
        
        self.window.mainloop()