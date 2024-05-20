
from tkinter import ttk
from tkinter import *
from utils.generic import center_window
import mysql.connector

class User:
    db_name = 'database.db'
    
    def __init__(self, window):
      self.wind = window
      self.wind.title("Usuarios")
      
      center_window(self.wind, 800, 500)
      
      # Creating a Frame Container
      frame = LabelFrame(self.wind, text='Nuevo Usuario')
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
      self.cedula = Entry(frame)
      self.cedula.grid(row=3, column=1)
      
      # Fecha de nacimiento Input
      Label(frame, text='Fecha de nacimiento: ').grid(row=4, column=0)
      self.birth_date = Entry(frame)
      self.birth_date.grid(row=4, column=1)
      
      # Rool Input
      Label(frame, text='Rol: ').grid(row=5, column=0)
      self.role = Entry(frame)
      self.role.grid(row=5, column=1)
      
      # Button Add Product
      ttk.Button(frame, text="Guardar Usuario").grid(row=6, columnspan=2, sticky=W + E)
      
      # Output Messages
      self.message = Label(text='', fg='red')
      self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)
      
      # Table
      self.tree = ttk.Treeview(height=10, columns=('Nombre', 'Apellido', 'Cedula', 'Fecha de nacimiento', 'rol' ))
      self.tree.grid(row=5, column=0, columnspan=2)
      self.tree.heading("#0", text='Nombre', anchor=CENTER)
      self.tree.heading('#1', text='Apellido', anchor=CENTER)
      self.tree.heading('#2', text='Cedula', anchor=CENTER)
      self.tree.heading('#3', text='Fecha de nacimiento', anchor=CENTER)
      self.tree.heading('#4', text='rol', anchor=CENTER)
      
      # Action buttons (EDIT, DELETE)
      ttk.Button(text='DELETE').grid(row=6, column=0, sticky=W+E)
      ttk.Button(text='EDIT').grid(row=6, column=1, sticky=W+E)
      
      # Filling the rows
      self.get_products()

    # def run_query(self, query, parameters = ()):
    #     with sqlite3.connect(self.db_name) as conn:
    #         cursor = conn.cursor()    
    #         result = cursor.execute(query, parameters)
    #         conn.commit()
    #     return result
    
    
    def connect_db(self):
        return mysql.connector.connect(
            host=self.db_name,
            user="root",
            password="mariadb",
            database="hotelDB"
        )


    # def get_products(self):
    #     #Cleaning table
    #     records = self.tree.get_children()
    #     for element in records:
    #         self.tree.delete(element)
    #     # Querying data
    #     query = 'SELECT * FROM product ORDER BY name DESC'
    #     db_rows = self.run_query(query)
    #     # Filling data
    #     for row in db_rows:
    #         self.tree.insert('', 0, text=row[1], values=row[2])    
        
    # def validation(self):
    #     return len(self.name.get()) != 0 and len(self.price.get()) != 0
    
    # def formatForm(self):
    #     self.name.delete(0, END)
    #     self.price.delete(0, END)
    
    # def add_product(self):
    #     if self.validation():
    #         query = 'INSERT INTO product VALUES(NULL,?,?)'
    #         parameters = (self.name.get(), self.price.get())
    #         self.run_query(query, parameters)
    #         self.formatForm()
    #         self.message['text']='Product {} added successfully'.format(self.name.get())
    #     else:
    #         self.message['text']='Name and price are required'
            
    #     self.get_products()
        
    # def delete_product(self):
    #     self.message['text'] = ''
    #     try:
    #         self.tree.item(self.tree.selection())['text'][0]
    #     except:
    #         self.message['text'] = 'Please select a record'
    #         return
    #     self.message['text'] = ''
    #     name = self.tree.item(self.tree.selection())['text']
    #     query = 'DELETE FROM product WHERE name = ?'
        
    #     self.run_query(query, (name, ))
        
    #     self.message['text'] = 'Record {} deleted successfully'.format(name)
    #     self.get_products()
        
    # def edit_product(self):
    #     self.message['text'] = ''
    #     try:
    #         self.tree.item(self.tree.selection())['text'][0]
    #     except:
    #         self.message['text'] = 'Please select a record'
    #         return
    #     self.message['text'] = ''
    #     name = self.tree.item(self.tree.selection())['text']
    #     old_price = self.tree.item(self.tree.selection())['values'][0]
        
    #     self.edit_wind = Toplevel()
    #     self.edit_wind.title = 'Edit Record'
        
    #     # Old Name
    #     Label(self.edit_wind, text='Old Name: ').grid(row=0, column=1)
    #     Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

    #     # New Name
    #     Label(self.edit_wind, text='New Name: ').grid(row=1, column=1)
    #     new_name = Entry(self.edit_wind)
    #     new_name.grid(row=1, column=2)
        
    #     # Old Price
    #     Label(self.edit_wind, text='Old Price: ').grid(row=2, column=1)
    #     Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)
        
    #     # New Price
    #     Label(self.edit_wind, text='New Price: ').grid(row=3, column=1)
    #     new_price = Entry(self.edit_wind)
    #     new_price.grid(row=3, column=2)
        
    #     # Edit Button
    #     ttk.Button(self.edit_wind, text='Update', command=lambda: self.edit_record(new_name, name, new_price, old_price)).grid(row=4, column=2, sticky=W)
        
    # def edit_record(self, new_name, name, new_price, price):
    #     query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
    #     parameters = (new_name, new_price, name, price)
    #     self.run_query(query, parameters)
    #     self.edit_wind.destroy()
    #     self.message['text'] = 'Product {} updated successfully'.format(name)
    #     self.get_products()
        
def instantiateUser():
    window = Tk()
    User(window)
    window.mainloop()
    
        
