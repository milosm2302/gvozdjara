export function useFilters() {
    const formatPrice = (price) =>
        new Intl.NumberFormat('sr-RS', {
            style: 'currency',
            currency: 'RSD',
            minimumFractionDigits: 2
        }).format(price)

    const truncate = (text, len) => {
        if (!text) return ''
        if (text.length <= len) return text
        return text.substring(0, len) + '...'
    }

    const salePercent = (product) => {
        if (!product.on_sale || !product.sale_price) return 0
        return Math.round(((product.price - product.sale_price) / product.price) * 100)
    }

    return {
        formatPrice,
        truncate,
        salePercent
    }
}
