Vanesa Nuñez Sierra

Planificador de Producción de Tartas

Aplicación web para planificar rutinas de producción de tartas, teniendo en cuenta el tipo de tarta, la cantidad, el equipamiento disponible y el tiempo de trabajo.

1. Descripción del proyecto

Este proyecto consiste en una aplicación web con arquitectura frontend-backend. Permite al usuario generar una planificación de producción mediante un servicio de inteligencia artificial.

La aplicación incorpora autenticación de usuarios, generación de rutinas y un reproductor musical.

2. Tecnologías utilizadas

Frontend

Vue 3

TypeScript

Vite

Tailwind CSS

Clerk para autenticación

Vitest para pruebas

Backend

Python

FastAPI

Pydantic

HTTPX

OpenRouter para integración con modelos de inteligencia artificial

Pytest para pruebas

Despliegue

Vercel CLI

Vercel Services para frontend y backend

3. Estructura del proyecto

/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── resultados_pruebas.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── __tests__/
│   ├── package.json
│   └── README.md
│
├── docs/
├── requirements.txt
├── vercel.toml
├── .gitignore
└── .vercelignore

4. Arquitectura y funcionamiento

El frontend está desarrollado con Vue 3 y se comunica con el backend mediante peticiones HTTP.

El backend utiliza FastAPI y proporciona los endpoints de la aplicación bajo el prefijo /api.

La generación de rutinas utiliza un servicio de inteligencia artificial conectado mediante OpenRouter. También existe un mecanismo de respuesta alternativa cuando el servicio de IA no está disponible.

La autenticación se realiza mediante Clerk. El frontend obtiene el token de sesión y lo envía al backend, que verifica la autenticación antes de procesar las peticiones protegidas.

Durante el desarrollo local, Vite utiliza un proxy para dirigir las peticiones /api al backend.

5. Instalación y ejecución local

Requisitos

Python 3

Node.js y npm

Credenciales de Clerk y OpenRouter para las funciones que las necesiten.

Backend

Desde la carpeta backend:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

El backend se ejecuta localmente en http://localhost:8000.

Frontend

Desde la carpeta frontend:

npm install
npm run dev

Vite inicia el servidor de desarrollo y muestra la dirección local en la terminal.

6. Variables de entorno

Las credenciales se configuran mediante archivos locales y variables de entorno de Vercel.

Variable

Uso

VITE_CLERK_PUBLISHABLE_KEY

Clave pública de Clerk para el frontend

CLERK_SECRET_KEY

Clave privada de Clerk para el backend

OPENROUTER_API_KEY

Autenticación con OpenRouter

OPENROUTER_MODEL

Modelo de IA seleccionado

Los archivos .env no deben incluirse en Git ni en los archivos públicos del despliegue.

7. Pruebas realizadas

Backend

9 pruebas superadas.

Comprobación de rutas principales y estado del servicio.

Comprobación de autenticación.

Validación de datos de entrada.

Comprobación de respuestas alternativas.

Resultado: 9 passed.

Se detectó un aviso de obsolescencia relacionado con el uso de HTTPX en Starlette TestClient.

Frontend

10 pruebas superadas.

Ejecución mediante Vitest.

Resultado: 10 passed.

8. Despliegue en Vercel

El proyecto está configurado para desplegar frontend y backend mediante Vercel Services.

Se utiliza Vercel CLI, sin integración automática con GitHub.

Se ha comprobado un despliegue Preview satisfactorio. El proyecto dispone también de un primer despliegue asignado al entorno Production, que no se utiliza para las pruebas de desarrollo.

Las variables de entorno están configuradas para Preview.

La configuración técnica del despliegue se documentará en docs/VERCEL.md.

9. Seguridad

Las claves privadas se almacenan como variables de entorno.

Los archivos .env están excluidos mediante reglas de Git y .vercelignore.

El backend verifica la autenticación de las peticiones protegidas.

El despliegue Preview tiene activada la protección de acceso de Vercel.

10. Documentación adicional

docs/VERCEL.md: configuración y despliegue en Vercel.

docs/DOCKER.md: documentación de Docker.

docs/AWS.md: documentación de AWS.

docs/DEFENSA.md: preparación de la defensa de la práctica.

Estos documentos se completarán conforme avance el proyecto.

11. Autoría y recursos

Proyecto académico de despliegue de aplicaciones web.

Música utilizada: Dance of the Sugar Plum Fairy – The Nutcracker, grabación de Kevin MacLeod, disponible en Wikimedia Commons bajo licencia Creative Commons Attribution 3.0 (CC BY 3.0).

Fuente: https://commons.wikimedia.org/wiki/File:Tchaikovsky_-_Dance_of_the_Sugar_Plum_Fairy_-_The_Nutcracker.ogg

Licencia: https://creativecommons.org/licenses/by/3.0/