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
        master.geometry("600x500") # Tamaño inicial de la ventana principal
        master.resizable(False, False)

        self.input_frame = tk.Frame(master, padx=10, pady=10)
        self.input_frame.pack(pady=10)
        self.button_frame = tk.Frame(master, padx=10, pady=7) # CAMBIO DE FEATURE #2: pady=7
        self.button_frame.pack(pady=5)

        self.list_frame = tk.Frame(master, padx=10, pady=10)
        self.list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5)) # CAMBIO DE FEATURE #3: pady=(0, 5)

        # LÍNEAS DE FEATURE #3
        self.info_label = tk.Label(master, text="Gestión de Contactos Activa", fg="blue", font=("Arial", 9))
        self.info_label.pack(pady=(0, 5))

        tk.Label(self.input_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=2)
        self.name_entry = tk.Entry(self.input_frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=2)
        tk.Label(self.input_frame, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=2)
        self.phone_entry = tk.Entry(self.input_frame, width=40)
        self.phone_entry.grid(row=1, column=1, pady=2)
        tk.Label(self.input_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=2)
        self.email_entry = tk.Entry(self.input_frame, width=40)
        self.email_entry.grid(row=2, column=1, pady=2)

        # LÍNEAS DE FEATURE #4: Campo de Notas y validación simulada
        tk.Label(self.input_frame, text="Notas (Opcional):").grid(row=3, column=0, sticky="w", pady=2)
        self.notes_entry = tk.Entry(self.input_frame, width=40)
        self.notes_entry.grid(row=3, column=1, pady=2)
        self.notes_entry.bind("<KeyRelease>", self.check_notes_length) # Simula validación de longitud

        self.add_button = tk.Button(self.button_frame, text="Agregar Contacto", command=self.add_contact, width=15)
        self.add_button.grid(row=0, column=0, padx=5)
        self.update_button = tk.Button(self.button_frame, text="Actualizar Contacto", command=self.update_contact, width=15)
        self.update_button.grid(row=0, column=1, padx=5)
        self.delete_button = tk.Button(self.button_frame, text="Eliminar Contacto", command=self.delete_contact, width=15)
        self.delete_button.grid(row=0, column=2, padx=5)

        # NUEVAS LÍNEAS PARA FEATURE #5: Botón Ver Detalles
        self.details_button = tk.Button(self.button_frame, text="Ver Detalles", command=self.show_details, width=15)
        self.details_button.grid(row=0, column=3, padx=5) # Este será el nuevo botón en la columna 3

        # CAMBIO DE FEATURE #5: Ajuste de columna para Limpiar Campos
        self.clear_button = tk.Button(self.button_frame, text="Limpiar Campos", command=self.clear_entries, width=15)
        self.clear_button.grid(row=0, column=4, padx=5) # AHORA EN LA COLUMNA 4

        self.contact_listbox = tk.Listbox(self.list_frame, height=15, width=80)
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.contact_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.contact_listbox.config(yscrollcommand=self.scrollbar.set)
        self.contact_listbox.bind('<<ListboxSelect>>', self.select_contact)

        load_data()
        self.view_contacts()

    def check_notes_length(self, event=None):
        """Simula una validación de longitud para el campo de notas."""
        notes_text = self.notes_entry.get()
        if len(notes_text) > 50: # Ejemplo: límite de 50 caracteres
            self.notes_entry.config(fg="red")
            self.info_label.config(text="Notas: Excede límite de 50 caracteres", fg="red")
        else:
            self.notes_entry.config(fg="black")
            self.info_label.config(text="Gestión de Contactos Activa", fg="blue")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END) # Limpia también el nuevo campo
        self.notes_entry.config(fg="black") # Resetea color
        self.info_label.config(text="Gestión de Contactos Activa", fg="blue")

    def view_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        if not CONTACTS:
            self.contact_listbox.insert(tk.END, "No hay contactos guardados.")
            return
        for i, contact in enumerate(CONTACTS):
            # Muestra también las notas, si existen
            notes_display = f", Notas: {contact.get('notes', 'N/A')}" if contact.get('notes') else ""
            display_text = f"{i+1}. Nombre: {contact['name']}, Teléfono: {contact['phone']}, Email: {contact['email']}{notes_display}"
            self.contact_listbox.insert(tk.END, display_text)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        notes = self.notes_entry.get().strip() # Obtiene el nuevo campo
        
        # Validación de campos obligatorios (mejorada para Feature #4)
        if not name or not phone:
            messagebox.showwarning(
                "¡Atención!",
                "Por favor, completa al menos el Nombre y el Teléfono para el contacto."
            )
            return

        # Simula validación de longitud para notas antes de guardar
        if len(notes) > 50:
             messagebox.showwarning("Error de Notas", "Las notas exceden el límite de 50 caracteres. Por favor, acorta el texto.")
             return

        new_contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "notes": notes # Añade el campo de notas
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
            self.notes_entry.insert(0, contact.get('notes', '')) # Carga el campo de notas, si existe

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
        notes = self.notes_entry.get().strip() # Obtiene el nuevo campo
        
        # Validación de campos obligatorios (mejorada para Feature #4)
        if not name or not phone:
            messagebox.showwarning(
                "¡Atención!",
                "El Nombre y el Teléfono son obligatorios para actualizar el contacto."
            )
            return

        # Simula validación de longitud para notas antes de guardar
        if len(notes) > 50:
             messagebox.showwarning("Error de Notas", "Las notas exceden el límite de 50 caracteres. Por favor, acorta el texto.")
             return

        CONTACTS[index]['name'] = name
        CONTACTS[index]['phone'] = phone
        CONTACTS[index]['email'] = email
        CONTACTS[index]['notes'] = notes # Actualiza el campo de notas
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

    # NUEVO MÉTODO PARA FEATURE #5: Mostrar Detalles
    def show_details(self):
        """Simula la apertura de una ventana o un panel con más detalles del contacto seleccionado."""
        selected_index_tuple = self.contact_listbox.curselection()
        if not selected_index_tuple:
            messagebox.showinfo("Información", "Por favor, selecciona un contacto para ver los detalles.")
            return
        index = selected_index_tuple[0]
        if 0 <= index < len(CONTACTS):
            contact = CONTACTS[index]
            details_text = f"Detalles del Contacto:\n\n" \
                           f"Nombre: {contact['name']}\n" \
                           f"Teléfono: {contact['phone']}\n" \
                           f"Email: {contact['email']}\n" \
                           f"Notas: {contact.get('notes', 'N/A')}"
            messagebox.showinfo("Detalles del Contacto", details_text)
        else:
            messagebox.showwarning("Error", "Selección inválida.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()