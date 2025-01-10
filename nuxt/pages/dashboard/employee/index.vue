<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { Employee } from '~/types/employee';
import type { DataTablePageEvent } from 'primevue/datatable';

// Refs for managing employees
const employee = ref<Employee[]>([]);
const selectedEmployees = ref();
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

// Fetch employees function
const { getEmployees } = useEmployee();

const loadEmployees = async () => {
    const response = await getEmployees({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value || 'id',
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });
   
    employee.value = response?.employees || [];
    totalRecords.value = response?.total_count || 0;
};

await loadEmployees();

// Event handlers
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

// Export CSV
const exportCSV = () => {
  dt.value.exportCSV();
};

// Debounced search
const debouncedSearch = debounce(() => {
  first.value = 0;
  loadEmployees();
}, 300);

// Handle global search input
const onGlobalSearch = (value: string) => {
  filters.value.global.value = value ;
  debouncedSearch();
};
</script>

<template>
        <div class="mb-12">
            <h3 class="mb-1">Todos os funcionários</h3>
            <p class="text-gray-500">Todas as informações dos funcionários</p>
        </div>

        <div>
        <div class="card">
            
            <div class="flex justify-between items-center mb-8 ">
                <IconField >
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
                    <NuxtLink to="/dashboard/employee/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                    </NuxtLink>
                    <Button label="Desativar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="" :disabled="!selectedEmployees || !selectedEmployees.length" />
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                v-model:selection="selectedEmployees"
                dataKey="id"
                :value="employee"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Funcionarios"
            >
                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id"/>
                    </template>
                </Column>
                <Column field="employee_name" header="Nome" sortable style="min-width: 16rem"></Column>
                <Column field="role_name" header="Função" sortable>
                    <template #body="slotProps">
                        <Tag 
                            :style="{ backgroundColor: slotProps.data.role_hex_color || '#ff0000', color: '#ffffff' }" 
                            :value="slotProps.data.role_name || 'Sem função'"
                        ></Tag>
                    </template>
                </Column>
                <Column field="department_name" header="Departamento" sortable ></Column>
                <Column field="state_name" header="Estado" sortable>
                    <template #body="slotProps">
                        <Tag :style="{ backgroundColor: slotProps.data.state_hex_color || '#ff0000', color: '#ffffff' }">
                            <div class="flex items-center gap-2 px-1">
                                <font-awesome :icon="slotProps.data.state_icon || 'fa-question-circle'" />
                                <span class="text-base">{{ slotProps.data.state_name || 'Sem Estado' }}</span>
                            </div>
                        </Tag>
                    </template>
                </Column>
                <Column :exportable="false" >
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/employee/action/edit?id=${slotProps.data.id}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button icon="pi pi-ban" outlined rounded severity="warn" class="mr-2" @click="" />
                        <NuxtLink :to="`/dashboard/employee/${slotProps.data.id}`">
                            <Button icon="pi pi-eye" outlined rounded severity="contrast" />
                        </NuxtLink>
                    </template>
                </Column>
            </DataTable>
        </div>
	</div>
</template>
