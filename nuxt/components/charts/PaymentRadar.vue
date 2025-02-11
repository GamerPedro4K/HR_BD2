<script setup lang="ts">
import { computed } from 'vue';
import type { PaymentAnalytics } from '~/types/analytics';

const props = defineProps<{
  paymentData: PaymentAnalytics;
}>();

const chartData = computed(() => ({
  labels: [
    'Salário Base',
    'Bônus Total',
    'Deduções',
    'Funcionários com Bônus',
    'Funcionários com Dedução',
    'Pagamento Médio'
  ],
  datasets: [{
    label: 'Métricas de Pagamento',
    data: [
      Number(props.paymentData.total_base_salary),
      Number(props.paymentData.total_bonus_amount),
      Number(props.paymentData.total_deduction_amount),
      props.paymentData.employees_with_bonus,
      props.paymentData.employees_with_deduction,
      Number(props.paymentData.average_payment)
    ],
    backgroundColor: 'rgba(99, 102, 241, 0.15)', // Indigo transparente
    borderColor: '#6366F1',                      // Indigo sólido
    pointBackgroundColor: [
      '#3B82F6', // blue-500
      '#10B981', // emerald-500
      '#F59E0B', // amber-500
      '#8B5CF6', // violet-500
      '#EC4899', // pink-500
      '#6366F1'  // indigo-500
    ],
    pointBorderColor: [
      '#2563EB', // blue-600
      '#059669', // emerald-600
      '#D97706', // amber-600
      '#7C3AED', // violet-600
      '#DB2777', // pink-600
      '#4F46E5'  // indigo-600
    ],
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: '#6366F1',
    pointRadius: 6,
    pointHoverRadius: 8,
    fill: true,
    borderWidth: 2
  }]
}));

const chartOptions = {
  plugins: {
    legend: {
      display: false // Remove a legenda pois só temos um dataset
    },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.9)', // gray-900 com transparência
      titleColor: '#fff',
      bodyColor: '#fff',
      padding: 12,
      boxPadding: 8,
      cornerRadius: 8,
      displayColors: false,
      callbacks: {
        title: (tooltipItems: any[]) => {
          return tooltipItems[0].label;
        },
        label: (context: any) => {
          const value = context.raw;
          if (context.label.includes('Salário') || context.label.includes('Bônus') || 
              context.label.includes('Deduções') || context.label.includes('Pagamento')) {
            return `Valor: € ${value.toLocaleString('pt-PT', { 
              minimumFractionDigits: 2,
              maximumFractionDigits: 2 
            })}`;
          }
          return `Total: ${value}`;
        }
      }
    }
  },
  scales: {
    r: {
      min: 0,
      grid: {
        color: 'rgba(203, 213, 225, 0.3)', // slate-200 com transparência
      },
      ticks: {
        backdropColor: 'transparent',
        color: '#475569', // slate-600
        font: {
          size: 11
        }
      },
      pointLabels: {
        color: '#334155', // slate-700
        font: {
          size: 12,
          weight: '500'
        }
      },
      angleLines: {
        color: 'rgba(203, 213, 225, 0.5)' // slate-200 com mais transparência
      }
    }
  },
  elements: {
    line: {
      tension: 0.2 // Suaviza levemente as linhas
    }
  },
  maintainAspectRatio: false
}
</script>

<template>
  <div class="card bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-surface-200 dark:border-surface-700 ">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-white">
        Métricas de Pagamento
      </h3>
      <div class="flex gap-2">
        <span class="px-3 py-1 text-xs font-medium bg-indigo-100 text-indigo-600 rounded-full dark:bg-indigo-500/20 dark:text-indigo-400">
          Mensal
        </span>
      </div>
    </div>
    
    <div class="h-80">
      <Chart 
        type="radar" 
        :data="chartData" 
        :options="chartOptions"
        class="h-full w-full"
      />
    </div>
    
    <div class="grid grid-cols-3 gap-4 mt-6 text-center">
      <div class="p-3 bg-blue-50 rounded-lg dark:bg-blue-500/10">
        <p class="text-sm text-blue-600 dark:text-blue-400 font-medium">Salário Base</p>
        <p class="text-lg font-semibold text-blue-700 dark:text-blue-300">
          {{ new Intl.NumberFormat('pt-PT', { 
            style: 'currency', 
            currency: 'EUR' 
          }).format(Number(props.paymentData.total_base_salary)) }}
        </p>
      </div>
      <div class="p-3 bg-emerald-50 rounded-lg dark:bg-emerald-500/10">
        <p class="text-sm text-emerald-600 dark:text-emerald-400 font-medium">Bônus Total</p>
        <p class="text-lg font-semibold text-emerald-700 dark:text-emerald-300">
          {{ new Intl.NumberFormat('pt-PT', { 
            style: 'currency', 
            currency: 'EUR' 
          }).format(Number(props.paymentData.total_bonus_amount)) }}
        </p>
      </div>
      <div class="p-3 bg-amber-50 rounded-lg dark:bg-amber-500/10">
        <p class="text-sm text-amber-600 dark:text-amber-400 font-medium">Deduções</p>
        <p class="text-lg font-semibold text-amber-700 dark:text-amber-300">
          {{ new Intl.NumberFormat('pt-PT', { 
            style: 'currency', 
            currency: 'EUR' 
          }).format(Number(props.paymentData.total_deduction_amount)) }}
        </p>
      </div>
    </div>
  </div>
</template>