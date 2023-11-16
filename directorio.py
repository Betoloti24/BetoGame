import os
import shutil
import ctypes

# Desactivar el atributo de solo lectura para la carpeta y su contenido
def remove_readonly(func, path, _):
    os.chmod(path, os.stat.S_IWRITE)
    func(path)
def copy_directory_contents(source_directory, destination_directory):
    # Define los atributos de archivo para ocultar
    FILE_ATTRIBUTE_HIDDEN = 0x02
    try:
        for item in os.listdir(source_directory):
            source_item = os.path.join(source_directory, item)
            destination_item = os.path.join(destination_directory, item)
            
            if (destination_item[-4:] != 'venv'):
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, destination_item)
                else:
                    shutil.copy2(source_item, destination_item)
                
                # Oculta el archivo o directorio que tiene nombre de .git en Windows
                if (destination_item[-4:] == '.git'):
                    ret = ctypes.windll.kernel32.SetFileAttributesW(destination_item, FILE_ATTRIBUTE_HIDDEN)

    except Exception as e:
        print(f"Error al copiar el directorio: {e}")


if __name__ == "__main__":
    # Obtiene el directorio actual
    source_directory = os.getcwd()

    # Obtiene el directorio padre del directorio actual
    # source_directory = os.path.dirname(source_directory)

    # Agrega el directorio de 'Programa' al resultado final
    source_directory = os.path.join(source_directory, 'BetoGame')

    destination_directory = r"C:\\BetoGame" # Ruta del directorio destino
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory, exist_ok=True)

    copy_directory_contents(source_directory, destination_directory)