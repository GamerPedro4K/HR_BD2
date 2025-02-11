<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { TypeBenefit } from '~/types/typebenefit';

const formRef = ref<any>(null);
const responseTypeBenefit = ref<TypeBenefit | null>(null);

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getTypeBenefit, createTypeBenefit, updateTypeBenefit } = useTypeBenefit();

const isEditMode = (route.params.action === 'edit');

const initialValues = ref<any>({
  name: '',
  description: '',
});

const getDataOnEdit = async () => {
  if (!isEditMode) return;
  
  try {
    responseTypeBenefit.value = await getTypeBenefit(route.query.id as string);
    if (!responseTypeBenefit.value) {
      await router.push('/dashboard/type-benefits');
      return;
    }
    
    initialValues.value = {
      name: responseTypeBenefit.value.name || '',
      description: responseTypeBenefit.value.description || '',
    };

  } catch (error) {
    console.error('Error fetching type benefit:', error);
  }
};

await getDataOnEdit();

const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Tipo de Benefício' : 'Adicionar Tipo de Benefício');

const schema = z.object({
  name: z.string()
    .min(1, 'Nome é obrigatório')
    .max(100, 'Nome deve ter menos de 100 caracteres'),
  description: z.string()
    .min(1, 'Descrição é obrigatória')
    .max(500, 'Descrição deve ter menos de 500 caracteres'),
});

const resolver = zodResolver(schema);
const previousRoute = useState('previousRoute');

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    const submissionData = {
      name: values.name,
      description: values.description,
    };

    try {
      if (isEditMode) {
        await updateTypeBenefit(route.query.id as string, submissionData);
      } else {
        await createTypeBenefit(submissionData);
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
    router.push('/dashboard/type-benefits');
  }
};
</script>

<template>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Tipo de Benefício' : 'Adicionar Novo Tipo de Benefício' }}</h3>
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
          <div v-if="isEditMode" class="font-semibold text-xl">ID Tipo de Benefício:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Nome*</div>
          <InputText 
            name="name" 
            type="text" 
            placeholder="Introduza o nome do tipo de benefício" 
            fluid
          />
          <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
            {{ $form.name.error.message }}
          </Message>

          <div class="font-semibold text-xl">Descrição*</div>
          <Textarea 
            name="description" 
            placeholder="Introduza a descrição do tipo de benefício" 
            :autoResize="true" 
            rows="3" 
            fluid
          />
          <Message v-if="$form.description?.invalid" severity="error" size="small" variant="simple">
            {{ $form.description.error.message }}
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