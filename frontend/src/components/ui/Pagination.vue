<template>
  <nav class="flex flex-wrap items-center justify-between px-2 pt-1 pb-3" aria-label="Paginación">
    <span class="text-xs text-gray-500 dark:text-gray-400">
      Showing {{ from }} to {{ to }} of {{ total }} entries
    </span>
    <div class="flex items-center">
      <!-- Previous Button -->
      <button
        :disabled="currentPage <= 1"
        @click="goPrev"
        class="flex items-center px-2.5 pt-1 pb-2 mr-2 mb-0 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
      >
        <svg class="w-2 h-2 mr-1" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        Previous
      </button>

      <!-- Page Indicator -->
      <span class="px-3 pt-1 pb-2 text-sm font-medium text-gray-900 dark:text-gray-100">
        Page {{ currentPage }} of {{ lastPage }}
      </span>

      <!-- Next Button -->
      <button
        :disabled="currentPage >= lastPage"
        @click="goNext"
        class="flex items-center px-2.5 pt-1 pb-2 ml-2 mb-0 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
      >
        Next
        <svg class="w-2 h-2 ml-1" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 001.414 0l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
const props = defineProps<{
  currentPage: number
  lastPage: number
  from: number
  to: number
  total: number
}>()

const emit = defineEmits(['update:page'])

const goPrev = () => {
  if (props.currentPage > 1) {
    emit('update:page', props.currentPage - 1)
  }
}

const goNext = () => {
  if (props.currentPage < props.lastPage) {
    emit('update:page', props.currentPage + 1)
  }
}
</script>
