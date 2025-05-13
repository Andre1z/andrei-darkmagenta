# Andrei DarkMagenta

Andrei DarkMagenta es una aplicación de escritorio desarrollada en Python utilizando Tkinter, que permite realizar operaciones de búsqueda y reemplazo en archivos. La aplicación cuenta con una interfaz gráfica moderna, con soporte para temas claros y oscuros, botones personalizados con esquinas redondeadas y un ícono personalizado.

## Características

- **Interfaz gráfica con Tkinter**: Ventana moderna y personalizable con modos claro y oscuro.
- **Búsqueda y reemplazo de texto**: Permite buscar palabras en un archivo, resaltarlas y aplicar reemplazos.
- **Botones personalizados**: Botones con diseño redondeado y efectos visuales.
- **Soporte para archivos**: Capacidad para abrir y guardar archivos de cualquier tipo.
- **Ícono personalizado**: Utiliza los archivos `darkmagenta.ico` y `darkmagenta.png` ubicados en el directorio `assets`.
- **Versión ejecutable**: Se incluye el ejecutable `search&replace.exe` para usuarios que no requieran el código fuente.

## Estructura del Proyecto

```
andrei-darkmagenta/ ├── .gitattributes ├── README.md # Este archivo (README.txt con formato Markdown) ├── _internal # Archivos internos y utilidades del proyecto ├── assets │ ├── darkmagenta.ico # Ícono en formato ICO │ └── darkmagenta.png # Ícono en formato PNG (usado en la interfaz) ├── search&replace.exe # Versión ejecutable de la aplicación └── src ├── init.py # Inicializa el paquete ├── main_tkinter.py # Punto de entrada de la aplicación gráfica ├── search_replace.py # Lógica de búsqueda y reemplazo de texto └── utils.py # Funciones utilitarias para manejo de archivos
```

## Uso

### Versión Ejecutable

Para usar la aplicación sin necesidad de instalar Python, simplemente ejecute el archivo: `search&replace.exe`


### Desde el Código Fuente

Si deseas ejecutar la aplicación desde el código fuente, asegúrate de tener Python 3.6 o superior instalado junto con Tkinter (incluido en la mayoría de las distribuciones de Python). Luego, sigue estos pasos:

1. Abre una terminal y navega hasta el directorio `src`:
    ```bash
    cd src
    ```
2. Ejecuta la aplicación:
    ```bash
    python main_tkinter.py
    ```

La aplicación se abrirá con una interfaz gráfica que te permitirá:

- Abrir y visualizar el contenido de cualquier archivo.
- Buscar y resaltar una palabra especificada.
- Aplicar cambios de reemplazo en el texto.
- Guardar los cambios realizados.
- Alternar entre modos claro y oscuro.

## Requisitos

- **Python**: Versión 3.6 o superior.
- **Tkinter**: Generalmente incluido en las instalaciones estándar de Python.

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Si deseas colaborar, por favor:

1. Haz un *fork* del repositorio.
2. Realiza tus cambios y mejoras.
3. Envía un *pull request* para revisión.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

¡Disfruta usando Andrei DarkMagenta y optimiza tu flujo de trabajo en la edición de archivos!