import { useRuntimeConfig } from '#app';
import type { TrainingTypesResponse } from '~/types/training';

export function useTraining() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Certificados - Verifique conexão', life: 3000 },
    };

    const getTrainingType = async (): Promise<TrainingTypesResponse> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<TrainingTypesResponse>(`${config.public.apiUrl}/api/training_types/`, {
                method: 'GET',
            });

            return response || { certificate_types: []};
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { training_types: []};
        }
    };


    return { getTrainingType };
}
