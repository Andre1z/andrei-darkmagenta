"""
Módulo: search_replace.py

Contiene la funcionalidad principal de búsqueda y reemplazo en textos.
"""

def search_and_replace(text: str, search_term: str, replacement: str) -> str:
    """
    Reemplaza todas las ocurrencias del término buscado en el texto por la
    cadena de reemplazo proporcionada.
    
    Args:
        text (str): Cadena de texto en la que se realizará la búsqueda y el reemplazo.
        search_term (str): Término que se buscará en el texto.
        replacement (str): Cadena que sustituirá cada ocurrencia encontrada.
    
    Returns:
        str: Nuevo texto con los términos reemplazados.
    
    Raises:
        ValueError: Se lanza si 'search_term' es una cadena vacía para evitar operaciones indeterminadas.
    """
    if search_term == "":
        raise ValueError("El término de búsqueda no puede estar vacío.")
    
    return text.replace(search_term, replacement)


if __name__ == "__main__":
    # Ejemplo de uso para pruebas rápidas
    ejemplo_texto = "La lluvia en España cae principalmente en la llanura."
    termino_busqueda = "lluvia"
    reemplazo = "tormenta"
    
    try:
        resultado = search_and_replace(ejemplo_texto, termino_busqueda, reemplazo)
        print("Texto original:  ", ejemplo_texto)
        print("Texto modificado:", resultado)
    except ValueError as error:
        print("Error:", error)