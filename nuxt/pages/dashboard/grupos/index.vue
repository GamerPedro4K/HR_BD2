<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { DataTablePageEvent } from 'primevue/datatable';
import { useAuthGroup } from '~/composables/useAuthGroup';
import type { AuthGroup } from '~/types/authgroup';

const confirm = useConfirm();
const authGroups = ref<AuthGroup[]>([]);
const selectedAuthGroups = ref();
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

const { getAuthGroups, deleteAuthGroup } = useAuthGroup();
const { removePermissionsFromGroup } = usePermission();

const loadAuthGroups = async () => {
    const response = await getAuthGroups({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });

    // Adiciona id_group em cada permissão
    const processedGroups = response?.auth_groups?.map(group => ({
        ...group,
        permissions: group.permissions?.map(permission => ({
            ...permission,
            id_group: group.id // Adiciona o id do grupo em cada permissão
        })) || []
    })) || [];

    authGroups.value = processedGroups;
    totalRecords.value = response?.total_count || 0;
};

await loadAuthGroups();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadAuthGroups();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadAuthGroups();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadAuthGroups();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadAuthGroups();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

const handleDeleteAuthGroup = async (id: number) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este grupo?',
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
            const success = await deleteAuthGroup(id, false);
            if (success) {
                loadAuthGroups();
            }
        },
    });
};

const handleBulkDelete = () => {
    if (!selectedAuthGroups.value?.length) return;

    confirm.require({
        message: 'Tem certeza que deseja apagar os grupos selecionados?',
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
            const deletePromises = selectedAuthGroups.value.map((group: AuthGroup) => 
                deleteAuthGroup(group.id, true)
            );

            await Promise.all(deletePromises);
            loadAuthGroups();
            selectedAuthGroups.value = [];
        },
        reject: () => {}
    });
};

const handleDeleteGroupPermission = (permissionId: number, groupId: number) =>  {
    confirm.require({
        message: 'Tem certeza que deseja remover esta permissão do grupo?',
        header: 'Confirmação',
        icon: 'pi pi-info-circle',
        rejectLabel: 'Cancelar',
        rejectProps: {
            label: 'Cancelar',
            severity: 'secondary',
            outlined: true
        },
        acceptProps: {
            label: 'Remover',
            severity: 'danger'
        },
        accept: async () => {
            const success = await removePermissionsFromGroup(groupId, [permissionId]);
            if (success) {
                loadAuthGroups();
            }
        },
    });
};
</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Grupos de Permissões</h3>
        <p class="text-gray-500">Gerenciamento de grupos e suas permissões</p>
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
                <NuxtLink to="/dashboard/grupos/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                </NuxtLink>
                <Button label="Apagar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="handleBulkDelete" :disabled="!selectedAuthGroups?.length" />
                <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
            </div>
        </div>
        <DataTable
            ref="dt"
            v-model:selection="selectedAuthGroups"
            v-model:expandedRows="expandedRows"
            dataKey="id"
            :value="authGroups"
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
            currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Grupos"
            :expandedRowIcon="'pi pi-chevron-down'"
            :collapsedRowIcon="'pi pi-chevron-right'"
        >
            <Column :expander="true" style="width: 3rem" />
            <Column selectionMode="multiple" style="width: 3rem"></Column>
            <Column header="ID Grupo" style="width: 7rem" :exportable="false">
                <template #body="slotProps">
                    <div class="flex items-center justify-center">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id"/>
                    </div>
                </template>
            </Column>
            <Column field="name" header="Nome" sortable style="min-width: 16rem"></Column>
            <Column :exportable="false" style="width: 8rem">
                <template #body="slotProps">
                    <NuxtLink :to="`/dashboard/grupos/action/edit?id=${slotProps.data.id}`">
                                <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                    </NuxtLink>
                    <Button 
                        icon="pi pi-trash" 
                        outlined 
                        rounded 
                        severity="danger" 
                        @click="handleDeleteAuthGroup(slotProps.data.id)" 
                    />
                </template>
            </Column>
            <template #expansion="slotProps">
                <div class="p-4">
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="mb-4">Permissões de {{ slotProps.data.name }}</h4>
                        <NuxtLink :to="`/dashboard/permissoes/action/add?id=${slotProps.data.id}`">
                            <Button label="Adicionar Permissão" icon="pi pi-plus" size="small"/>
                       </NuxtLink>
                    </div>
                    <DataTable :value="slotProps.data.permissions" v-if="slotProps.data.permissions.length">
                        <Column header="ID Permissão" style="width: 3rem" :exportable="false">
                            <template #body="slotProps">
                                <CopyToClipboardButton :textToCopy="slotProps.data.id"/>
                            </template>
                        </Column>
                        <Column field="name" header="Nome"></Column>
                        <Column field="codename" header="Código"></Column>
                        <Column>
                        <template #body="slotProps">
                            <Button 
                                icon="pi pi-trash" 
                                outlined 
                                rounded 
                                severity="danger" 
                                @click="handleDeleteGroupPermission(slotProps.data.id, slotProps.data.id_group)" 
                            />
                        </template>
                        </Column>
                    </DataTable>
                    <div v-else class="text-gray-500 italic">
                        Este grupo não possui permissões definidas
                    </div>
                </div>
            </template>
        </DataTable>
    </div>
</template>