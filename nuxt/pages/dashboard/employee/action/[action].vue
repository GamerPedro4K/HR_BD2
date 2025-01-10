<script setup lang="ts">
import { ref } from 'vue';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import { CountryService, type Country } from '~/service/CountryService';
import {ScheduleXCalendar} from "@schedule-x/vue";
import { createCalendar, viewMonthGrid } from '@schedule-x/calendar'
import '@schedule-x/theme-default/dist/index.css'
import {createResizePlugin} from "@schedule-x/resize";
import {createEventModalPlugin} from "@schedule-x/event-modal";
import {createScrollControllerPlugin} from "@schedule-x/scroll-controller";
import {createEventsServicePlugin} from "@schedule-x/events-service";
import { useLayout } from '~/layouts/composables/layout';
import type { Vacation } from '~/types/vacation';
import type { CalendarApp } from '@schedule-x/calendar';
import type { ContractType } from '~/types/contractType';
import type { Department, DepartmentListResponse } from '~/types/department';
import type { Role } from '~/types/roles';
import type { ContractState } from '~/types/contractState';
import type { EmployeeSubmission, FindEmployee } from '~/types/employee';
import { formatDateRequest } from '~/utils/date';
import type { SalaryHistory } from '~/types/salary';

const { isDarkTheme } = useLayout();
// # Declare variables
const formRef = ref<any>(null);
const countries = ref<Country[]>([]);
const calendarApp = shallowRef<CalendarApp | null>(null);
const certifications = ref<any>([]);
const training = ref<{ name: string; id_training_type: string; hours: number; description: string; start_date: Date | undefined; end_date: Date | undefined }[]>([]);
const vacations = ref<any>();
const contractType = ref<ContractType[]>();
const departments = ref<DepartmentListResponse>();
const departmentsList = ref<any>([]);
const trainingsNotDoneList = ref<any>([]);
const selectedContractType = ref<ContractType | null>(null);
const selectedContractState = ref<ContractState | null>(null);
const selectedDates = ref();
const contractStates = ref<ContractState[]>([]);

// # Declare variables for vacation Dialog
const visibleVacation = ref(false);

// # Declare editVariables
const responseEmployee = ref<FindEmployee | null>();
const responseSalary = ref<SalaryHistory | null>();


const testes = ref<any>();



// # Declare functions
const route = useRoute();
const router = useRouter();
const { getCertificationsType } = useCertification();
const { getTrainingType } = useTraining();
const { getAllVacations } = useVacations();
const { getContractTypes } = useContractType();
const { getDepartments } = useDepartment();
const { getContractStates } = useContractState();
const { addEmployee, editEmployee, getEmployee } = useEmployee()
const { getSalaryHistory } = useSalaryHistory();

// Check if the page is in edit mode
const isEditMode = (route.params.action === 'edit');

// # Get data functions
CountryService.getCountries().then((data) => (countries.value = data));

const getCertifications = async () => {
    const response = await getCertificationsType();
    certifications.value = response.certificate_types;
};

const getTrainings = async () => {
    const response = await getTrainingType();
    response.training_types.forEach(element => {
      training.value.push({ name: element.name, id_training_type: element.id_training_type, hours: element.hours, description: element.description, start_date: undefined, end_date: undefined,});
    });
};

const getVacations = async () => {
    const response = await getAllVacations();
    vacations.value = response.vacations.map((vacation: Vacation) => ({ 
      id: vacation.id_vacation, 
      title: 'Férias do ' + vacation.employee_name,
      people: [vacation.employee_name],
      start: vacation.start_date,
      end: vacation.end_date,
      calendarId: 'leisure'
    }));

    // Tenta imediatamente atualizar o calendário, caso já esteja inicializado
    if (calendarApp.value) {
      calendarApp.value.events.set(vacations.value);
    }
};

const getContract = async () => {
    const response = await getContractTypes({});
    contractType.value = response.contract_types;
};

const getDepartment = async () => {
    const response = await getDepartments();
    departmentsList.value = response.departments.map((department) => ({
      label: department.name,
      code: department.id_department,

      items: department.roles.map((role) => ({
        label: role.role_name,
        value: role.id_role,
      })),
    }));
    departments.value = response;
};

const getContractState = async () => {
    const response = await getContractStates();
    contractStates.value = response.contract_states;
};

// Initialize the form
const initialValues = ref<any>({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  phone: '',
  img_src: '',
  birth_date: null,
  selected_country: { code: 'PT', name: 'Portugal' },
  street: '',
  zip_code: '',
  city: '',
  district: '',
  treinamentos: [],
  certificados: [],
  vacations: [],
  role: {},
  contract_type: {},
  contract_state: {},
  base_salary: 0,
  extra_hour_rate: 0,
  start_date: new Date()
});

