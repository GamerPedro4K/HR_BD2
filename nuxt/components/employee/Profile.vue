<script setup lang="ts">
import { formatDate } from "~/utils/date";
import type { FindEmployee } from "~/types/employee";
import DataTable from "primevue/datatable";
import Column from "primevue/column";

const props = defineProps({
  json: {
    type: Object as PropType<FindEmployee>,
    required: true,
    default: () => ({}),
  },
});

const { json } = props;
const rows = 5; 
const totalRecords = json.trainings.length; 


</script>

<template>
  <Tabs value="0">
    <TabList>
      <Tab value="0">Informações pessoais</Tab>
      <Tab value="1">Trainamentos</Tab>
      <Tab value="2">Certificados</Tab>
    </TabList>
    <TabPanels>
      <TabPanel value="0">
        <div class="grid grid-cols-2 gap-4">
          <div class="p-2 w-[400px]">
            <div class="text-gray-400 dark:text-gray-500 text-md">Nome Completo</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.employee_name }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Telefone</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.phone }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Email</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.email }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Data de Nascimento</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ formatDate(json.birth_date) }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Data de Registo</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ formatDate(json.date_joined) }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Cargo</div>
            <div class="flex items-center space-x-2 text-[18px] mt-[12px]">
              <Tag :style="{ backgroundColor: json.contract.role.hex_color }" :value="json.contract.role.role_name"></Tag>
            </div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Departamento</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.contract.department.department_name }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Estado</div>
            <div class="flex items-center space-x-2 text-[18px] mt-[12px]">
              <Tag :style="{ backgroundColor: json.contract.contract_state.hex_color }" :value="json.contract.contract_state.state_name"></Tag>
              <font-awesome :icon="json.contract.contract_state.icon" class="f-size-22 m-1" />
            </div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Salário Base</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.contract.salary.base_salary }} EUR</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Cidade</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.location.city }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Endereço</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.location.address }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">Código Postal</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.location.zip_code }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 dark:text-gray-500 text-md">País</div>
            <div class="text-gray-900 dark:text-gray-100 text-[18px] mt-[12px]">{{ json.location.country }}</div>
            <hr class="border-gray-200 dark:border-gray-700" />
          </div>
        </div>
      </TabPanel>
       <TabPanel value="1">
        <div v-if="json.trainings.length > 0">
          <DataTable 
            :value="json.trainings"
            paginator
            :rows="rows"
            :totalRecords="totalRecords"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5, 10, 25, 50, 100]"
            class="shadow-md rounded-lg w-[100%]"
          >
            <Column field="training_type.training_type_name" header="Tipo de Treinamento" sortable/>
            <Column field="training_type.description" header="Descrição" sortable/>
            <Column field="training_type.hours" header="Duração (horas)" sortable/>
            <Column 
                header="Período" 
                field="start_date" 
                :sortable="true">
                <template #body="slotProps">
                  {{ formatDate(slotProps.data.start_date) }} - {{ formatDate(slotProps.data.end_date) }}
                </template>
            </Column>
          </DataTable>
        </div>
        <div v-else class="text-center text-gray-500 dark:text-gray-300">
          Nenhum treinamento encontrado.
        </div>
      </TabPanel>
      <TabPanel value="2">
        <div v-if="json.certifications.length > 0">
          <DataTable 
            :value="json.certifications"
            paginator
            :rows="5"
            :totalRecords="json.certifications.length"
            class="shadow-md rounded-lg w-[100%]"
          >
            <Column field="certificate_type.certificate_type_name" header="Certificado" sortable />
            <Column field="issuing_organization" header="Organização Emitente" sortable />
            <Column field="issue_date" header="Período de Validade" sortable>
              <template #body="slotProps">
                {{ formatDate(slotProps.data.issue_date) }} - {{ formatDate(slotProps.data.expiration_date) }}
              </template>
            </Column>
          </DataTable>
        </div>
        <div v-else class="text-center text-gray-500 dark:text-gray-300">
          Nenhum certificado encontrado.
        </div>
      </TabPanel>
    </TabPanels>
  </Tabs>
</template>
