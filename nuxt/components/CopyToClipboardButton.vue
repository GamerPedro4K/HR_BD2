<script setup>
const props = defineProps({
  textToCopy: {
    type: String,
    required: true,
  },
});

const copied = ref(false);

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.textToCopy);
    copied.value = true;

    setTimeout(() => {
      copied.value = false;
    }, 1000);
  } catch (error) {
    console.error("Falha ao copiar", error);
  }
};
</script>

<style scoped>
.p-button-success {
  transition: background-color 0.3s;
}

</style>
<template>
  <Button :icon="copied ? 'pi pi-check' : 'pi pi-copy'" variant="text" @click="copyToClipboard" raised rounded aria-label="Filter" :class="{ 'p-button-success': copied, 'p-button-primary': !copied }" />
</template>
