@echo off 
echo.
echo          DESINSTALACION DE BETOGAME
echo.
cd %~dp0

@REM Deshabilitamos y borramos la tarea programada
echo CONFIGRUACION DEL USUARIO
git config --global user.email "roiberthgonzalez091d@gmail.com"
git config --global user.name "Betoloti24"
echo Configuracion de Usuario: CORRECTA
echo.

@REM Ejecutamos la actualizacion de la rama
echo EJECUCION DE LA ACTUALIZACION
git pull origin main 
echo.
echo HA FINALIZADO EL PROCESO DE ACTUALIZACION
echo.
pause