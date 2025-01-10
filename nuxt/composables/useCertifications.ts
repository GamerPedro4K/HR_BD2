import { useRuntimeConfig } from '#app';
import type { CertificateTypesResponse } from '~/types/certifications';

export function useCertification() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Certificados - Verifique conexão', life: 3000 },
    };

    const getCertificationsType = async (): Promise<CertificateTypesResponse> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<CertificateTypesResponse>(`${config.public.apiUrl}/api/certificate_types/`, {
                method: 'GET',
            });

            return response || { certificate_types: []};
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { certificate_types: []};
        }
    };


    return { getCertificationsType };
}
