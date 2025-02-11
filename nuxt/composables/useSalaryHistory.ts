import { useRuntimeConfig } from '#app';
import type { SalaryHistory } from '~/types/salary';

export function useSalaryHistory() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Connection Error', detail: 'Check your connection.', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Error', detail: 'An error occurred.', life: 3000 },
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getSalaryHistories = async (params = {}): Promise<SalaryHistory[]> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<SalaryHistory[]>(`${config.public.apiUrl}/api/salary_history/`, {
                method: 'GET',
                headers: getAuthHeaders(),
                params,
            });

            return response || [];
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorConnection);
            return [];
        }
    };

    const getSalaryHistory = async (id: string): Promise<SalaryHistory[] | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<SalaryHistory[]>(`${config.public.apiUrl}/api/salary_history?id_employee=${id}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    };

    const createSalaryHistory = async (data: Omit<SalaryHistory, 'id_salary_history' | 'created_at' | 'updated_at' | 'deleted_at'>): Promise<SalaryHistory | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<SalaryHistory>(`${config.public.apiUrl}/api/salary_history/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Salary history created successfully.', life: 3000 });
            return response;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updateSalaryHistory = async (
        id: string,
        data: Partial<Omit<SalaryHistory, 'id_salary_history' | 'created_at' | 'updated_at' | 'deleted_at'>>
    ): Promise<SalaryHistory | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<SalaryHistory>(`${config.public.apiUrl}/api/salary_history/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Salary history updated successfully.', life: 3000 });
            return response;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deleteSalaryHistory = async (id: string): Promise<void> => {
        try {
            const config = useRuntimeConfig();
            await $fetch<void>(`${config.public.apiUrl}/api/salary_history/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Salary history deleted successfully.', life: 3000 });
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
        }
    };

    return { getSalaryHistories, getSalaryHistory, createSalaryHistory, updateSalaryHistory, deleteSalaryHistory };
}
