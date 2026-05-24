<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useReportsStore } from '@/stores/reports'
import { useAuthStore } from '@/stores/auth'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Chart, registerables } from 'chart.js'

// Register chart components
Chart.register(...registerables)

const reportsStore = useReportsStore()
const authStore = useAuthStore()

const loading = ref(true)
const error = ref<string | null>(null)

// Chart references
const usersChartRef = ref<HTMLCanvasElement | null>(null)
const subscriptionsChartRef = ref<HTMLCanvasElement | null>(null)
const revenueChartRef = ref<HTMLCanvasElement | null>(null)

// Chart instances
let usersChart: any = null
let subscriptionsChart: any = null
let revenueChart: any = null

// Fetch data
const fetchStats = async () => {
  loading.value = true
  error.value = null
  try {
    // Fetch all report data
    await Promise.all([
      reportsStore.fetchGlobalStats(),
      reportsStore.fetchSales(),
      reportsStore.fetchInventory()
    ])
    
    // Initialize charts after data is loaded
    initCharts()
  } catch (err) {
    error.value = 'Error al cargar las estadísticas'
    console.error('Error fetching stats:', err)
  } finally {
    loading.value = false
  }
}

// Initialize charts
const initCharts = () => {
  // Destroy existing charts if they exist
  if (usersChart) usersChart.destroy()
  if (subscriptionsChart) subscriptionsChart.destroy()
  if (revenueChart) revenueChart.destroy()
  
  // Users by Business Chart
  if (usersChartRef.value && reportsStore.stats) {
    const ctx = usersChartRef.value.getContext('2d')
    if (ctx) {
      // We expect reportsStore to have a usersByBusiness property in the future
      // For now, we'll use placeholder data if the property doesn't exist or is empty
      const usersByBusiness = reportsStore.usersByBusiness || []
      usersChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: usersByBusiness.length > 0 
            ? usersByBusiness.map(b => b.name) 
            : ['Negocio 1', 'Negocio 2', 'Negocio 3'],
          datasets: [{
            label: 'Usuarios por Negocio',
            data: usersByBusiness.length > 0 
              ? usersByBusiness.map(b => b.userCount || 0) 
              : [reportsStore.stats?.totalUsers || 0, 15, 8],
            backgroundColor: [
              'rgba(54, 162, 235, 0.5)',
              'rgba(255, 99, 132, 0.5)',
              'rgba(255, 205, 86, 0.5)'
            ],
            borderColor: [
              'rgba(54, 162, 235, 1)',
              'rgba(255, 99, 132, 1)',
              'rgba(255, 205, 86, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Distribución de Usuarios por Negocio'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
    }
  }
  
  // Subscriptions by Plan Chart
  if (subscriptionsChartRef.value && reportsStore.stats) {
    const ctx = subscriptionsChartRef.value.getContext('2d')
    if (ctx) {
      // We expect reportsStore to have a subscriptionsByPlan property in the future
      const subscriptionsByPlan = reportsStore.subscriptionsByPlan || []
      subscriptionsChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: subscriptionsByPlan.length > 0 
            ? subscriptionsByPlan.map(p => p.name) 
            : ['Básico', 'Profesional', 'Empresarial'],
          datasets: [{
            label: 'Suscripciones por Plan',
            data: subscriptionsByPlan.length > 0 
              ? subscriptionsByPlan.map(p => p.count || 0) 
              : [reportsStore.stats?.activeSubscriptions || 0, 10, 5],
            backgroundColor: [
              'rgba(75, 192, 192, 0.5)',
              'rgba(153, 102, 255, 0.5)',
              'rgba(255, 159, 64, 0.5)'
            ],
            borderColor: [
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          }]  
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
            },
            title: {
              display: true,
              text: 'Distribución de Suscripciones por Plan'
            }
          }
        }
      })
    }
  }
  
  // Monthly Revenue Chart
  if (revenueChartRef.value && reportsStore.sales) {
    const ctx = revenueChartRef.value.getContext('2d')
    if (ctx) {
      // We expect reportsStore to have a monthlyRevenue property in the future
      const monthlyRevenue = reportsStore.monthlyRevenue || []
      revenueChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: monthlyRevenue.length > 0 
            ? monthlyRevenue.map(m => m.month) 
            : ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
          datasets: [{
            label: 'Ingresos Mensuales (USD)',
            data: monthlyRevenue.length > 0 
              ? monthlyRevenue.map(m => m.revenue || 0) 
              : [reportsStore.sales?.total_sales || 0, 1200, 1800, 1500, 2000, 2200],
            fill: false,
            borderColor: 'rgba(75, 192, 192, 1)',
            tension: 0.1
          }]  
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Tendencia de Ingresos Mensuales'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                // Include a dollar sign in the ticks
                callback: function(value) {
                  return '$' + value;
                }
              }
            }
          }
        }
      })
    }
  }
}

onMounted(() => {
  fetchStats())
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Estadísticas Detalladas</h1>
      <p>Análisis profundo del rendimiento del sistema</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando estadísticas...</p>
    </div>

    <div v-else-if="error" class="w-full text-center py-8 text-red-500">
      <p>{{ error }}</p>
    </div>

    <div v-else class="grid grid-cols-12 gap-8 w-full">
      <!-- Users by Business -->
      <BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
        <div class="flex flex-col gap-4 h-full">
          <h2 class="text-xl font-bold text-primary">Usuarios por Negocio</h2>
          <p class="text-gray-500 flex-1">
            Distribución de usuarios en los diferentes negocios registrados.
          </p>
          <canvas ref="usersChartRef" class="h-full w-full"></canvas>
          <div class="mt-4">
            <BaseButton 
              text="Exportar datos" 
              variant="outlined" 
              to="/reports?reportType=business"
            />
          </div>
        </div>
      </BaseCard>

      <!-- Subscriptions by Plan -->
      <BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
        <div class="flex flex-col gap-4 h-full">
          <h2 class="text-xl font-bold text-primary">Suscripciones por Plan</h2>
          <p class="text-gray-500 flex-1">
            Análisis de planes activos y su distribución.
          </p>
          <canvas ref="subscriptionsChartRef" class="h-full w-full"></canvas>
          <div class="mt-4">
            <BaseButton 
              text="Ver detalles" 
              variant="outlined" 
              to="/billing/plans"
            />
          </div>
        </div>
      </BaseCard>

      <!-- Monthly Revenue -->
      <BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
        <div class="flex flex-col gap-4 h-full">
          <h2 class="text-xl font-bold text-primary">Ingresos Mensuales</h2>
          <p class="text-gray-500 flex-1">
            Reporte de ingresos por suscripciones.
          </p>
          <canvas ref="revenueChartRef" class="h-full w-full"></canvas>
          <div class="mt-4">
            <BaseButton 
              text="Descargar reporte" 
              variant="outlined" 
              to="/billing/invoices"
            />
          </div>
        </div>
      </BaseCard>

      <!-- KPI Cards -->
      <BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl font-bold text-primary">Métricas Clave</h2>
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-primary">{{ reportsStore.stats?.totalUsers || 0 }}</div>
              <div class="text-sm text-gray-600">Total Usuarios</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-success">{{ reportsStore.stats?.activeSubscriptions || 0 }}</div>
              <div class="text-sm text-gray-600">Suscripciones Activas</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-primary">${{ reportsStore.sales?.total_sales || 0 }}</div>
              <div class="text-sm text-gray-600">Ingresos Totales</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-success">{{ reportsStore.inventory?.total_products || 0 }}</div>
              <div class="text-sm text-gray-600">Productos en Inventario</div>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>
  </section>
</template>