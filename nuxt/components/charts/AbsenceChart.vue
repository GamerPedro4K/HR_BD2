<script setup lang="ts">
import { computed } from 'vue';
import type { AbsenceAnalytics } from '~/types/analytics';

const props = defineProps<{
  absences: AbsenceAnalytics[];
}>();

const totalDaysAbsent = computed(() => 
  props.absences.reduce((sum, abs) => sum + abs.total_days_absent, 0)
);

const averageDaysAbsent = computed(() => 
  Math.round(totalDaysAbsent.value / props.absences.length)
);

const maxDaysAbsent = computed(() => 
  Math.max(...props.absences.map(abs => abs.total_days_absent))
);

const chartData = computed(() => ({
  labels: props.absences.map(abs => abs.employee_name),
  datasets: [{
    label: 'Dias de Ausência',
    data: props.absences.map(abs => abs.total_days_absent),
    backgroundColor: [
      'rgba(99, 102, 241, 0.8)',   // indigo-500
      'rgba(139, 92, 246, 0.8)',   // violet-500
      'rgba(168, 85, 247, 0.8)',   // purple-500
      'rgba(217, 70, 239, 0.8)',   // fuchsia-500
      'rgba(236, 72, 153, 0.8)'    // pink-500
    ],
    borderColor: [
      'rgb(79, 70, 229)',    // indigo-600
      'rgb(124, 58, 237)',   // violet-600
      'rgb(147, 51, 234)',   // purple-600
      'rgb(192, 38, 211)',   // fuchsia-600
      'rgb(219, 39, 119)'    // pink-600
    ],
    borderWidth: 1,
    borderRadius: 6,
    barThickness: 24
  }]
}));

const chartOptions = {
  indexAxis: 'y',
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      titleColor: '#fff',
      bodyColor: '#fff',
      padding: 12,
      boxPadding: 8,
      cornerRadius: 8,
      displayColors: false,
      callbacks: {
        title: (items: any[]) => {
          const index = items[0].dataIndex;
          return props.absences[index].employee_name;
        },
        label: (context: any) => {
          const absence = props.absences[context.dataIndex];
          return [
            `Dias Ausente: ${absence.total_days_absent}`,
            `Total Ausências: ${absence.total_absences}`,
            `% do Total: ${((absence.total_days_absent / totalDaysAbsent.value) * 100).toFixed(1)}%`
          ];
        }
      }
    }
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(203, 213, 225, 0.3)',
        drawBorder: false
      },
      ticks: {
        color: '#475569',
        font: {
          size: 11
        },
        padding: 8
      },
      title: {
        display: true,
        text: 'Dias de Ausência',
        color: '#334155',
        font: {
          size: 13,
          weight: '600'
        },
        padding: { top: 15 }
      }
    },
    y: {
      grid: {
        display: false
      },
      ticks: {
        color: '#475569',
        font: {
          size: 11,
          weight: '500'
        }
      }
    }
  },
  maintainAspectRatio: false,
  responsive: true,
  interaction: {
    intersect: false,
    mode: 'index'
  },
  animation: {
    duration: 750
  }
}
</script>

<template>
  <div class="card bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-surface-200 dark:border-surface-700">
    <!-- Cabeçalho -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-white">
          Ausências por Funcionário
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Top {{ absences.length }} funcionários com mais ausências
        </p>
      </div>
      <div class="flex gap-2">
        <span class="px-3 py-1 text-xs font-medium bg-indigo-100 text-indigo-600 rounded-full dark:bg-indigo-500/20 dark:text-indigo-400">
          {{ absences.length }} Funcionários
        </span>
      </div>
    </div>

    <!-- Gráfico -->
    <div class="h-80">
      <Chart 
        type="bar" 
        :data="chartData" 
        :options="chartOptions" 
        class="h-full w-full"
      />
    </div>

    <!-- Métricas -->
    <div class="grid grid-cols-3 gap-4 mt-6">
      <div class="p-4 bg-indigo-50 rounded-lg dark:bg-indigo-500/10">
        <p class="text-sm text-indigo-600 dark:text-indigo-400 font-medium">Total de Dias</p>
        <p class="text-xl font-semibold text-indigo-700 dark:text-indigo-300">
          {{ totalDaysAbsent }}
        </p>
      </div>
      <div class="p-4 bg-violet-50 rounded-lg dark:bg-violet-500/10">
        <p class="text-sm text-violet-600 dark:text-violet-400 font-medium">Média de Dias</p>
        <p class="text-xl font-semibold text-violet-700 dark:text-violet-300">
          {{ averageDaysAbsent }}
        </p>
      </div>
      <div class="p-4 bg-purple-50 rounded-lg dark:bg-purple-500/10">
        <p class="text-sm text-purple-600 dark:text-purple-400 font-medium">Máximo de Dias</p>
        <p class="text-xl font-semibold text-purple-700 dark:text-purple-300">
          {{ maxDaysAbsent }}
        </p>
      </div>
    </div>
  </div>
</template>