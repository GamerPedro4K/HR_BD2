<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { Department } from '~/types/department';
import type { DataTablePageEvent } from 'primevue/datatable';

const departments = ref<Department[]>([]);
const selectedDepartments = ref();
const totalRecords = ref(0);
const expandedRows = ref({});

const rows = ref(25);
const first = ref(0);
const sortField = ref('');
const sortOrder = ref(1);
const router = useRouter();

const filters = ref({
 global: { value: null as string | null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getDepartments } = useDepartment();
const { deleteRole } = useRoles();
const confirm = useConfirm();

const loadDepartments = async () => {
   const response = await getDepartments({
       limit: rows.value,
       offset: first.value,
       order_by: sortField.value || 'name',
       order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
       global_search: filters.value.global?.value || '',
   });
  
   departments.value = response?.departments || [];
   totalRecords.value = response?.total_count || 0;
};

await loadDepartments();

const onPage = (event: DataTablePageEvent) => {
 first.value = event.first;
 rows.value = event.rows;
 loadDepartments();
};

const onSort = (event: any) => {
 sortField.value = event.sortField;
 sortOrder.value = event.sortOrder;
 loadDepartments();
};

const onFilter = (event: any) => {
 filters.value = event.filters;
 loadDepartments();
};

const exportCSV = () => {
 dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
 first.value = 0;
 loadDepartments();
}, 300);

const onGlobalSearch = (value: string) => {
 filters.value.global.value = value;
 debouncedSearch();
};

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
                loadDepartments();
            }
        },
        reject: () => {}
    });
};
</script>

<template>
    <ConfirmDialog></ConfirmDialog>
   <div class="mb-12">
       <h3 class="mb-1">Todos os Departamentos</h3>
       <p class="text-gray-500">Todas as informações dos departamentos</p>
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
               <NuxtLink to="/dashboard/departments/action/add">
                   <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
               </NuxtLink>
               <Button label="Desativar" icon="pi pi-ban" class="mr-2" severity="warn" outlined :disabled="!selectedDepartments || !selectedDepartments.length" />
               <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
           </div>
       </div>
       <DataTable
           ref="dt"
           v-model:selection="selectedDepartments"
           v-model:expandedRows="expandedRows"
           dataKey="id_department"
           :value="departments"
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
           currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Departamentos"
           :expandedRowIcon="'pi pi-chevron-down'"
           :collapsedRowIcon="'pi pi-chevron-right'"
       >
           <Column :expander="true" style="width: 3rem" />
           <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
           <Column header="ID" style="width: 3rem" :exportable="false">
               <template #body="slotProps">
                   <CopyToClipboardButton :textToCopy="slotProps.data.id_department"/>
               </template>
           </Column>
           <Column field="name" header="Nome" sortable style="min-width: 16rem"></Column>
           <Column field="description" header="Descrição" style="min-width: 16rem"></Column>
           <Column :exportable="false" >
                <template #body="slotProps">
                    <NuxtLink :to="`/dashboard/departments/action/edit?id=${slotProps.data.id_department}`">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                    </NuxtLink>
                </template>
            </Column>
           <!-- Expanded row template -->
           <template #expansion="slotProps">
               <div class="p-4">
                   <div class="flex justify-between items-center mb-4">
                       <h4>Cargos em {{ slotProps.data.name }}</h4>
                       <NuxtLink :to="`/dashboard/roles/action/add?id=${slotProps.data.id_department}`">
                           <Button 
                               label="Adicionar cargo" 
                               icon="pi pi-plus" 
                               size="small"
                           />
                       </NuxtLink>
                   </div>
                   <DataTable :value="slotProps.data.roles" v-if="slotProps.data.roles && slotProps.data.roles.length">
                       <Column field="role_name" header="Nome Cargo">
                           <template #body="roleProps">
                               <div class="flex items-center">
                                   <div 
                                       class="w-3 h-3 rounded-full mr-2"
                                       :style="{ backgroundColor: roleProps.data.hex_color }"
                                   ></div>
                                   {{ roleProps.data.role_name }}
                               </div>
                           </template>
                       </Column>
                       <Column field="description" header="Descrição"></Column>
                       <Column header="Tipos de Treinamento">
                           <template #body="roleProps">
                               <div class="flex items-center gap-2">
                                   {{ roleProps.data.training_types.length }} Treinamentos
                                   <NuxtLink :to="`/dashboard/roles/${roleProps.data.id_role}`" class="button-class" >
                                       <Button 
                                           icon="pi pi-search" 
                                           variant="text" 
                                           rounded
                                           raised
                                       />
                                   </NuxtLink>
                               </div>
                           </template>
                       </Column>
                       <Column>
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
                   <div v-else class="text-gray-500 italic">
                       Nenhum cargo definido para este departamento
                   </div>
               </div>
           </template>
       </DataTable>
   </div>
</template>