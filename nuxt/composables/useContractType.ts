import { useRuntimeConfig } from '#app';
import type { ContractType, ContractTypeListResponse, ContractTypeQueryParams } from '~/types/contractType';

export function useContractType() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Erro', detail: 'Ocorreu um problema', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

   
    const getContractTypes = async (params: ContractTypeQueryParams): Promise<ContractTypeListResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<ContractTypeListResponse>(`${config.public.apiUrl}api/contract_types/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { contract_types: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            return { contract_types: [], total_count: 0 };
        }
    };


    const getContractType = async (id: string): Promise<ContractType | null>   => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<ContractType>(`${config.public.apiUrl}/api/contract_types/${id}/`, {
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

    const createContractType = async (data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/contract_types/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de contrato criado', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updateContractType = async (id: string, data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/contract_types/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de contrato atualizado', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deleteContractType = async (id: string, bulk: boolean) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/contract_types/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            if(!bulk)
                $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de contrato excluído', life: 3000 });
            return true;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return false;
        }
    };

    return { getContractTypes, getContractType, createContractType, updateContractType, deleteContractType };
}