const getEmployeeOnEdit = async () => {
  if (!isEditMode) {
    return;
  }
  try {
    responseEmployee.value = await getEmployee(route.query.id as string);
    responseSalary.value = await getSalaryHistory(route.query.id as string);
    if (responseEmployee.value) {
      initialValues.value = {
        email: responseEmployee.value.email || '',
        password: '',
        first_name: responseEmployee.value.employee_name.split(' ')[0] || '',
        last_name: responseEmployee.value.employee_name.split(' ')[1] || '',
        phone: responseEmployee.value.phone || '',
        img_src: responseEmployee.value.photo || '',
        birth_date: new Date(responseEmployee.value.birth_date),
        selected_country: {
          code: responseEmployee.value?.location?.country || 'PT',
          name: countries.value.find(c => c.code === responseEmployee.value?.location?.country)?.name || 'Portugal',
        },
        street: responseEmployee.value.location.address || '',
        zip_code: responseEmployee.value.location.zip_code || '',
        city: responseEmployee.value.location.city || '',
        district: responseEmployee.value.location.district || '',
        treinamentos: responseEmployee.value.trainings.map(t => ({
          id_training_type: t.id_training,
          start_date: new Date(t.start_date),
          end_date: new Date(t.end_date),
        })),
        certificados: responseEmployee.value.certifications.map((c) => ({
          id_certificate_type: c.id_certification,
          name: c.certificate_type.certificate_type_name,
          description: c.certificate_type.description,
          issuing_organization: c.issuing_organization,
          issue_date: c.issue_date,
          expiration_date: c.expiration_date,
        })),
        /* vacations: vacations.value.filter((v: { employee_id: any; }) => v.employee_id === responseEmployee.value.id), */
        role: {
          value: responseEmployee.value.contract.role.id_role,
          label: responseEmployee.value.contract.role.role_name,
        },
        contract_type: {
          ...responseEmployee.value.contract.contract_type,
        },
        contract_state: {
          ...responseEmployee.value.contract.contract_state,
        },
        base_salary: responseEmployee.value.contract.salary.base_salary,
        extra_hour_rate: responseEmployee.value.contract.salary.extra_hour_rate,
        start_date: new Date(responseEmployee.value.contract.salary.start_date) || new Date(),
      };
      selectedContractType.value = contractType.value?.find((c) => c.id_contract_type === responseEmployee.value?.contract.contract_type.id_contract_type) || null;
      selectedContractState.value = contractStates.value.find((c) => c.id_contract_state === responseEmployee.value?.contract.contract_state.id_contract_state) || null;
      /* testes.value = responseEmployee.value.certifications.map((c) => ({
        id_certificate_type: c.id_certification,
        name: c.certificate_type.certificate_type_name,
        description: c.certificate_type.description,
        issuing_organization: c.issuing_organization,
        issue_date: c.issue_date,
        expiration_date: c.expiration_date,
      })); */
    }
  } catch (error) {
    console.log('Erro ao buscar dados do funcionário:', error);
    console.error('Erro ao buscar dados do funcionário:', error);
  }
};


// # Get data
await getCertifications();
await getTrainings();
await getVacations();
await getContract();
await getDepartment();
await getContractState();
await getEmployeeOnEdit()


// Breadcrumbs setup
const { breadcrumbs, home, updateLastBreadcrumbLabel } = useBreadcrumb();
updateLastBreadcrumbLabel(isEditMode ? 'Editar Funcionário' : 'Adicionar Funcionário');



// Define Zod Schema
const schema = z.object({
  first_name: z.string().min(1, 'Primeiro nome é obrigatório'),
  last_name: z.string().min(1, 'Último nome é obrigatório'),
  email: z.string().email('E-mail inválido').min(1, 'E-mail é obrigatório'),
  password: z.string().min(6, 'Password deve ter no mínimo 6 caracteres'),
  phone: z.string().min(9, 'Telefone inválido'),
  img_src: z.string().url('URL da imagem inválida'),
  birth_date: z
    .date({ message: 'Data de nascimento inválida' })
    .refine((date) => date <= new Date(), 'Data de nascimento não pode ser futura'),
  street: z.string().min(1, 'A morada é obrigatória'),
  zip_code: z.string().min(1, 'O código postal é obrigatório'),
  city: z.string().min(1, 'A cidade é obrigatória'),
  district: z.string().min(1, 'O distrito é obrigatório'),
  selected_country: z
    .object({
      code: z.string().min(1),
      name: z.string().min(1),
    })
    .refine((val) => val.code && val.name, 'O país é obrigatório'),
  treinamentos: z.array(
    z.object({
      start_date: z.date({ required_error: 'Verifique as datas dos treinamentos' }),
      end_date: z.date({ required_error: 'Verifique as datas dos treinamentos' }),
      id_training_type: z.string().min(1, 'Tipo de treinamento é obrigatório'),
    })
  ),
  certificados: z
  .array(
    z.object({
      id_certificate_type: z.string().min(1, 'O código é obrigatório'),
      name: z.string().min(1, 'O nome é obrigatório'),
      issuing_organization: z.string().min(1, 'A organização emissora é obrigatória'),
      issue_date: z.date({ message: 'Data de emissão inválida' }),
      expiration_date: z.date({ message: 'Data de expiração inválida' }).optional(),
    })
  )
  .optional(),
  vacations: z.any(),
  role: z.object({
    value: z.string({ required_error: 'O tipo de contrato é obrigatório' }),
  }),
  contract_type: z.object({
    id_contract_type: z.string({ required_error: 'O tipo de contrato é obrigatório' }),
  }),
  contract_state: z.object({
    id_contract_state: z.string({ required_error: 'O estado do contrato é obrigatório' }),
  }),
  base_salary: z.number().min(0, 'Salário base inválido'),
  extra_hour_rate: z.number().min(0, 'Valor por hora extra inválido'),
  start_date: z.date({ message: 'Data de início inválida' }).refine((date) => date <= new Date(), 'Data de início não pode ser futura'),
});


