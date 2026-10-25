"""
SUMMARY:
Script simulador y emulador del protocolo ADMS para el dispositivo biométrico ZKTeco K40.
Permite enviar peticiones HTTP POST con eventos de marcaje hacia el backend de SystemBioTrack
para desacoplar las pruebas de la lógica de asistencia del hardware físico.
"""

from datetime import datetime
import requests

# -------------------------------------------------------------------------
# Variables de configuración del cliente emulador (Formato: Ejemplo_Variable)
# -------------------------------------------------------------------------
Url_Servidor: str = "http://127.0.0.1:8000/api/asistencia/adms"
Id_Empleado_Prueba: int = 101  # Coincide con el empleado semilla cargado en PostgreSQL
Tipo_Evento_Default: str = "Entrada"


def simular_envio_marcaje(Id_Biometrico: int, Tipo_Evento: str = "Entrada") -> None:
    """
    SUMMARY:
    Construye la carga útil del evento y realiza el envío HTTP simulando al ZKTeco K40.
    """
    Payload_Marcaje: dict = {
        "id_empleado_biometrico": Id_Biometrico,
        "fecha_hora_marcaje": datetime.now().isoformat(),
        "tipo_marcaje": Tipo_Evento
    }

    Headers_Peticion: dict = {
        "User-Agent": "ZKTeco-K40-PushClient/1.0",
        "Content-Type": "application/json"
    }

    print(f"[*] Enviando marcaje simulado para ID biométrico: {Id_Biometrico}...")

    try:
        Respuesta_Servidor = requests.post(
            Url_Servidor,
            json=Payload_Marcaje,
            headers=Headers_Peticion,
            timeout=5
        )
        print(f"[+] Código HTTP recibido: {Respuesta_Servidor.status_code}")
        print(f"[+] Contenido de respuesta: {Respuesta_Servidor.text}")
    except requests.exceptions.ConnectionError:
        print("[!] Nota esperada: El servidor FastAPI aún no expone este endpoint (se implementa en la Fase 2).")
    except Exception as Error_Excepcion:
        print(f"[-] Ocurrió un error inesperado durante el envío: {Error_Excepcion}")


if __name__ == "__main__":
    # Marcaje de prueba con el empleado semilla configurado
    simular_envio_marcaje(Id_Biometrico=Id_Empleado_Prueba, Tipo_Evento=Tipo_Evento_Default)