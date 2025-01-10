import { useRuntimeConfig } from '#app';
import type { EmployeeListResponse, EmployeeQueryParams, EmployeeSubmission, FindEmployee } from '~/types/employee';

export function useEmployee() {
    const { $toast } = useNuxtApp();

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

    const getEmployees = async (params: EmployeeQueryParams) => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<EmployeeListResponse>(`${config.public.apiUrl}/api/employees/?${query}`, {
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
            const response = await $fetch<FindEmployee>(`${config.public.apiUrl}/api/employees/${id}`, {
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

    const editEmployee = async () => {
        try {
          return true
        } catch (error) {
          console.error(error);
          $toast.add(message.errorAdd);
          return null;
        }
    };
    

    return { getEmployees, getEmployee, addEmployee, editEmployee };
}
