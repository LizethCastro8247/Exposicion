# Monitoreo de Calidad del Aire (CO, NO₂, O₃)
**Nombre:** Lizeth Roxana Castro Reyes - 22211535  
**Materia:** Sistemas Programables

# Introducción
El proyecto consiste en diseñar e implementar un sistema de monitoreo de la calidad del aire, enfocado en los principales contaminantes atmosféricos: monóxido de carbono (CO), dióxido de nitrógeno (NO₂) y ozono (O₃). Este sistema permitirá la recolección de datos en tiempo real mediante sensores, inicialmente simulados, la transmisión de los datos mediante MQTT, su almacenamiento en InfluxDB y la visualización en Grafana. La arquitectura se implementará sobre una instancia en AWS, asegurando acceso remoto y escalabilidad.

# Objetivo General
Desarrollar un sistema integral de monitoreo de la calidad del aire que permita la recolección, almacenamiento, visualización y análisis de datos de CO, NO₂ y O₃ en tiempo real.

# Objetivos Específicos
1. Simular la adquisición de datos de sensores de CO, NO₂ y O₃.
2. Publicar los datos en tiempo real mediante el protocolo MQTT.
3. Almacenar los datos de manera estructurada y segura en InfluxDB.
4. Visualizar y analizar los datos en tiempo real en Grafana
5. Garantizar acceso remoto seguro mediante Tailscale y AWS.

# Justificación técnica
El sistema permite monitorear en tiempo real los niveles de CO, NO₂ y O₃ mediante sensores simulados, publicando datos por MQTT, almacenándolos en InfluxDB 2 y visualizándolos en Grafana. La arquitectura en AWS y el acceso seguro con Tailscale garantizan disponibilidad, escalabilidad y confiabilidad, ofreciendo una herramienta eficiente para la gestión ambiental basada en datos, ofreciendo una herramienta eficiente para la gestión ambiental basada en datos y con capacidad de ampliación a sensores físicos y alertas automáticas.


# Diagrama de arquitectua
```bash
+-------------------+
|  Sensores         |
|  (CO, NO₂, O₃)    |
|  Simulados        |
+---------+---------+
          |
          | Datos MQTT
          v
+-------------------+
|  Broker MQTT      |
|  (Mosquitto)      |
|  AWS / Local      |
+---------+---------+
          |
          | Suscripción y Publicación
          v
+-------------------+             +--------------------+
|  Python Script    |             |  Python Script     |
|  Publicador +     |------------>|  Suscriptor +      |
|  Simulador        |             |  InfluxDB Writer   |
+-------------------+             +---------+----------+
                                             |
                                             | Escritura de datos
                                             v
                                   +--------------------+
                                   |  InfluxDB 2        |
                                   |  Series Temporales |
                                   +---------+----------+
                                             |
                                             | Consulta de datos
                                             v
                                   +--------------------+
                                   | Grafana Dashboard  |
                                   | Visualización y   |
                                   | Análisis en tiempo |
                                   | real               |
                                   +--------------------+
```

---

# Desarrollo de Práctica
## Puertos
#### Antes de comenzar, en la instancia creada en AWS se agregan los puertos desde la pestaña "Security Groups" para los servicios a utilizar:
<img width="1919" height="873" alt="imagen" src="https://github.com/user-attachments/assets/59b23808-c53d-466b-b9e3-279e236e85cd" />

---

## Paso 1. Instalar Mosquitto (MQTT Broker)
#### Instalamos el servicio Mosquitto y sus herramientas de cliente:
```bash
sudo apt install -y mosquitto mosquitto-clients
```

<img width="841" height="145" alt="imagen" src="https://github.com/user-attachments/assets/4b30ee11-5168-4bc0-bc0e-c45a82d17f80"/>

#### Activa y arranca el servicio
```bash
sudo systemctl enable --now mosquitto
sudo systemctl start mosquitto
```
<img width="745" height="97" alt="imagen" src="https://github.com/user-attachments/assets/4b56dfe1-ae03-4cb0-9f15-5f31de191848" />

#### Verificamos que el servicio este corriendo
```bash
systemctl status mosquitto
```
<img width="1032" height="277" alt="imagen" src="https://github.com/user-attachments/assets/1ddf26cd-28d1-45f1-bab5-4efd02c8206a" />

---

## Paso 2. Instalar InfluxDB2
#### Añadir repositorio
```bash
curl -fsSL https://repos.influxdata.com/influxdata-archive_compat.key | sudo gpg --dearmor -o /usr/share/keyrings/influxdata-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/influxdata-archive-keyring.gpg] https://repos.influxdata.com/debian stable main" | sudo tee /etc/apt/sources.list.d/influxdata.list
```
<img width="1312" height="80" alt="imagen" src="https://github.com/user-attachments/assets/30b5788d-389e-413c-b2c6-160db814a27d" />

#### Instalar el servicio
```bash
sudo apt install -y influxdb2
```
<img width="635" height="119" alt="imagen" src="https://github.com/user-attachments/assets/8249b626-4d78-4863-a82c-e8eb723420b9" />

