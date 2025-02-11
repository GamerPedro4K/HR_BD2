<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { ContractLeaveType } from '~/types/contractleavetype ';

const formRef = ref<any>(null);
const responseLeaveType = ref<ContractLeaveType | null>(null);

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getContractLeaveType, createContractLeaveType, updateContractLeaveType } = useContractLeaveType();

const isEditMode = (route.params.action === 'edit');

const initialValues = ref<any>({
  leave_type: '',
  description: '',
  is_paid: false,
});

const getDataOnEdit = async () => {
  if (!isEditMode) return;
  
  try {
    responseLeaveType.value = await getContractLeaveType(route.query.id as string);
    if (!responseLeaveType.value) {
      await router.push('/dashboard/contract-leave-types');
      return;
    }
    
    initialValues.value = {
      leave_type: responseLeaveType.value.leave_type || '',
      description: responseLeaveType.value.description || '',
      is_paid: responseLeaveType.value.is_paid || false,
    };

  } catch (error) {
    console.error('Error fetching contract leave type:', error);
  }
};

await getDataOnEdit();

const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Tipo de Licença' : 'Adicionar Tipo de Licença');

const schema = z.object({
  leave_type: z.string()
    .min(1, 'Tipo de licença é obrigatório')
    .max(100, 'Tipo de licença deve ter menos de 100 caracteres'),
  description: z.string().optional(),
  is_paid: z.boolean({
    required_error: 'Status de pagamento é obrigatório',
    invalid_type_error: 'Status de pagamento deve ser um booleano',
  }),
});

const resolver = zodResolver(schema);
const previousRoute = useState('previousRoute');

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    const submissionData = {
      leave_type: values.leave_type,
      description: values.description || '',
      is_paid: values.is_paid,
    };

    try {
      if (isEditMode) {
        await updateContractLeaveType(route.query.id as string, submissionData);
      } else {
        await createContractLeaveType(submissionData);
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
    router.push('/dashboard/contract-leave-types');
  }
};
</script>

<template>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Tipo de Licença' : 'Adicionar Novo Tipo de Licença' }}</h3>
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
          <div v-if="isEditMode" class="font-semibold text-xl">ID Tipo de Licença:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Tipo de Licença*</div>
          <InputText 
            name="leave_type" 
            type="text" 
            placeholder="Introduza o tipo de licença" 
            fluid
          />
          <Message v-if="$form.leave_type?.invalid" severity="error" size="small" variant="simple">
            {{ $form.leave_type.error.message }}
          </Message>

          <div class="font-semibold text-xl">Descrição</div>
          <Textarea 
            name="description" 
            placeholder="Introduza a descrição da licença" 
            :autoResize="true" 
            rows="3" 
            fluid
          />
          <Message v-if="$form.description?.invalid" severity="error" size="small" variant="simple">
            {{ $form.description.error.message }}
          </Message>

          <div class="font-semibold text-xl">É Remunerado?*</div>
          <div class="flex items-center">
            <Checkbox 
              name="is_paid" 
              :binary="true"
            />
            <label class="ml-2">Sim, esta licença é remunerada</label>
          </div>
          <Message v-if="$form.is_paid?.invalid" severity="error" size="small" variant="simple">
            {{ $form.is_paid.error.message }}
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