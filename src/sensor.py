import json
import time
import random
import threading
from paho.mqtt.client import Client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuración InfluxDB
url = "http://100.121.224.89:8086"
token = "TU_TOKEN"
org = "SistemasProgramables"
bucket = "Temperatura"

# Conectar a InfluxDB
client_influx = InfluxDBClient(url=url, token=token, org=org)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)

# Configuración MQTT
broker = "100.121.224.89"
port = 1883
topic = "sensor"

# Cliente MQTT suscriptor
mqtt_sub = Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado exitosamente a MQTT Broker")
    else:
        print(f"Error de conexión MQTT, rc={rc}")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        point = Point("air_quality") \
            .tag("sensor", "simulado") \
            .field("co", float(payload["co"])) \
            .field("no2", float(payload["no2"])) \
            .field("o3", float(payload["o3"])) \
            .time(payload.get("timestamp", int(time.time())), WritePrecision.S)
        write_api.write(bucket=bucket, org=org, record=point)
        # Mostrar datos en consola
        print(f"Datos recibidos y guardados: {payload}")
    except Exception as e:
        print(f"Error al procesar mensaje: {e}")

mqtt_sub.on_connect = on_connect
mqtt_sub.on_message = on_message
mqtt_sub.connect(broker, port, 60)
mqtt_sub.loop_start()  # Corre en background

# Cliente MQTT publicador
mqtt_pub = Client()
mqtt_pub.connect(broker, port, 60)
mqtt_pub.loop_start()

# Mensaje de conexión a InfluxDB
try:
    client_influx.health()  # Verifica conexión a InfluxDB
    print("Conectado exitosamente a InfluxDB 2")
except Exception as e:
    print(f"Error de conexión InfluxDB: {e}")

# Publicación de datos simulados
while True:
    data = {
        "co": round(random.uniform(0.1, 2.0), 3),
        "no2": round(random.uniform(5, 50), 1),
        "o3": round(random.uniform(10, 100), 1),
        "timestamp": int(time.time())
    }
    mqtt_pub.publish(topic, json.dumps(data))
    print(f"Datos publicados: {data}")
    time.sleep(2)
