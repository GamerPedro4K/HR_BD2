<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useAnalytics } from '~/composables/useAnalytics';
import PaymentRadarChart from '~/components/charts/PaymentRadar.vue';
import DepartmentBubbleChart from '~/components/charts/DepartmentBubbleChart.vue';
import AbsencePolarChart from '~/components/charts/AbsenceChart.vue';
import EmployeeMetricCard from '~/components/charts/EmployeeMetricCard.vue';

const { getAnalytics } = useAnalytics();
const dashboardData = ref<any>(null);
const loading = ref(true);

onMounted(async () => {
  dashboardData.value = await getAnalytics();
  loading.value = false;
});

const totalEmployees = computed(() => {
  if (!dashboardData.value?.department_counts) return 0;
  return dashboardData.value.department_counts.reduce(
    (acc: any, dept: { total_employees: any; }) => acc + dept.total_employees, 0
  );
});

const formattedCurrency = (value: string | number) => {
  return new Intl.NumberFormat('pt-PT', {
    style: 'currency',
    currency: 'EUR'
  }).format(Number(value));
};
</script>

<template>
  <div class="grid">
    <div v-if="loading" class="col-12">
      <ProgressSpinner />
    </div>
    
    <template v-else-if="dashboardData">
        <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <EmployeeMetricCard
                title="Total de Funcionários"
                :value="totalEmployees"
                icon="pi-users"
                iconBackground="bg-blue-100 dark:bg-blue-500/10"
                iconColor="text-blue-500"
                :trend="{
                value: '24',
                label: 'novos este mês'
                }"
            />
            </div>

            <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <EmployeeMetricCard
                title="Média Salarial"
                :value="formattedCurrency(dashboardData.current_month_payments[0].average_payment)"
                icon="pi-money-bill"
                iconBackground="bg-green-100 dark:bg-green-500/10"
                iconColor="text-green-500"
                :trend="{
                value: '+5.2%',
                label: 'em relação ao mês anterior'
                }"
            />
            </div>

            <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <EmployeeMetricCard
                title="Funcionários com Bônus"
                :value="dashboardData.current_month_payments[0].employees_with_bonus"
                icon="pi-star"
                iconBackground="bg-orange-100 dark:bg-orange-500/10"
                iconColor="text-orange-500"
                :trend="{
                value: '31',
                label: 'receberam bônus'
                }"
            />
            </div>

            <div class="col-span-12 lg:col-span-6 xl:col-span-3">
            <EmployeeMetricCard
                title="Total de Ausências"
                :value="dashboardData.top_absences.reduce((acc: any, cur: any) => acc + cur.total_absences, 0)"
                icon="pi-calendar-times"
                iconBackground="bg-red-100 dark:bg-red-500/10"
                iconColor="text-red-500"
                :trend="{
                value: '5',
                label: 'funcionários ausentes'
                }"
            />
            </div>
        </div>
        <div class="col-12 lg:col-6 mt-3">
            <PaymentRadarChart :payment-data="dashboardData.current_month_payments[0]" />
        </div>
        <div class="col-12 lg:col-6 mt-3">
            <AbsencePolarChart :absences="dashboardData.top_absences" />
        </div>


      <div class="col-12 lg:col-6 mt-3">
            <DepartmentBubbleChart :department-salaries="dashboardData.department_salaries" />
      </div>

      
    </template>
  </div>
</template>