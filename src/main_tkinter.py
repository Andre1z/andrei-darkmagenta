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
        # Frame superior: contiene botones y entradas para búsqueda y reemplazo
        frame_top = tk.Frame(self)
        frame_top.pack(fill=tk.X, padx=10, pady=5)
        
        # Botón para abrir archivo
        btn_open = tk.Button(frame_top, text="Abrir Archivo", command=self.open_file)
        btn_open.grid(row=0, column=0, padx=5, pady=5)
        
        # Botón para guardar archivo
        btn_save = tk.Button(frame_top, text="Guardar Archivo", command=self.save_file)
        btn_save.grid(row=0, column=1, padx=5, pady=5)
        
        # Etiqueta y entrada para el término a buscar
        lbl_search = tk.Label(frame_top, text="Buscar:")
        lbl_search.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.entry_search = tk.Entry(frame_top, width=20)
        self.entry_search.grid(row=0, column=3, padx=5, pady=5)
        
        # Etiqueta y entrada para la cadena de reemplazo
        lbl_replace = tk.Label(frame_top, text="Reemplazar:")
        lbl_replace.grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.entry_replace = tk.Entry(frame_top, width=20)
        self.entry_replace.grid(row=0, column=5, padx=5, pady=5)
        
        # Botón para aplicar el reemplazo (usa la función search_and_replace)
        btn_replace = tk.Button(frame_top, text="Aplicar Reemplazo", command=self.apply_replace)
        btn_replace.grid(row=0, column=6, padx=5, pady=5)
        
        # Botón para buscar (solo resalta) la palabra en el recuadro "Buscar"
        btn_search = tk.Button(frame_top, text="Buscar Palabra", command=self.search_word)
        btn_search.grid(row=0, column=7, padx=5, pady=5)

        # Área de texto para mostrar y editar el contenido del archivo
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def open_file(self):
        """
        Abre un archivo (cualquier tipo) y carga su contenido en el área de texto.
        Si el archivo no es de texto, se intentará leerlo ignorando errores de decodificación.
        """
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=(("Todos los archivos", "*.*"),)
        )
        if file_path:
            try:
                # Para soportar cualquier tipo de archivo, read_file puede usar errors='replace'
                content = read_file(file_path)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file = file_path
                self.title(f"Buscar y Reemplazar - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo.\n{e}")

    def save_file(self):
        """
        Guarda el contenido actual del área de texto en el archivo abierto.
        Si no se tiene un archivo abierto, se invoca 'Guardar Como'.
        Antes de sobrescribir, se crea una copia de seguridad del archivo original.
        """
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                # Crear copia de seguridad del archivo
                backup_file(self.current_file)
                write_file(self.current_file, content)
                messagebox.showinfo("Guardado", "El archivo se ha guardado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo.\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Guarda el contenido en un nuevo archivo, permitiendo seleccionar cualquier tipo de archivo."""
        file_path = filedialog.asksaveasfilename(
            title="Guardar Archivo Como",
            defaultextension=".txt",
            filetypes=(("Todos los archivos", "*.*"),)
        )
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                write_file(file_path, content)
                self.current_file = file_path
                self.title(f"Buscar y Reemplazar - {os.path.basename(file_path)}")
                messagebox.showinfo("Guardado", "El archivo se ha guardado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo.\n{e}")

    def apply_replace(self):
        """
        Aplica la función de búsqueda y reemplazo al contenido del área de texto,
        sustituyendo todas las ocurrencias del término buscado por la cadena de reemplazo.
        """
        search_term = self.entry_search.get()
        replacement = self.entry_replace.get()
        content = self.text_area.get(1.0, tk.END)
        
        if search_term == "":
            messagebox.showwarning("Advertencia", "El término de búsqueda no puede estar vacío para el reemplazo.")
            return

        try:
            new_content = search_and_replace(content, search_term, replacement)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)
            messagebox.showinfo("Éxito", "El reemplazo se realizó correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar el reemplazo.\n{e}")

    def search_word(self):
        """
        Busca y resalta todas las ocurrencias del término ingresado en el recuadro "Buscar"
        dentro del área de texto, sin modificar el contenido.
        """
        search_term = self.entry_search.get()
        if search_term == "":
            messagebox.showwarning("Advertencia", "El término de búsqueda no puede estar vacío para la búsqueda.")
            return

        # Elimina resaltados anteriores
        self.text_area.tag_remove("highlight", "1.0", tk.END)

        idx = "1.0"
        count_matches = 0
        while True:
            idx = self.text_area.search(search_term, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            end_idx = f"{idx}+{len(search_term)}c"
            self.text_area.tag_add("highlight", idx, end_idx)
            count_matches += 1
            idx = end_idx

        # Configura el estilo del resaltado
        self.text_area.tag_config("highlight", background="yellow", foreground="black")
        
        if count_matches == 0:
            messagebox.showinfo("Buscar", f"No se encontraron coincidencias para '{search_term}'.")
        else:
            messagebox.showinfo("Buscar", f"Se encontraron {count_matches} coincidencia(s) para '{search_term}'.")

if __name__ == "__main__":
    app = SearchReplaceApp()
    app.mainloop()