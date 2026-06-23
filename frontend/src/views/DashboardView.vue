<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { api, ApiError } from '@/api/client'
import type { Link } from '@/types'
import { isValidAlias, isValidHttpUrl } from '@/utils/validation'

const links = ref<Link[]>([])
const targetUrl = ref('')
const alias = ref('')
const error = ref('')
const listError = ref('')
const listLoading = ref(true)
const creating = ref(false)
const deletingCode = ref<string | null>(null)
const confirmingCode = ref<string | null>(null)
const copied = ref<string | null>(null)

async function load() {
  listError.value = ''
  listLoading.value = true
  try {
    links.value = await api.listLinks()
  } catch (e) {
    listError.value =
      e instanceof ApiError ? e.message : 'Kurzlinks konnten nicht geladen werden.'
  } finally {
    listLoading.value = false
  }
}

onMounted(load)

async function create() {
  error.value = ''
  if (!isValidHttpUrl(targetUrl.value)) {
    error.value = 'Bitte eine gültige http(s)-URL eingeben.'
    return
  }
  if (alias.value.trim() && !isValidAlias(alias.value.trim())) {
    error.value = 'Alias: 3–32 Zeichen aus Buchstaben, Ziffern, „-" und „_".'
    return
  }
  creating.value = true
  try {
    await api.createLink(targetUrl.value.trim(), alias.value.trim() || undefined)
    targetUrl.value = ''
    alias.value = ''
    await load()
  } catch (e) {
    error.value = e instanceof ApiError ? e.message : 'Kurzlink konnte nicht angelegt werden.'
  } finally {
    creating.value = false
  }
}

async function remove(code: string) {
  error.value = ''
  deletingCode.value = code
  try {
    await api.deleteLink(code)
    confirmingCode.value = null
    await load()
  } catch (e) {
    error.value = e instanceof ApiError ? e.message : 'Löschen fehlgeschlagen.'
  } finally {
    deletingCode.value = null
  }
}

async function copy(link: Link) {
  try {
    await navigator.clipboard.writeText(link.short_url)
    copied.value = link.code
    window.setTimeout(() => {
      copied.value = null
    }, 1500)
  } catch {
    error.value = 'Kopieren nicht möglich.'
  }
}
</script>

<template>
  <section>
    <h1 class="text-2xl font-bold text-slate-900">Meine Kurzlinks</h1>
    <p class="mt-1 text-sm text-slate-500">
      Lege neue Kurzlinks an und behalte ihre Klicks im Blick.
    </p>

    <form
      class="mt-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:flex sm:items-end sm:gap-3"
      novalidate
      @submit.prevent="create"
    >
      <div class="flex-1">
        <label class="mb-1 block text-sm font-medium text-slate-700" for="target">Ziel-URL</label>
        <input
          id="target"
          v-model="targetUrl"
          type="url"
          placeholder="https://example.com/sehr/lange/url"
          class="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
        />
      </div>
      <div class="mt-3 sm:mt-0 sm:w-40">
        <label class="mb-1 block text-sm font-medium text-slate-700" for="alias">
          Alias <span class="text-slate-400">(optional)</span>
        </label>
        <input
          id="alias"
          v-model="alias"
          type="text"
          placeholder="mein-link"
          class="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
        />
      </div>
      <button
        type="submit"
        :disabled="creating"
        class="mt-3 w-full rounded-lg bg-indigo-600 px-5 py-2 font-medium text-white transition hover:bg-indigo-700 disabled:opacity-60 sm:mt-0 sm:w-auto"
      >
        {{ creating ? 'Anlegen …' : 'Anlegen' }}
      </button>
    </form>

    <p v-if="error" class="mt-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
      {{ error }}
    </p>

    <p v-if="listLoading" class="mt-6 text-sm text-slate-500">Kurzlinks werden geladen …</p>

    <p v-else-if="listError" class="mt-6 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
      {{ listError }}
    </p>

    <ul v-else-if="links.length" class="mt-6 space-y-3">
      <li
        v-for="link in links"
        :key="link.code"
        class="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between"
      >
        <div class="min-w-0">
          <a
            :href="link.short_url"
            target="_blank"
            rel="noopener"
            class="font-medium text-indigo-600 hover:underline"
          >
            {{ link.short_url }}
          </a>
          <p class="truncate text-sm text-slate-500">{{ link.target_url }}</p>
        </div>

        <div class="flex shrink-0 items-center gap-2 text-sm">
          <template v-if="confirmingCode === link.code">
            <span class="text-slate-500">Wirklich löschen?</span>
            <button
              type="button"
              :disabled="deletingCode === link.code"
              class="rounded-md bg-red-600 px-3 py-1.5 font-medium text-white transition hover:bg-red-700 disabled:opacity-60"
              @click="remove(link.code)"
            >
              {{ deletingCode === link.code ? 'Löscht …' : 'Ja, löschen' }}
            </button>
            <button
              type="button"
              class="rounded-md border border-slate-200 px-3 py-1.5 font-medium text-slate-600 transition hover:bg-slate-100"
              @click="confirmingCode = null"
            >
              Abbrechen
            </button>
          </template>
          <template v-else>
            <button
              type="button"
              class="rounded-md border border-slate-200 px-3 py-1.5 font-medium text-slate-600 transition hover:bg-slate-100"
              @click="copy(link)"
            >
              {{ copied === link.code ? 'Kopiert ✓' : 'Kopieren' }}
            </button>
            <RouterLink
              :to="{ name: 'stats', params: { code: link.code } }"
              class="rounded-md border border-slate-200 px-3 py-1.5 font-medium text-slate-600 transition hover:bg-slate-100"
            >
              Statistik
            </RouterLink>
            <button
              type="button"
              class="rounded-md border border-red-200 px-3 py-1.5 font-medium text-red-600 transition hover:bg-red-50"
              @click="confirmingCode = link.code"
            >
              Löschen
            </button>
          </template>
        </div>
      </li>
    </ul>

    <p
      v-else
      class="mt-6 rounded-xl border border-dashed border-slate-300 p-8 text-center text-slate-500"
    >
      Noch keine Kurzlinks – lege oben deinen ersten an.
    </p>
  </section>
</template>
