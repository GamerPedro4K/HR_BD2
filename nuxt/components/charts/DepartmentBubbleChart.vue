<script setup lang="ts">
import { computed } from 'vue';
import type { DepartmentSalary } from '~/types/analytics';

const props = defineProps<{
  departmentSalaries: DepartmentSalary[];
}>();

// Computar métricas
const totalEmployees = computed(() => 
  props.departmentSalaries.reduce((sum, dept) => sum + dept.employee_count, 0)
);

const avgSalaryTotal = computed(() => 
  (props.departmentSalaries.reduce((sum, dept) => sum + Number(dept.avg_salary), 0) / props.departmentSalaries.length).toFixed(2)
);

const maxSalaryDept = computed(() => {
  return props.departmentSalaries.reduce((max, dept) => 
    Number(dept.avg_salary) > Number(max.avg_salary) ? dept : max
  , props.departmentSalaries[0]);
});

const chartData = computed(() => ({
  datasets: [{
    label: 'Departamentos',
    data: props.departmentSalaries.map(dept => ({
      x: Number(dept.avg_salary),
      y: dept.employee_count,
      r: Math.sqrt(dept.employee_count) * 4 // Bolhas um pouco maiores
    })),
    backgroundColor: [
      'rgba(79, 70, 229, 0.7)',  // indigo-600
      'rgba(16, 185, 129, 0.7)', // emerald-500
      'rgba(245, 158, 11, 0.7)', // amber-500
      'rgba(139, 92, 246, 0.7)', // violet-500
      'rgba(236, 72, 153, 0.7)'  // pink-500
    ],
    borderColor: [
      'rgb(67, 56, 202)',      // indigo-700
      'rgb(4, 120, 87)',       // emerald-700
      'rgb(180, 83, 9)',       // amber-700
      'rgb(109, 40, 217)',     // violet-700
      'rgb(190, 24, 93)'       // pink-700
    ],
    borderWidth: 2,
    hoverBackgroundColor: [
      'rgba(79, 70, 229, 0.9)',
      'rgba(16, 185, 129, 0.9)',
      'rgba(245, 158, 11, 0.9)',
      'rgba(139, 92, 246, 0.9)',
      'rgba(236, 72, 153, 0.9)'
    ],
    hoverBorderColor: [
      'rgb(67, 56, 202)',
      'rgb(4, 120, 87)',
      'rgb(180, 83, 9)',
      'rgb(109, 40, 217)',
      'rgb(190, 24, 93)'
    ],
    hoverBorderWidth: 3
  }],
  labels: props.departmentSalaries.map(dept => dept.department_name)
}));

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-PT', {
    style: 'currency',
    currency: 'EUR'
  }).format(value);
};

const chartOptions = {
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
        label: (context: any) => {
          const dept = props.departmentSalaries[context.dataIndex];
          const percentageOfTotal = ((dept.employee_count / totalEmployees.value) * 100).toFixed(1);
          return [
            `Departamento: ${dept.department_name}`,
            `Média Salarial: ${formatCurrency(Number(dept.avg_salary))}`,
            `Funcionários: ${dept.employee_count} (${percentageOfTotal}%)`,
            `Salário Min: ${formatCurrency(Number(dept.min_salary))}`,
            `Salário Max: ${formatCurrency(Number(dept.max_salary))}`
          ];
        }
      }
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Média Salarial (€)',
        color: '#334155',
        font: {
          size: 13,
          weight: '600'
        },
        padding: { top: 15 }
      },
      grid: {
        color: 'rgba(203, 213, 225, 0.3)',
        drawBorder: false
      },
      ticks: {
        color: '#475569',
        callback: (value: number) => formatCurrency(value),
        font: {
          size: 11
        }
      }
    },
    y: {
      title: {
        display: true,
        text: 'Número de Funcionários',
        color: '#334155',
        font: {
          size: 13,
          weight: '600'
        }
      },
      grid: {
        color: 'rgba(203, 213, 225, 0.3)',
        drawBorder: false
      },
      ticks: {
        color: '#475569',
        font: {
          size: 11
        }
      }
    }
  },
  maintainAspectRatio: false,
  responsive: true,
  animation: {
    duration: 750
  }
};
</script>

<template>
  <div class="card bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-surface-200 dark:border-surface-700">
    <!-- Cabeçalho -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-white">
          Análise de Departamentos
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Relação entre salário médio e número de funcionários
        </p>
      </div>
      <div class="flex gap-2">
        <span class="px-3 py-1 text-xs font-medium bg-indigo-100 text-indigo-600 rounded-full dark:bg-indigo-500/20 dark:text-indigo-400">
          {{ departmentSalaries.length }} Departamentos
        </span>
      </div>
    </div>

    <!-- Gráfico -->
    <div class="h-80">
      <Chart type="bubble" :data="chartData" :options="chartOptions" class="h-full w-full" />
    </div>

    <!-- Métricas -->
    <div class="grid grid-cols-3 gap-4 mt-6">
      <div class="p-4 bg-indigo-50 rounded-lg dark:bg-indigo-500/10">
        <p class="text-sm text-indigo-600 dark:text-indigo-400 font-medium">Total de Funcionários</p>
        <p class="text-xl font-semibold text-indigo-700 dark:text-indigo-300">
          {{ totalEmployees }}
        </p>
      </div>
      <div class="p-4 bg-emerald-50 rounded-lg dark:bg-emerald-500/10">
        <p class="text-sm text-emerald-600 dark:text-emerald-400 font-medium">Média Salarial Geral</p>
        <p class="text-xl font-semibold text-emerald-700 dark:text-emerald-300">
          {{ formatCurrency(Number(avgSalaryTotal)) }}
        </p>
      </div>
      <div class="p-4 bg-amber-50 rounded-lg dark:bg-amber-500/10">
        <p class="text-sm text-amber-600 dark:text-amber-400 font-medium">Maior Média Salarial</p>
        <div class="text-amber-700 dark:text-amber-300">
          <p class="text-xl font-semibold">{{ formatCurrency(Number(maxSalaryDept.avg_salary)) }}</p>
          <p class="text-xs mt-1">{{ maxSalaryDept.department_name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>