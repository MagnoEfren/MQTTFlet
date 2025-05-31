import paho.mqtt.client as mqtt
import threading
import json


class MQTTClient:
    def __init__(self, on_data_callback):
        """
        Args:
            on_data_callback: Función que recibe los datos parseados del JSON
                             Ejemplo: on_data_callback({"n": 2730, "c": 31.0274, "p": 2.92771, "o": 3620})
        """
        self.client = None
        self.on_data_callback = on_data_callback
        self.connected = False
        self.broker = None
        self.port = None
        self.topic = None

    def connect(self, broker, port, topic, client_id, username=None, password=None, tls=False):
        """Conectar al broker MQTT"""
        try:
            # Usar la nueva API v2 para evitar el warning de deprecación
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
            
            if username and password:
                self.client.username_pw_set(username, password)
            if tls:
                self.client.tls_set()

            self.broker = broker
            self.port = port
            self.topic = topic

            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect

            print(f"Conectando a {broker}:{port}...")
            self.client.connect(self.broker, self.port, 60)
            
            # Iniciar loop en hilo separado
            thread = threading.Thread(target=self.client.loop_forever)
            thread.daemon = True
            thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    def on_connect(self, client, userdata, flags, reason_code, properties):
        """Callback cuando se conecta al broker - API v2"""
        if reason_code == 0:
            print(f"✅ Conectado exitosamente al broker")
            print(f"📡 Suscrito al topic: {self.topic}")
            self.client.subscribe(self.topic)
            self.connected = True
        else:
            print(f"❌ Error de conexión. Código: {reason_code}")
            self.connected = False

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        """Callback cuando se desconecta del broker - API v2"""
        print("🔌 Desconectado del broker MQTT")
        self.connected = False

    def on_message(self, client, userdata, msg):
        """Callback cuando llega un mensaje"""
        try:
            # Decodificar el mensaje
            message = msg.payload.decode()
            print(f"📨 Datos recibidos: {message}")
            
            # Parsear JSON
            data = json.loads(message)
            
            # Verificar que tiene la estructura esperada
            if isinstance(data, dict) and all(key in data for key in ['n', 'c', 'p', 'o']):
                # Llamar al callback con los datos parseados
                self.on_data_callback(data)
            else:
                print(f"⚠️ Formato de datos no válido: {message}")
                
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear JSON: {e}")
            print(f"Mensaje recibido: {message}")
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")

    def publish(self, topic, message):
        """Publicar un mensaje"""
        if self.connected and self.client:
            try:
                result = self.client.publish(topic, message)
                if result.rc == 0:
                    print(f"📤 Mensaje enviado a {topic}: {message}")
                    return True
                else:
                    print(f"❌ Error enviando mensaje. Código: {result.rc}")
                    return False
            except Exception as e:
                print(f"❌ Error al publicar: {e}")
                return False
        else:
            print("❌ No conectado al broker")
            return False

    def disconnect(self):
        """Desconectar del broker"""
        if self.client and self.connected:
            self.client.disconnect()
            print("🔌 Desconectando del broker...")