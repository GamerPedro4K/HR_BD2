import { useRuntimeConfig } from '#app';
import type { Permission, PermissionListResponse, PermissionQueryParams } from '~/types/permission';

export function usePermission() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Erro', detail: 'Ocorreu um problema', life: 3000 },
        successAdd: { severity: 'success', summary: 'Sucesso', detail: 'Permissões adicionadas com sucesso', life: 3000 },
        successRemove: { severity: 'success', summary: 'Sucesso', detail: 'Permissões removidas com sucesso', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getPermissions = async (params: PermissionQueryParams): Promise<PermissionListResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<PermissionListResponse>(`${config.public.apiUrl}api/permissions/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { permissions: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { permissions: [], total_count: 0 };
        }
    };

    const addPermissionsToGroup = async (group_id: number, permission_ids: number[]) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}api/permissions/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: {
                    group_id,
                    permission_ids
                },
            });

            $toast.add(message.successAdd);
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const removePermissionsFromGroup = async (group_id: number, permission_ids: number[]) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}api/permissions/remove_permissions/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: {
                    group_id,
                    permission_ids: Array.isArray(permission_ids) ? permission_ids : [permission_ids]
                },
            });
    
            $toast.add(message.successRemove);
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    return { getPermissions, addPermissionsToGroup, removePermissionsFromGroup };
}