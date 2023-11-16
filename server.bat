@echo off

REM Cambia el directorio al de tu proyecto Django
cd "C:\BetoGame"

REM Activar el entorno virtual si es necesario
REM activate.bat se encuentra en la carpeta "Scripts" del entorno virtual
call "C:\BetoGame\venv\Scripts\activate.bat"

REM Ejecutar el servidor de desarrollo de Django
python manage.py runserver
