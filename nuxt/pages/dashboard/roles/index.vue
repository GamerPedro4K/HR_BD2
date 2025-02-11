<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { RoleRequst } from '~/types/roles';
import type { DataTablePageEvent } from 'primevue/datatable';

const confirm = useConfirm();

// Refs for managing roles
const roles = ref<RoleRequst[]>([]);
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
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
});

// DataTable reference
const dt = ref();

// Fetch roles function
const { getRoles, deleteRole } = useRoles();

const loadRoles = async () => {
    const response = await getRoles({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value || 'role_name',
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });
   
    roles.value = response?.roles || [];
    totalRecords.value = response?.total_count || 0;
};

await loadRoles();

// Event handlers
const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadRoles();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadRoles();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadRoles();
};

// Export CSV
const exportCSV = () => {
    dt.value.exportCSV();
};

// Debounced search
const debouncedSearch = debounce(() => {
    first.value = 0;
    loadRoles();
}, 300);

// Handle global search input
const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

// Handle role deletion
const handleDeleteRole = async (id: string) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este cargo?',
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
            const success = await deleteRole(id);
            if (success) {
                loadRoles();
            }
        },
        reject: () => {}
  });
};
</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Todas as Funções</h3>
        <p class="text-gray-500">Gerenciamento de funções e permissões</p>
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
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                dataKey="id_role"
                :value="roles"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Funções"
            >
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id_role"/>
                    </template>
                </Column>
                <Column field="role_name" header="Nome da Função" sortable style="min-width: 16rem">
                    <template #body="slotProps">
                        <Tag 
                            :style="{ backgroundColor: slotProps.data.hex_color || '#ff0000', color: '#ffffff' }" 
                            :value="slotProps.data.role_name"
                        ></Tag>
                    </template>
                </Column>
                <Column field="department_name" header="Departamento" sortable></Column>
                <Column field="description" header="Descrição" sortable></Column>
                <Column field="training_types" header="Treinamentos" style="min-width: 12rem">
                    <template #body="slotProps">
                        <div class="flex flex-wrap gap-1">
                            <div v-if="slotProps.data.training_types.length > 0">
                                <Tag 
                                    v-for="(training, index) in slotProps.data.training_types.slice(0, 6)" 
                                    :key="training.id_training_type"
                                    :value="training.name"
                                    severity="info"
                                    class="mr-1 mb-1"
                                />
                                <Tag 
                                    v-if="slotProps.data.training_types.length > 6"
                                    value="..."
                                    severity="info"
                                    class="mr-1 mb-1"
                                />
                            </div>
                            <div v-else>
                                <Tag value="Nenhum treinamento" severity="warning" />
                            </div>
                        </div>
                    </template>
                </Column>
                <Column :exportable="false" style="width: 8rem">
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/roles/action/edit?id=${slotProps.data.id_role}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button 
                            icon="pi pi-trash" 
                            outlined 
                            rounded 
                            severity="danger" 
                            @click="handleDeleteRole(slotProps.data.id_role)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>