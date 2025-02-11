<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { DataTablePageEvent } from 'primevue/datatable';
import { useContractLeaveType } from '~/composables/useContractLeaveType';
import type { ContractLeaveType } from '~/types/contractleavetype ';

const confirm = useConfirm();
const route = useRoute();

const contractLeaveTypes = ref<ContractLeaveType[]>([]);
const selectedContractLeaveTypes = ref();
const totalRecords = ref(0);

const rows = ref(25);
const first = ref(0);
const sortField = ref('leave_type');
const sortOrder = ref(1);

const filters = ref({
    global: { value: route.query.find as string || null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getContractLeaveTypes, deleteContractLeaveType } = useContractLeaveType();

const loadContractLeaveTypes = async () => {
    const response = await getContractLeaveTypes({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });

    contractLeaveTypes.value = response?.contract_leave_types || [];
    totalRecords.value = response?.total_count || 0;
};

await loadContractLeaveTypes();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadContractLeaveTypes();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadContractLeaveTypes();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadContractLeaveTypes();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadContractLeaveTypes();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

const handleDeleteContractLeaveType = async (id: string) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este tipo de licença?',
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
            const success = await deleteContractLeaveType(id, false);
            if (success) {
                loadContractLeaveTypes();
            }
        },
    });
};

const handleBulkDelete = () => {
    if (!selectedContractLeaveTypes.value.length) return;

    confirm.require({
        message: 'Tem certeza que deseja apagar os estados de saida selecionados?',
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
            const deletePromises = selectedContractLeaveTypes.value.map((contractLeaveType: ContractLeaveType) => 
                deleteContractLeaveType(contractLeaveType.id_leave_type, true)
            );

            await Promise.all(deletePromises);
            loadContractLeaveTypes();
            selectedContractLeaveTypes.value = [];
        },
        reject: () => {}
    });
};
</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Estados de Saida</h3>
        <p class="text-gray-500">Gerenciamento de estados de saida de contrato</p>
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
                    <NuxtLink to="/dashboard/estado-saida/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                    </NuxtLink>
                    <Button label="Apagar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="handleBulkDelete" />
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                v-model:selection="selectedContractLeaveTypes"
                dataKey="id_leave_type"
                :value="contractLeaveTypes"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Estados de Licença"
            >
                <Column selectionMode="multiple" style="width: 3rem"></Column>
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id_leave_type"/>
                    </template>
                </Column>
                <Column field="leave_type" header="Tipo de Licença" sortable></Column>
                <Column field="description" header="Descrição" sortable></Column>
                <Column field="is_paid" header="Remunerado" sortable style="width: 8rem">
                    <template #body="slotProps">
                        <Tag :severity="slotProps.data.is_paid ? 'success' : 'danger'" :value="slotProps.data.is_paid ? 'Sim' : 'Não'" />
                    </template>
                </Column>
                <Column :exportable="false" style="width: 8rem">
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/estado-saida/action/edit?id=${slotProps.data.id_leave_type}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button 
                            icon="pi pi-trash" 
                            outlined 
                            rounded 
                            severity="danger" 
                            @click="handleDeleteContractLeaveType(slotProps.data.id_leave_type)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>