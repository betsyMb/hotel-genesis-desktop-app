from tkinter import ttk
from tkinter import *
from utils.generic import center_window
from tkcalendar import DateEntry
from datetime import datetime
from hotel.client import instantiateClient
from hotel.room import instantiateRoom
import pymysql

font = ('Comic Sans MS', 14)
mainColor = "#f59e0b"

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
      row = result.fetchone()
      if(row != None):
        self.clients_ids.append(row[0])
      
      return row
  
    def open_client_form(self):
         new_window = Toplevel(self.wind)
         instantiateClient(new_window)
    
    def open_room_form(self):
        new_window = Toplevel(self.wind)
        instantiateRoom(new_window)
            
    def add_dni_input(self):
        dni = self.cedula_entry_first.get()
        if dni:
            client = self.check_client_exists(dni)
            if client == None:
                self.cedula_entry_first.delete(0, END)
                self.open_client_form()

            else:
                self.dni_row += 1
                if self.cedula_entry_first.get() != '':
                    self.client_dnies.append(self.cedula_entry_first.get())
                # self.add_dni_button.grid(row=self.dni_row, column=2, pady=5)
                self.message["text"] = f'Cliente con DNI {dni} encontrado.'
                self.dni_row = self.dni_row + 1
                self.render_input()
                self.message.config(fg="green")
        
    
    def __init__(self, window, role):
        self.role = role
        self.wind = window
        self.wind.title("Entrada de Clientes")
        self.client_dnies = []
        self.current_date = datetime.now()
        center_window(self.wind, 1300, 700)
        self.clients_ids = []
        
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
        self.frame = LabelFrame(self.wind, text='Nueva entrada', font=font, padx=20, pady=20)
        self.frame.grid(row=0, column=0, columnspan=3, pady=20)
        
        self.dni_row = 3

        Label(self.frame, text='Cedula: ', font=font).grid(row=self.dni_row, column=0)
        self.cedula_entry_first = Entry(self.frame)
        self.cedula_entry_first.grid(row=self.dni_row, column=1)
     
        Label(self.frame, text='Cedula (opcional): ', font=font).grid(row=self.dni_row + 1, column=0)
        self.cedula_entry_second = Entry(self.frame)
        self.cedula_entry_second.grid(row=self.dni_row + 1, column=1)
        # Button to add more DNI inputs
        # self.add_dni_button = Button(self.frame, text="Agregar Cliente", font=font, command=self.add_dni_input)
        # self.add_dni_button.grid(row=self.dni_row + 1, column=1, pady=5)
  
        # self.add_dni_input()

        # Habitacion
        Label(self.frame, text='Nro de habitacion: ', font=font).grid(row=self.dni_row + 4, column=0)
        self.room_number = Entry(self.frame)
        self.room_number.grid(row=self.dni_row + 4, column=1)
        
       # Time  
        Label(self.frame, text='Fecha: ', font=font).grid(row=self.dni_row + 5, column=0)
        self.date = DateEntry(self.frame, width=12, background='darkblue',foreground='white', borderwidth=2, year=self.current_date.year,month=self.current_date.month,day=self.current_date.day,date_pattern='y-mm-dd', )
        self.date.grid(row=self.dni_row + 5, column=1)
        
        Label(self.frame, text='Hora: ', font=font).grid(row=self.dni_row + 6, column=0, padx=10, pady=10)
        self.hour = Spinbox(self.frame, from_=0, to=23, font=font, width=5)
        self.hour.grid(row=self.dni_row + 6, column=1, padx=10, pady=10)
              
        # Button Add Entry
        Button(self.frame, text="Guardar entrada", font=("Comic Sans MS", 10), command=self.add_entry_client).grid(row=self.dni_row + 7, columnspan=2, sticky=W + E)
        # Output Messages
        self.message = Label(self.frame, text='')
        self.message.grid(row=6, column=0, columnspan=3, sticky=W+E)
        # Table
        self.tree = ttk.Treeview(self.frame, height=10, columns=("id","Nombre y apellido","cedula", "entrada", "habitacion", "Fecha", "hora"))
        self.tree.grid(row=15, column=0, columnspan=2)
        # Define los encabezados de las columnas
        self.tree.heading("#0", text='Id', anchor=CENTER)
        self.tree.heading("#1", text='Nombre y apellido', anchor=CENTER)
        self.tree.heading("#2", text='Cedula', anchor=CENTER)
        self.tree.heading('#3', text='Entrada', anchor=CENTER)
        self.tree.heading('#4', text='Habitacion', anchor=CENTER)
        self.tree.heading('#5', text='Fecha', anchor=CENTER) 
        self.tree.heading('#6', text='Hora', anchor=CENTER) 
        
        # Action buttons (EDIT, DELETE)
        if self.role == 1:
            Button(self.wind, text='Eliminar', font=("Comic Sans MS", 10), command=self.delete_entry).grid(row=20, column=0, sticky=W+E)
        if self.role < 3:
            Button(self.wind, text='Editar', font=("Comic Sans MS", 10), command=self.edit_entry).grid(row=20, column=1, sticky=W+E)
                
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
                    hour VARCHAR(20),
                    FOREIGN KEY (client_id) REFERENCES clients(id),
                    FOREIGN KEY (entry_id) REFERENCES entries(id)
                )
            """)
            self.conn.commit()
   
        except pymysql.Error as e:
            self.message['text'] = f"Error al crear la tabla: {e}"
            self.message.config(fg="red")


    def get_entries(self):
        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Querying data
        query = 'SELECT * FROM entry_clients'
        query_user = "SELECT * FROM clients where id = %s"
        query_entry = "SELECT * FROM entries where id = %s"
        query_room = "SELECT * FROM rooms where id = %s"
        db_rows = self.run_query(query).fetchall()
        # Filling data
        for row in db_rows:
            user = self.run_query(query_user, (row[1])).fetchone()
            roomId = self.run_query(query_entry, (row[2])).fetchone()[1]
            roomNumber = self.run_query(query_room, (roomId)).fetchone()[1]
            self.tree.insert('', 0, text=row[0], values=(f"{user[1]} {user[2]}", user[3],row[2], roomNumber, row[3], row[4]))    
        
    def validation(self):
        return len(self.room_number.get()) != 0 and len(self.cedula_entry_first.get()) > 0
    
    def formatForm(self):
        self.cedula_entry_first.delete(0, END)
        self.cedula_entry_second.delete(0, END)
        self.room_number.delete(0, END)
    
    def add_entry_client(self):
        if self.validation():
            # USers
            dni = self.cedula_entry_first.get()
            if dni:
                client = self.check_client_exists(dni)
                if client == None:
                    self.cedula_entry_first.delete(0, END)
                    self.open_client_form()
                else:
                    if self.cedula_entry_first.get() != '':
                        self.client_dnies.append(self.cedula_entry_first.get())
                    # self.add_dni_button.grid(row=self.dni_row, column=2, pady=5)
                    self.message["text"] = f'Cliente con DNI {dni} encontrado.'
                    self.message.config(fg="green")
            
            dni_2 = self.cedula_entry_second.get()
            print(dni_2, "DMO DOSS")
            if dni_2:
                client = self.check_client_exists(dni_2)
                if client == None:
                    self.cedula_entry_second.delete(0, END)
                    self.open_client_form()
                    print("HERE")
                    return
                else:
                    if self.cedula_entry_second.get() != '':
                        self.client_dnies.append(self.cedula_entry_second.get())
                    # self.add_dni_button.grid(row=self.dni_row, column=2, pady=5)
                    self.message["text"] = f'Cliente con DNI {dni_2} encontrado.'
                    self.message.config(fg="green")
            # Rooms
            room_query = "SELECT id from rooms WHERE room_number = %s"
            room = self.run_query(room_query, (self.room_number.get())).fetchone()
            if room == None:
                self.room_number.delete(0, END)
                self.open_room_form()
            else:
                query_entry = 'INSERT INTO entries (room_id, time) VALUES(%s, %s)'
                entry_params = (room[0], self.date.get_date())
                entry_id = self.run_query(query_entry, entry_params).lastrowid
                print(room[0],  "ËNTRY PARAMS", entry_id)
                
                query_entry_client = 'INSERT INTO entry_clients (client_id, entry_id, time, hour) VALUES (%s, %s, %s, %s)'
                # Mapping clients to insert them into the entry and entry_clients tables
                for client_id in self.clients_ids:
                    self.run_query(query_entry_client, (client_id, entry_id, self.date.get_date(), self.hour.get()))

                self.formatForm()
                self.message['text']='Entrada de cliente {} Agregada Correctamente'.format(self.cedula_entry_first.get())
                self.message.config(fg="green")
        else:
            self.message['text']='Todos los campos son requeridos'
            self.message.config(fg="red")
            
        self.get_entries()
        
    def delete_entry(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except:
            self.message['text'] = 'Please select a record'
            self.message.config(fg="red")
            return
        self.message['text'] = ''
        id = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM entry_clients WHERE id = %s'
        
        self.run_query(query, (id))
        
        self.message['text'] = 'Entrada {} Eliminada'.format(id)
        self.message.config(fg="green")
        self.get_entries()
        
    def edit_entry(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except:
            self.message['text'] = 'Please select a record'
            self.message.config(fg="red")
            return
        self.message['text'] = ''
        print(self.tree.item(self.tree.selection()))
        entry_client_id = self.tree.item(self.tree.selection())["text"] 
        old_dni = self.tree.item(self.tree.selection())['values'][1]
        old_entry = self.tree.item(self.tree.selection())['values'][2]
        old_room = self.tree.item(self.tree.selection())['values'][3]
        old_time = self.tree.item(self.tree.selection())['values'][4]
        old_hour = self.tree.item(self.tree.selection())['values'][5]
        
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar entrada'
        
        # # Old DNI
        Label(self.edit_wind, text='Cedula anterior: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_dni), state='readonly').grid(row=0, column=2)

        # # New DNI
        Label(self.edit_wind, text='Nueva Cedula: ').grid(row=1, column=1)
        new_dni = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_dni ))
        new_dni.grid(row=1, column=2)
        
        # # Old entry
        Label(self.edit_wind, text='Entrada anterior: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_entry), state='readonly').grid(row=2, column=2)
        
        # # New entry
        Label(self.edit_wind, text='Nueva entrada: ').grid(row=3, column=1)
        new_entry = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_entry))
        new_entry.grid(row=3, column=2)
    
        # # Old room
        Label(self.edit_wind, text='Habitacion anterior: ').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_room), state='readonly').grid(row=4, column=2)
        
        # # New room
        Label(self.edit_wind, text='Nueva Habitacion: ').grid(row=5, column=1)
        new_room = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_room))
        new_room.grid(row=5, column=2)
     
        # # Old Time
        Label(self.edit_wind, text='Fecha anterior: ').grid(row=6, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_time), state='readonly').grid(row=6, column=2)
        
        # # New time
        Label(self.edit_wind, text='Nueva Fecha: ').grid(row=7, column=1)
        new_time = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_time))
        new_time.grid(row=7, column=2)
       
        # # Old hour
        Label(self.edit_wind, text='Hora anterior: ').grid(row=8, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_hour), state='readonly').grid(row=8, column=2)
        
        # # New time
        Label(self.edit_wind, text='Nueva Hora: ').grid(row=9, column=1)
        new_hour = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_hour))
        new_hour.grid(row=9, column=2)
        
        # # Edit Button
        ttk.Button(self.edit_wind, text='Actualizar', command=lambda: self.edit_record(new_dni, new_entry, new_room, new_time, new_hour, entry_client_id)).grid(row=10, column=2, sticky=W)
        
    def edit_record(self, new_dni, new_entry, new_room, new_time, new_hour, entry_client_id):
        # Check the client
        client_query = "SELECT id from clients where dni = %s"
        client_id = self.run_query(client_query, (new_dni.get())).fetchone()
        if client_id == None:
            new_dni.delete(0, END)
            self.open_client_form() 
            return
        # Check the room
        room_query = "SELECT id from rooms where room_number = %s"
        room_id = self.run_query(room_query, (new_room.get())).fetchone()
        if room_id == None:
            new_room.delete(0, END)
            self.open_room_form()
            return
        # check entry
        entry_query = "SELECT id from entries WHERE id = %s"
        entry_id = self.run_query(entry_query, (new_entry.get())).fetchone()
        if entry_id == None:
            self.message["text"] = f"La entrada {new_entry.get()} no existe"
            new_entry.delete(0, END)
            return
        update_entry_query = "UPDATE entries SET room_id = %s WHERE id = %s"
        self.run_query(update_entry_query, (room_id, entry_id))
        query = 'UPDATE entry_clients SET client_id = %s, entry_id = %s, time = %s, hour = %s, WHERE id = %s'
        parameters = (client_id[0], new_entry.get(), new_time.get(), new_hour.get(), entry_client_id)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Entrada {} Actualizada'.format(entry_client_id)
        self.message.config(fg="green")
        self.get_entries()
        
def instantiateEntryClient(role):
    window = Tk()
    EntryClient(window, role)
    window.mainloop()
