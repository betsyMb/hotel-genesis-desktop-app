
from tkinter import ttk
from tkinter import *
from utils.generic import center_window
import pymysql
from tkcalendar import DateEntry

class Client():
    
    def __init__(self, window, close):
      self.wind = window
      self.wind.title("Clientes")
      self.close = close
      
      center_window(self.wind, 800, 500)
      
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
      frame = LabelFrame(self.wind, text='Nuevo Cliente')
      frame.grid(row=0, column=0, columnspan=3, pady=20)
      
      # Name Input
      Label(frame, text='Nombre: ').grid(row=1, column=0)
      self.name = Entry(frame)
      self.name.focus()
      self.name.grid(row=1, column=1)
      
      # LastName Input
      Label(frame, text='Apellido: ').grid(row=2, column=0)
      self.last_name = Entry(frame)
      self.last_name.grid(row=2, column=1)
      
      # DNO Input
      Label(frame, text='Cedula: ').grid(row=3, column=0)
      self.dni = Entry(frame)
      self.dni.grid(row=3, column=1)
      
      # Fecha de nacimiento Input
      Label(frame, text='Fecha de nacimiento: ').grid(row=4, column=0)
      self.birth_date = DateEntry(frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, year=2000)
      self.birth_date.grid(row=4, column=1)
      
      # Button Add Product
      ttk.Button(frame, text="Guardar cliente", command=self.add_client).grid(row=5, columnspan=2, sticky=W + E)
      
      # Output Messages
      self.message = Label(text='', fg='red')
      self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)
      
      # Table
      self.tree = ttk.Treeview(height=10, columns=('Nombre', 'Apellido', 'Cedula', 'Fecha de nacimiento'))
      self.tree.grid(row=4, column=0, columnspan=2)
      self.tree.heading("#0", text='Nombre', anchor=CENTER)
      self.tree.heading('#1', text='Apellido', anchor=CENTER)
      self.tree.heading('#2', text='Cedula', anchor=CENTER)
      self.tree.heading('#3', text='Fecha de Nacimiento', anchor=CENTER)
      
      # Action buttons (EDIT, DELETE)
      ttk.Button(text='DELETE', command=self.delete_client).grid(row=5, column=0, sticky=W+E)
      ttk.Button(text='EDIT', command=self.edit_client).grid(row=5, column=1, sticky=W+E)
      
      # Filling the rows
      self.get_clients()

    def create_table(self):
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    last_name VARCHAR(100),
                    dni VARCHAR(20) UNIQUE,
                    birth_date DATE
                )
            """)
            self.conn.commit()
        except pymysql.Error as e:
            print(e, "ERROR HERE")
            self.message['text'] = f"Error al crear la tabla: {e}"

    def run_query(self, query, parameters=()):
     cursor = self.conn.cursor()
     cursor.execute(query, parameters)
     self.conn.commit()
     return cursor

    

    def get_clients(self):
        # Limpiar tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Consultar datos
        query = 'SELECT * FROM clients ORDER BY name DESC'
        db_rows = self.run_query(query).fetchall()
        # Llenar datos
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[4]))

        
    def validation(self):
        return len(self.name.get()) != 0 and len(self.last_name.get()) != 0 and len(self.dni.get()) != 0 and len(self.birth_date.get()) != 0
    
    def format_form(self):
        self.name.delete(0, END)
        self.last_name.delete(0, END)
        self.birth_date.delete(0, END)
        self.dni.delete(0, END)
    
    def add_client(self):
        if self.validation():
            query = 'INSERT INTO clients (name, last_name, dni, birth_date) VALUES (%s, %s, %s, %s)'
            parameters = (self.name.get(), self.last_name.get(), self.dni.get(), self.birth_date.get_date())
            self.run_query(query, parameters)
            self.format_form()
            self.message['text'] = 'Cliente {} Agregado Correctamente.'.format(self.name.get())
            if self.close == True:
                self.wind.destroy()
        else:
            self.message['text'] = 'Todos los campos son requeridos.'
            
        self.get_clients()
        
    def delete_client(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][1]
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        dni = self.tree.item(self.tree.selection())['values'][1]
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM clients WHERE dni = %s'
        
        self.run_query(query, (dni))
        
        self.message['text'] = 'Usuario {} eliminado correctamente'.format(name)
        self.get_clients()
        
    def edit_client(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        print(self.tree.item(self.tree.selection()), "SELECTION")
        name = self.tree.item(self.tree.selection())['text']
        old_last_name = self.tree.item(self.tree.selection())['values'][0]
        old_dni = self.tree.item(self.tree.selection())['values'][1]
        old_birth_date = self.tree.item(self.tree.selection())['values'][2]
        
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Record'
        
        # Old Name
        Label(self.edit_wind, text='nombre anterior: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

        # New Name
        Label(self.edit_wind, text='Nuevo nombre: ').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)
        
        # Old Last Name
        Label(self.edit_wind, text='Apellido anterior: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_last_name), state='readonly').grid(row=2, column=2)
        
        # New LAst Name
        Label(self.edit_wind, text='Nuevo apellido: ').grid(row=3, column=1)
        new_last_name = Entry(self.edit_wind)
        new_last_name.grid(row=3, column=2)
        
        # Old DNI
        Label(self.edit_wind, text='Cedula anterior: ').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_dni), state='readonly').grid(row=4, column=2)
        
        # New DNI
        Label(self.edit_wind, text='Nueva Cedula: ').grid(row=5, column=1)
        new_dni = Entry(self.edit_wind)
        new_dni.grid(row=5, column=2)
        
        # # Old Birth date
        Label(self.edit_wind, text='Fecha de Nacimiento anterior: ').grid(row=6, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_birth_date), state='readonly').grid(row=6, column=2)
        
        # # New Bieth date
        Label(self.edit_wind, text='Nueva  fecha de nacimiento: ').grid(row=7, column=1)
        new_birth_date = DateEntry(self.edit_wind, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, year=2000)
        new_birth_date.grid(row=7, column=2)
        
        # Edit Button
        ttk.Button(self.edit_wind, text='Update', command=lambda: self.edit_record(new_name.get(), new_last_name.get(), new_dni.get(), new_birth_date, old_dni )).grid(row=8, column=2, sticky=W)
        
    def edit_record(self, new_name, new_last_name, new_dni, new_birth_date, dni):
        query = 'UPDATE clients SET name = %s, last_name = %s, dni = %s, birth_date = %s WHERE dni = %s'
        print(new_name, new_last_name, new_dni, new_birth_date.get_date(),dni)
        parameters = (new_name, new_last_name, new_dni, new_birth_date.get_date(),dni)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Cliente {} actualizado correctamente'.format(dni)
        self.get_clients()
        
def instantiateClient(wind):
    if wind:
        window = wind
        Client(window, close=True)
        window.mainloop()
    else:
        window = Tk()
        Client(window, close=False)
        window.mainloop()
        
    
        
