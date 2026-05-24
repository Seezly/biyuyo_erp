<template>
  <nav class="flex items-center justify-center gap-2" aria-label="Pagination">
    <!-- Previous Button -->
    <button
      :disabled="page <= 1"
      @click="handlePageChange(page - 1)"
      class="px-3 py-1 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition-colors"
    >
      <i class="fa-solid fa-chevron-left"></i>
    </button>

    <!-- Page Numbers -->
    <template v-if="pageCount <= 7">
      <!-- Show all pages if 7 or fewer -->
      <template v-for="p in pageCount" :key="p">
        <button
          :class="[
            'px-3 py-1 rounded',
            page === p ? 'bg-primary text-white' : 'hover:bg-gray-100 transition-colors'
          ]"
          @click="handlePageChange(p)"
        >
          {{ p }}
        </button>
      </template>
    </template>
    <template v-else>
      <!-- Show first page -->
      <button
        :class="[
          'px-3 py-1 rounded',
          page === 1 ? 'bg-primary text-white' : 'hover:bg-gray-100 transition-colors'
        ]"
        @click="handlePageChange(1)"
      >
        1
      </button>
      
      <!-- Show ellipsis if needed -->
      <template v-if="page > 3">
        <span class="px-3 py-1 rounded">…</span>
      </template>
      
      <!-- Show pages around current page -->
      <template v-for="p in getPageRange(page, pageCount)" :key="p">
        <button
          :class="[
            'px-3 py-1 rounded',
            page === p ? 'bg-primary text-white' : 'hover:bg-gray-100 transition-colors'
          ]"
          @click="handlePageChange(p)"
        >
          {{ p }}
        </button>
      </template>
      
      <!-- Show ellipsis if needed -->
      <template v-if="page < pageCount - 2">
        <span class="px-3 py-1 rounded">…</span>
      </template>
      
      <!-- Show last page -->
      <button
        :class="[
          'px-3 py-1 rounded',
          page === pageCount ? 'bg-primary text-white' : 'hover:bg-gray-100 transition-colors'
        ]"
        @click="handlePageChange(pageCount)"
      >
        {{ pageCount }}
      </button>
    </template>

    <!-- Next Button -->
    <button
      :disabled="page >= pageCount"
      @click="handlePageChange(page + 1)"
      class="px-3 py-1 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition-colors"
    >
      <i class="fa-solid fa-chevron-right"></i>
    </button>
  </nav>
</template>

<script setup lang="ts">
const props = defineProps<{
  total: number;           // Total number of items
  page: number;            // Current page (1-indexed)
  pageCount: number;       // Total number of pages
}>();

const emit = defineEmits(['update']);

const handlePageChange = (page: number) => {
  if (page >= 1 && page <= props.pageCount && page !== props.page) {
    emit('update', page);
  }
};

// Generate a range of numbers for the middle section of pagination
function getPageRange(currentPage: number, totalPages: number): number[] {
  const start = Math.max(2, currentPage - 1);
  const end = Math.min(totalPages - 1, currentPage + 1);
  const range: number[] = [];
  for (let i = start; i <= end; i++) {
    range.push(i);
  }
  return range;
}
</script>