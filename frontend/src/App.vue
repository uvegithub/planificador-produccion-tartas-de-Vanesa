<script setup lang="ts">
import { computed, ref } from 'vue'
import {
  Bot,
  CakeSlice,
  CheckCircle2,
  Clock3,
  CookingPot,
  Factory,
  LoaderCircle,
  Sparkles,
  Thermometer,
  AlertCircle,
} from 'lucide-vue-next'

// Cliente HTTP y tipos para comunicarnos con FastAPI.
import { generarPlan as solicitarPlan } from './services/production'

import AuthControls from './components/AuthControls.vue'

// Tipos de los datos que enviamos y recibimos.
import type {
  PlanProduccionRequest,
  PlanProduccionResponse,
  TipoEquipamiento,
  TipoTarta,
} from './services/production'

// Función que envía la petición al backend.

// =====================================================
// 1. TIPOS DE DATOS
// Definimos los valores permitidos para evitar entradas
// que no estén contempladas en los requisitos.
// =====================================================

// =====================================================
// 2. OPCIONES DEL FORMULARIO
// Estas listas alimentarán los selectores y las casillas.
// =====================================================

const tiposTarta: { value: TipoTarta; label: string }[] = [
  { value: 'chocolate', label: 'Tarta de chocolate' },
  { value: 'queso', label: 'Tarta de queso' },
  { value: 'zanahoria', label: 'Tarta de zanahoria' },
  { value: 'fruta', label: 'Tarta de fruta' },
]

const equipos: { value: TipoEquipamiento; label: string }[] = [
  { value: 'horno_industrial', label: 'Horno industrial' },
  { value: 'batidora', label: 'Batidora' },
  { value: 'camara_frigorifica', label: 'Cámara frigorífica' },
  { value: 'mangas_pasteleras', label: 'Mangas pasteleras' },
]

// =====================================================
// 3. ESTADO REACTIVO DEL FORMULARIO
// ref() permite que Vue detecte los cambios realizados
// por el usuario y actualice automáticamente la pantalla.
// =====================================================

// Tipo de tarta seleccionado inicialmente.
const tipoTarta = ref<TipoTarta>('chocolate')

// Número de tartas que queremos producir.
const cantidad = ref(50)

// Tiempo disponible expresado en minutos.
const tiempoDisponible = ref(180)

// Equipos seleccionados inicialmente como ejemplo.
const equipamiento = ref<TipoEquipamiento[]>([
  'horno_industrial',
  'batidora',
  'camara_frigorifica',
])

// =====================================================
// 4. ESTADO DE LA PETICIÓN Y LOS RESULTADOS
// Preparado para mostrar carga, errores y el plan generado.
// =====================================================

// Indica si estamos esperando una respuesta.
const cargando = ref(false)

// Mensaje que mostraremos cuando ocurra un error.
const error = ref('')

// Resultado estructurado que se mostrará en tarjetas.
// Inicialmente es null porque aún no hay ningún plan.
// Resultado recibido del backend

const resultado = ref<PlanProduccionResponse | null>(null)

// =====================================================
// 5. VALIDACIONES DEL FORMULARIO
// computed() recalcula automáticamente las condiciones
// cuando el usuario cambia los valores.
// =====================================================

// La cantidad debe ser un entero entre 10 y 200,
// avanzando en incrementos de 10 unidades.
const cantidadValida = computed(
  () =>
    Number.isInteger(cantidad.value) &&
    cantidad.value >= 10 &&
    cantidad.value <= 200 &&
    cantidad.value % 10 === 0,
)

// El tiempo debe estar entre 60 y 480 minutos,
// en incrementos de 30 minutos.
const tiempoValido = computed(
  () =>
    Number.isInteger(tiempoDisponible.value) &&
    tiempoDisponible.value >= 60 &&
    tiempoDisponible.value <= 480 &&
    tiempoDisponible.value % 30 === 0,
)

// El formulario solo es válido si todos los campos
// cumplen sus restricciones y hay algún equipo elegido.
const formularioValido = computed(
  () =>
    cantidadValida.value &&
    tiempoValido.value &&
    equipamiento.value.length > 0,
)

// =====================================================
// 6. SELECCIÓN DEL EQUIPAMIENTO
// Añade un equipo si no estaba seleccionado y lo elimina
// si el usuario vuelve a pulsar sobre él.
// =====================================================

function toggleEquipo(equipo: TipoEquipamiento) {
  if (equipamiento.value.includes(equipo)) {
    equipamiento.value = equipamiento.value.filter(
      (elemento) => elemento !== equipo,
    )
  } else {
    equipamiento.value = [...equipamiento.value, equipo]
  }
}

