<script setup>
import { ref, computed, onMounted } from 'vue'

import ShopHeader from '../../components/ShopHeader.vue'
import { useProductStore } from '../../store/products'
import { useCategoryStore } from '../../store/categories'
import { useCartStore } from '../../store/cart'

import { useFilters } from '../../composables/useFilters'
import { useUiHelpers } from '../../composables/useUiHelpers'

const productStore = useProductStore()
const categoryStore = useCategoryStore()
const cartStore = useCartStore()

const { formatPrice, truncate, salePercent } = useFilters()
const { scrollTo } = useUiHelpers()

// Filters (local)
const selectedCategory = ref(null)
const searchQuery = ref('')
const showOnlyOnSale = ref(false)

const filters = computed(() => ({
  category: selectedCategory.value,
  search: searchQuery.value,
  showOnlyOnSale: showOnlyOnSale.value
}))

const productsList = computed(() =>
  productStore.filteredProducts(filters.value)
)

const cartCount = computed(() => cartStore.count)

const getTitle = computed(() => {
  if (searchQuery.value) return `Rezultati: "${searchQuery.value}"`
  if (selectedCategory.value) {
    const c = categoryStore.categories.find(c => c.id === selectedCategory.value)
    return c ? c.name : 'Proizvodi'
  }
  return 'Svi Proizvodi'
})

onMounted(() => {
  categoryStore.fetchCategories()
  productStore.fetchProducts()
})
</script>

<template>
  <div>
    <ShopHeader :cart-count="cartCount" @search="q => searchQuery = q" />

    <!-- Hero -->
    <section class="py-20 bg-gradient-to-br from-[#3555e4] to-[#64b5f6] text-white text-center">
      <h1 class="text-5xl font-bold mb-4">Dobrodošli u Gvozdjara Shop</h1>
      <button @click="scrollTo('products')" class="bg-white text-blue-600 px-8 py-3 rounded-full font-bold">
        Pogledaj proizvode
      </button>
    </section>

    <!-- Products -->
    <section id="products" class="py-16 mx-auto max-w-7xl grid grid-cols-[300px_1fr] gap-10 px-4">

      <!-- Sidebar -->
      <aside class="bg-white p-6 rounded-xl shadow-sm h-fit sticky top-20">
        <h3 class="font-semibold text-lg mb-4">Kategorije</h3>

        <button
          @click="selectedCategory = null"
          :class="selectedCategory === null ? 'text-blue-600 font-semibold' : ''"
          class="flex justify-between w-full py-2"
        >
          Sve kategorije
          <span>{{ productStore.products.length }}</span>
        </button>

        <div v-for="cat in categoryStore.categories" :key="cat.id">
          <button
            @click="selectedCategory = cat.id"
            :class="selectedCategory === cat.id ? 'text-blue-600 font-semibold' : ''"
            class="flex justify-between w-full py-2"
          >
            {{ cat.name }}
            <span>{{ categoryStore.countForCategory(cat.id, productStore.products) }}</span>
          </button>
        </div>

        <label class="flex items-center gap-2 mt-6">
          <input type="checkbox" v-model="showOnlyOnSale" />
          Samo na akciji
        </label>
      </aside>

      <!-- Products Grid -->
      <div>
        <h2 class="text-3xl font-bold mb-6">{{ getTitle }}</h2>

        <div v-if="productStore.loading" class="py-20 text-center">
          Učitavanje...
        </div>

        <div
          v-else-if="productsList.length"
          class="grid grid-cols-[repeat(auto-fill,minmax(300px,1fr))] gap-8"
        >
          <div
            v-for="p in productsList"
            :key="p.id"
            class="bg-white rounded-xl shadow hover:-translate-y-1 transition cursor-pointer"
          >
            <img :src="p.image" class="h-60 w-full object-cover" />

            <div class="p-4">
              <p class="text-xs text-blue-600">{{ p.category_name }}</p>

              <h3 class="text-lg font-semibold">{{ p.name }}</h3>

              <p class="text-sm text-gray-600">{{ truncate(p.description, 80) }}</p>

              <div class="flex justify-between items-center mt-4">
                <div>
                  <span class="text-green-700 text-xl font-bold">
                    {{ formatPrice(p.current_price) }}
                  </span>
                </div>

                <button
                  @click="cartStore.add(p)"
                  class="px-4 py-2 bg-blue-600 text-white rounded-full"
                >
                  {{ cartStore.isInCart(p.id) ? '✓ U korpi' : '+ Dodaj' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-20 text-gray-400">
          Nema rezultata.
        </div>
      </div>
    </section>
  </div>
</template>
