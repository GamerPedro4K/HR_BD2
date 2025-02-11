<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { Permission } from '~/types/permission';
import type { AuthGroup } from '~/types/authgroup';

const formRef = ref<any>(null);
const permissions = ref<Permission[]>([]);
const loading = ref(false);
const selectedGroup = ref<AuthGroup | null>(null);

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getPermissions, addPermissionsToGroup } = usePermission();
const { getAuthGroups } = useAuthGroup();

const groupId = computed(() => Number(route.query.id));

// Initial form values
const initialValues = ref<any>({
  permission_ids: [],
});

// Load group info and available permissions
const loadData = async () => {
  loading.value = true;
  try {
    // Load group info using getAuthGroups with search params
    const groupResponse = await getAuthGroups({
      limit: 25,
      offset: 0,
      order_by: 'name',
      order_direction: 'ASC',
      global_search: route.query.id as string
    });
    
    if (groupResponse.auth_groups && groupResponse.auth_groups.length > 0) {
      selectedGroup.value = groupResponse.auth_groups[0];
      
      // Atualizar initialValues com as permissões do grupo
      initialValues.value = {
        permission_ids: selectedGroup.value?.permissions?.map(p => p.id) ?? []
      };
    } else {
      $toast.add({ 
        severity: 'error', 
        summary: 'Erro', 
        detail: 'Grupo não encontrado', 
        life: 3000 
      });
      router.push('/dashboard/grupos');
      return;
    }

    // Load available permissions
    const response = await getPermissions({ 
      order_by: 'name',
      order_direction: 'ASC',
    });
    permissions.value = response.permissions;

  } catch (error) {
    console.error('Error loading data:', error);
    $toast.add({ 
      severity: 'error', 
      summary: 'Erro', 
      detail: 'Erro ao carregar dados', 
      life: 3000 
    });
  } finally {
    loading.value = false;
  }
};

await loadData();

// Form validation schema
const schema = z.object({
  permission_ids: z.array(z.number())
    .min(1, 'Selecione pelo menos uma permissão'),
});

const resolver = zodResolver(schema);

// Handle form submission
const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    try {
      const { values } = toRaw(all);
      await addPermissionsToGroup(groupId.value, values.permission_ids);
      router.push('/dashboard/grupos');
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  }
};

// Navigation
const goBack = () => {
  router.push('/dashboard/grupos');
};

// Update breadcrumb
const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel('Adicionar Permissões ao Grupo');

// Format permission name for display
const formatPermissionName = (name: string) => {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};
</script>

<template>
  <div>
    <h3 class="mb-3">Adicionar Permissões ao Grupo</h3>
    <BreadcrumbCustom :home="home" :breadcrumbs="breadcrumbs" />
    
    <div v-if="loading" class="card mt-5 p-4 flex justify-center">
      <ProgressSpinner />
    </div>

    <div v-else-if="selectedGroup" class="card mt-5">
      <!-- Group Info Section -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg">
        <div class="font-semibold text-xl mb-2">Grupo:</div>
        <div class="text-lg">{{ selectedGroup.name }}</div>
      </div>

      <!-- Permissions Form -->
      <Form
        ref="formRef"
        v-slot="$form"
        :resolver="resolver"
        :initial-values="initialValues"
        @submit="onSubmit"
        class="w-full"
      >
        <div class="flex flex-col gap-4 w-full">
          <div class="font-semibold text-xl">Permissões*</div>
          <MultiSelect
            name="permission_ids"
            :options="permissions"
            optionLabel="name"
            optionValue="id"
            placeholder="Selecione as permissões"
            display="chip"
            class="w-full"
            :filter="true"
          />
          <Message v-if="$form.permission_ids?.invalid" severity="error" size="small" variant="simple">
            {{ $form.permission_ids.error.message }}
          </Message>

          <!-- Lista de permissões selecionadas -->
          <div v-if="$form.permission_ids?.value?.length > 0" class="mt-4">
            <div class="font-semibold mb-2">Permissões Selecionadas:</div>
            <ul class="bg-gray-50 rounded-lg p-4">
              <li v-for="permissionId in $form.permission_ids?.value" :key="permissionId" 
                  class="flex items-center py-2 px-4 hover:bg-gray-100 rounded">
                <i class="pi pi-shield mr-2"></i>
                {{ formatPermissionName(permissions.find(p => p.id === permissionId)?.name || '') }}
              </li>
            </ul>
          </div>

          <div class="text-sm text-gray-500 pt-2">
            Os campos marcados com <span class="text-red-500">*</span> são obrigatórios.
          </div>

          <div class="flex justify-end gap-2 pt-4">
            <Button label="Cancelar" severity="secondary" @click="goBack()" />
            <Button type="submit" label="Adicionar Permissões" severity="primary"/>
          </div>
        </div>
      </Form>
    </div>

    <div v-else class="card mt-5 p-4">
      <Message severity="error" :closable="false">
        Não foi possível carregar o grupo. Por favor, tente novamente.
      </Message>
    </div>
  </div>
</template>