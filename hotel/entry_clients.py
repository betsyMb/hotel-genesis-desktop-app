from tkinter import ttk
from tkinter import *
from utils.generic import center_window
from tkcalendar import DateEntry
from datetime import datetime
from hotel.client import instantiateClient
import pymysql

class EntryClient:    
    
    def get_current_time(self):
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_selected_date(self):
        selected_date = self.date.get()
        if not selected_date:
            self.date = self.get_current_time()
            
    def check_client_exists(self, dni):
      query = "SELECT * FROM clients WHERE dni = %s"
      result = self.run_query(query, (dni,))
      print(result, "RESULT")
      self.clients_ids(result.lastrowid)
      return result.fetchone()
  
    def open_client_form(self):
         new_window = Toplevel(self.wind)
         instantiateClient(new_window)
            
    def add_dni_input(self):
        self.dni_row += 1
        # Label(self.frame, text='Cedula NOJODAAA: ').grid(row=self.dni_row, column=0)
        # self.cedula_entry = Entry(self.frame)
        # self.cedula_entry.grid(row=self.dni_row, column=1)
        if self.cedula_entry.get() != '':
            self.client_dnies.append(self.cedula_entry.get())
        # Update the Add Cliente button's position
        self.add_dni_button.grid(row=self.dni_row, column=2, pady=5)
        def validate_and_check_dni(event):
            dni = self.cedula_entry.get()
            if dni:
                client = self.check_client_exists(dni)
                if not client:
                    self.open_client_form()
                else:
                    self.message.config(text=f'Cliente con DNI {dni} encontrado.', fg='green')
        
        self.cedula_entry.bind('<FocusOut>', validate_and_check_dni)
    
    def __init__(self, window):
        self.wind = window
        self.wind.title("Entrada de Clientes")
        self.client_dnies = []
        self.current_date = datetime.now()
        center_window(self.wind, 800, 500)
        
        # Connecting to the DB
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="hoteldb"
        )  
        # Crear cursor
        self.cur = self.conn.cursor()  
        # Crear tabla si no existe
        self.create_table()   
        
        # Creating a Frame Container
        self.frame = LabelFrame(self.wind, text='Nueva entrada')
        self.frame.grid(row=0, column=0, columnspan=3, pady=20)
        
        self.dni_row = 3

        Label(self.frame, text='Cedula: ').grid(row=self.dni_row, column=0)
        self.cedula_entry = Entry(self.frame)
        self.cedula_entry.grid(row=self.dni_row, column=1)
        # Button to add more DNI inputs
        self.add_dni_button = Button(self.frame, text="Agregar Cliente", command=self.add_dni_input)
        self.add_dni_button.grid(row=self.dni_row, column=2, pady=5)
        
        self.add_dni_input()

        # Habitacion
        Label(self.frame, text='Nro de habitacion: ').grid(row=self.dni_row + 4, column=0)
        self.room_number = Entry(self.frame)
        self.room_number.grid(row=self.dni_row + 4, column=1)
        
       # Time  
        Label(self.frame, text='Hora: ').grid(row=self.dni_row + 5, column=0)
        self.date = DateEntry(self.frame, width=12, background='darkblue',
                                      foreground='white', 
                                      borderwidth=2, 
                                      year=self.current_date.year,
                                      month=self.current_date.month,
                                      day=self.current_date.day,
                                      date_pattern='y-mm-dd'
                                      )
        self.date.grid(row=self.dni_row + 5, column=1)
              
        # Button Add Entry
        ttk.Button(self.frame, text="Guardar entrada", command=self.add_entry_client).grid(row=self.dni_row + 6, columnspan=2, sticky=W + E)
        
        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=self.dni_row + 3, column=0, columnspan=3, sticky=W+E)
        
        # Table
        self.tree = ttk.Treeview(height=10, columns=("cedula", "nombre", "habitacion", "hora"))
        self.tree.grid(row=self.dni_row + 4, column=0, columnspan=3)
        
        # Define los encabezados de las columnas
        self.tree.heading("#0", text='Cedula', anchor=CENTER)
        self.tree.heading('#1', text='Entrada', anchor=CENTER)
        self.tree.heading('#2', text='Habitacion', anchor=CENTER)
        self.tree.heading('#3', text='Hora', anchor=CENTER)  
        # Define las columnas para ajustar el ancho y la alineación
        self.tree.column("#0", width=100, anchor=CENTER)
        self.tree.column("#1", width=100, anchor=CENTER)
        self.tree.column("#2", width=100, anchor=CENTER)
        self.tree.column("#3", width=100, anchor=CENTER)
        
        # Action buttons (EDIT, DELETE)
        ttk.Button(text='DELETE').grid(row=10, column=0, sticky=W+E)
        ttk.Button(text='EDIT').grid(row=10, column=1, sticky=W+E)
                
        # Filling the rows
        self.get_entries()

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
    
    def create_table(self):
        try:
            # Creating ENTRIES table
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    room_id INT,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (room_id) REFERENCES rooms(id)
                )
            """)
            self.conn.commit()
            
            # Creating ENTRIES_CLIENTS table
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS entry_clients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    client_id INT,
                    entry_id INT,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients(id),
                    FOREIGN KEY (entry_id) REFERENCES entries(id)
                )
            """)
            self.conn.commit()
   
        except pymysql.Error as e:
            self.message['text'] = f"Error al crear la tabla: {e}"


    def get_entries(self):
        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Querying data
        query = 'SELECT * FROM entry_clients ORDER BY name DESC'
        db_rows = self.run_query(query)
        # Filling data
        for row in db_rows:
            print(row, "ROW")
            self.tree.insert('', 0, text=row[1], values=row[2])    
        
    def validation(self):
        return len(self.room_number.get()) != 0
    
    def formatForm(self):
        self.name.delete(0, END)
        self.last_name.delete(0, END)
    
    def add_entry_client(self):
        if self.validation():
            query_entry = 'INSERT INTO entries (room_id, time) VALUES(%s, %s)'
            entry_params = (self.room_number.get(), self.date.get_date())
            entry_id = self.run_query(query_entry, entry_params).lastrowid
            
            query_entry_client = 'INSERT INTO entry_clients (client_id, entry_id, time) VALUES (%s, %s, %s)'
            # Mapping clients to insert them into the entry and entry_clients tables
            for client_id in self.client_dnies:
                self.run_query(query_entry_client, (1, entry_id, self.date.get_date()))

            self.formatForm()
            self.message['text']='Entrada de cliente {} Agregada Correctamente'.format(self.cedula_entry.get())
        else:
            self.message['text']='Todos los campos son requeridos'
            
        self.get_products()
        
    def delete_entry(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM entry_clients WHERE name = ?'
        
        self.run_query(query, (name, ))
        
        self.message['text'] = 'Record {} deleted successfully'.format(name)
        self.get_products()
        
    def edit_entry(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Record'
        
        # Old Name
        Label(self.edit_wind, text='Old Name: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

        # New Name
        Label(self.edit_wind, text='New Name: ').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)
        
        # Old Price
        Label(self.edit_wind, text='Old Price: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)
        
        # New Price
        Label(self.edit_wind, text='New Price: ').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)
        
        # Edit Button
        ttk.Button(self.edit_wind, text='Update', command=lambda: self.edit_record(new_name, name, new_price, old_price)).grid(row=4, column=2, sticky=W)
        
    def edit_record(self, new_name, name, new_price, price):
        query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Product {} updated successfully'.format(name)
        self.get_products()
        
def instantiateEntryClient():
    window = Tk()
    EntryClient(window)
    window.mainloop()
