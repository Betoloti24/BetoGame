import requests

def obtener_respuesta_api(url):
    try:
        # Realizar la solicitud a la API
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Imprimir el contenido de la respuesta en formato JSON
            print("Respuesta de la API:")
            print(response.json()['results'][0]['bcv'])
        else:
            print(f"Error en la solicitud a la API. Código de estado: {response.status_code}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

# URL de ejemplo de una API pública (puedes cambiarla por la que desees utilizar)
url_api = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/history"

# Llamar a la función con la URL de la API
obtener_respuesta_api(url_api)
