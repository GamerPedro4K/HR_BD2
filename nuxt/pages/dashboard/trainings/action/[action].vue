<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { TrainingType, TrainingTypeSubmission } from '~/types/trainingType';

const formRef = ref<any>(null);
const responseTrainingType = ref<TrainingType | null>(null);

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getTrainingType, addTrainingType, editTrainingType } = useTrainingType();

const isEditMode = (route.params.action === 'edit');

const initialValues = ref<any>({
  name: '',
  description: '',
  hours: 0,
});

const getDataOnEdit = async () => {
  if (!isEditMode) return;
  
  try {
    responseTrainingType.value = await getTrainingType(route.query.id as string);
    if (!responseTrainingType.value) {
      await router.push('/dashboard/training-types');
      return;
    }
    
    initialValues.value = {
      name: responseTrainingType.value.name || '',
      description: responseTrainingType.value.description || '',
      hours: responseTrainingType.value.hours || 0,
    };

  } catch (error) {
    console.error('Error fetching training type:', error);
  }
};

await getDataOnEdit();

const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Tipo de Treinamento' : 'Adicionar Tipo de Treinamento');

const schema = z.object({
  name: z.string().min(1, 'Nome é obrigatório').max(100, 'Nome deve ter menos de 100 caracteres'),
  description: z.string().min(1, 'Descrição é obrigatória'),
  hours: z.number({
    required_error: 'Horas são obrigatórias',
    invalid_type_error: 'Horas devem ser um número',
  }).min(0, 'Horas não podem ser negativas'),
});

const resolver = zodResolver(schema);
const previousRoute = useState('previousRoute');

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    const submissionData: TrainingTypeSubmission = {
      name: values.name,
      description: values.description,
      hours: values.hours,
    };

    try {
      if (isEditMode) {
        await editTrainingType(route.query.id as string, submissionData);
      } else {
        await addTrainingType(submissionData);
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
    router.push('/dashboard/training-types');
  }
};
</script>

<template>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Tipo de Treinamento' : 'Adicionar Novo Tipo de Treinamento' }}</h3>
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
          <div v-if="isEditMode" class="font-semibold text-xl">ID Tipo de Treinamento:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Nome*</div>
          <InputText name="name" type="text" placeholder="Introduza nome do tipo de treinamento" fluid/>
          <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
            {{ $form.name.error.message }}
          </Message>

          <div class="font-semibold text-xl">Descrição*</div>
          <Textarea name="description" placeholder="Introduza descrição do tipo de treinamento" :autoResize="true" rows="3" fluid/>
          <Message v-if="$form.description?.invalid" severity="error" size="small" variant="simple">
            {{ $form.description.error.message }}
          </Message>

          <div class="font-semibold text-xl">Horas*</div>
          <InputNumber name="hours" placeholder="Introduza as horas de treinamento" :min="0" fluid/>
          <Message v-if="$form.hours?.invalid" severity="error" size="small" variant="simple">
            {{ $form.hours.error.message }}
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