// =====================================================
// 7. GENERACIÓN DEL PLAN DE DEMOSTRACIÓN
// Simula una espera y prepara resultados de ejemplo.
// Más adelante sustituiremos esta parte por una petición
// HTTP real a FastAPI.
// =====================================================

async function generarPlan() {
  // Limpiamos los mensajes y resultados anteriores.
  error.value = ''
  resultado.value = null

  // Evitamos generar un plan si hay datos inválidos.
  if (!formularioValido.value) {
    error.value =
      'Revisa la cantidad, el tiempo disponible y selecciona al menos un equipo.'
    return
  }

  // Activamos el indicador de carga.
  cargando.value = true

  try {
    // Preparamos los cuatro parámetros que espera FastAPI.
    const datos: PlanProduccionRequest = {
      tipo_tarta: tipoTarta.value,
      cantidad: cantidad.value,
      tiempo_disponible_min: tiempoDisponible.value,
      equipamiento: [...equipamiento.value],
    }

    // Solicitamos el plan al backend.
    const respuesta = await solicitarPlan(datos)

    // Guardamos la respuesta recibida.
    resultado.value = respuesta

  } catch (err: unknown) {
    // Mostramos el mensaje de error si falla la petición.
    error.value =
      err instanceof Error
        ? err.message
        : 'No se ha podido generar el plan. Inténtalo de nuevo.'
  } finally {
    // Ocultamos el spinner tanto si hay éxito como si falla.
    cargando.value = false
  }
}
</script>

<!-- ===================================================
     8. PLANTILLA PRINCIPAL
     Toda la aplicación se muestra en una única página.
     =================================================== -->
