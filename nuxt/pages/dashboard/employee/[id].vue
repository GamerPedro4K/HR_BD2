<script setup lang="ts">
import type { FindEmployee } from '~/types/employee';
import { useRouter, useRoute } from 'vue-router'; 
import Profile from '~/components/employee/Profile.vue';
import Attendance from '~/components/employee/Attendance.vue';
import Schedule from '~/components/employee/Schedule.vue';
import Salary from '~/components/employee/Salary.vue';
import { useContractState } from '~/composables/useContractState';
import ContractState from '~/components/employee/ContractState.vue';
import type { AttendanceInterfaceResponse } from '~/types/attendance';
import type { ScheduleInterface } from '~/types/schedule';
import type { SalaryHistory } from '~/types/salary';
import type { ContractStateContractResponse } from '~/types/contractState';


//routing 
const route = useRoute();
const router = useRouter();

//breadcrumbs
const { breadcrumbs, home } = useBreadcrumb();

// Refs for managing employee
const employee = ref<FindEmployee>();
const attendance = ref<AttendanceInterfaceResponse>({
    data: [],
    count: 0
});
const schedule = ref<ScheduleInterface[]>();
const salary = ref<SalaryHistory[]>([]);
const contractState = ref<ContractStateContractResponse>({
    data: [],
    count: 0
});

// Fetch employee function
const { getEmployee, getEmployeeAtendance, getEmployeeSchedule } = useEmployee();
const { getSalaryHistory } = useSalaryHistory();
const { getContractStateContract } = useContractState();

const loadEmployees = async () => {
    const response = await getEmployee(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id);
    
    if(response)
        employee.value = response;
    else
        router.push('/dashboard/employee');
};

const loadEmployeeAtendance = async () => {
    const response = await getEmployeeAtendance(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id, { limit: 10, offset: 1 });
    
    if(response)
        attendance.value = response;
    else
        router.push('/dashboard/employee');
};

const loadEmployeeSchedule = async () => {
    const response = await getEmployeeSchedule(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id);
    
    if(response)
        schedule.value = response;
    else
        router.push('/dashboard/employee');
};

const loadEmployeeSalary = async () => {
    const response = await getSalaryHistory(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id);
    
    if(response)
        salary.value = response;
    else
        router.push('/dashboard/employee');
};

const loadEmployeeContractState = async () => {
    const response = await getContractStateContract({
        limit: 10,  
        offset: 0,  
    });

    if(response)
        contractState.value = response;
    else
        router.push('/dashboard/employee');
};

await loadEmployees();
await loadEmployeeAtendance();
await loadEmployeeSchedule();
await loadEmployeeSalary();
await loadEmployeeContractState();


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
        label: 'Agenda',
        icon: 'pi pi-calendar-times',
        command: () => {
            selectedMenuItem.value = 'Agenda';
        },
    },
    {
        label: 'Salário',
        icon: 'pi pi-dollar',
        command: () => {
            selectedMenuItem.value = 'Salário';
        },
    },
    {
        label: 'Estado da conta',
        icon: 'pi pi-file-check',
        command: () => {
            selectedMenuItem.value = 'Estado da conta';
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
                        {{ employee?.contract.role.role_name }}
                    </p>
                    <p class="flex items-center text-gray-600 mt-2">
                        <i class="pi pi-at mr-1.5" style="font-size: 1.5rem"></i>
                        {{ employee?.email}}
                    </p>
                </div>
            </div>
            <!-- TODO: faça um botaão que chame Check IN e de pois mude para Checkout quando for -->
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
            <div class="ml-2 flex-grow">
                <div v-if="selectedMenuItem === 'Perfil'" class="">
                    <Profile :json="employee"></Profile>
                </div>
                <div v-else-if="selectedMenuItem === 'Comparecimento'" class="mt-2">
                    <Attendance :attendance="attendance"></Attendance>
                </div>
                <div v-else-if="selectedMenuItem === 'Agenda'" class="mt-2">
                    <Schedule :schedule="schedule"></Schedule>
                </div>
                <div v-else-if="selectedMenuItem === 'Salário'" class="mt-2">
                    <Salary :salary="salary"></Salary>
                </div>
                <div v-else-if="selectedMenuItem === 'Estado da conta'" class="mt-2">
                    <ContractState :contractStates="contractState"></ContractState>
                </div>
            </div>
        </div>
    </div>
</template>
