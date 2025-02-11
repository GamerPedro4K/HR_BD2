<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { PaymentMethod } from '~/types/paymentmethod';

const formRef = ref<any>(null);
const responsePaymentMethod = ref<PaymentMethod | null>(null);

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getPaymentMethod, createPaymentMethod, updatePaymentMethod } = usePaymentMethod();

const isEditMode = (route.params.action === 'edit');

const initialValues = ref<any>({
  name: '',
  description: '',
  icon: '',
  hex_color: 'ff0000',
});

const getDataOnEdit = async () => {
  if (!isEditMode) return;
  
  try {
    responsePaymentMethod.value = await getPaymentMethod(route.query.id as string);
    if (!responsePaymentMethod.value) {
      await router.push('/dashboard/payment-methods');
      return;
    }
    
    initialValues.value = {
      name: responsePaymentMethod.value.name || '',
      description: responsePaymentMethod.value.description || '',
      icon: responsePaymentMethod.value.icon || '',
      hex_color: responsePaymentMethod.value.hex_color.startsWith('#') 
        ? responsePaymentMethod.value.hex_color 
        : `#${responsePaymentMethod.value.hex_color}` || '#ff0000',
    };

  } catch (error) {
    console.error('Error fetching payment method:', error);
  }
};

await getDataOnEdit();

const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Método de Pagamento' : 'Adicionar Método de Pagamento');

const schema = z.object({
  name: z.string()
    .min(1, 'Nome é obrigatório')
    .max(100, 'Nome deve ter menos de 100 caracteres'),
  description: z.string().min(1, 'Descrição é obrigatória'),
  icon: z.string().min(1, 'Ícone é obrigatório'),
  hex_color: z.string().min(1, 'Cor é obrigatória'),
});

const resolver = zodResolver(schema);
const previousRoute = useState('previousRoute');

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    const submissionData = {
      name: values.name,
      description: values.description || '',
      icon: values.icon,
      hex_color: values.hex_color.startsWith('#') ? values.hex_color : `#${values.hex_color}`,
    };

    try {
      if (isEditMode) {
        await updatePaymentMethod(route.query.id as string, submissionData);
      } else {
        await createPaymentMethod(submissionData);
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
    router.push('/dashboard/payment-methods');
  }
};
</script>

<template>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Método de Pagamento' : 'Adicionar Novo Método de Pagamento' }}</h3>
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
          <div v-if="isEditMode" class="font-semibold text-xl">ID Método de Pagamento:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Nome*</div>
          <InputText 
            name="name" 
            type="text" 
            placeholder="Introduza o nome do método de pagamento" 
            fluid
          />
          <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
            {{ $form.name.error.message }}
          </Message>

          <div class="font-semibold text-xl">Ícone* <a href="https://fontawesome.com/search?ic=free" target="_blank" class="text-sm text-blue-500">(Procurar ícones)</a></div>
          <div class="flex flex-col gap-2">
            <div class="flex items-center gap-4">
              <div class="flex-grow">
                <InputText 
                  name="icon" 
                  type="text" 
                  placeholder="Exemplo: fas fa-credit-card"
                  fluid
                />
              </div>
              <div class="w-10 h-10 flex items-center justify-center bg-gray-100 rounded">
                <font-awesome v-if="$form.icon?.value" :icon="$form.icon?.value" :style="{ color: $form.hex_color?.value }" class="text-2xl" />
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

          <div class="font-semibold text-xl">Descrição</div>
          <Textarea 
            name="description" 
            placeholder="Introduza a descrição do método de pagamento" 
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