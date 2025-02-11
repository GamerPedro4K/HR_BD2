import { useRuntimeConfig } from '#app';
import type { PaymentMethod, PaymentMethodListResponse, PaymentMethodQueryParams } from '~/types/paymentmethod';

export function usePaymentMethod() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Erro', detail: 'Ocorreu um problema', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getPaymentMethods = async (params: PaymentMethodQueryParams): Promise<PaymentMethodListResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<PaymentMethodListResponse>(`${config.public.apiUrl}api/payment_methods/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { payment_methods: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { payment_methods: [], total_count: 0 };
        }
    };

    const getPaymentMethod = async (id: string): Promise<PaymentMethod | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<PaymentMethod>(`${config.public.apiUrl}/api/payment_methods/${id}/`, {
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

    const createPaymentMethod = async (data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/payment_methods/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Método de pagamento criado', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updatePaymentMethod = async (id: string, data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/payment_methods/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Método de pagamento atualizado', life: 3000 });
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deletePaymentMethod = async (id: string, bulk: boolean) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/payment_methods/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            if(!bulk)
                $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Método de pagamento excluído', life: 3000 });
            return true;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorGeneric);
            return false;
        }
    };

    return { getPaymentMethods, getPaymentMethod, createPaymentMethod, updatePaymentMethod, deletePaymentMethod };
}