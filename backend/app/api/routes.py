import httpx

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth import (
    authenticate_user,
    create_access_token,
    create_user,
    get_user_from_token,
)
from app.models.auth_schemas import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserResponse,
)
from app.models.schemas import (
    PlanProduccionRequest,
    PlanProduccionResponse,
)
from app.services.ai_service import generar_plan_con_ia


router = APIRouter(prefix="/api", tags=["Producción"])

security = HTTPBearer(auto_error=False)


def verificar_autenticacion(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UserResponse:
    """Valida el token JWT y devuelve el usuario autenticado."""

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="No autenticado. Inicia sesión para continuar.",
        )

    user = get_user_from_token(credentials.credentials)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o caducado. Inicia sesión de nuevo.",
        )

    return UserResponse(**user)


@router.post("/auth/register", response_model=AuthResponse, status_code=201)
async def register(request: RegisterRequest) -> AuthResponse:
    """Registra un usuario nuevo y devuelve su token JWT."""

    user = create_user(request.email, request.password)

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una cuenta con ese correo electrónico.",
        )

    token = create_access_token(user["id"])

    return AuthResponse(
        access_token=token,
        user=UserResponse(**user),
    )


@router.post("/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest) -> AuthResponse:
    """Comprueba las credenciales e inicia una sesión."""

    user = authenticate_user(request.email, request.password)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Correo electrónico o contraseña incorrectos.",
        )

    token = create_access_token(user["id"])

    return AuthResponse(
        access_token=token,
        user=UserResponse(**user),
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user(
    user: UserResponse = Depends(verificar_autenticacion),
) -> UserResponse:
    """Devuelve los datos del usuario autenticado."""

    return user


@router.post("/generate-routine", response_model=PlanProduccionResponse)
async def generate_routine(
    request: PlanProduccionRequest,
    _: UserResponse = Depends(verificar_autenticacion),
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
