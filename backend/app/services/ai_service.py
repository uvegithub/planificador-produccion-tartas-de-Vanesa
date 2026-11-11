import os

import httpx

import json
from pathlib import Path

from dotenv import load_dotenv

from app.models.schemas import (
    PlanProduccionRequest,
    PlanProduccionResponse,
)

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def generar_plan_con_ia(
    request: PlanProduccionRequest,
) -> PlanProduccionResponse:

    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "No se ha encontrado OPENROUTER_API_KEY en el archivo .env"
        )

    instrucciones = f"""
    Eres un experto en planificación de producción de tartas
    para una pastelería profesional.

    Debes crear un plan de producción realista teniendo en cuenta:

    - Tipo de tarta: {request.tipo_tarta}
    - Cantidad: {request.cantidad}
    - Tiempo disponible: {request.tiempo_disponible_min} minutos
    - Equipamiento disponible: {request.equipamiento}

    Devuelve exclusivamente un objeto JSON válido, sin explicaciones
    fuera del JSON.

    El JSON debe contener estos campos:

    {{
        "resumen": "Resumen del plan",
        "viable_en_tiempo": true,
        "fases": [
            {{
                "nombre": "Nombre de la fase",
                "descripcion": "Descripción detallada",
                "duracion_minutos": 30,
                "equipamiento_necesario": [],
                "depende_de": []
            }}
        ],
        "controles_calidad": [
            {{
                "titulo": "Nombre del control",
                "descripcion": "Descripción del control"
            }}
        ],
        "alternativas": [
            {{
                "problema": "Problema posible",
                "solucion": "Solución propuesta"
            }}
        ],
        "duracion_total_minutos": 30
    }}

    Reglas importantes:
    - Adapta las fases al tipo y cantidad de tartas.
    - Utiliza únicamente equipamiento disponible.
    - Incluye tiempos estimados realistas.
    - Ordena las fases de forma secuencial.
    - El campo depende_de debe contener exclusivamente números enteros.
    - Nunca escribas nombres de fases dentro de depende_de.
    - Los números representan los índices de las fases, empezando por 0.
    - La primera fase tendrá depende_de: [].
    - La segunda fase tendrá depende_de: [0].
    - La tercera fase tendrá depende_de: [1].
    - La cuarta fase tendrá depende_de: [2].
    - Cada fase dependerá de la fase inmediatamente anterior.
    - Incluye controles de calidad y alternativas.
    - No inventes equipamiento que no esté disponible.
    - Los tiempos son estimaciones que deberán verificarse
      con la receta y los procesos reales de la pastelería.
    """

    datos_peticion = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": instrucciones,
            }
        ],
        "temperature": 0.3,
    }

    cabeceras = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=90.0) as cliente:
        respuesta = await cliente.post(
            OPENROUTER_URL,
            headers=cabeceras,
            json=datos_peticion,
        )

        respuesta.raise_for_status()

    resultado_api = respuesta.json()

    try:
        contenido = resultado_api["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "OpenRouter no ha devuelto una respuesta válida."
        )

    # Código anterior:
    #if not isinstance(contenido, str):
    #    raise RuntimeError(
    #        "La respuesta de la IA no tiene el formato esperado."
    #    )

    # Código que está funcionando:
    if not isinstance(contenido, str):
        raise RuntimeError(
          f"La respuesta de la IA no tiene el formato esperado. "
          f"Tipo recibido: {type(contenido).__name__}. "
          f"Claves del mensaje: "
          f"{list(resultado_api['choices'][0]['message'].keys())}"
        )

    contenido = contenido.strip()

    if contenido.startswith("```"):
        contenido = contenido.split("\n", 1)[-1]
        contenido = contenido.removesuffix("```").strip()

    try:
        datos_plan = json.loads(contenido)
    except json.JSONDecodeError:
        raise RuntimeError(
            "La IA ha devuelto un resultado que no es JSON válido."
        )

    if not isinstance(datos_plan, dict):
        raise RuntimeError("La IA no ha devuelto un plan válido.")

    try:
        datos_plan["duracion_total_minutos"] = sum(
            fase["duracion_minutos"]
            for fase in datos_plan["fases"]
        )

        datos_plan["viable_en_tiempo"] = (
            datos_plan["duracion_total_minutos"]
            <= request.tiempo_disponible_min
        )

        return PlanProduccionResponse.model_validate(datos_plan)

    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError(
            f"El plan generado no cumple el formato esperado: {error}"
        )