<template>
  <main class="min-h-screen bg-slate-950 px-4 py-8 text-slate-900 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-6xl">

      <!-- Cabecera de la aplicación -->
      <header class="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div class="rounded-2xl bg-violet-500 p-3 text-white">
          <CakeSlice :size="34" />
        </div>

        <div>
          <p class="text-sm font-semibold uppercase tracking-widest text-violet-300">
            Producción inteligente
          </p>
          <h1 class="mt-1 text-2xl font-bold text-white sm:text-3xl">
            Planificador de tartas
          </h1>
          <p class="mt-1 text-sm text-slate-400">
            Organiza tu producción con ayuda de la inteligencia artificial.
          </p>
        </div>
        <AuthControls />
      </header>

      <!-- Diseño en dos columnas: formulario y resultados -->
      <div class="grid gap-6 lg:grid-cols-2">

        <!-- ==========================================
             COLUMNA IZQUIERDA: FORMULARIO
             ========================================== -->
        <section class="rounded-2xl bg-white p-6 shadow-2xl sm:p-8">

          <div class="mb-7 flex items-center gap-3">
            <div class="rounded-xl bg-violet-100 p-3 text-violet-700">
              <Factory :size="24" />
            </div>
            <div>
              <h2 class="text-xl font-bold">Configuración de producción</h2>
              <p class="text-sm text-slate-500">
                Define las condiciones de tu fábrica.
              </p>
            </div>
          </div>

          <!-- El evento submit ejecuta generarPlan() -->
          <form class="space-y-6" @submit.prevent="generarPlan">

            <!-- Campo 1: tipo de tarta -->
            <div>
              <label for="tipo-tarta" class="mb-2 block text-sm font-semibold text-slate-700">
                1. Tipo de tarta
              </label>

              <select
                id="tipo-tarta"
                v-model="tipoTarta"
                class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-100"
              >
                <option
                  v-for="tipo in tiposTarta"
                  :key="tipo.value"
                  :value="tipo.value"
                >
                  {{ tipo.label }}
                </option>
              </select>
            </div>

            <!-- Campo 2: cantidad de unidades -->
            <div>
              <div class="mb-2 flex items-center justify-between gap-3">
                <label for="cantidad" class="text-sm font-semibold text-slate-700">
                  2. Cantidad de unidades
                </label>
                <span class="rounded-lg bg-violet-50 px-3 py-1 font-bold text-violet-700">
                  {{ cantidad }} tartas
                </span>
              </div>

              <input
                id="cantidad"
                v-model.number="cantidad"
                type="range"
                min="10"
                max="200"
                step="10"
                class="w-full cursor-pointer accent-violet-600"
              />

              <div class="mt-1 flex justify-between text-xs text-slate-400">
                <span>10 unidades</span>
                <span>200 unidades</span>
              </div>
            </div>

            <!-- Campo 3: tiempo disponible -->
            <div>
              <div class="mb-2 flex items-center justify-between gap-3">
                <label for="tiempo" class="text-sm font-semibold text-slate-700">
                  3. Tiempo disponible
                </label>
                <span class="rounded-lg bg-violet-50 px-3 py-1 font-bold text-violet-700">
                  {{ tiempoDisponible }} min
                </span>
              </div>

              <input
                id="tiempo"
                v-model.number="tiempoDisponible"
                type="range"
                min="60"
                max="480"
                step="30"
                class="w-full cursor-pointer accent-violet-600"
              />

              <div class="mt-1 flex justify-between text-xs text-slate-400">
                <span>1 hora</span>
                <span>8 horas</span>
              </div>
            </div>

            <!-- Campo 4: equipamiento disponible -->
            <fieldset>
              <legend class="mb-3 text-sm font-semibold text-slate-700">
                4. Equipamiento disponible
              </legend>

              <div class="space-y-2">
                <label
                  v-for="equipo in equipos"
                  :key="equipo.value"
                  class="flex cursor-pointer items-center gap-3 rounded-xl border p-3 transition"
                  :class="equipamiento.includes(equipo.value)
                    ? 'border-violet-300 bg-violet-50'
                    : 'border-slate-200 hover:border-violet-200'"
                >
                  <input
                    type="checkbox"
                    :checked="equipamiento.includes(equipo.value)"
                    class="size-4 accent-violet-600"
                    @change="toggleEquipo(equipo.value)"
                  />

                  <span class="flex-1 text-sm font-medium text-slate-700">
                    {{ equipo.label }}
                  </span>

                  <CheckCircle2
                    v-if="equipamiento.includes(equipo.value)"
                    :size="18"
                    class="text-violet-600"
                  />
                </label>
              </div>

              <p
                v-if="equipamiento.length === 0"
                class="mt-2 text-sm text-red-600"
              >
                Selecciona al menos un equipo.
              </p>
            </fieldset>

            <!-- Mensaje de error -->
            <div
              v-if="error"
              role="alert"
              class="flex items-start gap-2 rounded-xl bg-red-50 p-4 text-sm text-red-700"
            >
              <AlertCircle :size="20" class="shrink-0" />
              <p>{{ error }}</p>
            </div>

            <!-- Botón con estado de carga -->
            <button
              type="submit"
              :disabled="cargando || !formularioValido"
              class="flex w-full items-center justify-center gap-2 rounded-xl bg-violet-600 px-5 py-4 font-semibold text-white transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <LoaderCircle
                v-if="cargando"
                :size="20"
                class="animate-spin"
              />
              <Sparkles v-else :size="20" />

              {{ cargando ? 'Preparando el plan...' : 'Generar plan de producción' }}
            </button>

            <p class="text-center text-xs text-slate-400">
            El plan se genera mediante el backend FastAPI.
            </p>
          </form>
        </section>

        <!-- ==========================================
             COLUMNA DERECHA: RESULTADOS
             ========================================== -->
        <section class="rounded-2xl border border-slate-800 bg-slate-900 p-6 sm:p-8">

          <div class="mb-6 flex items-center gap-3">
            <div class="rounded-xl bg-slate-800 p-3 text-violet-300">
              <Bot :size="25" />
            </div>
            <div>
              <h2 class="text-xl font-bold text-white">Plan de producción</h2>
              <p class="text-sm text-slate-400">
                Fases, tiempos y controles de calidad.
              </p>
            </div>
          </div>

          <!-- Estado inicial: todavía no hay resultados -->
          <div
            v-if="!resultado && !cargando"
            class="flex min-h-80 flex-col items-center justify-center rounded-xl border border-dashed border-slate-700 px-6 text-center"
          >
            <div class="mb-4 rounded-2xl bg-slate-800 p-4 text-violet-300">
              <CookingPot :size="38" />
            </div>

            <h3 class="text-lg font-semibold text-white">
              Tu planificación aparecerá aquí
            </h3>

            <p class="mt-2 max-w-sm text-sm leading-6 text-slate-400">
              Configura los cuatro parámetros y genera un plan de demostración.
            </p>
          </div>

          <!-- Estado de carga: spinner animado -->
          <div
            v-else-if="cargando"
            class="flex min-h-80 flex-col items-center justify-center text-center"
            role="status"
            aria-live="polite"
          >
            <LoaderCircle :size="44" class="animate-spin text-violet-400" />
            <p class="mt-4 font-semibold text-white">
              Preparando la planificación
            </p>
            <p class="mt-2 text-sm text-slate-400">
              Estamos preparando la vista de resultados...
            </p>
          </div>

          <!-- Estado final: tarjetas del plan -->
          <div v-else-if="resultado" class="space-y-5">

            <!-- Tarjeta de resumen y duración -->
            <article class="rounded-xl bg-violet-500/10 p-4 ring-1 ring-violet-400/20">
              <p class="mb-2 text-xs font-semibold uppercase tracking-wider text-violet-300">
                Resumen del plan
              </p>

              <p class="text-sm leading-6 text-slate-200">
                {{ resultado.resumen }}
              </p>

              <!-- Indicador de viabilidad temporal -->
              <div
                class="mt-3 inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold"
                :class="resultado.viable_en_tiempo
                ? 'bg-emerald-500/10 text-emerald-300'
                : 'bg-amber-500/10 text-amber-300'"
              >
                <CheckCircle2 v-if="resultado.viable_en_tiempo" :size="18" />
                <Clock3 v-else :size="18" />

                {{ resultado.viable_en_tiempo
                ? 'El plan cabe en el tiempo disponible'
                : 'El tiempo disponible puede ser insuficiente' }}
              </div>

              <div class="mt-4 flex items-center gap-3 border-t border-violet-400/20 pt-4">
                <Clock3 :size="22" class="text-violet-300" />
                <div>
                  <p class="text-xs text-slate-400">Duración total estimada</p>
                  <p class="text-xl font-bold text-white">
                    {{ resultado.duracion_total_minutos }} minutos
                  </p>
                </div>
              </div>
            </article>

            <!-- Tarjetas de las fases de producción -->
            <div>
              <h3 class="mb-3 font-semibold text-white">
                Fases de producción
              </h3>

              <div class="space-y-3">
                <article
                  v-for="(fase, index) in resultado.fases"
                  :key="fase.nombre"
                  class="rounded-xl bg-slate-800 p-4"
                >
                  <div class="flex items-start gap-3">
                    <div class="flex size-8 shrink-0 items-center justify-center rounded-lg bg-violet-500/20 text-sm font-bold text-violet-300">
                      {{ index + 1 }}
                    </div>

                    <div class="min-w-0 flex-1">
                      <div class="flex flex-wrap items-center justify-between gap-2">
                        <h4 class="font-semibold text-white">
                          {{ fase.nombre }}
                        </h4>
                        <span class="text-xs text-violet-300">
                          {{ fase.duracion_minutos }} min
                        </span>
                      </div>

                      <!-- Descripción de la fase devuelta por FastAPI -->
                      <p class="mt-2 text-sm leading-6 text-slate-300">
                        {{ fase.descripcion }}
                      </p>

                      <!-- Equipamiento necesario -->
                      <p class="mt-2 text-xs text-slate-400">
                        Equipo:
                        {{ fase.equipamiento_necesario.join(', ') }}
                      </p>

                      <!-- Dependencias: los índices empiezan en cero -->
                      <p
                        v-if="fase.depende_de.length"
                        class="mt-1 text-xs text-slate-400"
                      >                      
                        Depende de las fases:
                        {{ fase.depende_de.map(indice => resultado!.fases[indice]?.nombre ?? `Fase ${indice + 1}`).join(', ') }}
                      </p>
                    </div>
                  </div>
                </article>
              </div>
            </div>

            <!-- Tarjeta de controles de calidad -->
            <article class="rounded-xl bg-slate-800 p-4">
              <h3 class="mb-3 flex items-center gap-2 font-semibold text-white">
                <CheckCircle2 :size="19" class="text-emerald-400" />
                Controles de calidad
              </h3>

              <ul class="space-y-2 text-sm leading-5 text-slate-300">
                <li
                  v-for="control in resultado.controles_calidad"
                  :key="control.titulo"
                  class="rounded-lg bg-slate-900/50 p-3"
                >
                  <p class="font-semibold text-slate-200">
                    {{ control.titulo }}
                  </p>
                  <p class="mt-1 text-sm leading-5 text-slate-400">
                    {{ control.descripcion }}
                  </p>
                </li>
              </ul>

              <p class="mt-3 flex items-start gap-2 text-xs leading-5 text-amber-300">
                <Thermometer :size="17" class="mt-0.5 shrink-0" />
                Los parámetros críticos deben seguir los procedimientos
                validados de la fábrica.
              </p>
            </article>

            <!-- Tarjeta de alternativas -->
            <article class="rounded-xl bg-slate-800 p-4">
              <h3 class="mb-3 font-semibold text-white">
                Alternativas de producción
              </h3>

              <ul class="space-y-2 text-sm leading-5 text-slate-300">
                <li
                  v-for="alternativa in resultado.alternativas"
                  :key="alternativa.problema"
                  class="rounded-lg bg-slate-900/50 p-3"
                  >
                  <p class="font-semibold text-slate-200">
                    {{ alternativa.problema }}
                  </p>
                  <p class="mt-1 text-sm leading-5 text-slate-400">
                    {{ alternativa.solucion }}
                  </p>
                </li>
              </ul>
            </article>

          </div>
        </section>
      </div>

      <!-- Pie de página -->
      <footer class="mt-6 text-center text-xs text-slate-500">
        Planificador de producción · Vue 3 · FastAPI · Pydantic
      </footer>
    </div>
  </main>
</template>