<template>
  <nav class="flex items-center gap-2 text-sm text-gray-500" aria-label="Breadcrumb">
    <router-link to="/" class="flex items-center gap-1 hover:text-primary transition-colors">
      <i class="fa-solid fa-home"></i>
      Inicio
    </router-link>
    <span class="mx-2">/</span>
    <template v-for="(route, index) in breadcrumbs" :key="index">
      <template v-if="index < breadcrumbs.length - 1">
        <router-link :to="route.path" class="flex items-center gap-1 hover:text-primary transition-colors">
          {{ route.meta.title || route.name }}
        </router-link>
        <span class="mx-2">/</span>
      </template>
      <template v-else>
        <span class="text-gray-700 font-medium">{{ route.meta.title || route.name }}</span>
      </template>
    </template>
  </nav>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const router = useRouter()

const breadcrumbs = computed(() => {
  const { matched } = route
  // Filter out routes that are not visible in breadcrumb (e.g., empty path children)
  return matched.filter((r) => {
    // Skip routes that are not intended to be displayed in breadcrumb
    // For example, we might skip the root route or routes with meta.hideInBreadcrumb
    return !r.meta.hideInBreadcrumb && (r.name || r.path !== '/')
  })
})
</script>