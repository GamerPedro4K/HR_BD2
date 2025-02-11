import { useRuntimeConfig } from '#app';
import type { ContractLeaveType, ContractLeaveTypeListResponse, ContractLeaveTypeQueryParams } from '~/types/contractleavetype ';

export function useContractLeaveType() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Erro', detail: 'Ocorreu um problema', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getContractLeaveTypes = async (params: ContractLeaveTypeQueryParams): Promise<ContractLeaveTypeListResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<ContractLeaveTypeListResponse>(`${config.public.apiUrl}api/contract_leave_types/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { contract_leave_types: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { contract_leave_types: [], total_count: 0 };
        }
    };

    const getContractLeaveType = async (id: string): Promise<ContractLeaveType | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<ContractLeaveType>(`${config.public.apiUrl}/api/contract_leave_types/${id}/`, {
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

    const createContractLeaveType = async (data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/contract_leave_types/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de licença criado', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updateContractLeaveType = async (id: string, data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/contract_leave_types/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de licença atualizado', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deleteContractLeaveType = async (id: string, bulk: boolean) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/contract_leave_types/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            if(!bulk)
                $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de licença excluído', life: 3000 });
            return true;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return false;
        }
    };

    return { getContractLeaveTypes, getContractLeaveType, createContractLeaveType, updateContractLeaveType, deleteContractLeaveType };
}