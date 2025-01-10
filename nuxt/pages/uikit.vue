
<script setup lang="ts">
  const layout = "app-layout";
</script>

<template>
  <div>
    <NuxtRouteAnnouncer />
  </div>
  <NuxtLayout :name="layout">
    <NuxtPage />
  </NuxtLayout>
</template>