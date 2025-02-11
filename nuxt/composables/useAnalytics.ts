import { useRouter } from 'vue-router';
import { useRuntimeConfig } from '#app';
import type { AuthResponse } from '~/types/auth';
import type { DashboardData } from '~/types/analytics';

export function useAnalytics() {
    const router = useRouter();
    const { $toast, $loadingIndicator } = useNuxtApp();

    const message = {
        success: { severity: 'success', summary: 'Sessão iniciada', detail: 'Bem-vindo', life: 3000 },
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorCredentials: { severity: 'error', summary: 'Credenciais inválidas', detail: 'Verifique o email e a palavra-passe', life: 3000 }
    };

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return token ? { Authorization: `Bearer ${token}` } : undefined;
    };

    const getAnalytics = async (): Promise<DashboardData | null> => {
        try {
            $loadingIndicator?.start();
            const config = useRuntimeConfig();
            const response = await $fetch<DashboardData>(`${config.public.apiUrl}api/analytics/`, {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            return response;
        } catch (error) {
            console.error(error);
            $toast.add(message.errorConnection);
            return null;
        }
    }

    return { getAnalytics };
}
