<script setup lang="ts">
import { formatDate } from "~/utils/date";
import type { FindEmployee } from "~/types/employee";

const props = defineProps({
  json: {
    type: Object as PropType<FindEmployee>,
    required: true,
    default: () => ({}),
  },
});
</script>

<template>
  <Tabs value="0">
    <TabList>
      <Tab value="0">Informações pessoais</Tab>
    </TabList>
    <TabPanels>
      <TabPanel value="0">
        <div class="grid grid-cols-2 gap-4 ">
          <div class="p-2 w-[400px]">
            <div class="text-gray-400 text-md">Nome Completo</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.employee_name }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Telefone</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.phone }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Email</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.email }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Data de Nascimento</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ formatDate(json.birth_date) }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Data de Registo</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ formatDate(json.date_joined) }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Cargo</div>
            <div class="flex items-center space-x-2 text-[18px] mt-[12px]">
              <Tag :style="{ backgroundColor: json.role_hex_color }" :value="json.role_name"></Tag>
            </div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Departamento</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.department_name }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Estado</div>
            <div class="flex items-center space-x-2 text-[18px] mt-[12px]">
              <Tag :style="{ backgroundColor: json.state_hex_color }" :value="json.state"></Tag>
              <i :class="json.icon" class="ml-2"></i>
            </div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Salário Base</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.base_salary }} EUR</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Cidade</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.city }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Endereço</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.address }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">Código Postal</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.zip_code }}</div>
            <hr class="border-gray-200" />
          </div>
          <div class="p-2">
            <div class="text-gray-400 text-md">País</div>
            <div class="text-gray-900 text-[18px] mt-[12px]">{{ json.country }}</div>
            <hr class="border-gray-200" />
          </div>
        </div>
      </TabPanel>
    </TabPanels>
  </Tabs>
</template>
