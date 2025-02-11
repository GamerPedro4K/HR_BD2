<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { ContractState } from '~/types/contractState';
import type { DataTablePageEvent } from 'primevue/datatable';
import { useContractState } from '~/composables/useContractState';

const confirm = useConfirm();
const route = useRoute();

const contractStates = ref<ContractState[]>([]);
const selectedContractStates = ref();
const totalRecords = ref(0);

const rows = ref(25);
const first = ref(0);
const sortField = ref('state');
const sortOrder = ref(1);

const filters = ref({
    global: { value: route.query.find as string || null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getContractStates, deleteContractState } = useContractState();

const loadContractStates = async () => {
    const response = await getContractStates({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });

    contractStates.value = response?.contract_states || [];
    totalRecords.value = response?.total_count || 0;
};

await loadContractStates();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadContractStates();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadContractStates();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadContractStates();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadContractStates();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

const handleDeleteContractState = async (id: string) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este estado de contrato?',
        header: 'Confirmação',
        icon: 'pi pi-info-circle',
        rejectLabel: 'Cancelar',
        rejectProps: {
            label: 'Cancel',
            severity: 'secondary',
            outlined: true
        },
        acceptProps: {
            label: 'Apagar',
            severity: 'danger'
        },
        accept: async () => {
            const success = await deleteContractState(id, false);
            if (success) {
                loadContractStates();
            }
        },
    });
};

const handleBulkDelete = () => {
    if (!selectedContractStates.value.length) return;

    confirm.require({
        message: 'Tem certeza que deseja apagar os estados de contrato selecionados?',
        header: 'Confirmação',
        icon: 'pi pi-info-circle',
        rejectLabel: 'Cancelar',
        rejectProps: {
            label: 'Cancelar',
            severity: 'secondary',
            outlined: true
        },
        acceptProps: {
            label: 'Apagar',
            severity: 'danger'
        },
        accept: async () => {
            const deletePromises = selectedContractStates.value.map((contractState: ContractState) => 
                deleteContractState(contractState.id_contract_state, true)
            );

            await Promise.all(deletePromises);
            loadContractStates();
            selectedContractStates.value = [];
        },
        reject: () => {}
    });
};
</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Estados de Contrato</h3>
        <p class="text-gray-500">Gerenciamento de estados de contrato</p>
    </div>

    <div>
        <div class="card">
            <div class="flex justify-between items-center mb-8">
                <IconField>
                    <InputIcon>
                        <i class="pi pi-search"></i>
                    </InputIcon>
                    <InputText 
                        class="w-[400px]"
                        v-model="filters['global'].value" 
                        placeholder="Pesquisa..." 
                        @input="onGlobalSearch(($event.target as HTMLInputElement).value)"
                    />
                </IconField>
                <div>
                    <NuxtLink to="/dashboard/estado-contrato/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                    </NuxtLink>
                    <Button label="Apagar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="handleBulkDelete" />
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                v-model:selection="selectedContractStates"
                dataKey="id_contract_state"
                :value="contractStates"
                :lazy="true"
                :paginator="true"
                :rows="rows"
                :filters="filters"
                @filter="onFilter"
                @sort="onSort"
                @page="onPage"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25, 50, 100]"
                :totalRecords="totalRecords"
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Estados de Contrato"
            >
                <Column selectionMode="multiple" style="width: 3rem"></Column>
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id_contract_state"/>
                    </template>
                </Column>
                <Column field="icon" header="Ícone" style="width: 5rem">
                    <template #body="slotProps">
                        <div class="flex items-center justify-center">
                            <font-awesome :icon="slotProps.data.icon" :style="{ color: slotProps.data.hex_color }" class="f-size-22 mr-4" />
                        </div>
                    </template>
                </Column>
                <Column field="state" header="Estado" sortable></Column>
                <Column field="description" header="Descrição" sortable></Column>
                <Column :exportable="false" style="width: 8rem">
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/estado-contrato/action/edit?id=${slotProps.data.id_contract_state}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button 
                            icon="pi pi-trash" 
                            outlined 
                            rounded 
                            severity="danger" 
                            @click="handleDeleteContractState(slotProps.data.id_contract_state)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>