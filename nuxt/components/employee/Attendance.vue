<script setup lang="ts">
const props = defineProps({
  id: {
    type: String,
    required: true,
    default: null
  },
});
</script>
<template>atend {{ props.id }}</template>