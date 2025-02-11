<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { ContractType } from '~/types/contractType';

const formRef = ref<any>(null);
const responseContractType = ref<ContractType | null>(null);

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getContractType, createContractType, updateContractType } = useContractType();

const isEditMode = (route.params.action === 'edit');

const initialValues = ref<any>({
  contract_type_name: '',
  description: '',
  termination_notice_period: 30,
  overtime_eligible: false,
  benefits_eligible: false,
});

const getDataOnEdit = async () => {
  if (!isEditMode) return;
  
  try {
    responseContractType.value = await getContractType(route.query.id as string);
    if (!responseContractType.value) {
      await router.push('/dashboard/contract-types');
      return;
    }
    
    initialValues.value = {
      contract_type_name: responseContractType.value.contract_type_name || '',
      description: responseContractType.value.description || '',
      termination_notice_period: responseContractType.value.termination_notice_period || 30,
      overtime_eligible: responseContractType.value.overtime_eligible || false,
      benefits_eligible: responseContractType.value.benefits_eligible || false,
    };

  } catch (error) {
    console.error('Error fetching contract type:', error);
  }
};

await getDataOnEdit();

const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Tipo de Contrato' : 'Adicionar Tipo de Contrato');

const schema = z.object({
  contract_type_name: z.string()
    .min(1, 'Nome do tipo de contrato é obrigatório')
    .max(100, 'Nome deve ter menos de 100 caracteres'),
  description: z.string()
    .min(1, 'Descrição é obrigatória'),
  termination_notice_period: z.number({
    required_error: 'Período de aviso prévio é obrigatório',
    invalid_type_error: 'Período deve ser um número',
  }).min(0, 'Período não pode ser negativo'),
  overtime_eligible: z.boolean(),
  benefits_eligible: z.boolean(),
});

const resolver = zodResolver(schema);
const previousRoute = useState('previousRoute');

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    const submissionData = {
      contract_type_name: values.contract_type_name,
      description: values.description,
      termination_notice_period: values.termination_notice_period,
      overtime_eligible: values.overtime_eligible,
      benefits_eligible: values.benefits_eligible,
    };

    try {
      if (isEditMode) {
        await updateContractType(route.query.id as string, submissionData);
      } else {
        await createContractType(submissionData);
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
    router.push('/dashboard/contract-types');
  }
};
</script>

<template>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Tipo de Contrato' : 'Adicionar Novo Tipo de Contrato' }}</h3>
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
          <div v-if="isEditMode" class="font-semibold text-xl">ID Tipo de Contrato:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Nome do Tipo de Contrato*</div>
          <InputText 
            name="contract_type_name" 
            type="text" 
            placeholder="Introduza nome do tipo de contrato" 
            fluid
          />
          <Message v-if="$form.contract_type_name?.invalid" severity="error" size="small" variant="simple">
            {{ $form.contract_type_name.error.message }}
          </Message>

          <div class="font-semibold text-xl">Descrição*</div>
          <Textarea 
            name="description" 
            placeholder="Introduza descrição do tipo de contrato" 
            :autoResize="true" 
            rows="3" 
            fluid
          />
          <Message v-if="$form.description?.invalid" severity="error" size="small" variant="simple">
            {{ $form.description.error.message }}
          </Message>

          <div class="font-semibold text-xl">Período de Aviso Prévio (dias)*</div>
          <InputNumber 
            name="termination_notice_period" 
            placeholder="Introduza o período de aviso prévio" 
            :min="0"
            fluid
          />
          <Message v-if="$form.termination_notice_period?.invalid" severity="error" size="small" variant="simple">
            {{ $form.termination_notice_period.error.message }}
          </Message>

          <div class="font-semibold text-xl">Elegível para Horas Extras</div>
          <Checkbox 
            name="overtime_eligible" 
            :binary="true"
          />
          <Message v-if="$form.overtime_eligible?.invalid" severity="error" size="small" variant="simple">
            {{ $form.overtime_eligible.error.message }}
          </Message>

          <div class="font-semibold text-xl">Elegível para Benefícios</div>
          <Checkbox 
            name="benefits_eligible" 
            :binary="true"
          />
          <Message v-if="$form.benefits_eligible?.invalid" severity="error" size="small" variant="simple">
            {{ $form.benefits_eligible.error.message }}
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