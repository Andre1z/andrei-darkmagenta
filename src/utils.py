"""
Módulo de utilidades para el proyecto Buscar y Reemplazar.

Este módulo incluye funciones auxiliares para:
- Leer archivos de texto.
- Escribir contenido en archivos.
- Crear copias de seguridad de archivos.
"""

import os
import shutil

def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """
    Lee el contenido de un archivo y lo devuelve como una cadena.

    Args:
        file_path (str): Ruta del archivo a leer.
        encoding (str): Codificación del archivo (por defecto 'utf-8').

    Returns:
        str: Contenido del archivo.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        IOError: Si ocurre un error al leer el archivo.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")
    
    try:
        with open(file_path, "r", encoding=encoding) as file:
            content = file.read()
        return content
    except Exception as e:
        raise IOError(f"Error al leer el archivo '{file_path}': {e}")

def write_file(file_path: str, content: str, encoding: str = "utf-8") -> None:
    """
    Escribe el contenido proporcionado en un archivo.

    Args:
        file_path (str): Ruta del archivo donde se escribirá.
        content (str): Texto a escribir en el archivo.
        encoding (str): Codificación a usar (por defecto 'utf-8').

    Raises:
        IOError: Si ocurre un error al escribir en el archivo.
    """
    try:
        with open(file_path, "w", encoding=encoding) as file:
            file.write(content)
    except Exception as e:
        raise IOError(f"Error al escribir en el archivo '{file_path}': {e}")

def backup_file(file_path: str) -> str:
    """
    Crea una copia de seguridad del archivo especificado.
    La copia se guarda en la misma ruta con la extensión ".bak".

    Args:
        file_path (str): Ruta del archivo original.

    Returns:
        str: Ruta del archivo de copia de seguridad.

    Raises:
        FileNotFoundError: Si el archivo original no existe.
        IOError: Si ocurre un error al crear la copia de seguridad.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")
    
    backup_path = file_path + ".bak"
    try:
        shutil.copy(file_path, backup_path)
        return backup_path
    except Exception as e:
        raise IOError(f"Error al crear la copia de seguridad para '{file_path}': {e}")

if __name__ == "__main__":
    # Código de prueba para validar el funcionamiento de las funciones.
    test_file = "test.txt"
    try:
        # Escribir un archivo de prueba.
        write_file(test_file, "Este es el contenido de prueba.\nLinea 2 del contenido.")
        print("Archivo escrito exitosamente.")

        # Leer el archivo y mostrar contenido.
        contenido = read_file(test_file)
        print("Contenido leído:")
        print(contenido)

        # Crear copia de seguridad del archivo.
        backup = backup_file(test_file)
        print(f"Copia de seguridad creada en: {backup}")
    except Exception as error:
        print("Se produjo un error:", error)
    finally:
        # Limpieza: elimina los archivos de prueba y su copia de seguridad si existen.
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(test_file + ".bak"):
            os.remove(test_file + ".bak")