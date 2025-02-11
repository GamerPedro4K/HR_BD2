import { useRuntimeConfig } from '#app';
import type { EmployeeListResponse, EmployeeQueryParams, EmployeeSubmission, FindEmployee } from '~/types/employee';
import type { ScheduleInterface } from '~/types/schedule';
import type { AttendanceInterfaceResponse, AttendanceInterfaceParams } from '~/types/attendance';
import { any } from 'zod';
export function useEmployee() {
    const { $toast } = useNuxtApp();

    enum isCheckedHandler { checked_in, checked_out, error, loading };
    let isCheckedIn = isCheckedHandler.loading;

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorCredentials: { severity: 'error', summary: 'Credenciais inválidas', detail: 'Verifique o email e a palavra-passe', life: 3000 },
        errorAdd: { severity: 'error', summary: 'Erro ao adicionar funcionário', detail: 'Não foi possível adicionar o funcionário. Verifique os dados.', life: 3000 },
        successAdd: { severity: 'success', summary: 'Funcionário Adicionado', detail: 'Funcionário foi adicionado com sucesso.', life: 3000 },
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getSubFromToken = (): string | null => {
        const token = localStorage.getItem('access_token');
        if (!token) return null;

        const payload = token.split('.')[1];
        if (!payload) return null;

        const decodedPayload = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));

        try {
            const parsedPayload = JSON.parse(decodedPayload);
            return parsedPayload.sub || null;
        } catch (error) {
            console.error('Erro ao decodificar o token:', error);
            return null;
        }
    };

    const getCheckInStatus = async () => {
        try {
            const config = useRuntimeConfig();
            const date = new Date().toISOString().split('T')[0];
            const id = getSubFromToken();
            if (!id) throw new Error('No sub found in token');
            const response = await $fetch<{ is_chekin: boolean }>(`${config.public.apiUrl}api/attendance/${id}/${date}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            isCheckedIn = response.is_chekin ? isCheckedHandler.checked_out : isCheckedHandler.checked_in;

            return isCheckedIn;
        } catch (error) {
            console.error(error);
            isCheckedIn = isCheckedHandler.error;
            $toast.add(message.errorConnection);
            return null;
        }
    }

    const getEmployees = async (params: EmployeeQueryParams) => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<EmployeeListResponse>(`${config.public.apiUrl}api/employees/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { employees: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { employees: [], total_count: 0 };
        }
    };

    const getEmployee = async (id: string): Promise<FindEmployee | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<FindEmployee>(`${config.public.apiUrl}api/employees/${id}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    }

    const addEmployee = async (data: EmployeeSubmission) => {
        try {
          const config = useRuntimeConfig();
          const response = await $fetch(`${config.public.apiUrl}auth/register/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              ...getAuthHeaders(),
            },
            body: data,
          });
    
          $toast.add(message.successAdd);
          return response;
        } catch (error) {
          console.error(error);
          $toast.add(message.errorAdd);
          return null;
        }
    };

    const editEmployee = async (data: EmployeeSubmission) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}api/employees/${data.employee.id_employee}/`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders(),
              },
              body: data,
            });
      
            $toast.add(message.successAdd);
            return response;
        } catch (error) {
          console.error(error);
          $toast.add(message.errorAdd);
          return null;
        }
    };
    
    const getEmployeeAtendance = async (id: string, params: AttendanceInterfaceParams): Promise<AttendanceInterfaceResponse | null> => {
        try {
            const config = useRuntimeConfig();
            const query = params ? new URLSearchParams(Object.entries(params)).toString() : '';
            const response = await $fetch<AttendanceInterfaceResponse>(`${config.public.apiUrl}api/attendance/${id}?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    }

    const getEmployeeSchedule = async (id: string): Promise<ScheduleInterface[] | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<ScheduleInterface[]>(`${config.public.apiUrl}api/schedule/${id}/`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    }

    const postCheckInOrChekOut = async (checked_in: boolean) => {
        try {
            const config = useRuntimeConfig();
            const id = getSubFromToken();
            if (!id) throw new Error('No sub found in token');
            const time = new Date().toISOString().split('T')[1].split('.')[0];
            const body = checked_in ? { 'checkin': time } : { 'checkout': time };
            const response = await $fetch<{ is_chekin: boolean }>(`${config.public.apiUrl}api/attendance/`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: body,
            });

            isCheckedIn = checked_in ? isCheckedHandler.checked_out : isCheckedHandler.checked_in;
            return isCheckedIn;
        } catch (error) {
            console.error(error);
            isCheckedIn = isCheckedHandler.error;
            $toast.add(message.errorConnection);
            return null;
        }
    }

    return { getEmployees, getEmployee, addEmployee, editEmployee, getEmployeeAtendance, getEmployeeSchedule, isCheckedHandler, getCheckInStatus, postCheckInOrChekOut };
}
