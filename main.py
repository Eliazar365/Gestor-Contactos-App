import tkinter as tk
from tkinter import messagebox
import json
import os

# --- Configuración de la aplicación ---
DATA_FILE = 'contacts.json'
CONTACTS = []

# --- Funciones de Persistencia de Datos ---
def load_data():
    global CONTACTS
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                CONTACTS = json.load(f)
            except json.JSONDecodeError:
                CONTACTS = []
                messagebox.showwarning("Error de Datos", "El archivo de datos está corrupto o vacío. Se ha inicializado uno nuevo.")
    else:
        CONTACTS = []
        messagebox.showinfo("Información", "Archivo de datos no encontrado o vacío. Se creará uno nuevo al guardar.")

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(CONTACTS, f, indent=4)

# --- Clase Principal de la Aplicación ---
class ContactManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Gestor de Contactos CRUD")
        master.geometry("600x500")
        master.resizable(False, False)

        self.input_frame = tk.Frame(master, padx=10, pady=10)
        self.input_frame.pack(pady=10)
        self.button_frame = tk.Frame(master, padx=10, pady=5)
        self.button_frame.pack(pady=5)
        self.list_frame = tk.Frame(master, padx=10, pady=10)
        self.list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Label(self.input_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=2)
        self.name_entry = tk.Entry(self.input_frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=2)
        tk.Label(self.input_frame, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=2)
        self.phone_entry = tk.Entry(self.input_frame, width=40)
        self.phone_entry.grid(row=1, column=1, pady=2)
        tk.Label(self.input_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=2)
        self.email_entry = tk.Entry(self.input_frame, width=40)
        self.email_entry.grid(row=2, column=1, pady=2)

        self.add_button = tk.Button(self.button_frame, text="Agregar Contacto", command=self.add_contact, width=15)
        self.add_button.grid(row=0, column=0, padx=5)
        self.update_button = tk.Button(self.button_frame, text="Actualizar Contacto", command=self.update_contact, width=15)
        self.update_button.grid(row=0, column=1, padx=5)
        self.delete_button = tk.Button(self.button_frame, text="Eliminar Contacto", command=self.delete_contact, width=15)
        self.delete_button.grid(row=0, column=2, padx=5)
        self.clear_button = tk.Button(self.button_frame, text="Limpiar Campos", command=self.clear_entries, width=15)
        self.clear_button.grid(row=0, column=3, padx=5)

        self.contact_listbox = tk.Listbox(self.list_frame, height=15, width=80)
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.contact_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.contact_listbox.config(yscrollcommand=self.scrollbar.set)
        self.contact_listbox.bind('<<ListboxSelect>>', self.select_contact)

        load_data()
        self.view_contacts()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def view_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        if not CONTACTS:
            self.contact_listbox.insert(tk.END, "No hay contactos guardados.")
            return
        for i, contact in enumerate(CONTACTS):
            display_text = f"{i+1}. Nombre: {contact['name']}, Teléfono: {contact['phone']}, Email: {contact['email']}"
            self.contact_listbox.insert(tk.END, display_text)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        if not name or not phone:
            messagebox.showwarning("Campos Vacíos", "El nombre y el teléfono son obligatorios.")
            return
        new_contact = {
            "name": name,
            "phone": phone,
            "email": email
        }
        CONTACTS.append(new_contact)
        save_data()
        self.clear_entries()
        self.view_contacts()
        messagebox.showinfo("Éxito", "Contacto agregado correctamente.")

    def select_contact(self, event):
        selected_index_tuple = self.contact_listbox.curselection()
        if not selected_index_tuple:
            return
        index = selected_index_tuple[0]
        self.clear_entries()
        if 0 <= index < len(CONTACTS):
            contact = CONTACTS[index]
            self.name_entry.insert(0, contact['name'])
            self.phone_entry.insert(0, contact['phone'])
            self.email_entry.insert(0, contact['email'])

    def update_contact(self):
        selected_index_tuple = self.contact_listbox.curselection()
        if not selected_index_tuple:
            messagebox.showwarning("Selección Necesaria", "Selecciona un contacto de la lista para actualizar.")
            return
        index = selected_index_tuple[0]
        if not (0 <= index < len(CONTACTS)):
             messagebox.showwarning("Error", "Selección inválida.")
             return
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        if not name or not phone:
            messagebox.showwarning("Campos Vacíos", "El nombre y el teléfono son obligatorios.")
            return
        CONTACTS[index]['name'] = name
        CONTACTS[index]['phone'] = phone
        CONTACTS[index]['email'] = email
        save_data()
        self.clear_entries()
        self.view_contacts()
        messagebox.showinfo("Éxito", "Contacto actualizado correctamente.")

    def delete_contact(self):
        selected_index_tuple = self.contact_listbox.curselection()
        if not selected_index_tuple:
            messagebox.showwarning("Selección Necesaria", "Selecciona un contacto de la lista para eliminar.")
            return
        index = selected_index_tuple[0]
        if not (0 <= index < len(CONTACTS)):
             messagebox.showwarning("Error", "Selección inválida.")
             return
        if messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que quieres eliminar este contacto?"):
            del CONTACTS[index]
            save_data()
            self.clear_entries()
            self.view_contacts()
            messagebox.showinfo("Éxito", "Contacto eliminado correctamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()