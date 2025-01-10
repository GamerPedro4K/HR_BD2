import { useRuntimeConfig } from '#app';
import type { Department, DepartmentListResponse } from '~/types/department';

export function useDepartment() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Connection Error', detail: 'Check your connection.', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Error', detail: 'An error occurred.', life: 3000 },
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getDepartments = async (): Promise<DepartmentListResponse> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<DepartmentListResponse>(
                `${config.public.apiUrl}/api/departments/`,
                {
                    method: 'GET',
                    headers: getAuthHeaders(),
                }
            );

            return response || { departments: [] };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { departments: [] };
        }
    };

    const getDepartment = async (id: string): Promise<Department | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<Department>(`${config.public.apiUrl}/api/departments/${id}`, {
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

    const createDepartment = async (data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/departments/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Department created successfully.', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updateDepartment = async (id: string, data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/departments/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Department updated successfully.', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deleteDepartment = async (id: string) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}/api/departments/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Department deleted successfully.', life: 3000 });
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
        }
    };

    return { getDepartments, getDepartment, createDepartment, updateDepartment, deleteDepartment };
}
