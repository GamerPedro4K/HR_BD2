<script setup lang="ts">
import type { FindEmployee } from '~/types/employee';
import { useRouter, useRoute } from 'vue-router'; 
import Profile from '~/components/employee/Profile.vue';
import Attendance from '~/components/employee/Attendance.vue';
import Saidas from '~/components/employee/Saidas.vue';

//routing 
const route = useRoute();
const router = useRouter();

//breadcrumbs
const { breadcrumbs, home } = useBreadcrumb();

// Refs for managing employee
const employee = ref<FindEmployee>();

// Fetch employee function
const { getEmployee } = useEmployee();

const loadEmployees = async () => {
    const response = await getEmployee(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id);
    
    if(response)
        employee.value = response;
    else
        router.push('/dashboard/employee');
};

await loadEmployees();


const selectedMenuItem = ref<string>('Perfil');


const items = ref([
    {
        label: 'Perfil',
        icon: 'pi pi-user',
        command: () => {
            selectedMenuItem.value = 'Perfil';
        },
    },
    {
        label: 'Comparecimento',
        icon: 'pi pi-calendar',
        command: () => {
            selectedMenuItem.value = 'Comparecimento';
        },
    },
    {
        label: 'Saidas',
        icon: 'pi pi-calendar-times',
        command: () => {
            selectedMenuItem.value = 'Saidas';
        },
    },
]);

</script>

<style>
.selected-menu-item {
    background: var(--primary-color);
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 8px 16px;
    transition: all 0.3s ease;
}
</style>

<template>
    <div class="mb-12">
        <h3 class="mb-1">{{employee?.employee_name}}</h3>
        <BreadcrumbCustom :home="home" :breadcrumbs="breadcrumbs" />
    </div>
    <div class="card" style="padding: 1.5rem;">
        <div class="flex justify-between mb-7">
            <div class="flex justify-start">
                <img :src="employee?.photo" alt="" class="rounded-lg h-[100px]">
                <div class="pl-4">
                    <h2 class="text-lg font-bold text-gray-800">{{ employee?.employee_name}}</h2>
                    <p class="flex items-center text-gray-600 mt-2">
                        <i class="pi pi-briefcase mr-1.5" style="font-size: 1.5rem"></i>
                        {{ employee?.department_name}}
                    </p>
                    <p class="flex items-center text-gray-600 mt-2">
                        <i class="pi pi-at mr-1.5" style="font-size: 1.5rem"></i>
                        {{ employee?.email}}
                    </p>
                </div>
            </div>
            <div>b</div>
        </div>
        <hr>
        <div class="flex justify-start">
            <div class="m-3">
                <PanelMenu :model="items" class="w-full md:w-60">
                    <template #item="{ item }">
                        <a
                            v-ripple
                            class="flex items-center cursor-pointer text-surface-700 dark:text-surface-0 px-4 py-2"
                            :href="item.url"
                            :target="item.target"
                            :class="{ 'selected-menu-item': selectedMenuItem === item.label }"
                            @click.prevent="(event) => item.command && item.command({ originalEvent: event, item })"
                        >
                            <span :class="item.icon"></span>
                            <span class="ml-2">{{ item.label }}</span>
                        </a>
                    </template>
                </PanelMenu>
            </div>
            <div class="ml-2">
                <div v-if="selectedMenuItem === 'Perfil'" class="">
                    <Profile :json="employee"></Profile>
                </div>
                <div v-else-if="selectedMenuItem === 'Comparecimento'" class="mt-2">
                    <Attendance :id="employee?.id"></Attendance>
                </div>
                <div v-else-if="selectedMenuItem === 'Saidas'" class="mt-2">
                    <Saidas :id="employee?.id"></Saidas>
                </div>
            </div>
        </div>
    </div>
</template>
