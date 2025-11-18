import { defineStore } from 'pinia'
import { api } from '@/services/api'

export const useAdminStatsStore = defineStore('adminStats', {
    state: () => ({
        categories: 0,
        subcategories: 0,
        products: 0
    }),

    actions: {
        async refresh() {
            try {
                const [cats, subs, prods] = await Promise.all([
                    api.get('/categories/'),
                    api.get('/subcategories/'),
                    api.get('/products/')
                ])

                this.categories = cats.data.length
                this.subcategories = subs.data.length
                this.products = prods.data.length

            } catch (e) {
                console.error("Greška pri učitavanju brojača:", e)
            }
        }
    }
})
