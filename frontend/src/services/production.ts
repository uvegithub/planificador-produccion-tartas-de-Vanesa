export type TipoTarta =
  | 'chocolate'
  | 'queso'
  | 'zanahoria'
  | 'fruta'

export type TipoEquipamiento =
  | 'horno_industrial'
  | 'batidora'
  | 'camara_frigorifica'
  | 'mangas_pasteleras'
  | 'linea_envasado'

export interface PlanProduccionRequest {
  tipo_tarta: TipoTarta
  cantidad: number
  tiempo_disponible_min: number
  equipamiento: TipoEquipamiento[]
}

export interface FaseProduccion {
  nombre: string
  descripcion: string
  duracion_minutos: number
  equipamiento_necesario: TipoEquipamiento[]
  depende_de: number[]
}

export interface ControlCalidad {
  titulo: string
  descripcion: string
}

export interface AlternativaProduccion {
  problema: string
  solucion: string
}

export interface PlanProduccionResponse {
  resumen: string
  viable_en_tiempo: boolean
  fases: FaseProduccion[]
  controles_calidad: ControlCalidad[]
  alternativas: AlternativaProduccion[]
  duracion_total_minutos: number
}

export async function generarPlan(
  datos: PlanProduccionRequest,
): Promise<PlanProduccionResponse> {
  const response = await fetch('/api/generate-routine', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(datos),
  })

  if (!response.ok) {
    let mensaje = `Error del servidor (${response.status})`

    try {
      const error = await response.json()
      if (Array.isArray(error.detail)) {
        mensaje = error.detail
          .map((item: { msg?: string }) => item.msg ?? 'Datos inválidos')
          .join('. ')
      } else if (typeof error.detail === 'string') {
        mensaje = error.detail
      }
    } catch {
      // Conservamos el mensaje HTTP si la respuesta no contiene JSON.
    }

    throw new Error(mensaje)
  }

  return (await response.json()) as PlanProduccionResponse
}