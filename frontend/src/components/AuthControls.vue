<script setup lang="ts">
import {
  Show,
  SignInButton,
  SignUpButton,
  UserButton,
} from '@clerk/vue'
</script>

<template>
  <div class="flex items-center gap-3">
    <Show when="signed-out">
      <SignInButton mode="modal">
        <button
          type="button"
          class="rounded-xl border border-violet-300 bg-white px-4 py-2 text-sm font-semibold text-violet-700 shadow-sm hover:bg-violet-50"
        >
          Iniciar sesión
        </button>
      </SignInButton>

      <SignUpButton mode="modal">
        <button
          type="button"
          class="rounded-xl bg-violet-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-violet-700"
        >
          Registrarse
        </button>
      </SignUpButton>
    </Show>

    <Show when="signed-in">
      <UserButton />
    </Show>
  </div>
</template>