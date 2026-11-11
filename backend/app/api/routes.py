from fastapi import APIRouter

import httpx

from app.models.schemas import (
    PlanProduccionRequest,
    PlanProduccionResponse,
)

from app.services.ai_service import generar_plan_con_ia

router = APIRouter(prefix="/api", tags=["Producción"])


@router.post("/generate-routine", response_model=PlanProduccionResponse)
async def generate_routine(
    request: PlanProduccionRequest,
) -> PlanProduccionResponse:
    """Genera un plan con IA y utiliza una demostración si falla."""

    try:
        return await generar_plan_con_ia(request)

    except (httpx.HTTPError, RuntimeError, ValueError, KeyError, TypeError) as error:
        print(f"Error al conectar con OpenRouter: {error}")

    return PlanProduccionResponse(
        resumen=(
            f"Plan de demostración para producir {request.cantidad} "
            f"tartas de {request.tipo_tarta}. "
            "Los tiempos son ilustrativos y deben verificarse."
        ),
        viable_en_tiempo=False,
        fases=[
            {
                "nombre": "Preparación",
                "descripcion": (
                    "Preparar los ingredientes y comprobar que los equipos "
                    "necesarios están disponibles."
                ),
                "duracion_minutos": 20,
                "equipamiento_necesario": request.equipamiento,
                "depende_de": [],
            },
        ],
        controles_calidad=[
            {
                "titulo": "Comprobación previa",
                "descripcion": (
                    "Verificar la receta aprobada, los ingredientes, "
                    "la higiene y los procedimientos aplicables."
                ),
            },
        ],
        alternativas=[
            {
                "problema": "Tiempo insuficiente",
                "solucion": (
                    "Revisar la planificación y calcular de nuevo la "
                    "capacidad antes de iniciar la producción."
                ),
            },
        ],
        duracion_total_minutos=20,
    )