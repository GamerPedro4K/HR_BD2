export function useBreadcrumb() {
    const route = useRoute();

    const breadcrumbs = computed(() => {
        const paths = route.path
            .split('/')
            .filter((segment) => segment && segment.toLowerCase() !== 'action'); // Exclude "action"

        const breadcrumbItems = paths.map((segment, index) => {
            const path = '/' + paths.slice(0, index + 1).join('/');
            return {
                label: capitalizeFirstLetter(segment),
                route: path,
                icon: undefined,
            };
        });

        return breadcrumbItems;
    });

    const home = {
        label: 'Dashboard',
        icon: 'pi pi-home',
        route: '/dashboard',
    };

    const updateLastBreadcrumbLabel = (newLabel: string, newRoute?: string) => {
        const lastBreadcrumb = breadcrumbs.value.at(-1);
        if (lastBreadcrumb) {
            lastBreadcrumb.label = newLabel;
            if (newRoute) {
                lastBreadcrumb.route = newRoute; // Update route dynamically
            }
        }
    };

    return { breadcrumbs, home, updateLastBreadcrumbLabel };
}

function capitalizeFirstLetter(val: string) {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}
