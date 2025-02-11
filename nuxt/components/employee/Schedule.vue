<script setup lang="ts">
import { defineProps, type PropType } from 'vue';

const props = defineProps({
  schedule: {
    type: Object as PropType<any>,
    required: true,
  },
});

const schedule = props.schedule.workSchedule;

// Função para obter o horário de um dia específico
const getDaySchedule = (day: string) => {
  return schedule[day] ? `${schedule[day].start} - ${schedule[day].end}` : 'No schedule';
};

// Dias da semana
const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'];

// Obter o dia da semana atual
const currentDay = new Date().toLocaleString('en-us', { weekday: 'long' }).toLowerCase();
</script>

<template>
  <div class="p-6 max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-xl transition-all">
    <div class="text-center mb-6">
      <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-200">Horários de Trabalho</h2>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
      <div v-for="(day, index) in days" :key="index" :class="{
        'bg-gradient-to-r from-green-100 to-green-200 dark:from-green-700 dark:to-green-800': day === currentDay,
        'bg-gradient-to-r from-indigo-100 to-indigo-200 dark:from-gray-700 dark:to-gray-800': day !== currentDay
      }" class="p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all">
        <div :class="{
          'text-xl font-semibold text-green-900 dark:text-green-100': day === currentDay,
          'text-xl font-semibold text-gray-900 dark:text-gray-100': day !== currentDay
        }" class="capitalize">
          {{ day.charAt(0).toUpperCase() + day.slice(1) }}
        </div>
        <div class="mt-2 text-gray-700 dark:text-gray-400">{{ getDaySchedule(day) }}</div>
      </div>
    </div>
  </div>
</template>
