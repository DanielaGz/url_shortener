# URL Shortener API

Este proyecto es una API para acortar URLs, construida con FastAPI y MongoDB. Permite a los usuarios convertir URLs largas en enlaces cortos y fáciles de compartir.

## Características

- **Acortamiento de URLs**: Convierte una URL larga en un enlace corto único.
- **Redirección Rápida**: Redirige eficientemente los enlaces cortos a sus URLs originales.
- **API Sencilla**: Una API RESTful fácil de usar para generar y gestionar enlaces.
- **Base de Datos NoSQL**: Utiliza MongoDB para un almacenamiento de datos rápido y escalable.
- **Despliegue en la Nube**: Configurado para un despliegue sencillo en Google Cloud App Engine.

## Tecnologías Utilizadas

- **Backend**: FastAPI, Python 3.10
- **Base de Datos**: MongoDB (con `motor` para operaciones asíncronas)
- **Servidor**: Uvicorn (servidor ASGI)
- **Validación de Datos**: Pydantic
- **Variables de Entorno**: python-dotenv
- **Despliegue**: Google Cloud App Engine

## Requisitos Previos

- Python 3.10 o superior
- Una base de datos MongoDB (local o en la nube como MongoDB Atlas)
- `pip` y `venv` para la gestión de paquetes y entornos virtuales

## Configuración Local

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/DanielaGz/url_shortener.git
    cd url_shortener
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto y añade las siguientes variables:
    ```
    MONGO_URI="tu_string_de_conexion_a_mongodb"
    CURRENT_URL="http://localhost:8000"
    ```

5.  **Ejecuta la aplicación:**
    ```bash
    uvicorn main:app --reload
    ```
    La API estará disponible en `http://localhost:8000`.

## Uso de la API

La documentación interactiva de la API (generada por Swagger UI) está disponible en `http://localhost:8000/docs`.

### Endpoints

#### 1. Acortar una URL

- **POST** `/shorten`
  - **Descripción**: Crea un enlace corto para una URL larga.
  - **Cuerpo de la Petición**:
    ```json
    {
      "long_url": "https://ejemplo.com/url/muy/larga/para/acortar"
    }
    ```
  - **Respuesta Exitosa (200 OK)**:
    ```json
    {
      "short_url": "http://localhost:8000/xxxxxx",
      "long_url": "https://ejemplo.com/url/muy/larga/para/acortar"
    }
    ```

#### 2. Redirigir a la URL Original

- **GET** `/{short_id}`
  - **Descripción**: Redirige a la URL original a partir de un ID corto.
  - **Parámetros de Ruta**:
    - `short_id` (string): El identificador único del enlace corto.
  - **Respuestas**:
    - **307 Temporary Redirect**: Si el `short_id` es válido, redirige al `long_url`.
    - **404 Not Found**: Si el `short_id` no se encuentra en la base de datos.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio.

## Licencia

Este proyecto está bajo la Licencia MIT.