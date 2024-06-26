
from tkinter import ttk
from tkinter import *
from utils.generic import center_window
import pymysql

font = ('Comic Sans MS', 14)
mainColor = "#f59e0b"
class Room:
    
    def __init__(self, window, role, close):
      self.wind = window
      self.role = role
      self.wind.title("Habitaciones")
      self.close = close
      center_window(self.wind, 1200, 600)
      
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
      if self.role != 3:
        frame = LabelFrame(self.wind, text='Nueva Habitacion', font=font, padx=20, pady=20)
      else:
        frame = LabelFrame(self.wind, text='Habitaciones', font=font, padx=20, pady=20)
      frame.grid(row=0, column=0, columnspan=3, pady=20)
      if self.role != 3:
      # Room Number Input
        Label(frame, text='Numero: ', font=font).grid(row=1, column=0)
        self.room_number = Entry(frame)
        self.room_number.focus()
        self.room_number.grid(row=1, column=1)
        
        # Type of room ("Family", "individual", "couple") Input
        Label(frame, text='Tipo de habitacion: ', font=font).grid(row=2, column=0)
        self.room_type = ttk.Combobox(frame, values=["Familiar", "Individual", "Pareja"], state='readonly')
        self.room_type.grid(row=2, column=1)
        self.room_type.set("Pareja")
        
        # Button Add Product
        Button(frame, text="Guardar Habitacion", font=font, command=self.add_room).grid(row=3, columnspan=2, sticky=W + E)
      
      # Output Messages
      self.message = Label(self.wind, text='', fg='red')
      self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)
      
      # Table
      style = ttk.Style()
      style.configure("Treeview.Heading", font=font)  # Fuente para encabezados
      style.configure("Treeview", font=('Comic Sans MS', 10)) 
      self.tree = ttk.Treeview(frame, height=10, columns=('ID','Numero', 'Tipo'))
      self.tree.grid(row=4, column=0, columnspan=2)
      self.tree.heading("#0", text='ID', anchor=CENTER)
      self.tree.heading("#1", text='Numero', anchor=CENTER)
      self.tree.heading('#2', text='Tipo', anchor=CENTER)
      
      # Action buttons (EDIT, DELETE)
      if self.role == 1:  
        Button(self.wind, text='Eliminar', font=font, command=self.delete_room).grid(row=5, column=0, sticky=W+E)
      if self.role < 3:
        Button(self.wind, text='Editar', font=font, command=self.edit_room).grid(row=5, column=1, sticky=W+E)
      
      # Filling the rows
      self.get_rooms()
      
    def get_room_type_number(self, room):
        if room == 'Familiar': 
            return 3
        elif room == 'Pareja':
            return 2
        else:
            return 1
        
    def get_room_type_string(self, room):
        if room == 3:
            return 'Familiar'
        elif room == 2:
            return 'Pareja'
        else:
            return "Individual"

    def create_table(self):
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    room_number INT,
                    room_type INT
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

    

    def get_rooms(self):
        # Limpiar tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Consultar datos
        query = 'SELECT * FROM rooms'
        db_rows = self.run_query(query).fetchall()
        # Llenar datos
        for row in db_rows:
            self.tree.insert('', 0, text=row[0], values=(row[1], self.get_room_type_string(row[2])))
        
    def validation(self):
        return len(self.room_number.get()) != 0 and len(self.room_type.get()) != 0
    
    def format_form(self):
        self.room_number.delete(0, END)
        self.room_type.delete(0, END)
    
    def add_room(self):
        if self.validation():
            query = 'INSERT INTO rooms (room_number, room_type) VALUES (%s, %s)'
            parameters = (self.room_number.get(), self.get_room_type_number(self.room_type.get()))
            self.run_query(query, parameters)
            self.format_form()
            self.message['text'] = 'Habitacion {} Creada Correctamente.'.format(self.room_number.get())
            if self.close == True:
                self.wind.destroy()
            else:
                self.message['text'] = 'Todos los campos son requeridos.'
            
        self.get_rooms()
        
    def delete_room(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        number = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM rooms WHERE room_number = %s'
        print(number, "HERE",  self.tree.item(self.tree.selection()))
        self.run_query(query, (number))
        
        self.message['text'] = 'Habitacion {} eliminada correctamente'.format(number)
        self.get_rooms()
        
    def edit_room(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        number = self.tree.item(self.tree.selection())['values'][0]
        old_type = self.tree.item(self.tree.selection())['values'][1]
        
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Record'
        
        # Old room_number
        Label(self.edit_wind, text='Numero de habitacion anterior: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=number), state='readonly').grid(row=0, column=2)

        # New room_number
        Label(self.edit_wind, text='Nuevo Numero de habitacion: ').grid(row=1, column=1)
        new_room_number = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=number))
        new_room_number.grid(row=1, column=2)
        
        # Old room_type
        Label(self.edit_wind, text='Tipo de habitacion anterior: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, old_type), state='readonly').grid(row=2, column=2)
        
        # New room_type
        Label(self.edit_wind, text='Nuevo Tipo de habitacion: ').grid(row=3, column=1)
        new_room_type = ttk.Combobox(self.edit_wind, values=["Familiar", "Individual", "Pareja"],  state='readonly')
        new_room_type.grid(row=3, column=2)
        new_room_type.set("Pareja")
        
        # Edit Button
        ttk.Button(self.edit_wind, text='Update', command=lambda: self.edit_record(new_room_number.get(), new_room_type.get(), number)).grid(row=4, column=2, sticky=W)
        
    def edit_record(self,new_room_number, new_room_type, number):
        query = 'UPDATE rooms SET room_number = %s, room_type = %s WHERE room_number = %s'
        parameters = (int(new_room_number), self.get_room_type_number(new_room_type), number)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Habitacion {} actualizada correctamente'.format(number)
        self.get_rooms()
        
def instantiateRoom(role, wind = False):
    if(wind):
        window = wind
        Room(window, role, close=True)
        window.mainloop()
    else:
        window = Tk()
        Room(window, role, close=False)
        window.mainloop()
    
        
