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

    const isTokenValid = async () =>  {
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
            const { data, error } = await useFetch<{ permissions: string[] }>(`${config.public.apiUrl}/api/permissions/`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                },
            });

            if (error.value) {
                throw new Error('Falha ao obter permissões');
            }

            permissions.value = data.value?.permissions || [];
            return permissions.value;
        } catch (err) {
            console.error('Erro ao obter permissões:', err);
            permissions.value = [];
            return [];
        }
    };

    const hasPermission = (permission: string): boolean => {
        return permissions.value.includes(permission);
    };
    

    return { login, logout, isTokenValid, getUserPermissions, hasPermission };
}
