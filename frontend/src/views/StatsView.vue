<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { api } from '@/api/client'
import type { Stats } from '@/types'

const props = defineProps<{ code: string }>()

const stats = ref<Stats | null>(null)
const error = ref('')

const days = computed(() => (stats.value ? Object.entries(stats.value.per_day) : []))
const maxCount = computed(() => Math.max(1, ...days.value.map(([, count]) => count)))

onMounted(async () => {
  try {
    stats.value = await api.stats(props.code)
  } catch {
    error.value = 'Statistik konnte nicht geladen werden.'
  }
})
</script>

<template>
  <section>
    <RouterLink to="/dashboard" class="text-sm text-indigo-600 hover:underline">
      ← Zurück zum Dashboard
    </RouterLink>

    <h1 class="mt-2 text-2xl font-bold text-slate-900">
      Statistik <span class="font-mono text-indigo-600">{{ code }}</span>
    </h1>

    <p v-if="error" class="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
      {{ error }}
    </p>

    <template v-else-if="stats">
      <div class="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <p class="text-sm font-medium text-slate-500">Klicks gesamt</p>
        <p class="mt-1 text-4xl font-bold text-slate-900">{{ stats.total }}</p>
      </div>

      <div class="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-sm font-medium text-slate-500">Klicks pro Tag</h2>
        <ul v-if="days.length" class="space-y-3">
          <li v-for="[day, count] in days" :key="day">
            <div class="mb-1 flex justify-between text-sm">
              <span class="font-mono text-slate-600">{{ day }}</span>
              <span class="font-medium text-slate-900">{{ count }}</span>
            </div>
            <div class="h-2 overflow-hidden rounded-full bg-slate-100">
              <div
                class="h-full rounded-full bg-indigo-500"
                :style="{ width: `${(count / maxCount) * 100}%` }"
              ></div>
            </div>
          </li>
        </ul>
        <p v-else class="text-sm text-slate-500">Noch keine Klicks erfasst.</p>
      </div>
    </template>
  </section>
</template>
