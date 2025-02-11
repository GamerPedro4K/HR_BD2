<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { CertificateType } from '~/types/certifications';
import type { DataTablePageEvent } from 'primevue/datatable';

const confirm = useConfirm();
const route = useRoute();

const certificateTypes = ref<CertificateType[]>([]);
const selectedCertificateTypes = ref();
const totalRecords = ref(0);

const rows = ref(25);
const first = ref(0);
const sortField = ref('name');
const sortOrder = ref(1);

const filters = ref({
    global: { value: route.query.find as string || null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getCertificateTypes, deleteCertificateType } = useCertification();

const loadCertificateTypes = async () => {
    const response = await getCertificateTypes({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });

    certificateTypes.value = response?.certificate_types || [];
    totalRecords.value = response?.total_count || 0;
};

await loadCertificateTypes();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadCertificateTypes();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadCertificateTypes();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadCertificateTypes();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadCertificateTypes();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

const handleDeleteCertificateType = async (id: string) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este tipo de certificado?',
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
            const success = await deleteCertificateType(id, false);
            if (success) {
                loadCertificateTypes();
            }
        },
    });
};

const handleBulkDelete = () => {
    if (!selectedCertificateTypes.value.length) return;

    confirm.require({
        message: 'Tem certeza que deseja apagar os tipos de certificado selecionados?',
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
            const deletePromises = selectedCertificateTypes.value.map((certificateType: CertificateType) => 
                deleteCertificateType(certificateType.id_certificate_type, true)
            );

            await Promise.all(deletePromises);
            loadCertificateTypes();
            selectedCertificateTypes.value = [];
        },
        reject: () => {}
    });
};
</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Tipos de Certificado</h3>
        <p class="text-gray-500">Gerenciamento de tipos de certificado</p>
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
                    <NuxtLink to="/dashboard/tipo-certificados/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                    </NuxtLink>
                    <Button label="Apagar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="handleBulkDelete" />
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                v-model:selection="selectedCertificateTypes"
                dataKey="id_certificate_type"
                :value="certificateTypes"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Tipos de Certificado"
            >
                <Column selectionMode="multiple" style="width: 3rem"></Column>
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id_certificate_type"/>
                    </template>
                </Column>
                <Column field="icon" header="Ícone" style="width: 5rem">
                    <template #body="slotProps">
                        <font-awesome :icon="slotProps.data.icon" :style="{ color: slotProps.data.hex_color }" class="f-size-22 mr-4" />
                    </template>
                </Column>
                <Column field="name" header="Nome" sortable></Column>
                <Column field="description" header="Descrição" sortable></Column>
                <Column :exportable="false" style="width: 8rem">
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/tipo-certificados/action/edit?id=${slotProps.data.id_certificate_type}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button 
                            icon="pi pi-trash" 
                            outlined 
                            rounded 
                            severity="danger" 
                            @click="handleDeleteCertificateType(slotProps.data.id_certificate_type)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>