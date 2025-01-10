<script setup>
const { logout } = useAuth();
</script>

<template>
    <div class="config-panel hidden absolute top-[3.25rem] right-0 w-64 p-4 bg-surface-0 dark:bg-surface-900 border border-surface rounded-border origin-top shadow-[0px_3px_5px_rgba(0,0,0,0.02),0px_0px_2px_rgba(0,0,0,0.05),0px_1px_4px_rgba(0,0,0,0.08)]">
        <div class="flex flex-col gap-4">
            <Button  severity="secondary" variant="text">
                <div class="w-full flex items-center justify-between">
                    <span>Ver Perfil</span>
                    <font-awesome icon="user" />
                </div>
            </Button>
            <Button  severity="danger" variant="text" @click="logout">
                <div class="w-full flex items-center justify-between">
                    <span>Terminar Sessão</span>
                    <font-awesome icon="arrow-right-from-bracket" />
                </div>
            </Button>
        </div>
    </div>
</template>
