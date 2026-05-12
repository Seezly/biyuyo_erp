<template>
  <div class="w-full">
    <div class="mb-4 flex justify-between items-center">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold text-primary">{{ title }}</h2>
        <p class="text-sm text-gray-500">{{ subtitle }}</p>
      </div>
      <div class="text-right">
        <slot name="toolbar">
          <button v-if="showAddButton" :to="addButtonRoute" class="btn-primary">
            <slot name="add-button-text">Añadir nuevo</slot>
          </button>
        </slot>
      </div>
    </div>

    <!-- Search and Filter -->
    <div class="mb-4 flex flex-wrap items-center gap-4">
      <div class="flex-1 min-w-0">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar..."
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          @keyup.enter="applyFilters"
        />
      </div>
      <div class="flex-1 min-w-0">
        <select
          v-model="filters.per_page"
          @change="applyFilters"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="10">10 por página</option>
          <option value="25">25 por página</option>
          <option value="50">50 por página</option>
          <option value="100">100 por página</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <p>Cargando datos...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-8 text-red-500">
      <p>{{ error }}</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && !error && (!data || data.length === 0)" class="text-center py-8">
      <p>No se encontraron resultados.</p>
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th
              v-for="(column, index) in columns"
              :key="index"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              :class="{ 'cursor-pointer sortable': column.sortable }"
              @click="column.sortable ? sortBy(column.key) : null"
            >
              {{ column.label }}
              <span v-if="column.sortable" class="ml-1">
                <svg v-if="sortKey === column.key" class="w-4 h-4" :class="{ 'text-primary': sortDirection === 'asc', 'text-gray-400': sortDirection === 'desc' }" viewBox="0 0 20 20" fill="currentColor">
                  <path v-if="sortDirection === 'asc'" d="M5 9l4-4 4 4H5z" />
                  <path v-else="sortDirection === 'desc'" d="M5 11l4 4 4-4H5z" />
                </svg>
              </span>
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr
            v-for="(item, index) in data"
            :key="index"
            class="bg-white hover:bg-gray-50"
          >
            <td
              v-for="(column, colIndex) in columns"
              :key="colIndex"
              class="px-6 py-4 whitespace-nowrap"
            >
              <slot :name="`cell-${column.key}`" :item="item">
                <!-- Default rendering -->
                <template v-if="column.format">
                  <span>{{ formatValue(item[column.key], column.format) }}</span>
                </template>
                <template v-else>
                  <span>{{ item[column.key] }}</span>
                </template>
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <Pagination
      v-if="pagination"
      :currentPage="pagination.current_page"
      :lastPage="pagination.last_page"
      :from="pagination.from"
      :to="pagination.to"
      :total="pagination.total"
      @update:page="changePage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import Pagination from './Pagination.vue'

interface Column {
  key: string
  label: string
  sortable?: boolean
  format?: 'currency' | 'date' | 'number' | 'boolean'
}

const props = defineProps<{
  title: string
  subtitle?: string
  columns: Column[]
  showAddButton?: boolean
  addButtonRoute?: string
  fetchFunction: (params: any) => Promise<any>
}>

const emit = defineEmits(['row-click', 'row-edit', 'row-delete'])

const state = ref({
  data: [] as any[],
  loading: false,
  error: null as string | null,
  pagination: null as {
    current_page: number
    last_page: number
    from: number
    to: number
    total: number
  } | null,
  filters: {
    search: '',
    per_page: 25,
    page: 1,
    sort_key: '',
    sort_direction: 'asc'
  } as any
})

const searchQuery = ref('')
const sortKey = ref('')
const sortDirection = ref<'asc' | 'desc'>('asc')

// Computed properties
const loading = computed(() => state.value.loading)
const error = computed(() => state.value.error)
const data = computed(() => state.value.data)
const pagination = computed(() => state.value.pagination)

// Filters for API
const filters = computed(() => ({
  search: state.value.filters.search,
  per_page: state.value.filters.per_page,
  page: state.value.filters.page,
  ordering: state.value.filters.sort_key
    ? (state.value.filters.sort_direction === 'desc' ? '-' : '') + state.value.filters.sort_key
    : ''
}))

// Format value based on column format
function formatValue(value: any, format: string): string {
  if (value === null || value === undefined) return ''
  
  switch (format) {
    case 'currency':
      return new Intl.NumberFormat('es-VE', {
        style: 'currency',
        currency: 'USD'
      }).format(value)
    case 'date':
      return new Date(value).toLocaleDateString('es-VE')
    case 'number':
      return new Intl.NumberFormat().format(value)
    case 'boolean':
      return value ? 'Sí' : 'No'
    default:
      return String(value)
  }
}

// Apply filters (triggered by search or per_page change)
function applyFilters() {
  state.value.filters.page = 1 // Reset to first page
  fetchData()
}

// Change sort
function sortBy(key: string) {
  if (state.value.filters.sort_key === key) {
    state.value.filters.sort_direction = 
      state.value.filters.sort_direction === 'asc' ? 'desc' : 'asc'
  } else {
    state.value.filters.sort_key = key
    state.value.filters.sort_direction = 'asc'
  }
  state.value.filters.page = 1
  fetchData()
  
  // Update computed refs
  sortKey.value = state.value.filters.sort_key
  sortDirection.value = state.value.filters.sort_direction
}

// Change page
function changePage(page: number) {
  state.value.filters.page = page
  fetchData()
}

// Fetch data from API
async function fetchData() {
  state.value.loading = true
  state.value.error = null
  
  try {
    const response = await props.fetchFunction(filters.value)
    state.value.data = response.data || response.results || []
    state.value.pagination = {
      current_page: response.meta?.current_page || response.page || 1,
      last_page: response.meta?.last_page || response.total_pages || 1,
      from: response.meta?.from || 1,
      to: response.meta?.to || state.value.data.length,
      total: response.meta?.total || response.total || state.value.data.length
    }
  } catch (e: any) {
    state.value.error = e.message || 'Error fetching data'
    console.error('DataTable fetch error:', e)
  } finally {
    state.value.loading = false
  }
}

// Watch for props changes that might require refetch
watch(() => props.fetchFunction, () => {
  // In practice, we might want to refetch if the function changes
  // For now, we'll rely on manual refresh
})

// Initial fetch
fetchData()
</script>