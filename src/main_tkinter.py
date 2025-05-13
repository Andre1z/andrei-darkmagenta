import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

from search_replace import search_and_replace
from utils import read_file, write_file, backup_file

class SearchReplaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Buscar y Reemplazar - Tkinter")
        self.geometry("800x600")
        self.current_file = None  # Ruta del archivo actualmente abierto
        self._create_widgets()

    def _create_widgets(self):
        # Marco superior: botones y entradas para búsqueda y reemplazo
        frame_top = tk.Frame(self)
        frame_top.pack(fill=tk.X, padx=10, pady=10)
        
        # Botón para abrir archivo de texto
        btn_open = tk.Button(frame_top, text="Abrir Archivo", command=self.open_file)
        btn_open.grid(row=0, column=0, padx=5)
        
        # Botón para guardar cambios
        btn_save = tk.Button(frame_top, text="Guardar Archivo", command=self.save_file)
        btn_save.grid(row=0, column=1, padx=5)
        
        # Etiqueta y entrada para el término de búsqueda
        lbl_search = tk.Label(frame_top, text="Buscar:")
        lbl_search.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.entry_search = tk.Entry(frame_top, width=30)
        self.entry_search.grid(row=1, column=1, padx=5, pady=5)
        
        # Etiqueta y entrada para la cadena de reemplazo
        lbl_replace = tk.Label(frame_top, text="Reemplazar:")
        lbl_replace.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        self.entry_replace = tk.Entry(frame_top, width=30)
        self.entry_replace.grid(row=1, column=3, padx=5, pady=5)
        
        # Botón para aplicar el reemplazo
        btn_replace = tk.Button(frame_top, text="Aplicar Reemplazo", command=self.apply_replace)
        btn_replace.grid(row=1, column=4, padx=5, pady=5)
        
        # Área de texto para mostrar y editar el contenido del archivo
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def open_file(self):
        """Abre un archivo de texto y carga su contenido en el área principal."""
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo de texto",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if file_path:
            try:
                content = read_file(file_path)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file = file_path
                self.title(f"Buscar y Reemplazar - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo.\n{e}")

    def save_file(self):
        """
        Guarda el contenido del área de texto en el archivo actual.
        Si no se ha seleccionado uno previamente, se invoca una opción 'Guardar Como'.
        Antes de sobrescribir, crea una copia de seguridad del archivo original.
        """
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                # Crear copia de seguridad
                backup_file(self.current_file)
                write_file(self.current_file, content)
                messagebox.showinfo("Guardado", "El archivo ha sido guardado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo.\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Si no hay un archivo abierto, permite guardar el contenido en una ubicación nueva."""
        file_path = filedialog.asksaveasfilename(
            title="Guardar Archivo Como",
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                write_file(file_path, content)
                self.current_file = file_path
                self.title(f"Buscar y Reemplazar - {os.path.basename(file_path)}")
                messagebox.showinfo("Guardado", "El archivo ha sido guardado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo.\n{e}")

    def apply_replace(self):
        """
        Ejecuta la función de búsqueda y reemplazo sobre el contenido
        del área de texto. Se valida que el término a buscar no sea vacío.
        """
        search_term = self.entry_search.get()
        replacement = self.entry_replace.get()
        content = self.text_area.get(1.0, tk.END)
        
        if search_term == "":
            messagebox.showwarning("Advertencia", "El término de búsqueda no puede estar vacío.")
            return

        try:
            new_content = search_and_replace(content, search_term, replacement)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)
            messagebox.showinfo("Éxito", "El reemplazo se realizó correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al realizar el reemplazo.\n{e}")

if __name__ == "__main__":
    app = SearchReplaceApp()
    app.mainloop()