const resolver = ref(zodResolver(schema));

const onSubmit = (all: any) => {
  console.log(toRaw(all))
  const hasErrors = all.errors && Object.keys(all.errors).some((key) => all.errors[key]?.length > 0);
  if(!hasErrors){
    const { values } = toRaw(all);
    const submissionData: EmployeeSubmission = {
      employee: {
        username: values.email,
        password: values.password,
        first_name: values.first_name,
        last_name: values.last_name,
        email: values.email,
        phone: values.phone,
        img_src: values.img_src,
        birth_date: formatDateRequest(values.birth_date), // Format birth_date
        id_group: 1,
      },
      employee_address: {
        street: values.street,
        zip_code: values.zip_code,
        city: values.city,
        district: values.district,
        country: values.selected_country?.code,
      },
      trainings: values.treinamentos?.map((training: any) => ({
        start_date: formatDateRequest(training.start_date),
        end_date: formatDateRequest(training.end_date),
        id_training_type: training.id_training_type,
      })) || [],
      certificates: values.certificados?.map((certificate: any) => ({
        id_certificate_type: certificate.id_certificate_type,
        name: certificate.name,
        issuing_organization: certificate.issuing_organization,
        issue_date: formatDateRequest(certificate.issue_date),
        expiration_date: formatDateRequest(certificate.expiration_date),
      })) || [],
      vacations: {
        start_date: formatDateRequest(values.vacations[0]),
        end_date: formatDateRequest(values.vacations[1]),
      },
      salary: {
        base_salary: values.base_salary,
        extra_hour_rate: values.extra_hour_rate,
        start_date: formatDateRequest(values.start_date),
      },
      contract: {
        id_contract_type: values.contract_type?.id_contract_type || null,
        id_contract_state: values.contract_state?.id_contract_state || null,
        id_role: values.role?.value,
      },
    };

    console.log("Formulário submetido:", submissionData);
    const response = addEmployee(submissionData);
  }
};

// Watch para sincronizar férias quando `calendarApp` estiver pronto
watch(calendarApp, (newCalendar) => {
  if (newCalendar && vacations.value.length > 0) {
    newCalendar.events.set(vacations.value);
  }
});

const onChangeVacation = (value: any) => {
  if (calendarApp.value && value.length === 2 && value[0] && value[1]) {
    calendarApp.value.events.set([
      ...vacations.value,
      { 
        id: 1, 
        title: 'Férias do Novo Funcionário', 
        start: value[0].toISOString().split('T')[0],
        end: value[1].toISOString().split('T')[0],
        people: ['Novo Funcionário'],
      }
    ]);
  }
};

// Check if the role has training
const onChangeRole = () => {
  setTimeout(() => {
    trainingsNotDoneList.value = [];
    departments.value?.departments.forEach((department: Department) => {
        department.roles.forEach((role:Role) => {
          if (role.id_role === formRef.value.states.role.value.value) {
            role.training_types.forEach((training) => {
              const trainingExists = formRef.value.states.treinamentos.value.some(
              (existingTraining: any) =>
                  existingTraining.id_training_type === training.id_training_type
              );

              if (!trainingExists) {
                trainingsNotDoneList.value.push(training);
              } 

            });
          }
        });
    });
  }, 500);
};


// Watch para sincronizar o contrato selecionado no formulário
watch(selectedContractType, (newValue, oldValue) => {
  formRef.value.states.contract_type.dirty = true;
  formRef.value.states.contract_type.touched = true;
  formRef.value.states.contract_type.value = toRaw(newValue);
});

