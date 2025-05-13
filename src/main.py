import argparse
import sys
import os
from search_replace import search_and_replace
from utils import read_file, write_file, backup_file

def parse_args():
    """
    Define y procesa los argumentos de la línea de comandos.

    Opciones:
      -f/--file: Ruta del archivo donde se realizará la búsqueda y el reemplazo.
      -s/--search: Término de búsqueda.
      -r/--replace: Texto de reemplazo.
      --backup: Bandera opcional para crear una copia de seguridad del archivo original.
      -o/--output: Ruta del archivo de salida. Si no se especifica, se sobrescribe el archivo original.
    """
    parser = argparse.ArgumentParser(
        description="Herramienta de línea de comandos para buscar y reemplazar contenido en archivos de texto."
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Ruta del archivo donde se realizará la operación."
    )
    parser.add_argument(
        "-s", "--search",
        required=True,
        help="Cadena de texto a buscar."
    )
    parser.add_argument(
        "-r", "--replace",
        required=True,
        help="Cadena de texto para reemplazar."
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Crea una copia de seguridad del archivo original."
    )
    parser.add_argument(
        "-o", "--output",
        help="Ruta del archivo de salida. Si no se proporciona, se sobrescribe el archivo original."
    )
    return parser.parse_args()

def main():
    args = parse_args()

    input_file = args.file
    search_term = args.search
    replacement = args.replace
    output_file = args.output if args.output else input_file

    # Verificar si el archivo de entrada existe
    if not os.path.exists(input_file):
        print(f"El archivo '{input_file}' no existe.")
        sys.exit(1)

    # Crear copia de seguridad si se solicita
    if args.backup:
        try:
            backup_path = backup_file(input_file)
            print(f"Copia de seguridad creada en: {backup_path}")
        except Exception as exc:
            print(f"Error al crear la copia de seguridad: {exc}")
            sys.exit(1)

    # Leer el contenido del archivo
    try:
        content = read_file(input_file)
    except Exception as exc:
        print(f"Error al leer el archivo: {exc}")
        sys.exit(1)

    # Aplicar la función de búsqueda y reemplazo
    try:
        modified_content = search_and_replace(content, search_term, replacement)
    except ValueError as ve:
        print(f"Error en la función de búsqueda y reemplazo: {ve}")
        sys.exit(1)

    # Escribir el resultado en el archivo de salida
    try:
        write_file(output_file, modified_content)
        print(f"Archivo guardado exitosamente en: {output_file}")
    except Exception as exc:
        print(f"Error al escribir el archivo: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()