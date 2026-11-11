from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


TipoTarta = Literal[
    "chocolate",
    "queso",
    "zanahoria",
    "fruta",
]

TipoEquipamiento = Literal[
    "horno_industrial",
    "batidora",
    "camara_frigorifica",
    "mangas_pasteleras",
    "linea_envasado",
]


class PlanProduccionRequest(BaseModel):
    """Parámetros que envía el frontend."""

    model_config = ConfigDict(extra="forbid")

    tipo_tarta: TipoTarta
    cantidad: Annotated[int, Field(ge=10, le=200, multiple_of=10)]
    tiempo_disponible_min: Annotated[
        int,
        Field(ge=60, le=480, multiple_of=30),
    ]
    equipamiento: Annotated[
        list[TipoEquipamiento],
        Field(min_length=1, max_length=5),
    ]

    @model_validator(mode="after")
    def validar_equipamiento_sin_duplicados(self):
        if len(self.equipamiento) != len(set(self.equipamiento)):
            raise ValueError("No se puede repetir el equipamiento.")
        return self


class FaseProduccion(BaseModel):
    """Una fase del plan de producción."""

    model_config = ConfigDict(extra="forbid")

    nombre: Annotated[str, Field(min_length=2, max_length=100)]
    descripcion: Annotated[str, Field(min_length=5, max_length=1000)]
    duracion_minutos: Annotated[int, Field(ge=0, le=1440)]
    equipamiento_necesario: list[TipoEquipamiento]
    depende_de: list[int] = Field(
        description="Índices de las fases previas necesarias; empiezan en 0."
    )


class ControlCalidad(BaseModel):
    """Comprobación de calidad o seguridad alimentaria."""

    model_config = ConfigDict(extra="forbid")

    titulo: Annotated[str, Field(min_length=2, max_length=100)]
    descripcion: Annotated[str, Field(min_length=5, max_length=1000)]


class AlternativaProduccion(BaseModel):
    """Alternativa ante una limitación de producción."""

    model_config = ConfigDict(extra="forbid")

    problema: Annotated[str, Field(min_length=3, max_length=200)]
    solucion: Annotated[str, Field(min_length=5, max_length=1000)]


class PlanProduccionResponse(BaseModel):
    """Respuesta estructurada que recibirá Vue."""

    model_config = ConfigDict(extra="forbid")

    resumen: Annotated[str, Field(min_length=10, max_length=1500)]
    viable_en_tiempo: bool
    fases: Annotated[
        list[FaseProduccion],
        Field(min_length=1, max_length=20),
    ]
    controles_calidad: Annotated[
        list[ControlCalidad],
        Field(min_length=1, max_length=10),
    ]
    alternativas: Annotated[
        list[AlternativaProduccion],
        Field(min_length=1, max_length=5),
    ]
    duracion_total_minutos: Annotated[int, Field(ge=0, le=1440)]