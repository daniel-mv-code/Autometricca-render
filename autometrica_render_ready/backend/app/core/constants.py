"""
Constantes globales y Enums del sistema AutoMétrica.
Aplica Clean Code #1: Nombres reveladores y eliminación de números y strings mágicos.
"""
from enum import Enum
import os


class RolUsuario(str, Enum):
    ADMIN = "admin"
    MECANICO = "mecanico"
    CLIENTE = "cliente"

    @classmethod
    def valores(cls) -> list[str]:
        return [rol.value for rol in cls]


class EstadoOrden(str, Enum):
    RECIBIDO = "Recibido"
    EN_DIAGNOSTICO = "En Diagnóstico"
    EN_REPARACION = "En Reparación"
    SERVICIO_FINALIZADO = "Servicio Finalizado"
    CANCELADO = "Cancelado"

    @classmethod
    def valores(cls) -> list[str]:
        return [estado.value for estado in cls]


# Reglas de negocio y validación de Orden de Servicio
CALIFICACION_MINIMA = 1
CALIFICACION_MAXIMA = 5

# Paginación estándar de consultas
PAGINACION_SKIP_DEFECTO = 0
PAGINACION_LIMITE_DEFECTO = 100

# Parámetros de seguridad y criptografía
PASSWORD_MIN_LONGITUD = 8
BCRYPT_ROUNDS = 12
BCRYPT_MAX_BYTES = 72

# Tokens y recuperación de contraseña
TOKEN_BYTES_SEGURIDAD = 24
TOKEN_EXPIRACION_MINUTOS = 30

# Autenticación JWT
JWT_SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
if os.getenv("ENVIRONMENT", "development").lower() == "production" and JWT_SECRET_KEY == "dev-only-change-me":
    raise RuntimeError("SECRET_KEY debe configurarse en producción.")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 Horas de sesión
