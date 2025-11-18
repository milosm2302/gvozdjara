import { createRouter, createWebHistory } from "vue-router";
import Login from "../admin/pages/Login.vue";
import AdminView from "../admin/pages/AdminView.vue";
import ShopView from "@/pages/user/ShopView.vue";
import CartView from "@/pages/user/CartView.vue";
import { useAuthStore } from "@/store/auth";

const router = createRouter({
    routes: [
        {
            path: '/',
            name: 'shop',
            component: ShopView
        },
        {
            path: '/cart',

            component: CartView
        },
        {
            path: '/admin',
            redirect: '/admin/login'
        },
        {
            path: '/admin/login',
            component: Login

        },
        {
            path: '/admin/panel',
            component: AdminView,
            meta: { requiresAuth: true }
        }
    ],
    history: createWebHistory(import.meta.env.BASE_URL),

})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/admin/login')
    } else if (to.path === '/admin/login' && authStore.isAuthenticated) {
        next('/admin/panel')
    } else {
        next()
    }
})


export default router
