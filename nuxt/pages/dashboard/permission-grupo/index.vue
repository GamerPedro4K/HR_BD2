<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { DataTablePageEvent } from 'primevue/datatable';
import type { Employee } from '~/types/permissionsusergroup';

const employees = ref<Employee[]>([]);
const totalRecords = ref(0);
const expandedRows = ref({});

const rows = ref(25);
const first = ref(0);
const sortField = ref('name');
const sortOrder = ref(1);

const filters = ref({
    global: { value: null as string | null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getEmployeePermissions } = useEmployeePermissionsGroup();

const loadEmployees = async () => {
    const response = await getEmployeePermissions({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });
    
    employees.value = response?.employees || [];
    totalRecords.value = response?.total_count || 0;
};

await loadEmployees();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadEmployees();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadEmployees();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadEmployees();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadEmployees();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};
</script>

<template>
    <div class="mb-12">
        <h3 class="mb-1">Permissões dos Utilizadores</h3>
        <p class="text-gray-500">Gerenciamento de permissões por grupos e Utilizadores</p>
    </div>
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
            v-model:expandedRows="expandedRows"
            dataKey="id_employee"
            :value="employees"
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
            currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Utilizadores"
            :expandedRowIcon="'pi pi-chevron-down'"
            :collapsedRowIcon="'pi pi-chevron-right'"
        >
            <Column :expander="true" style="width: 3rem" />
            <Column field="id_employee" header="ID" style="width: 3rem" :exportable="false">
                <template #body="slotProps">
                    <CopyToClipboardButton :textToCopy="slotProps.data.id_employee"/>
                </template>
            </Column>
            <Column field="name" header="Nome" sortable style="min-width: 16rem">
                <template #body="slotProps">
                    <div class="flex items-center">
                        <Avatar :image="slotProps.data.src" size="normal" shape="circle" class="mr-2" />
                        {{ slotProps.data.name }}
                    </div>
                </template>
            </Column>
            <Column field="groups" header="Grupos" sortable style="min-width: 12rem">
                <template #body="slotProps">
                    <div class="flex gap-2">
                        <Tag 
                            v-for="group in slotProps.data.groups" 
                            :key="group.group_id"
                            :value="group.group_name"
                            severity="info"
                        />
                    </div>
                </template>
            </Column>

            <!-- Expanded row template -->
            <template #expansion="slotProps">
                <div class="p-4">
                    <div v-for="group in slotProps.data.groups" :key="group.group_id" class="mb-6">
                        <h4 class="mb-4">{{ group.group_name }}</h4>
                        <DataTable :value="group.permissions">
                            <Column field="id" header="ID" style="width: 5rem"></Column>
                            <Column field="name" header="Nome"></Column>
                            <Column field="codename" header="Código"></Column>
                        </DataTable>
                    </div>
                    <div v-if="!slotProps.data.groups.length" class="text-gray-500 italic">
                        Nenhum grupo atribuído para este usuário
                    </div>
                </div>
            </template>
        </DataTable>
    </div>
</template>