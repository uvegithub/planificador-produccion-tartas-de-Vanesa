<script setup lang="ts">
import { ref, onBeforeUnmount } from 'vue'
import { Volume2, VolumeX } from 'lucide-vue-next'

const audio = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)
const error = ref('')

async function toggleMusic() {
  if (!audio.value) return

  if (isPlaying.value) {
    audio.value.pause()
    isPlaying.value = false
    return
  }

  try {
    await audio.value.play()
    isPlaying.value = true
    error.value = ''
  } catch {
    error.value = 'No se ha podido reproducir la música.'
  }
}

onBeforeUnmount(() => {
  audio.value?.pause()
})
</script>

<template>
  <div class="flex flex-col items-start gap-1">
    <audio
      ref="audio"
      src="/audio/danza-hada-azucar.ogg"
      loop
      preload="none"
    />

    <button
      type="button"
      @click="toggleMusic"
      :aria-label="isPlaying ? 'Silenciar música' : 'Activar música'"
      class="flex items-center gap-2 rounded-xl border border-violet-300 bg-white px-4 py-2 text-sm font-semibold text-violet-700 shadow-sm transition hover:bg-violet-50"
    >
      <Volume2 v-if="isPlaying" :size="18" />
      <VolumeX v-else :size="18" />

      {{ isPlaying ? 'Silenciar música' : 'Activar música' }}
    </button>

    <p v-if="error" class="text-xs text-red-400">
      {{ error }}
    </p>
  </div>
</template>