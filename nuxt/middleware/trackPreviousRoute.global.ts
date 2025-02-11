export default defineNuxtRouteMiddleware((to, from) => {
    const previousRoute = useState<string | null>('previousRoute', () => null);
    previousRoute.value = from.fullPath;
});