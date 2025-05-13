import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

from search_replace import search_and_replace
from utils import read_file, write_file

# --- Clase para botones redondeados ---

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, radius=20, padding=10, command=None,
                 bg="#1976d2", fg="#ffffff", hover_bg=None, font=None, **kwargs):
        # Se utiliza el color de fondo actual del padre para que el Canvas se integre
        tk.Canvas.__init__(self, parent, borderwidth=0, highlightthickness=0, bg=parent["bg"], **kwargs)
        self.command = command
        self.radius = radius
        self.padding = padding
        self.bg = bg  # Color principal del botón (no es el fondo del Canvas)
        self.fg = fg
        # Si no se especifica hover_bg, se oscurece ligeramente el bg
        self.hover_bg = hover_bg if hover_bg is not None else self._darker(bg, 0.9)
        self.text = text
        self.font = font or ("Helvetica", 10, "bold")
        self.bg_rect = None
        self.text_id = None
        self.draw_button()
        self.bind("<Button-1>", lambda e: self.on_click())
        self.bind("<Enter>", lambda e: self.on_enter())
        self.bind("<Leave>", lambda e: self.on_leave())
    
    def _darker(self, color, factor):
        # Oscurece el color multiplicando cada componente RGB por factor
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(int(max(min(c * factor, 255), 0)) for c in rgb)
        return "#%02x%02x%02x" % darker_rgb
    
    def draw_button(self):
        # Mide el tamaño del texto para calcular el tamaño mínimo del botón
        temp_id = self.create_text(0, 0, text=self.text, font=self.font, anchor="nw")
        bbox = self.bbox(temp_id)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        width = text_width + self.padding * 2
        height = text_height + self.padding * 2
        self.config(width=width, height=height)
        self.delete("all")
        # Dibuja un rectángulo redondeado
        self.bg_rect = self.round_rect(0, 0, width, height, self.radius, fill=self.bg, outline=self.bg)
        # Dibuja el texto centrado
        self.text_id = self.create_text(width / 2, height / 2, text=self.text, font=self.font, fill=self.fg)
    
    def round_rect(self, x1, y1, x2, y2, r, **kwargs):
        # Crea un polígono suavizado con esquinas redondeadas
        points = [x1 + r, y1,
                  x2 - r, y1,
                  x2, y1,
                  x2, y1 + r,
                  x2, y2 - r,
                  x2, y2,
                  x2 - r, y2,
                  x1 + r, y2,
                  x1, y2,
                  x1, y2 - r,
                  x1, y1 + r,
                  x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
      
    def on_click(self):
        if self.command:
            self.command()
    
    def on_enter(self):
        self.itemconfig(self.bg_rect, fill=self.hover_bg, outline=self.hover_bg)
    
    def on_leave(self):
        self.itemconfig(self.bg_rect, fill=self.bg, outline=self.bg)

# --- Aplicación principal con Tkinter ---

class SearchReplaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Modo claro por defecto
        self.dark_mode = False
        self.light_bg = "#f5f5f5"
        self.light_text = "#2c2c2c"
        self.dark_main_bg = "#121212"
        self.dark_text = "#e0e0e0"
        self.entry_light_bg = "#ffffff"
        self.entry_dark_bg = "#1e1e1e"
        self.entry_light_hl = "#cccccc"
        self.entry_dark_hl = "#424242"
        
        self.title("Buscar y Reemplazar - Tkinter")
        self.configure(bg=self.light_bg)
        self.geometry("900x650")
        self.current_file = None  # Archivo actualmente abierto
        self._create_widgets()

    def _create_widgets(self):
        # Frame para operaciones de archivo.
        self.frame_file = tk.Frame(self, bg=self.light_bg)
        self.frame_file.pack(fill=tk.X, padx=10, pady=5)
        
        self.btn_open = RoundedButton(self.frame_file, text="Abrir Archivo", command=self.open_file,
                                 bg="#1976d2", fg="#ffffff")
        self.btn_open.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_save = RoundedButton(self.frame_file, text="Guardar Cambios", command=self.save_file,
                                 bg="#1976d2", fg="#ffffff")
        self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón para cambiar de modo (claro/oscuro)
        self.btn_toggle = RoundedButton(self.frame_file, text="Modo Oscuro", command=self.toggle_theme,
                                        bg="#1976d2", fg="#ffffff")
        self.btn_toggle.pack(side=tk.RIGHT, padx=5, pady=5)

        # Frame para controles de búsqueda y reemplazo.
        self.frame_search = tk.Frame(self, bg=self.light_bg)
        self.frame_search.pack(fill=tk.X, padx=10, pady=5)
        
        # Etiqueta y campo "Buscar:"
        self.lbl_search = tk.Label(self.frame_search, text="Buscar:", bg=self.light_bg, fg=self.light_text)
        self.lbl_search.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_search = tk.Entry(self.frame_search, width=30, bg=self.entry_light_bg, fg=self.light_text,
                                     relief="flat", highlightthickness=1, highlightbackground=self.entry_light_hl)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Botón "Buscar Palabra" justo al lado.
        self.btn_search = RoundedButton(self.frame_search, text="Buscar Palabra", command=self.search_word,
                                        bg="#1976d2", fg="#ffffff")
        self.btn_search.grid(row=0, column=2, padx=5, pady=5)
        
        # Etiqueta y campo "Reemplazar:"
        self.lbl_replace = tk.Label(self.frame_search, text="Reemplazar:", bg=self.light_bg, fg=self.light_text)
        self.lbl_replace.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        self.entry_replace = tk.Entry(self.frame_search, width=30, bg=self.entry_light_bg, fg=self.light_text,
                                      relief="flat", highlightthickness=1, highlightbackground=self.entry_light_hl)
        self.entry_replace.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        
        # Botón "Aplicar Reemplazo"
        self.btn_replace = RoundedButton(self.frame_search, text="Aplicar Reemplazo", command=self.apply_replace,
                                        bg="#d32f2f", fg="#ffffff")
        self.btn_replace.grid(row=0, column=5, padx=5, pady=5)
        
        # Configuración para que los campos de entrada se expandan adecuadamente.
        self.frame_search.columnconfigure(1, weight=1)
        self.frame_search.columnconfigure(4, weight=1)
        
        # Área de texto para mostrar y editar el contenido.
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg=self.light_bg, fg=self.light_text,
                                                   insertbackground=self.light_text)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        if self.dark_mode:
            main_bg = self.dark_main_bg
            label_fg = self.dark_text
            entry_bg = self.entry_dark_bg
            entry_fg = self.dark_text
            entry_hl = self.entry_dark_hl
            text_area_bg = self.entry_dark_bg  # Usamos el mismos tono que en el entry
            text_area_fg = self.dark_text
            toggle_text = "Modo Claro"
        else:
            main_bg = self.light_bg
            label_fg = self.light_text
            entry_bg = self.entry_light_bg
            entry_fg = self.light_text
            entry_hl = self.entry_light_hl
            text_area_bg = self.light_bg
            text_area_fg = self.light_text
            toggle_text = "Modo Oscuro"
            
        # Actualizamos el fondo de la ventana y de los frames.
        self.configure(bg=main_bg)
        self.frame_file.configure(bg=main_bg)
        self.frame_search.configure(bg=main_bg)
        
        # Actualizamos las etiquetas.
        self.lbl_search.configure(bg=main_bg, fg=label_fg)
        self.lbl_replace.configure(bg=main_bg, fg=label_fg)
        
        # Actualizamos los campos de entrada.
        self.entry_search.configure(bg=entry_bg, fg=entry_fg, highlightbackground=entry_hl)
        self.entry_replace.configure(bg=entry_bg, fg=entry_fg, highlightbackground=entry_hl)
        
        # Actualizamos el área de texto.
        self.text_area.configure(bg=text_area_bg, fg=text_area_fg, insertbackground=text_area_fg)
        
        # Actualizamos el botón toggle (su texto y redibuja su contenido).
        self.btn_toggle.text = toggle_text
        self.btn_toggle.draw_button()
        
        # ¡IMPORTANTE! Actualizamos el fondo del Canvas de cada botón redondeado
        # para que coincida con el nuevo color del fondo, evitando que se vea blanco.
        for btn in (self.btn_open, self.btn_save, self.btn_toggle, self.btn_search, self.btn_replace):
            btn.configure(bg=main_bg)
            btn.draw_button()
    
    def open_file(self):
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
        search_term = self.entry_search.get()
        if search_term == "":
            messagebox.showwarning("Advertencia", "El término de búsqueda no puede estar vacío para la búsqueda.")
            return

        # Elimina resaltados anteriores.
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

        # Configuración del resaltado: amarillo claro para coincidencias
        self.text_area.tag_config("highlight", background="#fff59d", foreground="#2c2c2c")
        
        if count_matches == 0:
            messagebox.showinfo("Buscar", f"No se encontraron coincidencias para '{search_term}'.")
        else:
            messagebox.showinfo("Buscar", f"Se encontraron {count_matches} coincidencia(s) para '{search_term}'.")

if __name__ == "__main__":
    app = SearchReplaceApp()
    app.mainloop()