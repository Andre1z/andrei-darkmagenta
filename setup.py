#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

# Obtiene la ruta del directorio actual.
here = os.path.abspath(os.path.dirname(__file__))

# Lee el contenido del README para la descripción extendida.
with open(os.path.join(here, 'docs', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="andrei-darkmagenta",
    version="0.1.0",
    description="Proyecto para buscar y reemplazar términos en archivos de texto en Windows 11.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Andrei Buga",                      # Reemplaza con tu nombre si lo deseas.
    author_email="bugaandrei1@gmail.com",    # Reemplaza con tu email.
    url="https://github.com/Andre1z/andrei-darkmagenta",  # Si tienes un repositorio, actualiza la URL.
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        # Agrega aquí las dependencias necesarias (por ejemplo, "requests>=2.25.1")
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",  # Indicamos que se orienta a Windows.
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            # Asegúrate de tener una función `main()` en el archivo `main.py` para que este entry point funcione.
            'buscar-reemplazar=main:main',
        ],
    },
)