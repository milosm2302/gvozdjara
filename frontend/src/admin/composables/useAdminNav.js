import { ref } from 'vue'

export function useAdminNav() {
    const activeView = ref('products')

    const setView = (view) => {
        activeView.value = view
    }

    const views = [
        { id: 'categories', label: 'Kategorije', icon: '📁' },
        { id: 'subcategories', label: 'Podkategorije', icon: '📂' },
        { id: 'products', label: 'Proizvodi', icon: '📦' }
    ]

    return { activeView, setView, views }
}
