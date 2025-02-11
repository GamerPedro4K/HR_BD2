import { useRuntimeConfig } from '#app';
import type { AuthGroup, AuthGroupFormData, AuthGroupListResponse, AuthGroupQueryParams } from '~/types/authgroup';

export function useAuthGroup() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: {
            severity: 'error',
            summary: 'Erro de Ligação',
            detail: 'Por favor, verifique a sua ligação à Internet.',
            life: 3000
        },
        errorGeneric: {
            severity: 'error',
            summary: 'Erro',
            detail: 'Ocorreu um erro.',
            life: 3000
        },
        successCreate: {
            severity: 'success',
            summary: 'Sucesso',
            detail: 'Grupo criado com sucesso.',
            life: 3000
        },
        successUpdate: {
            severity: 'success',
            summary: 'Sucesso',
            detail: 'Grupo atualizado com sucesso.',
            life: 3000
        },
        successDelete: {
            severity: 'success',
            summary: 'Sucesso',
            detail: 'Grupo eliminado com sucesso.',
            life: 3000
        }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getAuthGroups = async (params: AuthGroupQueryParams): Promise<AuthGroupListResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<AuthGroupListResponse>(`${config.public.apiUrl}api/authgroup/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { auth_groups: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { auth_groups: [], total_count: 0 };
        }
    };

    const getAuthGroup = async (id: number): Promise<AuthGroup | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<AuthGroup>(`${config.public.apiUrl}/api/authgroup/${id}/`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    };

    const createAuthGroup = async (data: AuthGroupFormData) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/authgroup/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add(message.successCreate);
            return response;
        } catch (error) {
            console.error('Error creating group:', error);
            $toast.add(message.errorGeneric);
            throw error;
        }
    };

    const updateAuthGroup = async (id: number, data: AuthGroupFormData) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/authgroup/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add(message.successUpdate);
            return response;
        } catch (error) {
            console.error('Error updating group:', error);
            $toast.add(message.errorGeneric);
            throw error;
        }
    };

    const deleteAuthGroup = async (id: number, bulk: boolean = false) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/authgroup/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            if(!bulk)
                $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Grupo excluído', life: 3000 });
            return true;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return false;
        }
    };

    return { getAuthGroups, getAuthGroup, createAuthGroup, updateAuthGroup, deleteAuthGroup };
}