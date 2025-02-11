<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { Department } from '~/types/department';
import type { RoleRequst } from '~/types/roles';
import type { DataTablePageEvent } from 'primevue/datatable';

// Declare variables
const formRef = ref<any>(null);
const responseDepartment = ref<Department | null>(null);
const roles = ref<RoleRequst[]>([]);
const totalRecords = ref(0);

// Declare functions
const route = useRoute();
const router = useRouter();
const confirm = useConfirm();
const { getRoles, deleteRole } = useRoles();
const { getDepartment, createDepartment, updateDepartment } = useDepartment();

//table stuff
// Pagination and sorting
const dt = ref();
const rows = ref(25);
const first = ref(0);
const sortField = ref('');
const sortOrder = ref(1);


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
const exportCSV = () => {
    dt.value.exportCSV();
};

// Check if the page is in edit mode
const isEditMode = (route.params.action === 'edit');

// Initialize the form
const initialValues = ref<any>({
  name: '',
  description: '',
});

const getDepartmentOnEdit = async () => {
  if (!isEditMode) {
    return;
  }
  try {
    responseDepartment.value = await getDepartment(route.query.id as string);
    
    if (responseDepartment.value === null) {
      await router.push('/dashboard/departments');
      return;
    }
    
    initialValues.value = {
      name: responseDepartment.value.name || '',
      description: responseDepartment.value.description || '',
    };
  } catch (error) {
    console.error('Erro ao buscar dados do departamento:', error);
  }
};


const loadRoles = async () => {
    const response = await getRoles({
        limit: rows.value,
        offset: first.value,
        order_by: sortField.value || 'role_name',
        order_direction: sortOrder.value === 1 ? 'ASC' : 'DESC',
        global_search: responseDepartment.value?.id_department,
    });
   
    roles.value = response?.roles || [];
    totalRecords.value = response?.total_count || 0;
};

// Get data
await getDepartmentOnEdit();
await loadRoles();

// Breadcrumbs setup
const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Departamento' : 'Adicionar Departamento');

// Define Zod Schema
const schema = z.object({
  name: z.string().min(1, 'Nome é obrigatório').max(100, 'Nome tem de ter menos de 100 caracteres'),
  description: z.string().min(1, 'Descrição é obrigatório'),
});

const resolver = zodResolver(schema);

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    const submissionData = {
      name: values.name,
      description: values.description || '',
    };

    try {
      if (isEditMode) {
        await updateDepartment(route.query.id as string, submissionData);
        await router.push('/dashboard/departments');
      } else {
        const response = await createDepartment(submissionData);

        if (response.id_department) {
          await router.push(`/dashboard/departments/action/edit?id=${response.id_department}`);
        }
      }
      
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  }
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
                loadRoles();
            }
        },
        reject: () => {}
  });
};



</script>

<template>
  <ConfirmDialog></ConfirmDialog>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Departmento' : 'Adicionar Novo Departamento' }}</h3>
    <BreadcrumbCustom :home="home" :breadcrumbs="breadcrumbs" />
    <div class="card mt-5">
      <Form
        ref="formRef"
        v-slot="$form"
        :resolver="resolver"
        :initial-values="initialValues"
        @submit="onSubmit"
        class="w-full"
      >
        <div class="flex flex-col gap-4 w-full">
          <div v-if="isEditMode" class="font-semibold text-xl">ID Departamento:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Nome*</div>
          <InputText name="name" type="text" placeholder="Introduza nome do departamento" fluid/>
          <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
            {{ $form.name.error.message }}
          </Message>

          <div class="font-semibold text-xl">Descrição*</div>
          <Textarea name="description" placeholder="Introduza descrição do departamento" :autoResize="true" rows="3" fluid/>
          <Message v-if="$form.description?.invalid" severity="error" size="small" variant="simple">
            {{ $form.description.error.message }}
          </Message>

          <div class="card" v-if="isEditMode">
            <h3>Funções do departamento:</h3>
            <div class="flex justify-between items-center mb-8">
                <div></div>
                <div>
                  <NuxtLink :to="`/dashboard/roles/action/add?id=${route.query.id as string}`">
                        <Button label="Adicionar" icon="pi pi-plus" class="mr-2" />
                  </NuxtLink>
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
          <div v-if="!isEditMode" class="p-4">
              <h1 class="d-center">Para adicionar Cargos a este departamento, primeiro crie o departamento.</h1>
          </div>

          <div class="text-sm text-gray-500 pt-2">
            Os campos marcados com <span class="text-red-500">*</span> são obrigatórios.
          </div>

          <div class="flex justify-end gap-2 pt-4">
            <Button label="Cancelar" severity="secondary" @click="router.push('/dashboard/departments')"/>
            <Button type="submit" :label="isEditMode ? 'Atualizar' : 'Criar'" severity="primary"/>
          </div>
        </div>
      </Form>
    </div>
  </div>
</template>