import os
import json

# ---------------------------
# CONFIGURACIÓN DE USUARIOS
# ---------------------------
ADMIN_ID = 7293647496 # Reemplaza con el ID real del administrador
USERS_DB_FILE = "usuarios.json"

def load_users() -> list:
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, "r") as f:
            return json.load(f)
    else:
        return [ADMIN_ID]

def save_users(users: list) -> None:
    with open(USERS_DB_FILE, "w") as f:
        json.dump(users, f)

USUARIOS_AUTORIZADOS = load_users()
FREE_MODE = True  # Modo libre (si es True, no se exige autorización)

# ---------------------------
# CONFIGURACIÓN DE CANALES Y GRUPOS
# ---------------------------
# IDs de canales obligatorios (normalmente negativos)
REQUIRED_CHANNELS = [
    -1002523446802,  # Reemplaza con el ID real del primer canal obligatorio
    -1002299771420   # Reemplaza con el ID real del segundo canal obligatorio
]

# URLs de los canales obligatorios, para que el usuario pueda unirse
REQUIRED_CHANNELS_URLS = {
    "grupo1": "https://t.me/nequi_bot_of",  # Reemplaza por el enlace real
    "grupo2": "https://t.me/nequibotfree"   # Reemplaza por el enlace real
}

# Chats (grupos o canales) en los que el bot está autorizado a funcionar
ALLOWED_CHATS = [
    -1002523446802  #conemplaza con el ID real de un grupo o canal autorizado
]

# Enlace al grupo autorizado (para notificar en caso de uso en chats no permitidos)
ALLOWED_CHAT_LINK = "https://t.me/nequibotfree"  # Reemplaza con el enlace real

# ---------------------------
# CONFIGURACIÓN DE FUENTES
# ---------------------------
FONT_PATH = "fuentes/fuente.ttf"           # Ruta a la fuente principal
FONT_MOVIMIENTOS_PATH = "fuente.ttf" # Ruta a la fuente para movimientos (si es diferente)

# ---------------------------
# CONFIGURACIÓN DE COMPROBANTES
# ---------------------------
COMPROBANTES = {
    "comprobante1": {
        "template": "img/plantilla1.jpg",  # Ruta a la plantilla del comprobante 1
        "output": "comprobante1_generado.png",
        "styles": {
            "nombre": {"size": 40, "color": "#1b0b19", "pos": (100, 885)},
            "telefono": {"size": 40, "color": "#1b0b19", "pos": (200, 1080)},
            "valor1": {"size": 40, "color": "#1b0b19", "pos": (300, 980)},
            "fecha": {"size": 40, "color": "#1b0b19", "pos": (60, 1200)},
        },
    },
    "comprobante2": {
        "template": "img/plantilla2.jpeg",
        "output": "comprobante2_generado.png",
        "styles": {
            "nombre": {"size": 28, "color": "#1b0b19", "pos": (86, 575)},
            "telefono": {"size": 28, "color": "#1b0b19", "pos": (86, 735)},
            "valor1": {"size": 28, "color": "#1b0b19", "pos": (86, 670)},
            "fecha": {"size": 28, "color": "#1b0b19", "pos": (86, 820)},
        },
    },
    "comprobante3": {
        "template": "img/plantilla3.jpeg",
        "output": "comprobante3_generado.png",
        "styles": {
            "nombre": {"size": 30, "color": "#1b0b19", "pos": (-8000, 795)},
            "telefono": {"size": 30, "color": "#1b0b19", "pos": (500, 895)},
            "valor1": {"size": 30, "color": "#1b0b19", "pos": (50, 845)},
            "fecha": {"size": 30, "color": "#1b0b19", "pos": (50, 970)},
        },
    },
    "comprobante4": {
        "template": "img/plantilla4.jpg",
        "output": "comprobante4_generado.png",
        "styles": {
            "nombre": {"size": 23, "color": "#1b0b19", "pos": (9999, 99999)},  # No se muestra
            "telefono": {"size": 24, "color": "#1b0b19", "pos": (400, 485)},
            "valor1": {"size": 23, "color": "#1b0b19", "pos": (630, 540)},
            "fecha": {"size": 23, "color": "#1b0b19", "pos": (60, 620)},
        },
    },
    "comprobante5": {
        "template": "img/plantilla5.jpg",
        "output": "comprobante5_generado.png",
        "styles": {
            "nombre": {"size": 22, "color": "#1b0b19", "pos": (230, 430)},
            "telefono": {"size": 22, "color": "#1b0b19", "pos": (200, 604)},
            "valor1": {"size": 22, "color": "#1b0b19", "pos": (200, 700)},
            "fecha": {"size": 22, "color": "#1b0b19", "pos": (200, 960)},  # No se dibuja en comprobante5
            "cc": {"size": 22, "color": "#1b0b19", "pos": (200, 800)},
        },
    },
    "movimientos": {
        "template": "img/movimientos.jpg",
        "output": "movimiento_generado.png",
        "styles": {
            "nombre": {"size": 30, "color": "#1b0b19", "pos": (40, 465)},
            "valor1": {"size": 30, "color": "#007500", "pos": (10, 45)},
        },
    },
}

# ---------------------------
# CONFIGURACIÓN DE LOS CAMPOS DE CONVERSACIÓN
# ---------------------------
conversation_fields = {
    "comprobante1": [
        ("name", "👤 Digite el nombre:"),
        ("phone", "📞 Digite el número:"),
        ("value", "💸 Digite el valor:")
    ],
    "comprobante2": [
        ("name", "👤 Digite el nombre:"),
        ("phone", "📞 Digite el número:"),
        ("value", "💸 Digite el valor:")
    ],
    "comprobante3": [
        ("name", "👤 Digite el nombre:"),
        ("phone", "📞 Digite el número:"),
        ("value", "💸 Digite el valor:")
    ],
    "comprobante4": [
        ("phone", "📞 Digite el número:"),
        ("value", "💸 Digite el valor:")
    ],
    "comprobante5": [
        ("name", "👤 Digite el nombre:"),
        ("phone", "📞 Digite el número:"),
        ("value", "💸 Digite el valor:"),
        ("cc", "🎫 Comprobante el CC:")
    ],
    "movimientos": [
        ("name", "Digite el nombre:"),
        ("value", "Digite el valor:")
    ]
}

# Títulos para mostrar en los prompts de conversación
comprobante_titles = {
    "comprobante1": "Comprobante 1",
    "comprobante2": "Comprobante 2",
    "comprobante3": "Comprobante 3",
    "comprobante4": "Comprobante 4",
    "comprobante5": "Comprobante 5",
    "movimientos": "Movimientos"
}