import { useRuntimeConfig } from '#app';
import type { ContractState, ContractStateListResponse } from '~/types/contractState';

export function useContractState() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Connection Error', detail: 'Check your connection.', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Error', detail: 'An error occurred.', life: 3000 },
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getContractStates = async (): Promise<ContractStateListResponse> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<ContractStateListResponse>(
                `${config.public.apiUrl}/api/contract_states/`,
                {
                    method: 'GET',
                    headers: getAuthHeaders(),
                }
            );

            return response || { contract_states: [] };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { contract_states: [] };
        }
    };

    const getContractState = async (id: string): Promise<ContractState | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<ContractState>(`${config.public.apiUrl}/api/contract_states/${id}`, {
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

    const createContractState = async (data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/contract_states/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Contract state created successfully.', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updateContractState = async (id: string, data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/contract_states/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Contract state updated successfully.', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deleteContractState = async (id: string) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}/api/contract_states/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            $toast.add({ severity: 'success', summary: 'Success', detail: 'Contract state deleted successfully.', life: 3000 });
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
        }
    };

    return { getContractStates, getContractState, createContractState, updateContractState, deleteContractState };
}
