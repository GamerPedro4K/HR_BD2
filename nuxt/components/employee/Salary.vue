<script setup lang="ts">
import type { SalaryHistory } from '~/types/salary';
import { defineProps, type PropType } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import CopyToClipboardButton from '~/components/CopyToClipboardButton.vue';
import Button from 'primevue/button';

const props = defineProps({
    salary: {
        type: Array as PropType<SalaryHistory[]>,
        required: true,
    },
});
const { salary } = props;


</script>

<template>
    <div class="card training-card-padding" >
        <div class="font-semibold text-xl">Histórico de Salários</div>
        <DataTable 
            :value="salary || []" 
            dataKey="id_salary_history" 
            tableStyle="min-width: 50rem" 
            scrollable 
            scrollHeight="500px"
        >
            <Column header="ID Contrato"  :exportable="false">
            <template #body="slotProps">
                <CopyToClipboardButton :textToCopy="slotProps.data.id_contract"/>
            </template>
            </Column>
            <Column field="base_salary" header="Salário">.
            <template #body="slotProps">
                {{ slotProps.data.base_salary }} €
            </template>
            </Column>
            <Column field="extra_hour_rate" header="Hora Extra">.
            <template #body="slotProps">
                {{ slotProps.data.extra_hour_rate }} €
            </template>
            </Column>
            <Column field="start_date" header="Data Início"></Column>
            <Column field="benefits_eligible" header="Apróvado Por">
            <template #body="slotProps">
                <NuxtLink :to="`/dashboard/employee/${slotProps.data.id_employee_aproved_by}`" target="_blank">
                <Button icon="pi pi-search" variant="text" raised rounded/>
                </NuxtLink>
            </template>
            </Column>
        </DataTable>
    </div>
</template>