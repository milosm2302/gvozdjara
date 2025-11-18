import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
    state: () => ({
        items: JSON.parse(localStorage.getItem('cart') || '[]')
    }),

    getters: {
        count: (state) => {
            return state.items.reduce((sum, i) => sum + i.quantity, 0)
        },

        subtotal: (state) => {
            return state.items.reduce((sum, i) => sum + (i.price * i.quantity), 0)
        },

        shipping: (state) => {
            return state.items.length === 0 ? 0 : state.items.reduce((sum, i) => sum + (i.price * i.quantity), 0) > 5000
                ? 0
                : 300
        },

        total: (state) => {
            return state.subtotal + state.shipping
        },

        isInCart: (state) => (id) => {
            return state.items.some(i => i.id === id)
        }
    },

    actions: {
        save() {
            localStorage.setItem('cart', JSON.stringify(this.items))
        },

        load() {
            const saved = localStorage.getItem('cart')
            if (saved) {
                this.items = JSON.parse(saved)
            }
        },

        add(product) {
            const found = this.items.find(i => i.id === product.id)

            if (found) {
                found.quantity++
            } else {
                this.items.push({
                    id: product.id,
                    name: product.name,
                    price: parseFloat(product.current_price),
                    image: product.image,
                    quantity: 1
                })
            }

            this.save()
        },

        increase(item) {
            item.quantity++
            this.save()
        },

        decrease(item) {
            if (item.quantity > 1) {
                item.quantity--
                this.save()
            }
        },

        remove(item) {
            this.items = this.items.filter(i => i.id !== item.id)
            this.save()
        },

        clear() {
            this.items = []
            this.save()
        }
    }
})
