AUTOMETRICA - DESPLIEGUE EN RENDER (PLAN GRATUITO)
==================================================

1. RESULTADO DE LA REVISION Y ADVERTENCIAS IMPORTANTES
------------------------------------------------------
El repositorio contiene un backend FastAPI + SQLAlchemy (NO Django) y un
frontend React/Vite. No se usan manage.py, gunicorn WSGI ni WhiteNoise.
El backend se inicia con Uvicorn como aplicación ASGI.

Cambios incluidos:
- DATABASE_URL estricto en producción; no hay fallback a SQLite. En desarrollo
  se permite SQLite local si DATABASE_URL no está definido.
- SECRET_KEY se obtiene del entorno para firmar JWT.
- CORS se limita a los orígenes indicados en CORS_ORIGINS.
- Se importa app.models antes de crear las tablas.
- Se retiró de la aplicación desplegable el endpoint público que borraba
  registros de todas las tablas.
- bootstrap_admin.py crea un usuario con rol admin y su taller.
- Axios acepta VITE_API_URL.
- .gitignore excluye entornos, bases de datos, cachés y secretos.

ADVERTENCIAS CRITICAS:
A. El ZIP original incluía backend/.env con credenciales reales de correo/API.
   Considéralas comprometidas: revoca/regenera la contraseña de aplicación
   Gmail y la clave de Resend inmediatamente. No las copies a GitHub.
   Este paquete preparado NO incluye los .env originales.
B. El ZIP incluía un repositorio .git anidado. Si los secretos llegaron a
   commits, quitarlos del último archivo no elimina el historial. Crea un
   repositorio limpio o elimina los secretos del historial antes de publicar.
C. El código tenía una clave JWT fija en constants.py. Ahora se exige SECRET_KEY
   en producción. Los tokens firmados con la clave antigua deberán renovarse.
D. El esquema se crea con SQLAlchemy create_all y ALTER TABLE manuales. No hay
   migraciones versionadas (Alembic). Es una solución inicial, no sustituye
   migraciones controladas. Haz respaldo antes de cambiar modelos.
E. Render Free bloquea conexiones SMTP salientes en puertos 25, 465 y 587.
   Para correo real usa una API HTTPS como Resend.
F. No se encontraron referencias WebSocket/Socket.IO en los archivos fuente
   revisados. Publica frontend y backend por separado.
G. El plan gratuito es para pruebas/hobby, no para producción crítica: el
   backend duerme tras 15 minutos sin tráfico, el primer acceso puede tardar
   cerca de un minuto, el disco local es efímero y PostgreSQL Free vence a los
   30 días (1 GB y sin backups). Exporta los datos y migra antes del vencimiento.

2. ESTRUCTURA
-------------
Sube a GitHub el contenido de esta carpeta conservando backend/, frontend/ y
.gitignore. No subas backend/.env ni frontend/.env. Usa .env.example solo como
plantilla local. build.sh está dentro de backend/.

3. REQUISITOS PREVIOS
---------------------
- Cuenta en https://render.com
- Cuenta en https://github.com
- Proyecto subido a un repositorio GitHub
- PostgreSQL creado en Render
- URL pública del backend y frontend después de desplegarlos

4. CREAR EL REPOSITORIO GITHUB
------------------------------
1. Descomprime el paquete preparado.
2. Abre la carpeta autometrica_render_ready.
3. Inicializa un repositorio Git nuevo (el .git anidado original se excluyó).
4. Ejecuta:
      git init
      git add .
      git commit -m "Preparar AutoMetrica para Render"
      git branch -M main
      git remote add origin https://github.com/USUARIO/REPOSITORIO.git
      git push -u origin main
5. Comprueba que GitHub no muestre .env, *.db, venv/ ni node_modules/.

5. CREAR POSTGRESQL EN RENDER
-----------------------------
1. En Render Dashboard selecciona New + > PostgreSQL.
2. Nombre sugerido: autometrica-db.
3. Selecciona región y plan Free.
4. Crea la base de datos.
5. Copia Internal Database URL si el backend estará en Render y en la misma
   región. En otro caso, usa External Database URL.
6. Guarda la URL como DATABASE_URL en el Web Service. Es un secreto.
7. PostgreSQL Free expira 30 días después de su creación; no es gratuito
   permanente.

6. CREAR EL BACKEND FASTAPI COMO WEB SERVICE
--------------------------------------------
1. En Render Dashboard selecciona New + > Web Service.
2. Conecta GitHub y autoriza el repositorio.
3. Selecciona el repositorio AutoMétrica.
4. Configura:
   Name: autometrica-api
   Branch: main
   Root Directory: backend
   Runtime/Language: Python 3
   Build Command: bash build.sh
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
5. Antes de desplegar, configura las variables de entorno de la sección 7.
6. Pulsa Create Web Service.
7. Al terminar, copia la URL pública, por ejemplo
   https://autometrica-api.onrender.com.

7. VARIABLES DE ENTORNO DEL BACKEND
-----------------------------------
Obligatorias:
  ENVIRONMENT=production
  DATABASE_URL=<Internal Database URL de Render PostgreSQL>
  SECRET_KEY=<secreto aleatorio largo y único>
  CORS_ORIGINS=https://TU-FRONTEND.onrender.com
  BOOTSTRAP_ADMIN_NAME=Administrador AutoMétrica
  BOOTSTRAP_ADMIN_EMAIL=correo-administrador@dominio.com
  BOOTSTRAP_ADMIN_PASSWORD=<contraseña segura y única>

