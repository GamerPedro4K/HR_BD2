import { useRouter } from 'vue-router';
import { useRuntimeConfig } from '#app';
import { jwtDecode } from 'jwt-decode';
import type { AuthResponse } from '~/types/auth';


export function useAuth() {
    const router = useRouter();
    const { $toast, $loadingIndicator } = useNuxtApp();

    const permissions = useState<string[]>('userPermissions', () => []);

    const message = {
        success: { severity: 'success', summary: 'Sessão iniciada', detail: 'Bem-vindo', life: 3000 },
        errorConnection: { severity: 'error', summary: 'Ocorreu um erro', detail: 'Verifique conexão', life: 3000 },
        errorCredentials: { severity: 'error', summary: 'Credenciais inválidas', detail: 'Verifique o email e a palavra-passe', life: 3000 }
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

    const login = async (email: string, password: string) => {
        try {
            $loadingIndicator.start();

            const config = useRuntimeConfig();
            const { data, error } = await useFetch<AuthResponse>(`${config.public.apiUrl}/auth/login/`, {
                method: 'POST',
                body: { email, password },
            });

            if (error.value) {
                $toast.add(error.value.data.statusCode === 404 ? message.errorConnection : message.errorCredentials);
                $loadingIndicator.finish({ error: true });
                return false;
            }

            if (data.value) {
                localStorage.setItem('access_token', data.value.access);
                localStorage.setItem('refresh_token', data.value.refresh);

                $toast.add(message.success);
                router.push('/dashboard');
                $loadingIndicator.finish();
                return true;
            }
        } catch (error) {
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            $toast.add(message.errorConnection);
            $loadingIndicator.finish({ error: true });
            return false;
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        $toast.add({ severity: 'warn', summary: 'Sessão terminada', detail: 'Volte em breve!', life: 3000 });
        router.push('/');
    };

    const refreshToken = async (): Promise<boolean> => {
        const config = useRuntimeConfig();
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken) return false;

        try {
            const { data, error } = await useFetch<AuthResponse>(`${config.public.apiUrl}/api/token/refresh/`, {
                method: 'POST',
                body: { refresh: refreshToken },
            });

            if (data.value) {
                localStorage.setItem('access_token', data.value.access);
                return true;
            }

            return false;
        } catch {
            return false;
        }
    };

    const isTokenValid = async () => {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) return false;

        try {
            const decodedToken: { exp: number } = jwtDecode(accessToken);
            const currentTime = Math.floor(Date.now() / 1000);

            if (decodedToken.exp > currentTime) {
                await getUserPermissions();
                return true;
            }

            // Try to refresh the token if it's expired
            const refreshed = await refreshToken();
            if (refreshed) {
                await getUserPermissions();
            }
            return refreshed;
        } catch {
            return false;
        }
    };

    const getUserPermissions = async (): Promise<string[]> => {
        try {
            const config = useRuntimeConfig();
            const data = await $fetch<{ permissions: string[] }>(`${config.public.apiUrl}api/user_permissions/`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                },
            });


            permissions.value = data.permissions || [];
            return permissions.value;
        } catch (error) {
            console.error('Erro ao obter permissões:', error);
            if ((error as any).response?.status === 403) { router.replace('/pages/forbidden'); }

            permissions.value = [];
            return [];
        }
    };

    const hasPermission = (permission: string | string[]): boolean => {
        if (Array.isArray(permission)) {
            return permission.some(perm => permissions.value.includes(perm));
        } else {
            return permissions.value.includes(permission);
        }
    };

    return { login, logout, isTokenValid, getUserPermissions, hasPermission, getSubFromToken };
}
