import { useRuntimeConfig } from '#app';
import type { Vacation, VacationListResponse } from '~/types/vacation';

export function useVacations() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Férias - Verifique conexão', life: 3000 },
        successCreate: { severity: 'success', summary: 'Sucesso', detail: 'Férias criadas com sucesso', life: 3000 },
        successUpdate: { severity: 'success', summary: 'Sucesso', detail: 'Férias atualizadas com sucesso', life: 3000 },
        successDelete: { severity: 'success', summary: 'Sucesso', detail: 'Férias deletadas com sucesso', life: 3000 },
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getAllVacations = async (): Promise<VacationListResponse> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<Vacation[]>(`${config.public.apiUrl}/api/vacations/`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return { vacations: response };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { vacations: [] };
        }
    };

    const getVacationsByDepartment = async (departmentId: string | null = null): Promise<VacationListResponse> => {
        try {
            const config = useRuntimeConfig();
            const params = departmentId ? `?department_id=${departmentId}` : '';
            const response = await $fetch<Vacation[]>(`${config.public.apiUrl}/api/vacations/${params}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return { vacations: response };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { vacations: [] };
        }
    };

    const createVacation = async (data: Record<string, any>): Promise<Vacation | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<Vacation>(`${config.public.apiUrl}/api/vacations/`, {
                method: 'POST',
                body: data,
                headers: getAuthHeaders(),
            });

            $toast.add(message.successCreate);
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    };

    const updateVacation = async (id: string, data: Record<string, any>): Promise<Vacation | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<Vacation>(`${config.public.apiUrl}/api/vacations/${id}/`, {
                method: 'PUT',
                body: data,
                headers: getAuthHeaders(),
            });

            $toast.add(message.successUpdate);
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    };

    const deleteVacation = async (id: string): Promise<boolean> => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}/api/vacations/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            $toast.add(message.successDelete);
            return true;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return false;
        }
    };

    return { getAllVacations, getVacationsByDepartment, createVacation, updateVacation, deleteVacation };
}