// Watch para sincronizar o estado do contrato selecionado no formulário
watch(selectedContractState, (newValue, oldValue) => {
  formRef.value.states.contract_state.dirty = true;
  formRef.value.states.contract_state.touched = true;
  formRef.value.states.contract_state.value = toRaw(newValue);
});


let eventsServicePlugin = createEventsServicePlugin();

calendarApp.value = createCalendar({
  locale: 'pt-BR',
  isDark: isDarkTheme.value,
  selectedDate: new Date().toLocaleDateString("fr-CA"),
  firstDayOfWeek: 1,
  minDate: new Date().toLocaleDateString("fr-CA"),
  views: [viewMonthGrid],
  defaultView: viewMonthGrid.name,
  plugins: [
      createResizePlugin(),
      createScrollControllerPlugin({
        initialScroll: '08:00'
      }),
      createEventModalPlugin(),
      eventsServicePlugin,
  ],
  isResponsive: false,
  events: [],
  calendars: {
    work: {
      colorName: 'work',
      lightColors: {
        container: '#fff',
        onContainer: '#000',
        main: '#fff',
      },
      darkColors: {
        container: '#000',
        onContainer: '#fff',
        main: '#000',
      },
    },
    leisure: {
      colorName: 'leisure',
      lightColors: {
        main: '#1c7df9',
        container: '#d2e7ff',
        onContainer: '#002859',
      },
      darkColors: {
        main: '#c0dfff',
        onContainer: '#dee6ff',
        container: '#426aa2',
      },
    },
  }
});

</script>

<style>
.p-password-input {
  width: 100%;
}

.sx-vue-calendar-wrapper {
  height: 1000px;
  width: 100%;
}
</style>



