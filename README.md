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
+-------------------+ 
|  Python Script    | 
|  Publicador +     |
|  Simulador        |  
+-------------------+  
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
| Visualización y    |
| Análisis en tiempo |
| real               |
+--------------------+
```

---

# Desarrollo de Práctica
## Puertos
#### Antes de comenzar, en la instancia creada en AWS se agregan los puertos desde la pestaña "Security Groups" para los servicios a utilizar:
<img width="1919" height="873" alt="Captura de pantalla 2025-10-20 220936" src="https://github.com/user-attachments/assets/b12b433f-228e-40c5-ad9d-8c33d9775b33" />

---

## Paso 1. Instalar Mosquitto (MQTT Broker)
#### Instalamos el servicio Mosquitto y sus herramientas de cliente:
```bash
sudo apt install -y mosquitto mosquitto-clients
```
<img width="841" height="145" alt="Captura de pantalla 2025-10-20 185216" src="https://github.com/user-attachments/assets/98a21d3e-85b6-48f3-a6a6-a66069995da2" />

#### Activa y arranca el servicio
```bash
sudo systemctl enable --now mosquitto
sudo systemctl start mosquitto
```
<img width="745" height="97" alt="Captura de pantalla 2025-10-20 185358" src="https://github.com/user-attachments/assets/83093c34-f58a-49d6-a5cb-76ecc71bb7c5" />

#### Verificamos que el servicio este corriendo
```bash
systemctl status mosquitto
```
<img width="1032" height="277" alt="Captura de pantalla 2025-10-20 190105" src="https://github.com/user-attachments/assets/4b04349f-eb67-429f-9aea-7101030bc4bc" />

---

## Paso 2. Instalar InfluxDB2
#### Añadir repositorio
```bash
curl -fsSL https://repos.influxdata.com/influxdata-archive_compat.key | sudo gpg --dearmor -o /usr/share/keyrings/influxdata-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/influxdata-archive-keyring.gpg] https://repos.influxdata.com/debian stable main" | sudo tee /etc/apt/sources.list.d/influxdata.list
```
<img width="1312" height="80" alt="Captura de pantalla 2025-10-20 191026" src="https://github.com/user-attachments/assets/7b551f5b-e403-448a-b0bd-ac1dda092239" />

#### Instalar el servicio
```bash
sudo apt install -y influxdb2
```
<img width="635" height="119" alt="Captura de pantalla 2025-10-20 191609" src="https://github.com/user-attachments/assets/a37a209e-c71a-409f-8041-004b195a15bc" />


#### Activar y arrancar el servicio
```bash
sudo systemctl enable influxdb
sudo systemctl start influxdb
```
#### Verificamos el servicio que este ejecutandose
```bash
systemctl status influxdb
```
<img width="1011" height="247" alt="Captura de pantalla 2025-10-20 191833" src="https://github.com/user-attachments/assets/d97bcc73-681f-4974-a00a-393258a8dd5a" />


#### Por último, creamos nuestro setup de la base de datos
```bash
influx setup
```
<img width="785" height="349" alt="Captura de pantalla 2025-10-20 192628" src="https://github.com/user-attachments/assets/cbedbc9d-37d9-4997-81f2-04b995251e76" />

Nota: la contraseña debe de ser mínimo de 8 dígitos.

---

## Paso 3. Instalar Grafana
#### Instalar dependencias
```bash
sudo apt install -y software-properties-common wget apt-transport-https
```
<img width="1107" height="119" alt="Captura de pantalla 2025-10-20 193052" src="https://github.com/user-attachments/assets/a8f9c90a-8f24-412c-9f05-1a4e4d41dbf0" />

#### Agregamos el repositorio oficial
```bash
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
```
<img width="1080" height="138" alt="Captura de pantalla 2025-10-20 193048" src="https://github.com/user-attachments/assets/b8edd41c-ae70-4852-9196-d0e44a21f98c" />

#### Instalar grafana
```bash
sudo apt install -y grafana
```
<img width="638" height="118" alt="Captura de pantalla 2025-10-20 193936" src="https://github.com/user-attachments/assets/fd3035de-734f-46fc-a8de-28a62688639e" />

#### Habilitar y arrancar
```bash
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```
<img width="1488" height="122" alt="Captura de pantalla 2025-10-20 194056" src="https://github.com/user-attachments/assets/432b53d6-85cc-4173-8dbd-04de5f415cb1" />

#### Verificamos el servicio
```bash
systemctl status grafana-server
```
<img width="1098" height="255" alt="Captura de pantalla 2025-10-20 194214" src="https://github.com/user-attachments/assets/0f6d6f14-f6c9-493e-9750-355131e9cb0f" />

---

## Paso 4. Instalar Tailscale
#### Iniciamos conexión con tailscale
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```
<img width="848" height="133" alt="Captura de pantalla 2025-10-20 184135" src="https://github.com/user-attachments/assets/75b0f9ee-49f6-430a-83ad-ab9ef31b698b" />

#### Una vez instalado el servicio con el siguiente comando iniciamos la conexión
```bash
sudo tailscale up
```
#### Aparecerá el siguiente enlace, donde podemos establece la conexión. Una vez validado el enlace este mandará un mensaje indicando que se conecto con exito.

<img width="603" height="155" alt="Captura de pantalla 2025-10-20 184706" src="https://github.com/user-attachments/assets/6989ffba-c8ce-4c5d-b887-b4101dc58cc0" />

---

## Paso 5. Crear programa en Python
#### Instalar soporte para entornos virtuales
```bash
sudo apt install -y python3-venv
```
<img width="656" height="110" alt="image" src="https://github.com/user-attachments/assets/dc777d39-6ea9-483f-be8c-d2fd260f2c56" />

#### Crear y activar el entorno
```bash
python3 -m venv env
source env/bin/activate
```
<img width="511" height="65" alt="Captura de pantalla 2025-10-20 195126" src="https://github.com/user-attachments/assets/92374057-0700-48db-8eae-e61d69a08c7c" />

#### Instalar librerias
```bash
pip install paho-mqtt influxdb-client
```
<img width="802" height="139" alt="Captura de pantalla 2025-10-20 195238" src="https://github.com/user-attachments/assets/2e483c1c-0b43-45b2-9f00-ab9f4c5faf08" />

#### Creamos el archivo para agregar el código
```bash
nano sensor.py
```
<img width="1919" height="642" alt="Captura de pantalla 2025-10-20 232912" src="https://github.com/user-attachments/assets/aad1a2ef-59b8-46b9-a3cf-04b0befd2ec3" />

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
