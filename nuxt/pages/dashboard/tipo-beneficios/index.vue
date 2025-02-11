<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { DataTablePageEvent } from 'primevue/datatable';
import { useTypeBenefit } from '~/composables/useTypeBenefit';
import type { TypeBenefit } from '~/types/typebenefit';

const confirm = useConfirm();
const route = useRoute();

const typeBenefits = ref<TypeBenefit[]>([]);
const selectedTypeBenefits = ref();
const totalRecords = ref(0);

const rows = ref(25);
const first = ref(0);
const sortField = ref('name');
const sortOrder = ref(1);

const filters = ref({
    global: { value: route.query.find as string || null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getTypeBenefits, deleteTypeBenefit } = useTypeBenefit();

const loadTypeBenefits = async () => {
    const response = await getTypeBenefits({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });

    typeBenefits.value = response?.type_benefits || [];
    totalRecords.value = response?.total_count || 0;
};

await loadTypeBenefits();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadTypeBenefits();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadTypeBenefits();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadTypeBenefits();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadTypeBenefits();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

const handleDeleteTypeBenefit = async (id: string) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este tipo de benefício?',
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
            const success = await deleteTypeBenefit(id, false);
            if (success) {
                loadTypeBenefits();
            }
        },
    });
};

const handleBulkDelete = () => {
    if (!selectedTypeBenefits.value.length) return;

    confirm.require({
        message: 'Tem certeza que deseja apagar os tipos de benefício selecionados?',
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
            const deletePromises = selectedTypeBenefits.value.map((typeBenefit: TypeBenefit) => 
                deleteTypeBenefit(typeBenefit.id_type_benefit, true)
            );

            await Promise.all(deletePromises);
            loadTypeBenefits();
            selectedTypeBenefits.value = [];
        },
        reject: () => {}
    });
};
</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Tipos de Benefício</h3>
        <p class="text-gray-500">Gerenciamento de tipos de benefício</p>
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
                    <NuxtLink to="/dashboard/tipo-beneficios/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                    </NuxtLink>
                    <Button label="Apagar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="handleBulkDelete" />
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                v-model:selection="selectedTypeBenefits"
                dataKey="id_type_benefit"
                :value="typeBenefits"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Tipos de Benefício"
            >
                <Column selectionMode="multiple" style="width: 3rem"></Column>
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id_type_benefit"/>
                    </template>
                </Column>
                <Column field="name" header="Nome" sortable></Column>
                <Column field="description" header="Descrição" sortable></Column>
                <Column :exportable="false" style="width: 8rem">
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/tipo-beneficios/action/edit?id=${slotProps.data.id_type_benefit}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button 
                            icon="pi pi-trash" 
                            outlined 
                            rounded 
                            severity="danger" 
                            @click="handleDeleteTypeBenefit(slotProps.data.id_type_benefit)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>