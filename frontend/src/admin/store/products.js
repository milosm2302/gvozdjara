import { defineStore } from 'pinia'
import { api } from '@/services/api'
import { useAuthStore } from '@/store/auth'

export const useProductStore = defineStore('adminProducts', {
    state: () => ({
        list: [],
        loading: false,
        error: null
    }),

    actions: {
        async fetch() {
            this.loading = true
            try {
                const res = await api.get('products/')
                this.list = res.data
            } catch (e) {
                console.error('Greška fetch proizvoda:', e)
            } finally {
                this.loading = false
            }
        },

        async create(payload) {
            const auth = useAuthStore()

            await api.post(
                'products/',
                payload,
                { headers: { Authorization: `Bearer ${auth.accessToken}` } }
            )

            await this.fetch()
        },

        async update(id, payload) {
            const auth = useAuthStore()

            await api.put(
                `products/${id}/`,
                payload,
                { headers: { Authorization: `Bearer ${auth.accessToken}` } }
            )

            await this.fetch()
        },

        async remove(id) {
            const auth = useAuthStore()

            await api.delete(
                `products/${id}/`,
                { headers: { Authorization: `Bearer ${auth.accessToken}` } }
            )

            await this.fetch()
        }
    }
})
