<script setup lang="ts">
import { ref } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import type { ContractStateContractResponse } from '~/types/contractState';
import { format } from 'date-fns';

const formatDate = (dateString: string | null | undefined) => {
    return dateString ? format(new Date(dateString), 'dd/MM/yyyy HH:mm:ss') : '-';
};


const contractStates = ref<ContractStateContractResponse>({
    data: [],
    count: 0
});
const rows = ref(10);
const first = ref(0);

const { getContractStateContract } = useContractState();

const loadContractStates = async () => {
    const response = await getContractStateContract({
        limit: rows.value,
        offset: first.value,
    });
    if (response) {
        contractStates.value = response;
    }
};

const props = defineProps<{
    contractStates: ContractStateContractResponse;
}>();

const { contractStates: propContractStates } = props;

onMounted(() => {
    contractStates.value  = propContractStates;
});

const onPage = (event: any) => {
    first.value = event.first;
    rows.value = event.rows;
    loadContractStates();
};
</script>

<template>
    <DataTable 
        :value="contractStates.data || []" 
        :paginator="true" 
        :rows="rows" 
        :totalRecords="contractStates.count" 
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5, 10, 25, 50, 100]"
        :lazy="true" 
        @page="onPage"
    >
        <Column field="contract_state.id_contract_state_contract" header="ID">
            <template #body="slotProps">
                <CopyToClipboardButton :textToCopy="slotProps.data.contract_state.id_contract_state_contract"/>
            </template>
        </Column>
        <Column field="contract_state.id_contract" header="Contract ID" >
            <template #body="slotProps">
                <CopyToClipboardButton :textToCopy="slotProps.data.contract_state.id_contract"/>
            </template>
        </Column>
        <Column field="contract_state.created_at" header="Criado">
            <template #body="slotProps">
                {{ formatDate(slotProps.data.contract_state.created_at) }}
            </template>
        </Column>

        <Column field="contract_state.updated_at" header="Modificado">
            <template #body="slotProps">
                {{ formatDate(slotProps.data.contract_state.updated_at) }}
            </template>
        </Column>

        <Column header="State">
            <template #body="slotProps">
                <span :style="{ color: slotProps.data.state.hex_color }">
                    <i :class="slotProps.data.state.icon" class="mr-2"></i>
                    {{ slotProps.data.state.state }}
                </span>
            </template>
        </Column>
        <Column header="Description">
            <template #body="slotProps">
                {{ slotProps.data.state.description }}
            </template>
        </Column>
    </DataTable>
</template>