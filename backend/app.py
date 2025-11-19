from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError # Para manejar errores de duplicados en DB
from datetime import datetime
import routeros_api
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- Configuración de la Aplicación Flask ---
app = Flask(__name__)
# Configuración básica y de seguridad
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ispmax_default_secret_key_2025')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'ispmax_default_jwt_secret_2025')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False # Tokens no expiran para simplicidad, ajustar en producción

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ispmax.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@ispmax.com')

# Inicialización de Extensiones
CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)

# --- Modelos de Base de Datos ---
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # IMPORTANTE: En producción, ESTE CAMPO DEBE SER UN HASH DE CONTRASEÑA (e.g., usando bcrypt).
    password = db.Column(db.String(128), nullable=False) 
    ip_address = db.Column(db.String(15), unique=True) # IP debería ser única
    mac_address = db.Column(db.String(17))
    plan_speed = db.Column(db.Integer, default=100)
    plan_price = db.Column(db.Float, default=450.0)
    is_active = db.Column(db.Boolean, default=True)

# --- Servicio de Integración MikroTik ---
class MikroTikService:
    def __init__(self):
        # La conexión se intentará solo cuando sea necesaria
        pass

    def get_api(self):
        """Intenta conectarse y retorna el objeto API, o None si falla."""
        host = os.getenv('MIKROTIK_HOST', '192.168.88.1')
        user = os.getenv('MIKROTIK_USER', 'admin')
        password = os.getenv('MIKROTIK_PASS', '')
        port = int(os.getenv('MIKROTIK_PORT', 8728))

        try:
            # Usamos ApiPool para gestionar la conexión de manera eficiente
            connection = routeros_api.RouterOsApiPool(
                host=host,
                username=user,
                password=password,
                port=port,
                use_ssl=False,
                plaintext_login=True
            )
            api = connection.get_api()
            print("MikroTik conectado con éxito.")
            return api
        except Exception as e:
            print(f"Error conectando MikroTik en {host}:{port}. Error: {e}")
            return None

    def setup_client(self, client):
        """Configura la Cola Simple y el Lease DHCP en MikroTik."""
        api = self.get_api()
        if not api:
            return {"success": False, "message": "No se pudo conectar al MikroTik."}

        # 1. Configurar Queue Simple (limitador de velocidad)
        queue_resource = api.get_resource('/queue/simple')
        queue_name = client.username
        
        # Buscar si la cola ya existe
        existing_queue = queue_resource.get(name=queue_name)

        target_limit = f"{client.plan_speed}M/{client.plan_speed}M"

        try:
            if existing_queue:
                # Si existe, actualizamos
                queue_id = existing_queue[0]['.id']
                queue_resource.set(
                    **{'.id': queue_id}, 
                    target=client.ip_address,
                    **{'max-limit': target_limit}
                )
                print(f"Queue '{queue_name}' actualizada.")
            else:
                # Si no existe, creamos
                queue_resource.add(
                    name=queue_name, 
                    target=client.ip_address,
                    **{'max-limit': target_limit}
                )
                print(f"Queue '{queue_name}' creada.")

            # 2. Configurar Lease DHCP estático
            lease_resource = api.get_resource('/ip/dhcp-server/lease')
            mac = client.mac_address or '00:00:00:00:00:00'
            
            # Buscamos si existe un lease para esa IP
            existing_lease = lease_resource.get(address=client.ip_address)

            if existing_lease:
                # Si existe, actualizamos
                lease_id = existing_lease[0]['.id']
                lease_resource.set(
                    **{'.id': lease_id}, 
                    **{'mac-address': mac},
                    comment=client.username,
                    **{'always-broadcast': 'yes'}
                )
                print(f"Lease para {client.ip_address} actualizado.")
            else:
                # Si no existe, creamos
                lease_resource.add(
                    address=client.ip_address,
                    **{'mac-address': mac},
                    comment=client.username,
                    # Usamos 'always-broadcast=yes' para forzar la estaticidad
                    **{'always-broadcast': 'yes'} 
                )
                print(f"Lease para {client.ip_address} creado.")

            return {"success": True, "message": "Configuración MikroTik completada."}
        
        except routeros_api.exceptions.RouterOsApiCommunicationError as e:
            print(f"Error de comunicación con MikroTik: {e}")
            return {"success": False, "message": f"Error de comunicación con MikroTik: {e}"}
        except Exception as e:
            print(f"Error general al configurar MikroTik: {e}")
            return {"success": False, "message": f"Error general al configurar MikroTik: {e}"}

