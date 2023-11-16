@echo off 
echo.
@REM Obtén la ruta del directorio del script actual
cd %~dp0

@REM Copiamos el proyecto en la carpeta raiz
echo.
echo           INSTALACION DE BETOGAME
echo.

@REM Generamos la base de datos
echo CREANDO BASE DE DATOS
call "C:\Program Files\WinRAR\WinRAR.exe" x -y -o+ "PlataformaWeb\db.rar" "PlataformaWeb"
del "PlataformaWeb\db.rar"
echo Base de Datos: CORRECTO
echo.

@REM Creamos el entorno virtual
echo CREANDO ENTORNO VIRTUAL
cd "PlataformaWeb"
call pip install virtualenv > nul
call py -m venv venv 
echo Entorno Virtual: CORRECTO
echo.
echo INSTALANDO DEPENDENCIAS
call venv\Scripts\activate.bat
call python.exe -m pip install --upgrade pip > nul
call pip install -r requirements.txt > nul
call venv\Scripts\deactivate.bat
echo Instalacion de Dependencias: CORRECTO
echo.
cd %~dp0

@REM Creamos la tarea programada
echo CREANDO TAREA PROGRAMADA DEL SERVIDOR
schtasks /create /tn "EjecutarServidorBetoGame" /tr "C:\BetoGame\servidor.bat"  /sc onstart /ru "NT AUTHORITY\SYSTEM" /f > nul
schtasks /run /tn "EjecutarServidorBetoGame" > nul
echo Tarea Programada para la Ejecucion del Servidor: CORRECTO
echo.

echo INSTLACION FINALIZADA CON EXITO
echo.
pause

start msedge 127.0.0.1:8000