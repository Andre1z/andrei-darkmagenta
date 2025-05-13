"""
Paquete principal para el proyecto "Buscar y Reemplazar".

Este paquete contiene la funcionalidad de búsqueda y reemplazo en textos,
así como utilidades para el manejo de archivos.
"""

__version__ = "0.1.0"

# Importamos las funciones que se consideren parte de la API pública del paquete.
from .search_replace import search_and_replace
from .utils import read_file, write_file, backup_file