# Inicialización global del servicio
mikrotik = MikroTikService()

# --- Endpoints de la API ---

@app.route('/api/register', methods=['POST'])
def register():
    """Registra un nuevo cliente y lo configura en MikroTik."""
    data = request.json
    required = ['username', 'email', 'password', 'ip_address', 'plan_speed']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan datos requeridos: username, email, password, ip_address, plan_speed"}), 400

    # Simulando el hash de contraseña (REEMPLAZAR EN PRODUCCIÓN)
    # password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    try:
        client = Client(
            username=data['username'],
            email=data['email'],
            password=data['password'], # Usando texto plano solo para el ejemplo. ¡Cambiar a hash!
            ip_address=data['ip_address'],
            mac_address=data.get('mac_address', '00:00:00:00:00:00'),
            plan_speed=data['plan_speed'],
            plan_price=data['plan_speed'] * 4.5
        )
        db.session.add(client)
        db.session.commit()

        # Configuración en MikroTik
        mikrotik_result = mikrotik.setup_client(client)
        
        if mikrotik_result["success"]:
            return jsonify({"msg": "Cliente creado con éxito y configurado en MikroTik."}), 201
        else:
            # Si MikroTik falla, el cliente se creó en la DB. Podrías querer hacer un rollback.
            # Por ahora, solo reportamos el error de configuración de MT.
            return jsonify({
                "msg": "Cliente creado en DB, pero falló la configuración de MikroTik.",
                "mikrotik_error": mikrotik_result["message"]
            }), 201
            
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El username, email o IP ya están en uso."}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error desconocido al crear cliente: {e}"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Autentica al cliente y retorna un token JWT."""
    data = request.json
    required = ['email', 'password']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan email y/o password"}), 400

    client = Client.query.filter_by(email=data['email']).first()

    # Validar existencia y contraseña
    # IMPORTANTE: Usar bcrypt.check_password_hash(client.password_hash, data['password'])
    if client and client.password == data['password']: 
        token = create_access_token(identity=client.id)
        return jsonify({"token": token, "user_id": client.id})
    
    return jsonify({"error": "Credenciales inválidas"}), 401


@app.route('/api/client/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    """Obtiene la información de un cliente (protegida por JWT)."""
    current_user_id = get_jwt_identity()
    
    # Solo el propio usuario puede ver su perfil (o podrías añadir lógica de rol de Admin)
    if current_user_id != client_id:
        # Aquí podrías añadir un chequeo si el usuario es un administrador
        # if not is_admin(current_user_id):
        #     return jsonify({"error": "Acceso no autorizado"}), 403
        pass # Si el usuario autenticado tiene permiso para ver cualquier ID

    client = db.session.get(Client, client_id)
    if client:
        return jsonify({
            "id": client.id,
            "username": client.username,
            "email": client.email,
            "plan_speed": client.plan_speed,
            "ip_address": client.ip_address,
            "is_active": client.is_active,
            "mac_address": client.mac_address
        })
    return jsonify({"error": "Cliente no encontrado"}), 404

@app.route('/api/send_email', methods=['POST'])
@jwt_required()
def send_test_email():
    """Endpoint para probar la funcionalidad de Flask-Mail."""
    data = request.json
    recipient = data.get('recipient_email')
    
    if not recipient:
        return jsonify({"error": "Falta el correo del destinatario."}), 400
        
    try:
        msg = Message(
            subject="Prueba de Configuración ISPMAX",
            recipients=[recipient],
            body=f"Hola,\n\nEste es un correo de prueba enviado por la API de ISPMAX el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\nSaludos!"
        )
        mail.send(msg)
        return jsonify({"msg": "Correo de prueba enviado con éxito!"}), 200
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return jsonify({"error": f"Fallo al enviar el correo. Revise su configuración de MAIL: {e}"}), 500


# --- Inicialización de la Aplicación ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada o actualizada.")
    
    # IMPORTANTE: Desactivar debug en producción
    app.run(host='0.0.0.0', port=5000, debug=False)