Opcionales:
  RESEND_API_KEY=<clave API de Resend>
  RESEND_FROM=AutoMétrica <correo-verificado@tu-dominio.com>
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=<correo>
  SMTP_PASSWORD=<contraseña de aplicación>
  SMTP_FROM_NAME=AutoMétrica
  SMTP_FROM_EMAIL=<correo>
  TWILIO_ACCOUNT_SID=<SID>
  TWILIO_AUTH_TOKEN=<token>
  TWILIO_PHONE_NUMBER=<número>

DEBUG no aplica como ajuste de Django en esta app FastAPI. ALLOWED_HOSTS también
es una configuración Django; no aplica como tal a FastAPI/Starlette. El origen
del navegador se controla con CORS_ORIGINS. CORS no reemplaza autenticación.

Genera SECRET_KEY localmente con:
  python -c "import secrets; print(secrets.token_urlsafe(48))"
Copia el resultado a Render. No uses la clave de ejemplo ni la guardes en Git.

ADMINISTRADOR INICIAL:
Las tres variables BOOTSTRAP_ADMIN_* crean el usuario administrador. La
contraseña debe tener al menos 8 caracteres, mayúscula, minúscula y carácter
especial. El script crea un taller inicial si no existe. Si el usuario ya
existe, no modifica su contraseña. No compartas estas credenciales ni las
pongas en archivos versionados.

8. PUBLICAR EL FRONTEND REACT/VITE COMO STATIC SITE
---------------------------------------------------
1. En Render Dashboard selecciona New + > Static Site.
2. Conecta el mismo repositorio.
3. Configura:
   Name: autometrica-frontend
   Branch: main
   Root Directory: frontend
   Build Command: npm ci && npm run build
   Publish Directory: dist
4. En Environment configura:
   VITE_API_URL=https://TU-BACKEND.onrender.com/api/v1
   Sustituye por la URL real del Web Service.
5. Crea el Static Site y copia su URL pública.
6. Regresa al Web Service backend y cambia CORS_ORIGINS por el origen exacto
   del Static Site (https://...onrender.com, sin barra final).
7. Guarda y ejecuta un nuevo deploy del backend.

VITE_API_URL se incorpora al bundle durante el build. Si cambia la URL del
backend, actualiza la variable y vuelve a desplegar el Static Site.
El proxy de vite.config.js solo funciona en desarrollo local.

9. QUÉ HACE build.sh
--------------------
1. Instala pip y backend/requirements.txt.
2. Verifica que DATABASE_URL permita conectarse.
3. Importa la aplicación y crea las tablas declaradas en SQLAlchemy (app.main
   también ejecuta los ALTER TABLE manuales que ya tenía el proyecto).
4. Ejecuta bootstrap_admin.py para crear taller y administrador si las
   variables BOOTSTRAP_ADMIN_* están definidas.

No ejecuta migraciones Django ni recopila estáticos del backend. El frontend
tiene su propio build de Vite y se publica como Static Site.

10. VERIFICACIONES POST-DESPLIEGUE
----------------------------------
1. Abre https://TU-BACKEND.onrender.com/; debe responder JSON con el mensaje
   de API y la ruta /docs.
2. Abre https://TU-BACKEND.onrender.com/health; debe responder {"status":"ok"}.
3. Abre https://TU-BACKEND.onrender.com/docs; debe aparecer Swagger UI.
4. Abre el frontend e inicia sesión con el administrador inicial.
5. Verifica logs de conexión PostgreSQL y build.
6. Crea un registro de prueba y comprueba que persiste después de reiniciar.
7. Prueba CORS desde el dominio real del frontend.
8. No uses SQLite ni archivos locales para persistencia de producción.

11. PROBLEMAS COMUNES
---------------------
- ModuleNotFoundError: Root Directory debe ser backend y requirements.txt debe
  estar en esa carpeta. Usa:
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
- Error PostgreSQL: revisa DATABASE_URL, base activa, región y URL interna o
  externa correcta.
- "DATABASE_URL es obligatorio": falta DATABASE_URL o ENVIRONMENT=production.
- Error SECRET_KEY: configura una clave aleatoria y vuelve a desplegar.
- CORS en navegador: CORS_ORIGINS debe contener el origen exacto del Static
  Site, con https:// y sin ruta ni barra final.
- Frontend llama a localhost: actualiza VITE_API_URL y reconstruye el Static
  Site; VITE_* se fija durante npm run build.
- Error creando tablas: consulta el primer error SQL en logs y revisa que los
  modelos/columnas sean compatibles.
- Primer acceso lento: comportamiento esperado después de inactividad Free.
- Correo no sale por SMTP: Render Free bloquea puertos 25, 465 y 587. Usa
  Resend por HTTPS.
- Datos desaparecen: no uses SQLite ni archivos locales. Render Free Postgres
  no es permanente; exporta antes de 30 días.
- Administrador no aparece: revisa que BOOTSTRAP_ADMIN_NAME, EMAIL y PASSWORD
  estén definidas durante el build. El log indica si fue omitido o creado.
- Dependencias fallan: revisa versión Python, requirements.txt y logs del build.

12. LIMITACIONES Y RECOMENDACIONES
-----------------------------------
- Free Web Service se suspende tras 15 minutos sin tráfico; despertar puede
  tardar alrededor de un minuto.
- El filesystem del servicio web es efímero.
- PostgreSQL Free: 1 GB, expira a los 30 días y no tiene backups.
- El servicio puede reiniciarse. Mantén datos persistentes en PostgreSQL.
- No se recomienda este plan para datos reales sensibles o servicio comercial
  crítico.
- Antes de producción real, implementar Alembic, pruebas de autorización,
  backups externos, almacenamiento de archivos externo y observabilidad.
  Revisar además endpoints administrativos y de borrado.

REFERENCIAS OFICIALES
---------------------
https://render.com/docs/deploy-fastapi
https://render.com/docs/free
https://render.com/docs/your-first-deploy
https://render.com/docs/troubleshooting-deploys
