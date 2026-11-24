"""Crea un taller inicial y un usuario administrador de forma idempotente."""
import os
import sys

from app.database import SessionLocal
from app import models
from app.security import hash_password, validar_complejidad_password


def main():
    email = os.getenv("BOOTSTRAP_ADMIN_EMAIL", "").strip().lower()
    password = os.getenv("BOOTSTRAP_ADMIN_PASSWORD", "")
    name = os.getenv("BOOTSTRAP_ADMIN_NAME", "").strip()
    workshop_name = os.getenv("BOOTSTRAP_TALLER_NOMBRE", "AutoMétrica").strip()
    workshop_code = os.getenv("BOOTSTRAP_TALLER_CODIGO", "AUTOMETRICA-ADMIN").strip()

    if not (email and password and name):
        print("Bootstrap admin omitido: configura BOOTSTRAP_ADMIN_EMAIL, BOOTSTRAP_ADMIN_PASSWORD y BOOTSTRAP_ADMIN_NAME.")
        return

    valid, message = validar_complejidad_password(password)
    if not valid:
        raise SystemExit(f"BOOTSTRAP_ADMIN_PASSWORD no cumple la política: {message}")

    db = SessionLocal()
    try:
        existing = db.query(models.Usuario).filter(models.Usuario.correo == email).first()
        if existing:
            print(f"El usuario administrador {email} ya existe; no se modifica.")
            return

        workshop = db.query(models.Taller).filter(models.Taller.codigo_unico == workshop_code).first()
        if not workshop:
            workshop = models.Taller(nombre=workshop_name, codigo_unico=workshop_code, activo=True)
            db.add(workshop)
            db.flush()

        admin = models.Usuario(
            taller_id=workshop.id,
            nombre_completo=name,
            correo=email,
            contrasena_hash=hash_password(password),
            rol="admin",
            activo=True,
        )
        db.add(admin)
        db.commit()
        print(f"Administrador inicial creado: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
