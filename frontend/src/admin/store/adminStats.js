import { defineStore } from 'pinia'
import { api } from '../../services/api'
import { useAuthStore } from '../../store/auth'

export const useAdminStatsStore = defineStore('adminStats', {
    state: () => ({
        categories: 0,
        subcategories: 0,
        products: 0,
        orders: 0,
    }),

    actions: {
        async refresh() {
            const auth = useAuthStore()

            try {
                const [cats, subs, prods, ords] = await Promise.all([
                    api.get('/categories/'),
                    api.get('/subcategories/'),
                    api.get('/products/'),
                    api.get('/orders/', {
                        headers: { Authorization: `Bearer ${auth.accessToken}` }
                    })
                ])

                this.categories = cats.data.length
                this.subcategories = subs.data.length
                this.products = prods.data.length
                this.orders = ords.data.length


            } catch (e) {
                console.error("Greška pri učitavanju brojača:", e)
            }
        }
    }
})
