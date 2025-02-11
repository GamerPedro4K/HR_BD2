<template>
    
</template>
<script setup>
const props = defineProps(['error']);
const router = useRouter();

onMounted(() => {
if (props.error.statusCode === 403) {
    router.replace('/pages/forbidden');
}
if (props.error.statusCode === 404) {
    router.replace('/pages/notfound');
}
});


</script>
