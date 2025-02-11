import { useRuntimeConfig } from '#app';
import type { EmployeePermissionsQueryParams, EmployeePermissionsResponse } from '~/types/permissionsusergroup';

export function useEmployeePermissionsGroup() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Erro', detail: 'Ocorreu um problema', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getEmployeePermissions = async (params: EmployeePermissionsQueryParams): Promise<EmployeePermissionsResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<EmployeePermissionsResponse>(`${config.public.apiUrl}api/permissions_user_group/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { employees: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            return { employees: [], total_count: 0 };
        }
    };

    return { getEmployeePermissions };
}