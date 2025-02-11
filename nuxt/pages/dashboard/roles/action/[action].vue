<script setup lang="ts">
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import type { AuthGroupFormData, AuthGroupListResponse } from '~/types/authgroup';
import type { RoleRequst, RoleSubmission } from '~/types/roles';
import type { TrainingType } from '~/types/training';

const formRef = ref<any>(null);
const responseRole = ref<RoleRequst | null>(null);
const trainingTypes = ref<TrainingType[]>([]);
const authGroups = ref<AuthGroupListResponse>();

const route = useRoute();
const router = useRouter();
const { $toast } = useNuxtApp();
const { getRole, addRole, editRole } = useRoles();
const { getTrainingType } = useTraining();
const { getAuthGroups } = useAuthGroup();

const isEditMode = (route.params.action === 'edit');

const initialValues = ref<any>({
  role_name: '',
  hex_color: 'ff0000',
  description: '',
  auth_group: null,
  training_type: [],
});

const getDataOnEdit = async () => {
  if (!isEditMode) return;
  
  try {
    responseRole.value = await getRole(route.query.id as string);
    if (!responseRole.value) {
      await router.push('/dashboard/departments');
      return;
    }
    
    initialValues.value = {
      role_name: responseRole.value.role_name || '',
      hex_color: responseRole.value.hex_color || 'ff0000',
      description: responseRole.value.description || '',
      auth_group: responseRole.value.id_auth_group || '',
      training_type: responseRole.value.training_types.map(t => t.id_training_type),
    };

  } catch (error) {
    console.error('Error fetching role:', error);
  }
};

const loadAuthGroups = async () => {
  const response = await getAuthGroups({});
  authGroups.value = response;
};

const loadTrainingTypes = async () => {
  const response = await getTrainingType();
  trainingTypes.value = response?.training_types || [];
};

await getDataOnEdit();
await loadTrainingTypes();
await loadAuthGroups();

const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Função' : 'Adicionar Função');

const schema = z.object({
  role_name: z.string().min(1, 'Nome é obrigatório').max(100, 'Nome deve ter menos de 100 caracteres'),
  hex_color: z.string().min(1, 'Cor é obrigatória'),
  description: z.string().min(1, 'Descrição é obrigatória'),
  training_type: z.array(z.string()).optional(),
  auth_group: z.number({
  invalid_type_error: 'Grupo é obrigatório',
  required_error: 'Grupo é obrigatório'
  }),
});

const resolver = zodResolver(schema);
const previousRoute = useState('previousRoute');

const onSubmit = async (all: any) => {
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  
  if (!hasErrors) {
    const { values } = toRaw(all);
    let submissionData: RoleSubmission = {
      ...values,
      hex_color: values.hex_color.startsWith('#') ? values.hex_color : `#${values.hex_color}`,
      id_auth_group: values.auth_group,
      training_types: values.training_type,
      auth_group: undefined,
      training_type: undefined,
    };

    if(!isEditMode)
      submissionData.id_department = route.query.id as string

    try {
      if (isEditMode) {
        await editRole(route.query.id as string, submissionData);
      } else {
        await addRole(submissionData);
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
    router.push('/dashboard/roles');
  }
};

</script>

<template>
  <div>
    <h3 class="mb-3">{{ isEditMode ? 'Editar Função' : 'Adicionar Nova Função' }}</h3>
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
          <div v-if="isEditMode" class="font-semibold text-xl">ID Função:</div>
          <InputText v-if="isEditMode" :model-value="route.query.id as string" type="text" disabled fluid/>

          <div class="font-semibold text-xl">Nome*</div>
          <InputText name="role_name" type="text" placeholder="Introduza nome da função" fluid/>
          <Message v-if="$form.role_name?.invalid" severity="error" size="small" variant="simple">
            {{ $form.role_name.error.message }}
          </Message>

          <div class="font-semibold text-xl">Cor*</div>
          <InputText type="text" name="hex_color" hidden />
          <ClientOnly>
            <ColorPicker name="hex_color" format="hex" fluid :default-color="$form.hex_color?.value"/>
          </ClientOnly>
          <Message v-if="$form.hex_color?.invalid" severity="error" size="small" variant="simple">
            {{ $form.hex_color.error.message }}
          </Message>

          <div class="font-semibold text-xl">Descrição*</div>
          <Textarea name="description" placeholder="Introduza descrição da função" :autoResize="true" rows="3" fluid/>
          <Message v-if="$form.description?.invalid" severity="error" size="small" variant="simple">
            {{ $form.description.error.message }}
          </Message>

          <div class="font-semibold text-xl">Treinamentos</div>
          <MultiSelect 
            name="training_type" 
            :options="trainingTypes" 
            optionLabel="name" 
            optionValue="id_training_type" 
            placeholder="Selecione os treinamentos" 
            display="chip" 
            fluid
          />
          <Message v-if="$form.training_type?.invalid" severity="error" size="small" variant="simple">
            {{ $form.training_type.error.message }}	
          </Message>

          <div class="font-semibold text-xl">Grupo do utilizador (Permissões)</div>
          <Select name="auth_group" optionValue="id" :options="authGroups?.auth_groups" optionLabel="name" placeholder="Selecione grupo" fluid />
          <Message v-if="$form.auth_group?.invalid" severity="error" size="small" variant="simple">
            {{ $form.auth_group.error.message }}
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