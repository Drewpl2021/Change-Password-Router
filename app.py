import requests
import schedule
import time
from datetime import datetime
import random
import string

# Configuración del router
ROUTER_IP = "192.168.1.1"  # Cambia a la IP de tu router
USERNAME = "admin"          # Usuario del router
PASSWORD = "admin"          # Contraseña del router
WIFI_SETTINGS_URL = f"http://{ROUTER_IP}/change_password"  # URL específica para cambiar el wifi

# Función para generar una nueva contraseña aleatoria
def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    new_password = ''.join(random.choice(characters) for i in range(length))
    return new_password

# Función para cambiar la contraseña de wifi
def change_wifi_password():
    # Nueva contraseña generada aleatoriamente
    new_password = generate_password()
    
    # Datos necesarios para el cambio de configuración
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "wifi_password": new_password
    }
    
    # Autenticación en la interfaz del router (esto depende de la configuración exacta de tu router)
    session = requests.Session()
    login_url = f"http://{ROUTER_IP}/login"  # URL de inicio de sesión del router
    session.post(login_url, data={"username": USERNAME, "password": PASSWORD})
    
    # Enviar solicitud para cambiar la contraseña
    response = session.post(WIFI_SETTINGS_URL, data=payload)
    
    if response.status_code == 200:
        print(f"Contraseña de wifi cambiada con éxito a las {datetime.now()} a: {new_password}")
    else:
        print(f"Error al cambiar la contraseña. Código de estado: {response.status_code}")

# Programar el cambio de contraseña a las 3 p.m. todos los días
schedule.every().day.at("15:00").do(change_wifi_password)

print("Automatización de cambio de contraseña iniciada. La contraseña se actualizará todos los días a las 3 p.m.")

# Mantener el script en ejecución
while True:
    schedule.run_pending()
    time.sleep(1)
