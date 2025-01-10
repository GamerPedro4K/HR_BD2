<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import { useAuth } from '~/composables/useAuth';

const layout = "app-layout";

const loading = ref(true);
const router = useRouter();

onBeforeMount(async () => {
    const { isTokenValid } = useAuth();

    if (await isTokenValid()) {
    } else {
      router.push('/');
    }

    loading.value = false;
});
</script>

<template>
  <client-only>
    <div v-if="loading">
      <Loading></Loading>
    </div>
    <div v-else>
      <NuxtLayout :name="layout">
        <NuxtPage  />
      </NuxtLayout>
    </div>
  </client-only>
</template>
