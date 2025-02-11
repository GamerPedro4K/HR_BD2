import { useRuntimeConfig } from '#app';
import type { TypeBenefit, TypeBenefitListResponse, TypeBenefitQueryParams } from '~/types/typebenefit';

export function useTypeBenefit() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Erro', detail: 'Ocorreu um problema', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getTypeBenefits = async (params: TypeBenefitQueryParams): Promise<TypeBenefitListResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<TypeBenefitListResponse>(`${config.public.apiUrl}api/type_benefits/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { type_benefits: [], total_count: 0 };
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorConnection);
            return { type_benefits: [], total_count: 0 };
        }
    };

    const getTypeBenefit = async (id: string): Promise<TypeBenefit | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<TypeBenefit>(`${config.public.apiUrl}/api/type_benefits/${id}/`, {
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

    const createTypeBenefit = async (data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/type_benefits/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de benefício criado', life: 3000 });
            return response;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updateTypeBenefit = async (id: string, data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/type_benefits/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de benefício atualizado', life: 3000 });
            return response;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deleteTypeBenefit = async (id: string, bulk: boolean) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/type_benefits/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            if (!bulk)
                $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de benefício excluído', life: 3000 });
            return true;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
            return false;
        }
    };

    return { getTypeBenefits, getTypeBenefit, createTypeBenefit, updateTypeBenefit, deleteTypeBenefit };
}