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
andrei-darkmagenta/
├── .gitattributes      # Configuraciones específicas de Git (por ejemplo, normalización de finales de línea).
├── README.md           # Documentación del proyecto en formato Markdown, con instrucciones de uso, características y demás información relevante.
├── _internal           # Carpeta reservada para archivos internos o scripts de soporte que no se distribuyen directamente.
├── assets              # Directorio de recursos gráficos e íconos.
│   ├── darkmagenta.ico # Ícono de la aplicación en formato ICO (usado generalmente en Windows).
│   └── darkmagenta.png # Imagen en formato PNG usada como ícono en la interfaz de la aplicación.
├── search&replace.exe  # Ejecutable de la aplicación para usuarios que prefieren no trabajar con el código fuente.
└── src                 # Directorio que contiene el código fuente de la aplicación.
    ├── __init__.py     # Inicializa el paquete, definiendo la API pública del proyecto.
    ├── main_tkinter.py # Punto de entrada de la aplicación, que contiene la interfaz gráfica basada en Tkinter.
    ├── search_replace.py  # Módulo que implementa la lógica principal de búsqueda y reemplazo de texto.
    └── utils.py        # Módulo con funciones utilitarias (por ejemplo, lectura/escritura de archivos, validaciones, etc.).

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



