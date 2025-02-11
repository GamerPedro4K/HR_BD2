<script setup lang="ts">
import { debounce } from 'lodash-es';
import { FilterMatchMode } from '@primevue/core/api';
import type { DataTablePageEvent } from 'primevue/datatable';
import { usePaymentMethod } from '~/composables/usePaymentMethod';
import type { PaymentMethod } from '~/types/paymentmethod';

const confirm = useConfirm();
const route = useRoute();

const paymentMethods = ref<PaymentMethod[]>([]);
const selectedPaymentMethods = ref();
const totalRecords = ref(0);

const rows = ref(25);
const first = ref(0);
const sortField = ref('name');
const sortOrder = ref(1);

const filters = ref({
    global: { value: route.query.find as string || null, matchMode: FilterMatchMode.CONTAINS },
});

const dt = ref();

const { getPaymentMethods, deletePaymentMethod } = usePaymentMethod();

const loadPaymentMethods = async () => {
    const response = await getPaymentMethods({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value,
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: filters.value.global?.value || '',
    });

    paymentMethods.value = response?.payment_methods || [];
    totalRecords.value = response?.total_count || 0;
};

await loadPaymentMethods();

const onPage = (event: DataTablePageEvent) => {
    first.value = event.first;
    rows.value = event.rows;
    loadPaymentMethods();
};

const onSort = (event: any) => {
    sortField.value = event.sortField;
    sortOrder.value = event.sortOrder;
    loadPaymentMethods();
};

const onFilter = (event: any) => {
    filters.value = event.filters;
    loadPaymentMethods();
};

const exportCSV = () => {
    dt.value.exportCSV();
};

const debouncedSearch = debounce(() => {
    first.value = 0;
    loadPaymentMethods();
}, 300);

const onGlobalSearch = (value: string) => {
    filters.value.global.value = value;
    debouncedSearch();
};

const handleDeletePaymentMethod = async (id: string) => {
    confirm.require({
        message: 'Tem certeza que deseja apagar este método de pagamento?',
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
            const success = await deletePaymentMethod(id, false);
            if (success) {
                loadPaymentMethods();
            }
        },
    });
};

const handleBulkDelete = () => {
    if (!selectedPaymentMethods.value.length) return;

    confirm.require({
        message: 'Tem certeza que deseja apagar os métodos de pagamento selecionados?',
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
            const deletePromises = selectedPaymentMethods.value.map((paymentMethod: PaymentMethod) => 
                deletePaymentMethod(paymentMethod.id_payment_method, true)
            );

            await Promise.all(deletePromises);
            loadPaymentMethods();
            selectedPaymentMethods.value = [];
        },
        reject: () => {}
    });
};
</script>

<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="mb-12">
        <h3 class="mb-1">Métodos de Pagamento</h3>
        <p class="text-gray-500">Gerenciamento de métodos de pagamento</p>
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
                    <NuxtLink to="/dashboard/tipo-pagamento/action/add">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                    </NuxtLink>
                    <Button label="Apagar" icon="pi pi-ban" class="mr-2" severity="warn" outlined @click="handleBulkDelete" />
                    <Button label="Exportar" icon="pi pi-upload" class="mr-2" severity="secondary" @click="exportCSV" />
                </div>
            </div>

            <DataTable
                ref="dt"
                v-model:selection="selectedPaymentMethods"
                dataKey="id_payment_method"
                :value="paymentMethods"
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
                currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} Métodos de Pagamento"
            >
                <Column selectionMode="multiple" style="width: 3rem"></Column>
                <Column header="ID" style="width: 3rem" :exportable="false">
                    <template #body="slotProps">
                        <CopyToClipboardButton :textToCopy="slotProps.data.id_payment_method"/>
                    </template>
                </Column>
                <Column field="icon" header="Ícone" style="width: 5rem">
                    <template #body="slotProps">
                        <div class="flex items-center justify-center">
                            <font-awesome :icon="slotProps.data.icon" :style="{ color: slotProps.data.hex_color }" class="f-size-22 mr-4" />
                        </div>
                    </template>
                </Column>
                <Column field="name" header="Nome" sortable></Column>
                <Column field="description" header="Descrição" sortable></Column>
                <Column field="hex_color" header="Cor" style="width: 8rem">
                    <template #body="slotProps">
                        <div class="flex items-center">
                            <div 
                                class="w-6 h-6 rounded-full mr-2" 
                                :style="{ backgroundColor: slotProps.data.hex_color }"
                            ></div>
                        </div>
                    </template>
                </Column>
                <Column :exportable="false" style="width: 8rem">
                    <template #body="slotProps">
                        <NuxtLink :to="`/dashboard/tipo-pagamento/action/edit?id=${slotProps.data.id_payment_method}`">
                            <Button icon="pi pi-pencil" outlined rounded class="mr-2" />
                        </NuxtLink>
                        <Button 
                            icon="pi pi-trash" 
                            outlined 
                            rounded 
                            severity="danger" 
                            @click="handleDeletePaymentMethod(slotProps.data.id_payment_method)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>