# Guía de Despliegue: FastAPI a Google Cloud Run

Este documento describe el proceso paso a paso para desplegar esta aplicación FastAPI en Google Cloud Run, incluyendo la configuración del proyecto y la solución de problemas comunes.

## 1. Prerrequisitos

- Tener instalado y configurado el [SDK de Google Cloud](https://cloud.google.com/sdk/docs/install) (`gcloud` CLI).
- Tener un proyecto de Google Cloud con la API de Cloud Run habilitada.
- Tener una cuenta de MongoDB Atlas con un clúster creado.

## 2. Estructura y Configuración del Proyecto

Asegúrate de que tu proyecto tenga los siguientes archivos con la configuración correcta:

### `requirements.txt`

Este archivo debe listar todas las dependencias de Python. Es crucial incluir `gunicorn` para que sirva la aplicación en Cloud Run.

```
fastapi
uvicorn
gunicorn
motor
python-dotenv
# ... y otras dependencias
```

### `Procfile`

Este archivo le indica a Google Cloud cómo iniciar tu aplicación. El comando especifica que Gunicorn debe usar Uvicorn para manejar una aplicación ASGI (como FastAPI). El `--timeout` es importante para evitar que los workers se reinicien si la conexión a la base de datos es lenta durante el inicio.

```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker --timeout 120 main:app
```

### `main.py`

Para asegurar que Cloud Run pueda realizar las verificaciones de estado (health checks) correctamente, tu aplicación debe responder con un código `200 OK` en la ruta raíz (`/`).

```python
@app.get("/", summary="Health check")
async def root():
    return {"status": "ok"}
```

## 3. Configuración de la Base de Datos (MongoDB Atlas)

Este fue el paso más crítico para el éxito del despliegue.

- **Causa del problema:** Por defecto, los clústeres de MongoDB Atlas solo permiten conexiones desde direcciones IP que han sido explícitamente autorizadas. Las instancias de Cloud Run tienen direcciones IP dinámicas que no están en esa lista, por lo que la conexión falla y la aplicación no puede iniciarse.
- **Solución:** Debes añadir una regla a la "IP Access List" de tu clúster en MongoDB Atlas para permitir conexiones desde cualquier lugar.

    1.  Inicia sesión en **MongoDB Atlas**.
    2.  Ve a **Network Access** en la sección "Security".
    3.  Haz clic en **"Add IP Address"**.
    4.  Selecciona **"Allow Access From Anywhere"** (esto añade la IP `0.0.0.0/0`).
    5.  Confirma el cambio.

## 4. El Comando de Despliegue

Una vez que la configuración del proyecto y de la base de datos es correcta, puedes desplegar tu aplicación usando `gcloud run deploy`.

- **Variables de Entorno:** No uses archivos `.env` en producción. Las variables de entorno (como la URI de la base de datos) deben pasarse de forma segura durante el despliegue usando la bandera `--set-env-vars`.
- **Comillas:** Es importante encerrar los valores de las variables de entorno entre comillas (`"`) para evitar que el terminal interprete caracteres especiales (como el `&` en la URI de MongoDB).

Aquí está el comando final que utilizamos:

```bash
gcloud run deploy url-shortener \
  --source . \
  --region=us-central1 \
  --memory=512Mi \
  --cpu=1 \
  --max-instances=1 \
  --allow-unauthenticated \
  --set-env-vars="MONGO_URI=TU_MONGO_URI_AQUI" \
  --set-env-vars="CURRENT_URL=LA_URL_DE_TU_SERVICIO_AQUI"
```

## 5. Verificación

Después de un despliegue exitoso, accede a la URL de tu servicio proporcionada por Cloud Run. Si todo está configurado correctamente, la aplicación debería responder sin errores. Si encuentras problemas, revisa los logs del servicio en la consola de Google Cloud.

