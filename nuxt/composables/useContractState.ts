import { useRuntimeConfig } from '#app';
import type { ContractState, ContractStateContractParams, ContractStateContractResponse, ContractStateListResponse, ContractStateQueryParams } from '~/types/contractState';

export function useContractState() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Erro de Conexão', detail: 'Verifique a sua conexão.', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Erro', detail: 'Ocorreu um erro.', life: 3000 },
        successCreate: { severity: 'success', summary: 'Sucesso', detail: 'Estado de contrato criado com sucesso.', life: 3000 },
        successUpdate: { severity: 'success', summary: 'Sucesso', detail: 'Estado de contrato atualizado com sucesso.', life: 3000 },
        successDelete: { severity: 'success', summary: 'Sucesso', detail: 'Estado de contrato apagado com sucesso.', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getSubFromToken = (): string | null => {
        const token = localStorage.getItem('access_token');
        if (!token) return null;

        const payload = token.split('.')[1];
        if (!payload) return null;

        const decodedPayload = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));

        try {
            const parsedPayload = JSON.parse(decodedPayload);
            return parsedPayload.sub || null;
        } catch (error) {
            console.error('Erro ao decodificar o token:', error);
            return null;
        }
    };

    const getContractStates = async (params: ContractStateQueryParams): Promise<ContractStateListResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<ContractStateListResponse>(`${config.public.apiUrl}api/contract_states/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { contract_states: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { contract_states: [], total_count: 0 };
        }
    };

    const getContractState = async (id: string): Promise<ContractState | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<ContractState>(`${config.public.apiUrl}/api/contract_states/${id}/`, {
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
            const response = await $fetch(`${config.public.apiUrl}api/contract_states/`, {
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
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updateContractState = async (id: string, data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}api/contract_states/${id}/`, {
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
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deleteContractState = async (id: string, bulk: boolean) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/contract_states/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            if (!bulk) $toast.add(message.successDelete);
            return true;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return false;
        }
    };

    const getContractStateContract = async (params: ContractStateContractParams | null): Promise<ContractStateContractResponse | null> => {
        try {
            const sub = getSubFromToken();
            const config = useRuntimeConfig();
            const query = params ? new URLSearchParams(Object.entries(params)).toString() : '';
            const response = await $fetch<ContractStateContractResponse>(
                `${config.public.apiUrl}api/contract_state_contracts/${sub}?${query}`,
                {
                    method: 'GET',
                    headers: getAuthHeaders(),
                }
            );

            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    return { getContractStates, getContractState, createContractState, updateContractState, deleteContractState, getContractStateContract };
}
