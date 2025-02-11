<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { ContractType } from '~/types/contractType';
import type { DataTablePageEvent } from 'primevue/datatable';
import { useContractType } from '~/composables/useContractType';

const confirm = useConfirm();
const route = useRoute();

const contractTypes = ref<ContractType[]>([]);
const selectedContractTypes = ref();
const totalRecords = ref(0);

const rows = ref(25);
const first = ref(0);
const sortField = ref('contract_type_name');
const sortOrder = ref(1);

const filters = ref({
    global: { value: route.query.find as string || null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getContractTypes, deleteContractType } = useContractType();

const loadContractTypes = async () => {
    const response = await getContractTypes({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });

    contractTypes.value = response?.contract_types || [];
    totalRecords.value = response?.total_count || 0;
};

await loadContractTypes();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadContractTypes();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadContractTypes();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadContractTypes();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadContractTypes();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

const handleDeleteContractType = async (id: string) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este tipo de contrato?',
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
            const success = await deleteContractType(id, false);
            if (success) {
                loadContractTypes();
            }
        },
    });
};

const handleBulkDelete = () => {
    if (!selectedContractTypes.value.length) return;

    confirm.require({
        message: 'Tem certeza que deseja apagar os tipos de treinamento selecionados?',
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
            const deletePromises = selectedContractTypes.value.map((contractType: ContractType ) => 
                deleteContractType(contractType.id_contract_type, true)
            );

            await Promise.all(deletePromises);
            loadContractTypes();
            selectedContractTypes.value = [];
        },
        reject: () => {}
    });
};

</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Todos os Tipos de Contratos</h3>
        <p class="text-gray-500">Gerenciamento de tipos de contratos</p>
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
                    <NuxtLink to="/dashboard/tipo-contrato/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                    </NuxtLink>
                    <Button label="Apagar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="handleBulkDelete" />
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                v-model:selection="selectedContractTypes"
                dataKey="id_contract_type"
                :value="contractTypes"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Tipos de Contrato"
            >
                <Column selectionMode="multiple" style="width: 3rem"></Column>
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id_contract_type"/>
                    </template>
                </Column>
                <Column field="contract_type_name" header="Nome" sortable></Column>
                <Column field="description" header="Descrição" sortable></Column>
                <Column field="termination_notice_period" header="Período de aviso de rescisão" sortable></Column>
                <Column field="overtime_eligible" header="Horas Extras" sortable>
                    <template #body="slotProps">
                        <Tag v-if="slotProps.data.overtime_eligible" severity="success">Sim</Tag>
                        <Tag v-else severity="danger">Não</Tag>
                    </template>
                </Column>
                <Column field="benefits_eligible" header="Benefícios" sortable>
                    <template #body="slotProps">
                        <Tag v-if="slotProps.data.benefits_eligible" severity="success">Sim</Tag>
                        <Tag v-else severity="danger">Não</Tag>
                    </template>
                </Column>
                <Column :exportable="false" style="width: 8rem">
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/tipo-contrato/action/edit?id=${slotProps.data.id_contract_type}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button 
                            icon="pi pi-trash" 
                            outlined 
                            rounded 
                            severity="danger" 
                            @click="handleDeleteContractType(slotProps.data.id_contract_type)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>
