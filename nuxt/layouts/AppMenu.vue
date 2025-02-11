<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Home',
        items: [{ label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/dashboard' }]
    },
    {
        label: 'Gestão',
        items: [
            { label: 'Funcionários', icon: 'pi pi-fw pi-id-card', to: '/dashboard/employee' },
            { label: 'Departamentos', icon: 'pi pi-fw pi-users', to: '/dashboard/departments' },
            { label: 'Cargos', icon: 'pi pi-fw pi-users', to: '/dashboard/roles' },
        ]
    },
    {
        label: 'Categorias',
        items: [
            { label: 'Tipos de Formações', icon: 'pi pi-fw pi-id-card', to: '/dashboard/trainings' },
            { label: 'Tipos de contratos', icon: 'pi pi-fw pi-id-card', to: '/dashboard/tipo-contrato' },
            { label: 'Estado dos contratos', icon: 'pi pi-fw pi-id-card', to: '/dashboard/estado-contrato' },
            { label: 'Estado de saída', icon: 'pi pi-fw pi-id-card', to: '/dashboard/estado-saida' },
            { label: 'Tipo de pagamento', icon: 'pi pi-fw pi-id-card', to: '/dashboard/tipo-pagamento' },
            { label: 'Tipo de benefícios', icon: 'pi pi-fw pi-id-card', to: '/dashboard/tipo-beneficios' },
            { label: 'Tipo de certificado', icon: 'pi pi-fw pi-id-card', to: '/dashboard/tipo-certificados' },
        ]
    },
    {
        label: 'Permissões',
        items: [
            { label: 'Grupos', icon: 'pi pi-fw pi-id-card', to: '/dashboard/grupos' },
            { label: 'Permissões', icon: 'pi pi-fw pi-id-card', to: '/dashboard/permissoes' },
            { label: 'Utilizadores', icon: 'pi pi-fw pi-id-card', to: '/dashboard/permission-grupo' },
        ]
    }
    /* {
        label: 'Pages',
        icon: 'pi pi-fw pi-briefcase',
        to: '/pages',
        items: [
            {
                label: 'Auth',
                icon: 'pi pi-fw pi-user',
                items: [
                    {
                        label: 'Login',
                        icon: 'pi pi-fw pi-sign-in',
                        to: '/auth/login'
                    },
                    {
                        label: 'Error',
                        icon: 'pi pi-fw pi-times-circle',
                        to: '/auth/error'
                    },
                    {
                        label: 'Access Denied',
                        icon: 'pi pi-fw pi-lock',
                        to: '/auth/access'
                    }
                ]
            },
            {
                label: 'Crud',
                icon: 'pi pi-fw pi-pencil',
                to: '/pages/crud'
            },
            {
                label: 'Not Found',
                icon: 'pi pi-fw pi-exclamation-circle',
                to: '/pages/notfound'
            },
            {
                label: 'Empty',
                icon: 'pi pi-fw pi-circle-off',
                to: '/pages/empty'
            }
        ]
    }, */
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
