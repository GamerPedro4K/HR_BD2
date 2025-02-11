<script setup lang="ts">
defineProps<{
  title: string;
  value: number | string;
  icon: string;
  iconBackground: string;
  iconColor: string;
  trend?: {
    value: number | string;
    label: string;
  };
}>();
</script>

<template>
  <div class="card bg-surface-0 dark:bg-surface-900 rounded-xl p-5 mb-0 border border-surface-200 dark:border-surface-700 shadow-md hover:shadow-lg transition-all duration-300 ease-in-out transform hover:-translate-y-1">
    <div class="flex justify-between mb-4">
      <div class="flex-grow">
        <span class="block text-sm uppercase tracking-wider text-muted-color font-medium mb-4">{{ title }}</span>
        <div class="text-surface-900 dark:text-surface-0 font-medium text-2xl">{{ value }}</div>
      </div>
      <div 
        :class="`flex items-center justify-center w-12 h-12 rounded-xl ${iconBackground} transition-transform duration-300 hover:scale-110`"
      >
        <i :class="`pi ${icon} ${iconColor} text-xl`"></i>
      </div>
    </div>
    <div v-if="trend" class="flex items-center gap-2">
      <span class="text-primary font-medium">{{ trend.value }}</span>
      <span class="text-muted-color text-sm">{{ trend.label }}</span>
    </div>
  </div>
</template>
