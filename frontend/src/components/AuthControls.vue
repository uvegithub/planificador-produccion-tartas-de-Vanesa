<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  register,
  login,
  getCurrentUser,
  clearSession,
  type AuthUser,
} from '../services/auth'

const user = ref<AuthUser | null>(null)
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const mode = ref<'login' | 'register'>('login')

onMounted(async () => {
  user.value = await getCurrentUser()
})

async function submitAuth() {
  error.value = ''
  loading.value = true

  try {
    const result =
      mode.value === 'register'
        ? await register(email.value, password.value)
        : await login(email.value, password.value)

    user.value = result.user
    password.value = ''
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'No se pudo completar la autenticación.'
  } finally {
    loading.value = false
  }
}

function logout() {
  clearSession()
  user.value = null
  email.value = ''
  password.value = ''
  error.value = ''
}
</script>

<template>
  <div class="flex items-center gap-3">
    <div v-if="user" class="flex items-center gap-3">
      <span class="text-sm font-medium text-violet-700">
        {{ user.email }}
      </span>

      <button
        type="button"
        class="rounded-xl border border-violet-300 bg-white px-4 py-2 text-sm font-semibold text-violet-700 shadow-sm hover:bg-violet-50"
        @click="logout"
      >
        Cerrar sesión
      </button>
    </div>

    <div v-else class="flex flex-col items-end gap-2">
      <div class="flex items-center gap-2">
        <button
          type="button"
          class="rounded-xl border border-violet-300 bg-white px-4 py-2 text-sm font-semibold text-violet-700 shadow-sm hover:bg-violet-50"
          @click="mode = 'login'; error = ''"
        >
          Iniciar sesión
        </button>

        <button
          type="button"
          class="rounded-xl bg-violet-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-violet-700"
          @click="mode = 'register'; error = ''"
        >
          Registrarse
        </button>
      </div>

      <form
        class="flex flex-col gap-2 rounded-xl border border-violet-200 bg-white p-3 shadow-sm"
        @submit.prevent="submitAuth"
      >
        <p class="text-sm font-semibold text-violet-800">
          {{ mode === 'login' ? 'Accede a tu cuenta' : 'Crea tu cuenta' }}
        </p>

        <input
          v-model="email"
          type="email"
          placeholder="Correo electrónico"
          autocomplete="email"
          required
          class="rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-violet-500"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Contraseña"
          :autocomplete="mode === 'login' ? 'current-password' : 'new-password'"
          :minlength="mode === 'register' ? 8 : 1"
          maxlength="128"
          required
          class="rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-violet-500"
        />

        <button
          type="submit"
          :disabled="loading"
          class="rounded-lg bg-violet-600 px-4 py-2 text-sm font-semibold text-white hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{
            loading
              ? 'Procesando...'
              : mode === 'login'
                ? 'Entrar'
                : 'Crear cuenta'
          }}
        </button>

        <p v-if="error" class="text-xs text-red-600">
          {{ error }}
        </p>
      </form>
    </div>
  </div>
</template>



¿Qué incorpora?
- Registro de usuarios nuevos.
- Inicio de sesión con correo y contraseña.
- Recuperación de la sesión al cargar la página.
- Visualización del correo del usuario autenticado.
- Cierre de sesión.
- Mensajes de error y estado de carga.
Paso 5.5. Guardar y comprobar
Guarda con Ctrl + S.

Después, desde la carpeta backend, ejecuta:
Get-Content ..\frontend\src\components\AuthControls.vue | Select-Object -First 20


Pásame el resultado. Después conectaremos App.vue con el token JWT y comprobaremos la compilación de Vue.