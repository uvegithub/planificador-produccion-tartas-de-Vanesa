import os

from fastapi import APIRouter, Depends, HTTPException, Request

from clerk_backend_api import authenticate_request_async
from clerk_backend_api.security.types import (
    AuthenticateRequestOptions,
    AuthStatus,
)

import httpx

from app.models.schemas import (
    PlanProduccionRequest,
    PlanProduccionResponse,
)

from app.services.ai_service import generar_plan_con_ia

router = APIRouter(prefix="/api", tags=["Producción"])

async def verificar_autenticacion(request: Request) -> None:
    """Comprueba que la petición contiene una sesión válida de Clerk."""

    secret_key = os.getenv("CLERK_SECRET_KEY")

    if not secret_key:
        raise HTTPException(
            status_code=500,
            detail="No está configurada la clave secreta de Clerk.",
        )

    options = AuthenticateRequestOptions(
        secret_key=secret_key,
        accepts_token=["session_token"],
    )

    auth_state = await authenticate_request_async(request, options)

    if auth_state.status != AuthStatus.SIGNED_IN:
        raise HTTPException(
            status_code=401,
            detail="No autenticado. Inicia sesión para continuar.",
        )

@router.post("/generate-routine", response_model=PlanProduccionResponse)
async def generate_routine(
    request: PlanProduccionRequest,
    _: None = Depends(verificar_autenticacion),
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