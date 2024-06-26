
from tkinter import ttk
from tkinter import *
from utils.generic import center_window
import pymysql
from tkcalendar import DateEntry

font = ('Comic Sans MS', 14)
mainColor = "#f59e0b"
class User:
    def convert_role_to_number(self, role):
        if role == "Admin":
            return 1
        elif role == "Administrador":
            return 2
        else:
            return 3
        
    def conver_role_to_string(self, role):
        if role == 1:
            return "Admin"
        elif role == 2:
            return "Administrador"
        else:
            return "Usuario"
        
    def __init__(self, window, role, close):
      self.wind = window
      self.role = role
      self.wind.title("Usuarios")
      self.close = close
      center_window(self.wind, 1200, 700)
      
      # Conection to the database
      self.conn = pymysql.connect(
          host="localhost",
          user="root",
          password="root",
          database="hoteldb"
      )
      self.cur = self.conn.cursor()
      self.create_table()
      
      # Creating a Frame Container
      frame = LabelFrame(self.wind, padx=20, pady=20)
      if role != 3:
        frame = LabelFrame(self.wind, text='Nuevo Usuario', padx=20, pady=20)
      else:
        frame = LabelFrame(self.wind, text='Usuarios', padx=20, pady=20)
          
      frame.grid(row=0, column=0, columnspan=3, pady=20)
      if role != 3:
      # Name Input
        Label(frame, text='Nombre: ', font=font).grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
        
        # LastName Input
        Label(frame, text='Apellido: ', font=font).grid(row=2, column=0)
        self.last_name = Entry(frame)
        self.last_name.grid(row=2, column=1)
        
        # DNO Input
        Label(frame, text='Cedula: ', font=font).grid(row=3, column=0)
        self.dni = Entry(frame)
        self.dni.grid(row=3, column=1)
        
        # Password Input
        Label(frame, text='Password: ', font=font).grid(row=4, column=0)
        self.password = Entry(frame)
        self.password.grid(row=4, column=1)
        
        
        # Role
        Label(frame, text='Rol: ', font=font).grid(row=5, column=0)
        self.role = ttk.Combobox(frame, values=[], state='readonly', font=('Comic Sans MS', 10))
        if role == 1:
            self.role = ttk.Combobox(frame, values=["Admin", "Administrador", "Usuario"], state='readonly', font=('Comic Sans MS', 10))
        elif role == 2:
            self.role = ttk.Combobox(frame, values=["Administrador", "Usuario"], state='readonly', font=('Comic Sans MS', 10))
        self.role.grid(row=5, column=1)
        self.role.set("Usuario")
        
        # Fecha de nacimiento Input
        Label(frame, text='Fecha de nacimiento: ', font=font).grid(row=6, column=0)
        self.birth_date = DateEntry(frame, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, year=2000)
        self.birth_date.grid(row=6, column=1)
        
        # Button Add Product
        Button(frame, text="Guardar Usuario", command=self.add_user, height=1, font=font).grid(row=7, columnspan=2, sticky=W + E)
      
      # Output Messages
      self.message = Label(self.wind, text='', fg='red')
      self.message.grid(row=8, column=0, columnspan=2, sticky=W+E)
      
      # Table
      style = ttk.Style()
      style.configure("Treeview.Heading", font=font)  # Fuente para encabezados
      style.configure("Treeview", font=('Comic Sans MS', 10)) 
       
      self.tree = ttk.Treeview(frame, height=10, columns=('Nombre', 'Apellido', 'Cedula', 'Rol' , 'Fecha de nacimiento'))
      if role == 3:
        self.tree.grid(row=1, column=0, columnspan=2)
      else:
        self.tree.grid(row=8, column=0, columnspan=2)
      
      self.tree.heading("#0", text='Nombre', anchor='w')
      self.tree.heading('#1', text='Apellido', anchor='w')
      self.tree.heading('#2', text='Cedula', anchor='w')
      self.tree.heading('#3', text='Rol', anchor='w')
      self.tree.heading('#4', text='Fecha de Nacimiento', anchor='w')
      
      # Action buttons (EDIT, DELETE)
      if role == 1: 
        Button(self.wind, text='DELETE', font=font, height=1, command=self.delete_user ).grid(row=5, column=0, sticky=W+E)
      if role < 3:
        Button(self.wind, text='EDIT', font=font, height=1, command=self.edit_user).grid(row=5, column=1, sticky=W+E)
      
      # Filling the rows
      self.get_users()

    def create_table(self):
        try:
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

    def run_query(self, query, parameters=()):
     cursor = self.conn.cursor()
     cursor.execute(query, parameters)
     self.conn.commit()
     return cursor

    

    def get_users(self):
        # Limpiar tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Consultar datos
        query = 'SELECT * FROM users ORDER BY name DESC'
        db_rows = self.run_query(query).fetchall()
        # Llenar datos
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], self.conver_role_to_string(row[5]), row[6]))

        
    def validation(self):
        return len(self.name.get()) != 0 and len(self.last_name.get()) != 0 and len(self.dni.get()) != 0 and len(self.birth_date.get()) != 0 and len(self.role.get()) != 0
    
    def format_form(self):
        self.name.delete(0, END)
        self.last_name.delete(0, END)
        self.birth_date.delete(0, END)
        self.password.delete(0, END)
        self.role.delete(0, END)
        self.dni.delete(0, END)
    
    def add_user(self):
        if self.validation():
            query = 'INSERT INTO users (name, last_name, dni, password, role, birth_date) VALUES (%s, %s, %s, %s, %s, %s)'
            parameters = (self.name.get(), self.last_name.get(), self.dni.get(), self.password.get(), self.convert_role_to_number(self.role.get()), self.birth_date.get_date())
            self.run_query(query, parameters)
            self.format_form()
            self.message['text'] = 'Usuario {} Agregado Correctamente.'.format(self.name.get())
            if self.close == True:
                self.wind.destroy()
        else:
            self.message['text'] = 'Todos los campos son requeridos.'
            
        self.get_users()
        
    def delete_user(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][1]
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.message['text'] = 'Seleccione una fila'
            return
        self.message['text'] = ''
        dni = self.tree.item(self.tree.selection())['values'][1]
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM users WHERE dni = %s'
        
        self.run_query(query, (dni))
        
        self.message['text'] = 'Usuario {} eliminado correctamente'.format(name)
        self.get_users()
        
    def edit_user(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        old_last_name = self.tree.item(self.tree.selection())['values'][0]
        old_dni = self.tree.item(self.tree.selection())['values'][1]
        old_role = self.tree.item(self.tree.selection())['values'][2]
        old_birth_date = self.tree.item(self.tree.selection())['values'][3]
        
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Record'
        
        # Old Name
        Label(self.edit_wind, text='nombre anterior: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

        # New Name
        Label(self.edit_wind, text='Nuevo nombre: ').grid(row=1, column=1)
        new_name = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=name))
        new_name.grid(row=1, column=2)
        
        # Old Last Name
        Label(self.edit_wind, text='Apellido anterior: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_last_name), state='readonly').grid(row=2, column=2)
        
        # New LAst Name
        Label(self.edit_wind, text='Nuevo apellido: ').grid(row=3, column=1)
        new_last_name = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_last_name))
        new_last_name.grid(row=3, column=2)
        
        # Old DNI
        Label(self.edit_wind, text='Cedula anterior: ').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_dni), state='readonly').grid(row=4, column=2)
        
        # New DNI
        Label(self.edit_wind, text='Nueva Cedula: ').grid(row=5, column=1)
        new_dni = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_dni))
        new_dni.grid(row=5, column=2)
     
        # Old Rol
        Label(self.edit_wind, text='Rol anterior: ').grid(row=6, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_role), state='readonly').grid(row=6, column=2)

        # New Rol
        Label(self.edit_wind, text='Nueva Rol: ').grid(row=7, column=1)
        new_role = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_role))
        new_role = ttk.Combobox(self.edit_wind, values=["Admin", "Administrador", "Usuario"],  state='readonly')
        new_role.set("Usuario")
        new_role.grid(row=7, column=2)
        
        # # Old Birth date
        Label(self.edit_wind, text='Fecha de Nacimiento anterior: ').grid(row=8, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_birth_date), state='readonly').grid(row=8, column=2)
        
        # # New Bieth date
        Label(self.edit_wind, text='Nueva  fecha de nacimiento: ').grid(row=9, column=1)
        new_birth_date = DateEntry(self.edit_wind, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, year=2000)
        new_birth_date.grid(row=9, column=2)
        
        # Edit Button
        ttk.Button(self.edit_wind, text='Update', command=lambda: self.edit_record(new_name.get(), new_last_name.get(), new_dni.get(), new_role.get() , new_birth_date, old_dni )).grid(row=10, column=2, sticky=W)
        
    def edit_record(self, new_name, new_last_name, new_dni, new_role, new_birth_date, dni):
        query = 'UPDATE users SET name = %s, last_name = %s, dni = %s, role = %s, birth_date = %s WHERE dni = %s'
        parameters = (new_name, new_last_name, new_dni, self.convert_role_to_number(new_role) , new_birth_date.get_date(), dni)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Usuario {} actualizado correctamente'.format(dni)
        self.get_users()
        
def instantiateUser(role, wind = False):
    if wind:
        window = wind
        User(window, role, close=True)
        window.mainloop()
    else:
        window = Tk()
        User(window, role, close=False)
        window.mainloop()
    
        
