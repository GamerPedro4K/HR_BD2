import { useRuntimeConfig } from '#app';
import type { CertificateType, CertificateTypeListResponse, CertificateTypeQueryParams } from '~/types/certifications';

export function useCertification() {
    const { $toast } = useNuxtApp();
    const router = useRouter();


    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Certificados - Verifique conexão', life: 3000 },
        errorGeneric: { severity: 'error', summary: 'Erro', detail: 'Ocorreu um problema', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getCertificateTypes = async (params: CertificateTypeQueryParams): Promise<CertificateTypeListResponse> => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<CertificateTypeListResponse>(`${config.public.apiUrl}api/certificate_types/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { certificate_types: [], total_count: 0 };
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorConnection);
            return { certificate_types: [], total_count: 0 };
        }
    };

    const getCertificateType = async (id: string): Promise<CertificateType | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<CertificateType>(`${config.public.apiUrl}/api/certificate_types/${id}/`, {
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

    const createCertificateType = async (data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/certificate_types/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de certificado criado', life: 3000 });
            return response;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const updateCertificateType = async (id: string, data: any) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}/api/certificate_types/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de certificado atualizado', life: 3000 });
            return response;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
            return null;
        }
    };

    const deleteCertificateType = async (id: string, bulk: boolean) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/certificate_types/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            if (!bulk)
                $toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Tipo de certificado excluído', life: 3000 });
            return true;
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            console.error(error);
            $toast.add(message.errorGeneric);
            return false;
        }
    };

    return { getCertificateTypes, getCertificateType, createCertificateType, updateCertificateType, deleteCertificateType };
}