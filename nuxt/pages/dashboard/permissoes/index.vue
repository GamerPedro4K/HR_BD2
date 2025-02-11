<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { Permission } from '~/types/permission';
import type { DataTablePageEvent } from 'primevue/datatable';
import { usePermission } from '~/composables/usePermission';

const route = useRoute();

const permissions = ref<Permission[]>([]);
const totalRecords = ref(0);

const rows = ref(25);
const first = ref(0);
const sortField = ref('id');
const sortOrder = ref(1);

const filters = ref({
    global: { value: route.query.find as string || null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getPermissions } = usePermission();

const loadPermissions = async () => {
    const response = await getPermissions({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });

    permissions.value = response?.permissions || [];
    totalRecords.value = response?.total_count || 0;
};

await loadPermissions();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadPermissions();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadPermissions();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadPermissions();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadPermissions();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};
</script>

<template>
    <div class="mb-12">
        <h3 class="mb-1">Permissões do Sistema</h3>
        <p class="text-gray-500">Lista de todas as permissões disponíveis</p>
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
                :value="permissions"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Permissões"
            >
                <Column header="ID" field="id" style="width: 5rem" sortable></Column>
                <Column field="name" header="Nome" sortable></Column>
                <Column field="codename" header="Código" sortable></Column>
            </DataTable>
        </div>
    </div>
</template>