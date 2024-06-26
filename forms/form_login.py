from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import utils.generic as utils
from forms.choose_instance import instantiateChooseInstance
from hotel.user import instantiateUser
import pymysql

font = ('Comic Sans MS', 14)

class App:
    
    def run_query(self, query, parameters=()):
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="hoteldb"
        )  
        cursor = conn.cursor()  
        cursor.execute(query, parameters)
        conn.commit()
        return cursor
    
    def validate(self):
        user = self.username.get()
        password = self.password.get()
        try:
            query_all_users = "SELECT * FROM users"
            all_users = self.run_query(query_all_users, ())
            users_list = all_users.fetchall()
            if len(users_list) == 0:
                new_window = Toplevel(self.window)
                instantiateUser(1, new_window)
                return
            query = "SELECT * from users WHERE dni = %s"
            result = self.run_query(query, (user))
            resultUser = result.fetchone()
            if resultUser != None and password == resultUser[4]:
                role = resultUser[5]
                self.window.destroy()
                instantiateChooseInstance(role)
            else:
                messagebox.showerror(message='Usuario o contraseña incorrectos', title='Error')
        except pymysql.Error as e :
            self.create_table()
            messagebox.showerror(message='Hubo un error, intente de nuevo', title='Error')
            return
    
    def __init__(self):
        self.window = Tk()
        self.window.title("Inicio de sesion")
        self.window.geometry("800x500")
        self.window.config(bg="#f59e0b")
        self.window.resizable(width=0, height=0)
    
        utils.center_window(self.window, 800, 500)
        
        logo = utils.read_image("./images/logo.png", (200, 200))
        
        # Frame Logo
        frame_logo = Frame(self.window, bd=0, width=300, relief=SOLID, padx=10, pady=10, bg='#f59e0b')
        frame_logo.pack(side='left', expand=NO, fill=BOTH)
        
        label = Label(frame_logo, image=logo, bg='#f59e0b')
        label.place(x=0,y=0,relwidth=1, relheight=1)
        
        # Frame Form
        frame_form = Frame(self.window, bd=0, relief=SOLID)
        frame_form.pack(side='right', expand=YES, fill=BOTH)
        
        # Frame Form Top
        frame_form_top = Frame(frame_form, height=50, bd=0, relief=SOLID, bg='black')
        frame_form_top.pack(side='top', fill=X)
        title = Label(frame_form_top, text='Inicio de sesion', font=('Comic Sans MS', 30), fg='#000', pady=50)
        title.pack(expand=YES, fill=BOTH)
        
        # Frame Form Inputs
        frame_form_fill = Frame(frame_form, height=50, bd=0, relief=SOLID)
        frame_form_fill.pack(side='bottom', expand=YES, fill=BOTH)
        
        user_label = Label(frame_form_fill, text="Usuario", font=font, fg='#000', anchor=W)
        user_label.pack(fill=X, padx=20, pady=5)
        self.username = Entry(frame_form_fill, font=font, bd=0, )
        self.username.pack(fill=X, padx=20, pady=10)
        
        password_label = Label(frame_form_fill, text='Contraseña', font=font, fg='#000', anchor=W)
        password_label.pack(fill=X, padx=20, pady=5)
        self.password = Entry(frame_form_fill, font=font, bd=0,)
        self.password.pack(fill=X, padx=20, pady=10)
        self.password.config(show="*")
        
        # Button
        loginButton = Button(frame_form_fill, text='Iniciar sesion', bg='#f59e0b', font=('Times', 15, BOLD), bd=0, command=self.validate)
        loginButton.pack(fill=X, padx=20, pady=20)
        
        self.window.mainloop()
    
    def create_table(self):
        try:
          self.conn = pymysql.connect(
          host="localhost",
          user="root",
          password="root",
          database="hoteldb"
          )
          self.cur = self.conn.cursor()
          self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    last_name VARCHAR(100),
                    dni VARCHAR(20) UNIQUE,
                    password VARCHAR(20),
                    role INT CHECK (role IN (1, 2, 3)),
                    birth_date DATE
                )
            """)
          self.conn.commit()
        except pymysql.Error as e:
            self.message['text'] = f"Error al crear la tabla: {e}"