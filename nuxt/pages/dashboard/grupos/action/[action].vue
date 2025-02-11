<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { AuthGroup, AuthGroupFormData } from '~/types/authgroup';

const formRef = ref<any>(null);
const responseAuthGroup = ref<AuthGroup | null>(null);

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getAuthGroup, createAuthGroup, updateAuthGroup } = useAuthGroup();

const isEditMode = (route.params.action === 'edit');

const initialValues = ref<AuthGroupFormData>({
  name: '',
});

const getDataOnEdit = async () => {
  if (!isEditMode) return;
  
  try {
    responseAuthGroup.value = await getAuthGroup(Number(route.query.id));
    if (!responseAuthGroup.value) {
      await router.push('/dashboard/auth-groups');
      return;
    }
    
    initialValues.value = {
      name: responseAuthGroup.value.name || '',
    };

  } catch (error) {
    console.error('Error fetching auth group:', error);
  }
};

await getDataOnEdit();

const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Grupo' : 'Adicionar Grupo');

const schema = z.object({
  name: z.string()
    .min(1, 'Nome é obrigatório')
    .max(100, 'Nome deve ter menos de 100 caracteres'),
});

const resolver = zodResolver(schema);
const previousRoute = useState('previousRoute');

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    const submissionData: AuthGroupFormData = {
      name: values.name,
    };

    try {
      if (isEditMode) {
        await updateAuthGroup(Number(route.query.id), submissionData);
      } else {
        await createAuthGroup(submissionData);
      }

      goBack();
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  }
};

const goBack = () => {
  if (previousRoute.value) {
    router.push(previousRoute.value);
  } else {
    router.push('/dashboard/auth-groups');
  }
};
</script>

<template>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Grupo' : 'Adicionar Novo Grupo' }}</h3>
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
          <div v-if="isEditMode" class="font-semibold text-xl">ID Grupo:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Nome do Grupo*</div>
          <InputText 
            name="name" 
            type="text" 
            placeholder="Introduza o nome do grupo" 
            fluid
          />
          <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
            {{ $form.name.error.message }}
          </Message>

          <div class="text-sm text-gray-500 pt-2">
            Os campos marcados com <span class="text-red-500">*</span> são obrigatórios.
          </div>

          <div class="flex justify-end gap-2 pt-4">
            <Button label="Cancelar" severity="secondary" @click="goBack()" />
            <Button type="submit" :label="isEditMode ? 'Atualizar' : 'Criar'" severity="primary"/>
          </div>
        </div>
      </Form>
    </div>
  </div>
</template>