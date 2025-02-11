<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const { hasPermission } = useAuth();

const model = ref([
    {
        label: 'Home',
        items: [{ label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/dashboard' }]
    },
    {
        label: 'Gestão',
        items: [
            { label: 'Funcionários', icon: 'pi pi-fw pi-user', to: '/dashboard/employee', visible: hasPermission(["view_all_employees", "view_employee", "create_employee", "update_employee"])},
            { label: 'Departamentos', icon: 'pi pi-fw pi-sitemap', to: '/dashboard/departments', visible: hasPermission(["view_all_departments", "view_department", "create_department", "update_department", "delete_department"]) },
            { label: 'Cargos', icon: 'pi pi-fw pi-briefcase', to: '/dashboard/roles', visible: hasPermission(["view_all_roles", "view_role", "create_role", "update_role", "delete_role"]) },
        ]
    },
    {
        label: 'Categorias',
        items: [
            { label: 'Tipos de Formações', icon: 'pi pi-fw pi-graduation-cap', to: '/dashboard/trainings', visible: hasPermission(["view_all_training_types", "view_training_type", "create_training_type", "update_training_type", "delete_training_type"]) },
            { label: 'Tipos de contratos', icon: 'pi pi-fw pi-file', to: '/dashboard/tipo-contrato', visible: hasPermission(["view_all_contract_types", "view_contract_type", "create_contract_type", "update_contract_type", "delete_contract_type"]) },
            { label: 'Estado dos contratos', icon: 'pi pi-fw pi-flag', to: '/dashboard/estado-contrato', visible: hasPermission(["view_all_contract_states", "view_contract_state", "create_contract_state", "update_contract_state", "delete_contract_state" ]) },
            { label: 'Estado de saída', icon: 'pi pi-fw pi-sign-out', to: '/dashboard/estado-saida', visible: hasPermission(["view_all_contract_leave_types", "view_contract_leave_type", "create_contract_leave_type", "update_contract_leave_type", "delete_contract_leave_type"]) },
            { label: 'Tipo de pagamento', icon: 'pi pi-fw pi-money-bill', to: '/dashboard/tipo-pagamento', visible: hasPermission(["view_all_payment_methods", "view_payment_method", "create_payment_method", "update_payment_method", "delete_payment_method"]) },
            { label: 'Tipo de benefícios', icon: 'pi pi-fw pi-gift', to: '/dashboard/tipo-beneficios', visible: hasPermission(["view_all_type_benefits", "view_type_benefit", "create_type_benefit", "update_type_benefit", "delete_type_benefit"]) },
            { label: 'Tipo de certificado', icon: 'pi pi-fw pi-verified', to: '/dashboard/tipo-certificados', visible: hasPermission(["view_all_certificate_types", "view_certificate_type", "create_certificate_type", "update_certificate_type", "delete_certificate_type"]) },
        ]
    },
    {
        label: 'Permissões',
        items: [
            { label: 'Grupos', icon: 'pi pi-fw pi-users', to: '/dashboard/grupos', visible: hasPermission(["view_all_auth_groups", "view_auth_group", "create_auth_group", "update_auth_group", "delete_auth_group", "add_group_permissions", "delete_group_permissions"]) },
            { label: 'Permissões', icon: 'pi pi-fw pi-shield', to: '/dashboard/permissoes', visible: hasPermission("view_all_permissions") },
            { label: 'Utilizadores', icon: 'pi pi-fw pi-user-edit', to: '/dashboard/permission-grupo', visible: hasPermission("view_all_permissions_user_group") },
        ]
    },
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