<template>
  <h3 class="mb-3" v-if="!isEditMode">Adicionar Novo Funcionário</h3>
  <h3 class="mb-3" v-else>Editar Funcionário</h3>
  <BreadcrumbCustom :home="home" :breadcrumbs="breadcrumbs" />
  <div class="card mt-5">
    <Form ref="formRef" v-slot="$form" :resolver="resolver" :initialValues="initialValues" @submit="onSubmit" class="w-full">
      <Stepper value="1" class="w-full">
        <StepList>
          <Step value="1">Dados Pessoais</Step>
          <Step value="2">Morada</Step>
          <Step value="3">Empresa</Step>
          <Step value="4">Contrato</Step>
          <Step value="5">Férias</Step>
        </StepList>
        <StepPanels>
          <!-- Step 1: Personal Data -->
          <StepPanel v-slot="{ activateCallback }" value="1">
            <div class="card flex justify-center">
              <div class="flex flex-col gap-4 w-full">
                <div v-if="isEditMode" class="font-semibold text-xl">ID Funcionário:</div>
                <InputText
                  v-if="isEditMode"
                  name="id_employee"
                  type="text"
                  :placeholder="route.query.id as string || 'ID do Funcionário'"
                  disabled
                  fluid
                />

                <div class="font-semibold text-xl">Nome do Funcionário*</div>
                <InputText
                  v-keyfilter.alpha
                  name="first_name"
                  type="text"
                  placeholder="Introduza o Primeiro Nome"
                  fluid
                />
                <Message v-if="$form.first_name?.invalid" severity="error" size="small" variant="simple">{{ $form.first_name.error.message }}</Message>

                <InputText
                  v-keyfilter.alpha
                  name="last_name"
                  type="text"
                  placeholder="Introduza o Último Nome"
                  fluid
                />
                <Message v-if="$form.last_name?.invalid" severity="error" size="small" variant="simple">{{ $form.last_name.error.message }}</Message>

                <div class="font-semibold text-xl">Email*</div>
                <InputText
                  name="email"
                  type="email"
                  placeholder="Introduza o Email"
                  fluid
                />
                <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple">{{ $form.email.error.message }}</Message>

                <div class="font-semibold text-xl">Password*</div>
                <Password
                  name="password"
                  placeholder="Introduza a Password"
                  toggleMask
                  fluid
                ><template #header>
                    <div class="font-semibold text-xm mb-4">Escolha uma password</div>
                  </template>
                  <template #footer>
                    <Divider />
                    <ul class="pl-2 ml-2 my-0 leading-normal">
                      <li>Minimo de 6 caracteres.</li>
                    </ul>
                  </template>
                </Password>
                <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple">{{ $form.password.error.message }}</Message>

                <div class="font-semibold text-xl">Telefone*</div>
                <InputMask
                  name="phone"
                  mask="999 999 999"
                  placeholder="Introduza o Telefone"
                  fluid
                />
                <Message v-if="$form.phone?.invalid" severity="error" size="small" variant="simple">{{ $form.phone.error.message }}</Message>

                <div class="font-semibold text-xl">Imagem de Perfil*</div>
                <InputText
                  name="img_src"
                  type="text"
                  placeholder="Introduza a URL da Imagem de Perfil"
                  fluid
                />
                <Message v-if="$form.img_src?.invalid" severity="error" size="small" variant="simple">{{ $form.img_src.error.message }}</Message>
                <div v-if="!$form.img_src?.invalid && $form.img_src?.touched || isEditMode" class="flex justify-center pt-4">
                  <img
                    :src="$form.img_src?.value"
                    alt="Imagem de Perfil"
                    class="max-h-40 rounded-md shadow-md"
                  />
                </div>

                <div class="font-semibold text-xl">Data de Nascimento*</div>
                <DatePicker
                  name="birth_date"
                  placeholder="Introduza a Data de Nascimento"
                  dateFormat="dd-mm-yy"
                  fluid
                />
                <Message v-if="$form.birth_date?.invalid" severity="error" size="small" variant="simple">{{ $form.birth_date.error.message }}</Message>

                <div class="text-sm text-gray-500 pt-2">
                  Os campos marcados com <span class="text-red-500">*</span> são obrigatórios.
                </div>

                <div class="flex justify-end pt-4">
                  <Button label="Próximo" icon="pi pi-arrow-right" iconPos="right" @click="activateCallback('2')" />
                </div>
              </div>
            </div>
          </StepPanel>

          <!-- Step 2: Address -->
          <StepPanel v-slot="{ activateCallback }" value="2">  
            <div class="card flex justify-center">
              <div class="flex flex-col gap-4 w-full">
                <div class="font-semibold text-xl">Morada*</div>

                <InputText
                  name="street"
                  type="text"
                  placeholder="Introduza a Morada"
                  fluid
                />
                <Message v-if="$form.street?.invalid" severity="error" size="small" variant="simple">{{ $form.street.error.message }}</Message>

                <div class="font-semibold text-xl">Código Postal*</div>
                <InputText
                  name="zip_code"
                  type="text"
                  placeholder="Introduza o Código Postal"
                  fluid
                />
                <Message v-if="$form.zip_code?.invalid" severity="error" size="small" variant="simple">{{ $form.zip_code.error.message }}</Message>

                <div class="font-semibold text-xl">Cidade*</div>
                <InputText
                  v-keyfilter.alpha
                  name="city"
                  type="text"
                  placeholder="Introduza a Cidade"
                  fluid
                />
                <Message v-if="$form.city?.invalid" severity="error" size="small" variant="simple">{{ $form.city.error.message }}</Message>

                <div class="font-semibold text-xl">Distrito*</div>
                <InputText
                  v-keyfilter.alpha
                  name="district"
                  type="text"
                  placeholder="Introduza o Distrito"
                  fluid
                />
                <Message v-if="$form.district?.invalid" severity="error" size="small" variant="simple">{{ $form.district.error.message }}</Message>

                <div class="font-semibold text-xl">País*</div>
                <Select
                  name="selected_country"
                  :options="countries"
                  filter
                  optionLabel="name"
                  placeholder="Selecione um País"
                >
                  <template #value="slotProps">
                    <div v-if="slotProps.value" class="flex items-center-center">
                      <img
                        :alt="slotProps.value.label"
                        :src="`https://cdn.jsdelivr.net/gh/hampusborgos/country-flags@main/svg/${slotProps.value.code.toLowerCase()}.svg`"
                        :class="`mr-2 flag flag-${slotProps.value.code.toLowerCase()}`"
                        style="width: 18px"
                      />
                      <div>{{ slotProps.value.name }}</div>
                    </div>
                    <span v-else>{{ slotProps.placeholder }}</span>
                  </template>
                  <template #option="slotProps">
                    <div class="flex items-center">
                      <img
                        :alt="slotProps.option.label"
                        :src="`https://cdn.jsdelivr.net/gh/hampusborgos/country-flags@main/svg/${slotProps.option.code.toLowerCase()}.svg`"
                        :class="`mr-2 flag flag-${slotProps.option.code.toLowerCase()}`"
                        style="width: 18px"
                      />
                      <div>{{ slotProps.option.name }}</div>
                    </div>
                  </template>
                </Select>
                <Message v-if="$form.selected_country?.invalid" severity="error" size="small" variant="simple">{{ $form.selected_country.error.message }}</Message>

                <div class="text-sm text-gray-500 pt-2">
                  Os campos marcados com <span class="text-red-500">*</span> são obrigatórios.
                </div>

                <div class="flex pt-6 justify-between">
                  <Button label="Voltar" severity="secondary" icon="pi pi-arrow-left" @click="activateCallback('1')" />
                  <Button label="Próximo" icon="pi pi-arrow-right" iconPos="right" @click="activateCallback('3')" />
                </div>
              </div>
            </div>
          </StepPanel>

          <!-- Step 3: Company -->
          <StepPanel v-slot="{ activateCallback }" value="3">
            <div class="card flex justify-center">
              <div class="flex flex-col gap-4 w-full">
                {{ certifications }}
                <div class="font-semibold text-xl">Certificados</div>
                <MultiSelect 
                :model-value="$form.certificados?.value"
                  name="certificados" 
                  :options="certifications" 
                  optionLabel="name" 
                  filter 
                  placeholder="Selecionar Certificados" 
                  fluid
                  :loading="certifications.length === 0" 
                />
                {{ $form.certificados?.value }}
                <Message v-if="$form.certificados?.invalid" severity="error" size="small" variant="simple">{{ $form.certificados?.error?.message }}</Message>

                <div v-for="(item, index) in $form.certificados?.value":key="index">
                  <div class="card training-card-padding" style="background-color: var(--surface-ground);">
                    <div class="flex mb-1">
                      <div class="font-semibold text-xl">{{ item.name }}</div>
                      <div class="text-sm ml-auto rounded-lg p-2 text-white" style="background-color: var(--primary-color);">
                        {{ item }}
                       <!--  <font-awesome :icon="item.data.icon" :style="{ color: slotProps.data.hex_color }" class="f-size-22 mr-4" /> -->
                      </div>
                    </div>
                    <div class="text-sm mb-3">{{ item.description }}</div>
                    <div class="font-semibold text-sm mb-2">Organização Emissora</div>
                    <InputText
                      v-model="item.issuing_organization"
                      type="text"
                      placeholder="Introduza a Organização Emissora"
                      fluid
                    />
                    <div class="font-semibold text-sm mb-2 mt-1">Data Emitida*</div>
                    <DatePicker
                      v-model="item.issue_date"
                      placeholder="Introduza a data de emissão"
                      dateFormat="dd-mm-yy"
                      fluid
                      :max-date="new Date()"
                    />
                    <div class="font-semibold text-sm mb-2 mt-1">Data Expiração</div>
                    <DatePicker
                      v-model="item.expiration_date"
                      placeholder="Introduza a Data de Expiração"
                      dateFormat="dd-mm-yy"
                      fluid
                      :min-date="new Date()"
                    />
                    <div class="flex justify-end pt-4">
                      <Button label="Remover" icon="pi pi-times" severity="danger"  @click="$form.certificados?.value.splice(index, 1);"  />
                    </div>                     
                  </div>
                </div>


                <div class="font-semibold text-xl">Treinamentos</div>
                <MultiSelect 
                  name="treinamentos" 
                  :options="training" 
                  optionLabel="name" 
                  filter 
                  placeholder="Selecionar Treinamentos" 
                  fluid
                  :loading="certifications.length === 0" 
                  @update:modelValue="onChangeRole()"
                />
                <Message v-if="$form.treinamentos?.invalid" severity="error" size="small" variant="simple">{{ $form.treinamentos?.error?.message }}</Message>

                <div v-for="(item, index) in $form.treinamentos?.value":key="index">
                  <div class="card training-card-padding" style="background-color: var(--surface-ground);">
                    <div class="flex mb-1">
                      <div class="font-semibold text-xl">{{ item.name }}</div>
                      <div class="text-sm ml-auto rounded-lg p-2 text-white" style="background-color: var(--primary-color);">{{ item.hours }} Horas</div>
                    </div>
                    <div class="text-sm mb-3">{{ item.description }}</div>
                    <div class="font-semibold text-sm mb-2">Data de Início*</div>
                    <DatePicker
                      v-model="item.start_date"
                      placeholder="Introduza a Data de Início"
                      dateFormat="dd-mm-yy"
                      fluid
                      :max-date="item.end_date"
                    />
                    <div class="font-semibold text-sm mb-2 mt-1">Data de Fim*</div>
                    <DatePicker
                      v-model="item.end_date"
                      placeholder="Introduza a Data de Fim"
                      dateFormat="dd-mm-yy"
                      fluid
                      :min-date="item.start_date"
                    />
                    <div class="flex justify-end pt-4">
                      <Button label="Remover" icon="pi pi-times" severity="danger"  @click="$form.treinamentos?.value.splice(index, 1); onChangeRole()"  />
                    </div>                     
                  </div>
                </div>

                <div class="text-sm text-gray-500 pt-2">
                  Os campos marcados com <span class="text-red-500">*</span> são obrigatórios.
                </div>

                <div class="flex pt-6 justify-between">
                  <Button label="Voltar" severity="secondary" icon="pi pi-arrow-left" @click="activateCallback('2')" />
                  <Button label="Próximo" icon="pi pi-arrow-right" iconPos="right" @click="activateCallback('4')" />
                </div>
              </div>
            </div>
          </StepPanel>

          <!-- Step 4: Contract -->
          <StepPanel v-slot="{ activateCallback }" value="4">
            <div class="card flex justify-center">
              <div class="flex flex-col w-full">
                <div class="flex flex-col gap-4 mb-12">
                  <div class="font-semibold text-xl">Salário Base*</div>
                  <InputNumber name="base_salary" mode="currency" currency="EUR" locale="de-DE" placeholder="Introduza o Salário Base" :min="0"  fluid/>
                  <Message v-if="$form.base_salary?.invalid" severity="error" size="small" variant="simple">{{ $form.base_salary.error.message }}</Message>
                  
                  <div class="font-semibold text-xl">Valor por Hora Extra*</div>
                  <InputNumber name="extra_hour_rate" mode="currency" currency="EUR" locale="de-DE" placeholder="Introduza o Valor por Hora Extra" :min="0"  fluid/>
                  <Message v-if="$form.extra_hour_rate?.invalid" severity="error" size="small" variant="simple">{{ $form.extra_hour_rate.error.message }}</Message>

                  <div class="font-semibold text-xl">Data de Início*</div>
                  <DatePicker name="start_date" placeholder="Introduza a Data de Início" dateFormat="dd-mm-yy" fluid :min-date="new Date()" />
                  <Message v-if="$form.start_date?.invalid" severity="error" size="small" variant="simple">{{ $form.start_date.error.message }}</Message>
                  
                  <div v-if="isEditMode" class="card training-card-padding" >
                    <div class="font-semibold text-xl">Histórico de Salários</div>
                    <DataTable 
                      :value="responseSalary" 
                      dataKey="id_salary_history" 
                      tableStyle="min-width: 50rem" 
                      scrollable 
                      scrollHeight="500px"
                    >
                      <Column header="ID Contrato"  :exportable="false">
                        <template #body="slotProps">
                            <CopyToClipboardButton :textToCopy="slotProps.data.id_contract"/>
                        </template>
                      </Column>
                      <Column field="base_salary" header="Salário">.
                        <template #body="slotProps">
                          {{ slotProps.data.base_salary }} €
                        </template>
                      </Column>
                      <Column field="extra_hour_rate" header="Hora Extra">.
                        <template #body="slotProps">
                          {{ slotProps.data.extra_hour_rate }} €
                        </template>
                      </Column>
                      <Column field="start_date" header="Data Início"></Column>
                      <Column field="benefits_eligible" header="Apróvado Por">
                        <template #body="slotProps">
                          <NuxtLink :to="`/dashboard/employee/${slotProps.data.id_employee_aproved_by}`" target="_blank">
                            <Button icon="pi pi-search" variant="text" raised rounded/>
                          </NuxtLink>
                        </template>
                      </Column>
                    </DataTable>
                  </div>

                </div>

                <div class="font-semibold text-xl">Tipo de Contrato*</div>
                <InputText name="contract_type" type="text" class="hidden" /><!-- DONT REMOVE IMPORTANT IN ORDER TO form.contract_type WORK -->
                <DataTable 
                  :value="contractType" 
                  dataKey="id_contract_type" 
                  tableStyle="min-width: 50rem" 
                  scrollable 
                  scrollHeight="500px" 
                  v-model:selection="selectedContractType"
                >
                  <Column selectionMode="single" headerStyle="width: 3rem" ></Column>
                  <Column field="contract_type_name" header="Nome"></Column>
                  <Column field="description" header="Descrição"></Column>
                  <Column field="termination_notice_period" header="Período de aviso de rescisão">.
                    <template #body="slotProps">
                      {{ slotProps.data.termination_notice_period }} dias
                    </template>
                  </Column>
                  <Column field="overtime_eligible" header="Overtime">
                    <template #body="slotProps">
                      <i v-if="slotProps.data.overtime_eligible" class="pi pi-check p-2 rounded-full text-white dark:text-black" style="background-color: var(--primary-color);"></i>
                      <i v-else class="pi pi-times p-2 rounded-full text-white dark:text-black" style="background-color: var(--p-button-danger-background);"></i>
                    </template>
                  </Column>
                  <Column field="benefits_eligible" header="Benefícios">
                    <template #body="slotProps">
                      <i v-if="slotProps.data.benefits_eligible" class="pi pi-check p-2 rounded-full text-white dark:text-black" style="background-color: var(--primary-color);"></i>
                      <i v-else class="pi pi-times p-2 rounded-full text-white dark:text-black" style="background-color: var(--p-button-danger-background);"></i>
                    </template>
                  </Column>
                </DataTable>
                <Message v-if="$form.contract_type?.invalid" severity="error" size="large" variant="simple">{{ $form.contract_type.error.message }}</Message>

                <div class="font-semibold text-xl mt-12">Estado do Contrato*</div>
                <InputText name="contract_state" type="text" class="hidden" /><!-- DONT REMOVE IMPORTANT IN ORDER TO form.contract_state WORK -->
                <DataTable 
                  :value="contractStates" 
                  dataKey="id_contract_state" 
                  tableStyle="min-width: 50rem" 
                  scrollable 
                  scrollHeight="500px" 
                  v-model:selection="selectedContractState"
                >
                  <Column selectionMode="single" headerStyle="width: 3rem" ></Column>
                  <Column field="benefits_eligible" header="Nome">
                    <template #body="slotProps" >
                      <div class="flex items-center">
                        <font-awesome :icon="slotProps.data.icon" :style="{ color: slotProps.data.hex_color }" class="f-size-22 mr-4" />
                        <span class="f-weight-500">
                          {{ slotProps.data.state }}
                        </span>
                      </div>
                    </template>
                  </Column>
                  <Column field="description" header="Descrição"></Column>
                </DataTable>
                <Message v-if="$form.contract_state?.invalid" severity="error" size="large" variant="simple">{{ $form.contract_state.error.message }}</Message>


                <div class="font-semibold text-xl mt-12">Cargo na empresa*</div>
                <Select 
                  :options="departmentsList" 
                  optionLabel="label" 
                  optionGroupLabel="label" 
                  optionGroupChildren="items" 
                  placeholder="Selecionar Cargo" 
                  class="w-full" 
                  name="role"
                  @update:modelValue="onChangeRole"
                  filter
                >
                  <template #optiongroup="slotProps">
                      <div class="flex items-center">
                          <div style="background-color: var(--primary-color); width: 12px; height: 12px; border-radius: 12px; margin-right: 10px;"></div>
                          <div>{{ slotProps.option.label }}</div>
                      </div>
                  </template>
                </Select>
                <Message v-if="$form.role?.invalid" severity="error" size="small" variant="simple">{{ $form.role.error.message }}</Message>

                <div v-if="trainingsNotDoneList.length === 0">Não existem treinamentos em falta</div>
                <div v-else class="card training-card-padding mt-5" style="background-color: var(--surface-ground);">
                  <div class="text-xl f-bold">Treinamentos em falta:</div>
                  <ol class="m-3">
                    <li v-for="(item, index) in trainingsNotDoneList" :key="index" class="flex items-center mb-2">
                      <img src="https://i.imgur.com/sAHJ87o.png" alt="" width="30"  class="mr-2">
                      <span class="text-lg f-bold"> - {{ item.name }}</span>
                    </li>
                  </ol>
                </div>
                
                
                <div class="text-sm text-gray-500 pt-2">
                  Os campos marcados com <span class="text-red-500">*</span> são obrigatórios.
                </div>

                <div class="flex pt-6 justify-between">
                  <Button label="Voltar" severity="secondary" icon="pi pi-arrow-left" @click="activateCallback('3')" />
                  <Button label="Próximo" icon="pi pi-arrow-right" iconPos="right" @click="activateCallback('5')" />
                </div>
              </div>
            </div>
          </StepPanel>

          <!-- Step 5: Vacations -->
          <StepPanel v-slot="{ activateCallback }" value="5">
            <div class="card flex justify-center">
              <div class="flex flex-col gap-4 w-full">
                <div class="flex justify-between items-center">
                  <div class="font-semibold text-xl">Férias:</div>
                  <Button label="Adicionar" icon="pi pi-plus" severity="success" @click="visibleVacation = true" />
                </div>
                <ClientOnly>
                      <ScheduleXCalendar v-if="calendarApp" :calendar-app="calendarApp" ></ScheduleXCalendar>
                </ClientOnly>
              </div>
            </div>

            <Dialog v-model:visible="visibleVacation" modal header="Selecionar datas*" :style="{ width: '25rem' }" >
              <div class="flex flex-col  w-full gap-4">
                <DatePicker v-model="selectedDates"  @update:modelValue="onChangeVacation" name="vacations" selectionMode="range" :manualInput="false"  inline :min-date="new Date()" :default-value="$form.vacations?.value"/>
                <Message v-if="$form.vacations?.invalid" severity="error" size="small" variant="simple">{{ $form.vacations.error.message }}</Message>
              </div>
              <div class="flex justify-end mt-4">
                  <Button type="button" label="Fechar" severity="secondary" @click="visibleVacation = false"></Button>
              </div>
            </Dialog>

            <div class="flex pt-6 justify-between">
              <Button label="Voltar" severity="secondary" icon="pi pi-arrow-left" @click="activateCallback('4')" />
              <Button type="submit" label="Submeter" icon="pi pi-check" />
            </div>
          </StepPanel>
        </StepPanels>
      </Stepper>
    </Form>
  </div>
</template>

<style>
.p-password-input {
  width: 100%;
}
.training-card-padding {
  padding: 15px !important;
}
</style>