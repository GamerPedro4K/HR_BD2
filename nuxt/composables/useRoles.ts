import { useRuntimeConfig } from '#app';
import type { RoleListResponse, RoleQueryParams, RoleSubmission, Role, RoleRequst } from '~/types/roles';

export function useRoles() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorAdd: { severity: 'error', summary: 'Erro ao adicionar função', detail: 'Não foi possível adicionar a função. Verifique os dados.', life: 3000 },
        successAdd: { severity: 'success', summary: 'Função Adicionada', detail: 'Função foi adicionada com sucesso.', life: 3000 },
        errorUpdate: { severity: 'error', summary: 'Erro ao atualizar função', detail: 'Não foi possível atualizar a função.', life: 3000 },
        successUpdate: { severity: 'success', summary: 'Função Atualizada', detail: 'Função foi atualizada com sucesso.', life: 3000 },
        errorDelete: { severity: 'error', summary: 'Erro ao excluir função', detail: 'Não foi possível excluir a função.', life: 3000 },
        successDelete: { severity: 'success', summary: 'Função Excluída', detail: 'Função foi excluída com sucesso.', life: 3000 },
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getRoles = async (params: RoleQueryParams) => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<RoleListResponse>(`${config.public.apiUrl}api/roles/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { roles: [], total_count: 0 };
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorConnection);
            return { roles: [], total_count: 0 };
        }
    };

    const getRole = async (id: string): Promise<RoleRequst | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<RoleRequst>(`${config.public.apiUrl}api/roles/${id}`, {
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

    const addRole = async (data: RoleSubmission) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}api/roles/`, {
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
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorAdd);
            return null;
        }
    };

    const editRole = async (id: string, data: RoleSubmission) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}api/roles/${id}/`, {
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
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorUpdate);
            return null;
        }
    };

    const deleteRole = async (id: string) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/roles/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            $toast.add(message.successDelete);
            return true;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorDelete);
            return false;
        }
    };

    return {
        getRoles,
        getRole,
        addRole,
        editRole,
        deleteRole,
    };
}