import { useRuntimeConfig } from '#app';
import type { TrainingTypeListResponse, TrainingTypeQueryParams, TrainingTypeSubmission, TrainingType } from '~/types/trainingType';

export function useTrainingType() {
    const { $toast } = useNuxtApp();

    const message = {
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorAdd: { severity: 'error', summary: 'Erro ao adicionar tipo de treinamento', detail: 'Não foi possível adicionar o tipo de treinamento. Verifique os dados.', life: 3000 },
        successAdd: { severity: 'success', summary: 'Tipo de Treinamento Adicionado', detail: 'Tipo de treinamento foi adicionado com sucesso.', life: 3000 },
        errorUpdate: { severity: 'error', summary: 'Erro ao atualizar tipo de treinamento', detail: 'Não foi possível atualizar o tipo de treinamento.', life: 3000 },
        successUpdate: { severity: 'success', summary: 'Tipo de Treinamento Atualizado', detail: 'Tipo de treinamento foi atualizado com sucesso.', life: 3000 },
        errorDelete: { severity: 'error', summary: 'Erro ao excluir tipo de treinamento', detail: 'Não foi possível excluir o tipo de treinamento.', life: 3000 },
        successDelete: { severity: 'success', summary: 'Tipo de Treinamento Excluído', detail: 'Tipo de treinamento foi excluído com sucesso.', life: 3000 },
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getTrainingTypes = async (params: TrainingTypeQueryParams) => {
        try {
            const config = useRuntimeConfig();
            const query = new URLSearchParams(Object.entries(params)).toString();
            const response = await $fetch<TrainingTypeListResponse>(`${config.public.apiUrl}api/training_types/?${query}`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response || { training_types: [], total_count: 0 };
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return { training_types: [], total_count: 0 };
        }
    };

    const getTrainingType = async (id: string): Promise<TrainingType | null> => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch<TrainingType>(`${config.public.apiUrl}api/training_types/${id}`, {
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

    const addTrainingType = async (data: TrainingTypeSubmission) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}api/training_types/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: data,
            });

            $toast.add(message.successAdd);
            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorAdd);
            return null;
        }
    };

    const editTrainingType = async (id: string, data: TrainingTypeSubmission) => {
        try {
            const config = useRuntimeConfig();
            const response = await $fetch(`${config.public.apiUrl}api/training_types/${id}/`, {
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
            $toast.add(message.errorUpdate);
            return null;
        }
    };

    const deleteTrainingType = async (id: string, bulk: boolean) => {
        try {
            const config = useRuntimeConfig();
            await $fetch(`${config.public.apiUrl}api/training_types/${id}/`, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            if (!bulk)
                $toast.add(message.successDelete);
            return true;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorDelete);
            return false;
        }
    };

    return {
        getTrainingTypes,
        getTrainingType,
        addTrainingType,
        editTrainingType,
        deleteTrainingType,
    };
}