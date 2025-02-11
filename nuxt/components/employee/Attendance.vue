<script setup lang="ts">
import { ref, onMounted } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import type { AttendanceInterfaceResponse } from '~/types/attendance';
import { format } from 'date-fns';
import { useEmployee } from '~/composables/useEmployee';
import { useRoute } from 'vue-router'; 


const route = useRoute();

const attendance = ref<AttendanceInterfaceResponse>({
    data: [],
    count: 0
});
const rows = ref(10);
const first = ref(0);

const { getEmployeeAtendance } = useEmployee();  

const loadAttendance = async () => {
    const response = await getEmployeeAtendance(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id, {
        limit: rows.value,
        offset: first.value,
    });
    if (response) {
        attendance.value = response;
    }
};

const props = defineProps<{
    attendance: AttendanceInterfaceResponse;
}>();

const { attendance: propAttendance } = props;

onMounted(() => {
  attendance.value = propAttendance;
    loadAttendance();
});

const onPage = (event: any) => {
    first.value = event.first;
    rows.value = event.rows;
    loadAttendance();
};

</script>

<template>
    <div class="p-4">
        <DataTable 
            v-if="attendance.data && attendance.count > 0" 
            :value="attendance.data" 
            :paginator="true" 
            :rows="rows" 
            :totalRecords="attendance.count" 
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5, 10, 25, 50, 100]"
            :lazy="true" 
            @page="onPage"
            class="shadow-md rounded-lg w-[100%]"
        >
            
            <Column field="date" header="Data" >
                <template #body="slotProps">
                    {{ format(new Date(slotProps.data.date), 'dd/MM/yyyy') }}
                </template>
            </Column>

            <Column header="Check-in">
                <template #body="slotProps">
                    <div v-if="Array.isArray(slotProps.data.sessions) && slotProps.data.sessions.length > 0">
                        <div v-for="(session, index) in slotProps.data.sessions" :key="index">
                            {{ session.checkin }}
                        </div>
                    </div>
                    <div v-else>N/A</div>
                </template>
            </Column>

            <Column header="Check-out">
                <template #body="slotProps">
                    <div v-if="Array.isArray(slotProps.data.sessions) && slotProps.data.sessions.length > 0">
                        <div v-for="(session, index) in slotProps.data.sessions" :key="index">
                            {{ session.checkout }}
                        </div>
                    </div>
                    <div v-else>N/A</div>
                </template>
            </Column>

        </DataTable>

        <div v-else class="text-center text-gray-500 mt-4">
            Nenhuma presença encontrada.
        </div>
    </div>
</template>
