import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

from search_replace import search_and_replace
from utils import read_file, write_file  # Se elimina la función backup_file

class SearchReplaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Buscar y Reemplazar - Tkinter")
        self.geometry("900x650")
        self.current_file = None  # Ruta del archivo actualmente abierto
        self._create_widgets()

    def _create_widgets(self):
        # Frame para operaciones con el archivo: Abrir y Guardar Cambios
        self.frame_file = tk.Frame(self)
        self.frame_file.pack(fill=tk.X, padx=10, pady=5)

        btn_open = tk.Button(self.frame_file, text="Abrir Archivo", command=self.open_file)
        btn_open.pack(side=tk.LEFT, padx=5, pady=5)

        btn_save = tk.Button(self.frame_file, text="Guardar Cambios", command=self.save_file)
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame para controles de búsqueda y reemplazo
        self.frame_search = tk.Frame(self)
        self.frame_search.pack(fill=tk.X, padx=10, pady=5)

        # Columna 0: Etiqueta "Buscar:"
        lbl_search = tk.Label(self.frame_search, text="Buscar:")
        lbl_search.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Columna 1: Entrada para el término a buscar
        self.entry_search = tk.Entry(self.frame_search, width=30)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Columna 2: Botón para buscar (resaltar) la palabra
        btn_search = tk.Button(self.frame_search, text="Buscar Palabra", command=self.search_word)
        btn_search.grid(row=0, column=2, padx=5, pady=5)

        # Columna 3: Etiqueta "Reemplazar:"
        lbl_replace = tk.Label(self.frame_search, text="Reemplazar:")
        lbl_replace.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Columna 4: Entrada para la cadena de reemplazo
        self.entry_replace = tk.Entry(self.frame_search, width=30)
        self.entry_replace.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Columna 5: Botón para aplicar el reemplazo
        btn_replace = tk.Button(self.frame_search, text="Aplicar Reemplazo", command=self.apply_replace)
        btn_replace.grid(row=0, column=5, padx=5, pady=5)

        # Configuramos las columnas 1 y 4 para que se expandan adecuadamente
        self.frame_search.columnconfigure(1, weight=1)
        self.frame_search.columnconfigure(4, weight=1)

        # Área de texto para visualizar y editar el contenido del archivo.
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def open_file(self):
        """
        Abre un archivo (cualquier tipo), carga su contenido en el área de texto y actualiza el título.
        """
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=(("Todos los archivos", "*.*"),)
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
        Guarda el contenido del área de texto en el archivo abierto.
        Si no se ha seleccionado archivo, invoca 'Guardar Como'.
        Nota: Se sobrescribe el archivo editado, sin crear archivos .bak.
        """
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                write_file(self.current_file, content)
                messagebox.showinfo("Guardado", "El archivo se ha guardado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo.\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """
        Permite guardar el contenido en una nueva ubicación.
        Soporta cualquier tipo de archivo.
        """
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
        Busca y resalta todas las ocurrencias del término ingresado en la entrada "Buscar"
        dentro del área de texto, sin modificar el contenido.
        """
        search_term = self.entry_search.get()
        if search_term == "":
            messagebox.showwarning("Advertencia", "El término de búsqueda no puede estar vacío para la búsqueda.")
            return

        # Se eliminan resaltados anteriores
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

        self.text_area.tag_config("highlight", background="yellow", foreground="black")

        if count_matches == 0:
            messagebox.showinfo("Buscar", f"No se encontraron coincidencias para '{search_term}'.")
        else:
            messagebox.showinfo("Buscar", f"Se encontraron {count_matches} coincidencia(s) para '{search_term}'.")


if __name__ == "__main__":
    app = SearchReplaceApp()
    app.mainloop()