#### Activar y arrancar el servicio
```bash
sudo systemctl enable influxdb
sudo systemctl start influxdb
```
#### Verificamos el servicio que este ejecutandose
```bash
systemctl status influxdb
```
<img width="1011" height="247" alt="imagen" src="https://github.com/user-attachments/assets/8c0a66ff-dd54-4e09-a122-2996bb4ab6fc" />

#### Por último, creamos nuestro setup de la base de datos
```bash
influx setup
```
<img width="785" height="349" alt="imagen" src="https://github.com/user-attachments/assets/98ba4fa5-54b0-4e79-966a-81986e8172a2" />

Nota: la contraseña debe de ser mínimo de 8 dígitos.

---

## Paso 3. Instalar Grafana
#### Instalar dependencias
```bash
sudo apt install -y software-properties-common wget apt-transport-https
```
<img width="1107" height="119" alt="imagen" src="https://github.com/user-attachments/assets/1bff8ddf-40ae-4be0-b85a-54df844c76a1" />

#### Agregamos el repositorio oficial
```bash
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
```

#### Instalar grafana
```bash
sudo apt install -y grafana
```
<img width="638" height="118" alt="imagen" src="https://github.com/user-attachments/assets/171144a3-e7cb-4e1a-bbfe-f3f58783825c" />

#### Habilitar y arrancar
```bash
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```
<img width="1488" height="122" alt="imagen" src="https://github.com/user-attachments/assets/d9fcde31-93d3-4ade-be1b-276cbc52eeda" />

#### Verificamos el servicio
```bash
systemctl status grafana-server
```
<img width="1098" height="255" alt="imagen" src="https://github.com/user-attachments/assets/56375e26-41bc-44ec-ab40-b3b15cb1a0f4" />

---

## Paso 4. Instalar Tailscale
#### Iniciamos conexión con tailscale
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

#### Una vez instalado el servicio con el siguiente comando iniciamos la conexión
```bash
sudo tailscale up
```
#### Aparecerá el siguiente enlace, donde podemos establece la conexión. Una vez validado el enlace este mandará un mensaje indicando que se conecto con exito.

<img width="603" height="155" alt="imagen" src="https://github.com/user-attachments/assets/b5d1c1a2-a9b3-46e1-928f-0d467f67a5f8" />

---

## Paso 5. Crear programa en Python
#### Instalar soporte para entornos virtuales
```bash
sudo apt install -y python3-venv
```
<img width="656" height="110" alt="imagen" src="https://github.com/user-attachments/assets/61e49a73-6626-4c84-93c1-c3758d781caa" />

#### Crear y activar el entorno
```bash
python3 -m venv env
source env/bin/activate
```
<img width="511" height="65" alt="imagen" src="https://github.com/user-attachments/assets/301f8baa-ab1e-45e0-8251-64045147fd0d" />

#### Instalar librerias
```bash
pip install paho-mqtt influxdb-client
```
<img width="802" height="139" alt="imagen" src="https://github.com/user-attachments/assets/55a937c0-b858-44b7-b9d3-5cfba4f22d9a" />

#### Creamos el archivo para agregar el código
```bash
nano sensor.py
```
<img width="1919" height="642" alt="imagen" src="https://github.com/user-attachments/assets/04fd1832-5ea5-4907-9b82-f941a2f74fd4" />


#### Por último se inicia el programa
```bash
pyhton3 sensor.py
```

---

# Verificación
## Consola
Los datos se imprimen en la consola
<img width="1315" height="590" alt="Captura de pantalla 2025-10-20 214703" src="https://github.com/user-attachments/assets/8a58650d-e495-43c4-86a2-873e835a0bb7" />

## InfluxDB
Los datos se van almacenando
Calidad de aire
<img width="1920" height="1080" alt="Captura de pantalla 2025-10-20 214819" src="https://github.com/user-attachments/assets/bf1b8990-a4f9-4cf8-825b-7a4ee36ebec3" />

Monóxido de carbono (Co)
<img width="1917" height="883" alt="image" src="https://github.com/user-attachments/assets/40f8353f-327e-4a06-9c6f-2fed6fca5146" />

Dióxido de nitrógeno (no2)
<img width="1918" height="889" alt="image" src="https://github.com/user-attachments/assets/e9eb35c0-a83f-4d36-a0c7-2cbf97296d8d" />

Ozono (O3)
<img width="1919" height="879" alt="image" src="https://github.com/user-attachments/assets/89385f10-9097-4c1f-8200-5f697c5fb43c" />

## Grafana
Se muestran cada uno de los datos
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/102216c1-aba4-48bc-ac81-b00f41226f66" />

## MQTT
Desde la aplicación de "MQTT Explorer" en PC
<img width="1264" height="892" alt="Captura de pantalla 2025-10-20 220502" src="https://github.com/user-attachments/assets/c149d9ff-d99b-47b5-8dcb-ccab529c4a0d" />

Desde la Aplicación de "MyMQTT" en dispositivo móvil
![Captura de pantalla 2025-10-20 a las 22 13 49_2d81b373](https://github.com/user-attachments/assets/2512deaf-d492-4218-8842-c46c65a89ecb)

---
