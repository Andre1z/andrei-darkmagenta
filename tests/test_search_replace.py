import os
import sys
import unittest

# Agrega el directorio 'src' al path para poder importar el módulo search_replace.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from search_replace import search_and_replace

class TestSearchReplace(unittest.TestCase):
    """Pruebas unitarias para la funcionalidad de búsqueda y reemplazo."""

    def test_basic_replacement(self):
        """Prueba que se reemplace correctamente una ocurrencia simple."""
        text = "Hola mundo"
        search_term = "mundo"
        replacement = "Python"
        expected = "Hola Python"
        result = search_and_replace(text, search_term, replacement)
        self.assertEqual(result, expected)

    def test_multiple_replacements(self):
        """Prueba que se reemplacen todas las ocurrencias múltiples en un texto."""
        text = "uno, dos, uno, tres, uno"
        search_term = "uno"
        replacement = "1"
        expected = "1, dos, 1, tres, 1"
        result = search_and_replace(text, search_term, replacement)
        self.assertEqual(result, expected)

    def test_no_occurrence(self):
        """Prueba que si no se encuentra la cadena a buscar, se retorne el texto original."""
        text = "Sin coincidencias en este texto."
        search_term = "inexistente"
        replacement = "algo"
        expected = text
        result = search_and_replace(text, search_term, replacement)
        self.assertEqual(result, expected)

    def test_empty_text(self):
        """Prueba que al pasar un texto vacío se retorne una cadena vacía."""
        text = ""
        search_term = "algo"
        replacement = "nada"
        expected = ""
        result = search_and_replace(text, search_term, replacement)
        self.assertEqual(result, expected)

    def test_empty_replacement(self):
        """Prueba que al reemplazar con una cadena vacía se eliminen las ocurrencias."""
        text = "Eliminar palabra palabra"
        search_term = "palabra"
        replacement = ""
        expected = text.replace(search_term, replacement)
        result = search_and_replace(text, search_term, replacement)
        self.assertEqual(result, expected)

    def test_empty_search_term(self):
        """
        Prueba que la función lance ValueError cuando la cadena a buscar está vacía.
        Se evita así una operación indeterminada.
        """
        text = "Texto de prueba"
        search_term = ""
        replacement = "algo"
        with self.assertRaises(ValueError):
            search_and_replace(text, search_term, replacement)

if __name__ == "__main__":
    unittest.main()