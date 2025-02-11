<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { TrainingType } from '~/types/trainingType';
import type { DataTablePageEvent } from 'primevue/datatable';

const confirm = useConfirm();
const route = useRoute();

// Refs for managing training types
const trainingTypes = ref<TrainingType[]>([]);
const selectedTrainingTypes = ref();
const totalRecords = ref(0);

// Pagination and sorting
const rows = ref(25);
const first = ref(0);
const sortField = ref('');
const sortOrder = ref(1);

// Filters
const filters = ref<{
    global: { value: string | null; matchMode: string };
}>({
    global: { value: route.query.find as string || null, matchMode: FilterMatchMode.CONTAINS },
});

// DataTable reference
const dt = ref();

// Fetch training types function
const { getTrainingTypes, deleteTrainingType } = useTrainingType();

const loadTrainingTypes = async () => {
    const response = await getTrainingTypes({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value || 'name',
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });
   
    trainingTypes.value = response?.training_types || [];
    totalRecords.value = response?.total_count || 0;
};

await loadTrainingTypes();

// Event handlers
const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadTrainingTypes();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadTrainingTypes();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadTrainingTypes();
};

// Export CSV
const exportCSV = () => {
    dt.value.exportCSV();
};

// Debounced search
const debouncedSearch = debounce(() => {
    first.value = 0;
    loadTrainingTypes();
}, 300);

// Handle global search input
const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

// Handle training type deletion
const handleDeleteTrainingType = async (id: string) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este tipo de treinamento?',
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
            const success = await deleteTrainingType(id, false);
            if (success) {
                loadTrainingTypes();
            }
        },
        reject: () => {}
  });
};

const handleBulkDelete = () => {
    if (!selectedTrainingTypes.value.length) return;

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
            const deletePromises = selectedTrainingTypes.value.map((trainingType: TrainingType) => 
                deleteTrainingType(trainingType.id_training_type, true)
            );

            await Promise.all(deletePromises);
            loadTrainingTypes();
            selectedTrainingTypes.value = [];
        },
        reject: () => {}
    });
};

</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Todos os Tipos de Treinamentos</h3>
        <p class="text-gray-500">Gerenciamento de tipos de treinamentos</p>
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
                    <NuxtLink to="/dashboard/trainings/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                    </NuxtLink>
                    <Button label="Apagar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="handleBulkDelete" :disabled="!selectedTrainingTypes || !selectedTrainingTypes.length" />
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                v-model:selection="selectedTrainingTypes"
                dataKey="id_training_type"
                :value="trainingTypes"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Tipos de Treinamento"
            >
                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id_training_type"/>
                    </template>
                </Column>
                <Column field="name" header="Nome" sortable style="min-width: 16rem"></Column>
                <Column field="description" header="Descrição" sortable></Column>
                <Column field="hours" header="Horas" sortable></Column>
                <Column :exportable="false" style="width: 8rem">
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/trainings/action/edit?id=${slotProps.data.id_training_type}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button 
                            icon="pi pi-trash" 
                            outlined 
                            rounded 
                            severity="danger" 
                            @click="handleDeleteTrainingType(slotProps.data.id_training_type)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>