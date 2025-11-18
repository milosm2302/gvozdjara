<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import Password from 'primevue/password';
import InputText from 'primevue/inputtext';
import FloatLabel from 'primevue/floatlabel';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Message from 'primevue/message';

const router = useRouter();
const authStore = useAuthStore();
const username = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
    error.value = '';
    const success = await authStore.login(username.value, password.value);

    if (success) {
        router.push('/admin/panel');
    } else {
        error.value = "Invalid credentials";
    }
};
</script>

<template>
    <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);">
        <Card style="width: 100%; max-width: 450px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); border-radius: 16px;">
            <template #header>
                <div style="text-align: center; padding: 2.5rem 1.5rem; background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); color: white; border-radius: 16px 16px 0 0;">
                    <h1 style="font-size: 2rem; font-weight: 700; margin: 0 0 0.5rem 0;">Login</h1>
                    <p style="margin: 0; color: #e3f2fd; font-size: 0.95rem;">Enter your credentials to continue</p>
                </div>
            </template>

            <template #content>
                <form @submit.prevent="handleLogin" style="padding: 2rem 1.5rem;">
                    <Message 
                        v-if="error" 
                        severity="error" 
                        :closable="false"
                        style="margin-bottom: 1.5rem;"
                    >
                        {{ error }}
                    </Message>

                    <div style="margin-bottom: 2rem;">
                        <FloatLabel variant="on">
                            <InputText 
                                id="username" 
                                v-model="username" 
                                style="width: 100%; padding: 0.75rem 1rem; border: 2px solid #e3f2fd; border-radius: 8px; font-size: 1rem;"
                            />
                            <label for="username" style="color: #1976d2; font-weight: 500;">Username</label>
                        </FloatLabel>
                    </div>

                    <div style="margin-bottom: 2rem;">
                        <FloatLabel variant="on">
                            <Password 
                                id="password"
                                v-model="password" 
                                toggleMask 
                                :feedback="false"
                                inputStyle="width: 100%; padding: 0.75rem 1rem; border: 2px solid #e3f2fd; border-radius: 8px; font-size: 1rem;"
                                style="width: 100%;"
                            />
                            <label for="password" style="color: #1976d2; font-weight: 500;">Password</label>
                        </FloatLabel>
                    </div>

                    <Button 
                        type="submit" 
                        label="Sign In" 
                        icon="pi pi-sign-in"
                        severity="info"
                        style="width: 100%; padding: 0.85rem; font-size: 1.05rem; font-weight: 600; background: #1976d2; border: none; border-radius: 8px;"
                    />
                </form>
            </template>

            <template #footer>
                <div style="text-align: center; padding: 0 1.5rem 1.5rem 1.5rem; color: #64b5f6; font-size: 0.875rem;">
                    <i class="pi pi-shield" style="margin-right: 0.5rem;"></i>
                    Secure login with encrypted connection
                </div>
            </template>
        </Card>
    </div>
</template>

<style scoped>
/* Focus states */
:deep(.p-inputtext:focus) {
    border-color: #1976d2 !important;
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.15) !important;
}

:deep(.p-password input:focus) {
    border-color: #1976d2 !important;
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.15) !important;
}

:deep(.p-button:hover) {
    background: #1565c0 !important;
    border-color: #1565c0 !important;
}

:deep(.p-float-label label) {
    font-size: 0.95rem;
}
</style>