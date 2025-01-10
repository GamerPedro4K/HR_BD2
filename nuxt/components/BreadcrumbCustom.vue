<template>
    <Breadcrumb :home="home" :model="breadcrumbs" class="rounded-lg">
        <template #item="{ item, props }">
            <template v-if="item === breadcrumbs.at(-1)">
                <span>
                    <i v-if="item.icon" :class="item.icon" style="margin-right: 0.5rem;"></i>
                    {{ item.label }}
                </span>
            </template>
            <template v-else>
                <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
                    <a :href="href" v-bind="props.action" @click="navigate">
                        <i v-if="item.icon" :class="item.icon" style="margin-right: 0.5rem;"></i>
                        {{ item.label }}
                    </a>
                </router-link>
                <a v-else :href="item.url" :target="item.target" v-bind="props.action">
                    <span>{{ item.label }}</span>
                </a>
            </template>
        </template>
    </Breadcrumb>
</template>

<script setup lang="ts">
defineProps({
    home: {
        type: Object as PropType<{ label: string; icon: string; route: string }>,
        required: true,
    },
    breadcrumbs: {
        type: Array as PropType<Array<{ label: string; route?: string; icon?: string; url?: string }>>,
        required: true,
    },
});
</script>
