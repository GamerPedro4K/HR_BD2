<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { ContractState } from '~/types/contractState';

const formRef = ref<any>(null);
const responseContractState = ref<ContractState | null>(null);

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getContractState, createContractState, updateContractState } = useContractState();

const isEditMode = (route.params.action === 'edit');

const initialValues = ref<any>({
  icon: '',
  hex_color: 'ff0000',
  state: '',
  description: '',
});

const getDataOnEdit = async () => {
  if (!isEditMode) return;
  
  try {
    responseContractState.value = await getContractState(route.query.id as string);
    if (!responseContractState.value) {
      await router.push('/dashboard/contract-states');
      return;
    }
    
    initialValues.value = {
      icon: responseContractState.value.icon || '',
      hex_color: responseContractState.value.hex_color.startsWith('#') ? responseContractState.value.hex_color : `#${responseContractState.value.hex_color}` || '#ff0000',
      state: responseContractState.value.state || '',
      description: responseContractState.value.description || '',
    };

  } catch (error) {
    console.error('Error fetching contract state:', error);
  }
};

await getDataOnEdit();

const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Estado de Contrato' : 'Adicionar Estado de Contrato');

const schema = z.object({
  icon: z.string().min(1, 'Ícone é obrigatório'),
  hex_color: z.string().min(1, 'Cor é obrigatória'),
  state: z.string()
    .min(1, 'Estado é obrigatório')
    .max(100, 'Estado deve ter menos de 100 caracteres'),
  description: z.string().optional(),
});

const resolver = zodResolver(schema);
const previousRoute = useState('previousRoute');

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    const submissionData = {
      icon: values.icon,
      hex_color: values.hex_color,
      state: values.state,
      description: values.description || '',
    };

    try {
      if (isEditMode) {
        await updateContractState(route.query.id as string, submissionData);
      } else {
        await createContractState(submissionData);
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
    router.push('/dashboard/contract-states');
  }
};
</script>

<template>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Estado de Contrato' : 'Adicionar Novo Estado de Contrato' }}</h3>
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
          <div v-if="isEditMode" class="font-semibold text-xl">ID Estado de Contrato:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Ícone* <a href="https://fontawesome.com/search?ic=free" target="_blank" class="text-sm text-blue-500">(Procurar ícones)</a></div>
          <div class="flex flex-col gap-2">
            <div class="flex items-center gap-4">
              <div class="flex-grow">
                <InputText 
                  name="icon" 
                  type="text" 
                  placeholder="Exemplo: fas fa-times-circle"
                  fluid
                />
              </div>
              <div class="w-10 h-10 flex items-center justify-center bg-gray-100 rounded">
                <font-awesome v-if="$form.icon?.value" :icon="$form.icon?.value":style="{ color: $form.hex_color?.value }"class="text-2xl" />
                <font-awesome v-else icon="fa-question-circle" class="text-2xl text-gray-400" />
              </div>
            </div>
            <small class="text-gray-500">Formato: fas fa-icon-name</small>
            <Message v-if="$form.icon?.invalid" severity="error" size="small" variant="simple">
              {{ $form.icon.error.message }}
            </Message>
          </div>

          <div class="font-semibold text-xl">Cor*</div>
          <InputText type="text" name="hex_color" hidden />
          <ClientOnly>
            <ColorPicker name="hex_color" format="hex" fluid :default-color="$form.hex_color?.value"/>
          </ClientOnly>
          <Message v-if="$form.hex_color?.invalid" severity="error" size="small" variant="simple">
            {{ $form.hex_color.error.message }}
          </Message>

          <div class="font-semibold text-xl">Estado*</div>
          <InputText 
            name="state" 
            type="text" 
            placeholder="Introduza o nome do estado" 
            fluid
          />
          <Message v-if="$form.state?.invalid" severity="error" size="small" variant="simple">
            {{ $form.state.error.message }}
          </Message>

          <div class="font-semibold text-xl">Descrição</div>
          <Textarea 
            name="description" 
            placeholder="Introduza a descrição do estado" 
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