<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import TheHeader from '@/components/TheHeader.vue'
import TheFooter from '@/components/TheFooter.vue'
import { useProductStore } from '@/store/products'
import { useCategoryStore } from '@/store/categories'
import { useCartStore } from '@/store/cart'

const router = useRouter()
const productStore = useProductStore()
const categoryStore = useCategoryStore()
const cartStore = useCartStore()

// Filters
const selectedCategory = ref(null)
const searchQuery = ref('')
const showOnlyOnSale = ref(false)

const formatPrice = (price) => {
  return new Intl.NumberFormat('sr-RS', {
    style: 'currency',
    currency: 'RSD',
    minimumFractionDigits: 0
  }).format(price)
}

const salePercent = (oldPrice, newPrice) => {
  return Math.round(((oldPrice - newPrice) / oldPrice) * 100)
}

const filteredProducts = computed(() => {
  let products = productStore.products || []

  // Filter by category
  if (selectedCategory.value) {
    products = products.filter(p => p.category === selectedCategory.value)
  }

  // Filter by search
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    products = products.filter(p =>
      p.name.toLowerCase().includes(query) ||
      p.description.toLowerCase().includes(query)
    )
  }

  // Filter by on_sale
  if (showOnlyOnSale.value) {
    products = products.filter(p => p.on_sale)
  }

  return products
})

const featuredProducts = computed(() => {
  return (productStore.products || []).filter(p => p.featured).slice(0, 4)
})

const viewProductDetail = (productId) => {
  router.push(`/proizvod/${productId}`)
}

// Product quantities (key = product.id, value = quantity)
const productQuantities = ref({})

// Selected variants per product (key = product.id, value = variant or null)
const selectedVariants = ref({})

// Get quantity for a product (default 1)
const getQuantity = (productId) => {
  return productQuantities.value[productId] || 1
}

// Set quantity for a product
const setQuantity = (productId, quantity) => {
  if (quantity < 1) quantity = 1
  productQuantities.value[productId] = quantity
}

// Get selected variant for a product
const getSelectedVariant = (product) => {
  // If already selected, return it
  if (selectedVariants.value[product.id]) {
    return selectedVariants.value[product.id]
  }
  // Otherwise, auto-select first variant if product has variants
  if (product.variants && product.variants.length > 0) {
    selectedVariants.value[product.id] = product.variants[0]
    return product.variants[0]
  }
  return null
}

// Set selected variant for a product
const setSelectedVariant = (productId, variant) => {
  selectedVariants.value[productId] = variant
}

// Get price for a product (considering selected variant)
const getProductPrice = (product) => {
  const variant = getSelectedVariant(product)
  if (variant && variant.final_price) {
    return parseFloat(variant.final_price)
  }
  return parseFloat(product.current_price) || 0
}

// Add product to cart directly from card
const addToCartFromCard = (product) => {
  const quantity = getQuantity(product.id)
  const variant = getSelectedVariant(product)

  const productToAdd = {
    ...product,
    selectedVariant: variant
  }

  cartStore.add(productToAdd, quantity)
}

onMounted(async () => {
  await categoryStore.fetchCategories()
  await productStore.fetchProducts()
})
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <TheHeader />

    <main class="flex-1">

      <!-- Hero sekcija -->
      <div class="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
          <h1 class="text-5xl font-bold mb-6 bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
            Kovano gvožđe i bravarijski proizvodi
          </h1>
          <p class="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Širok asortiman kvalitetnih proizvoda - profili, ograde, ukrasni elementi i mnogo više
          </p>
          <div class="flex gap-4 justify-center">
            <a
              href="#products"
              class="bg-[#1976d2] hover:bg-[#1565c0] text-white font-semibold px-8 py-3 rounded-lg transition"
            >
              Pogledaj katalog
            </a>
            <router-link
              to="/kontakt"
              class="bg-white hover:bg-gray-100 text-gray-900 font-semibold px-8 py-3 rounded-lg transition"
            >
              Kontaktiraj nas
            </router-link>
          </div>
        </div>
      </div>

      <!-- Featured Products -->
      <div v-if="featuredProducts.length > 0" class="bg-white py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">Izdvojeni proizvodi</h2>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div
              v-for="product in featuredProducts"
              :key="product.id"
              @click="viewProductDetail(product.id)"
              class="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-xl transition cursor-pointer group"
            >
              <div class="relative h-48 bg-gray-100 overflow-hidden">
                <img
                  v-if="product.images && product.images.length > 0"
                  :src="`http://localhost:8000${product.images[0].image}`"
                  :alt="product.name"
                  class="w-full h-full object-cover group-hover:scale-110 transition duration-300"
                />
                <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                  <span class="text-4xl">📦</span>
                </div>

                <div v-if="product.on_sale" class="absolute top-2 right-2 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                  -{{ salePercent(product.price, product.sale_price) }}%
                </div>
              </div>

              <div class="p-4">
                <p class="text-xs text-[#1565c0] font-semibold mb-1">{{ product.category_name }}</p>
                <h3 class="font-semibold text-gray-900 mb-2 line-clamp-1">{{ product.name }}</h3>

                <div class="flex items-center justify-between mt-3">
                  <div>
                    <p v-if="product.on_sale" class="text-sm text-gray-400 line-through">{{ formatPrice(product.price) }}</p>
                    <p class="text-lg font-bold text-green-700">{{ formatPrice(product.current_price) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Products Section -->
      <div id="products" class="py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">

            <!-- Sidebar -->
            <aside class="lg:col-span-1">
              <div class="bg-white rounded-xl shadow-lg p-6 sticky top-24">
                <h3 class="font-bold text-lg mb-4 text-gray-900">Filteri</h3>

                <!-- Search -->
                <div class="mb-6">
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Pretraga..."
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1976d2] focus:border-transparent"
                  />
                </div>

                <!-- Categories -->
                <div class="mb-6">
                  <h4 class="font-semibold text-sm text-gray-700 mb-3">Kategorije</h4>

                  <button
                    @click="selectedCategory = null"
                    :class="selectedCategory === null ? 'bg-[#e3f2fd] text-[#1565c0] font-semibold' : 'text-gray-700 hover:bg-gray-50'"
                    class="w-full text-left px-3 py-2 rounded-lg transition mb-1"
                  >
                    Sve kategorije
                  </button>

                  <button
                    v-for="cat in categoryStore.categories"
                    :key="cat.id"
                    @click="selectedCategory = cat.id"
                    :class="selectedCategory === cat.id ? 'bg-[#e3f2fd] text-[#1565c0] font-semibold' : 'text-gray-700 hover:bg-gray-50'"
                    class="w-full text-left px-3 py-2 rounded-lg transition mb-1"
                  >
                    {{ cat.name }}
                  </button>
                </div>

                <!-- On Sale Filter -->
                <div>
                  <label class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 px-3 py-2 rounded-lg transition">
                    <input
                      v-model="showOnlyOnSale"
                      type="checkbox"
                      class="w-4 h-4 text-[#1565c0] rounded focus:ring-[#1976d2]"
                    />
                    <span class="text-sm text-gray-700">Samo na akciji</span>
                  </label>
                </div>
              </div>
            </aside>

            <!-- Products Grid -->
            <div class="lg:col-span-3">
              <div class="mb-6 flex justify-between items-center">
                <h2 class="text-2xl font-bold text-gray-900">
                  {{ selectedCategory ? categoryStore.categories.find(c => c.id === selectedCategory)?.name : 'Svi proizvodi' }}
                </h2>
                <p class="text-gray-600">{{ filteredProducts.length }} proizvoda</p>
              </div>

              <!-- Loading -->
              <div v-if="productStore.loading" class="text-center py-20">
                <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#1565c0]"></div>
                <p class="text-gray-600 mt-4">Učitavanje proizvoda...</p>
              </div>

              <!-- Products Grid -->
              <div
                v-else-if="filteredProducts.length > 0"
                class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6"
              >
                <div
                  v-for="product in filteredProducts"
                  :key="product.id"
                  class="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-xl transition group flex flex-col h-full"
                >
                  <div
                    @click="viewProductDetail(product.id)"
                    class="cursor-pointer flex-1 flex flex-col"
                  >
                    <div class="relative h-56 bg-gray-100 overflow-hidden flex-shrink-0">
                      <img
                        v-if="product.images && product.images.length > 0"
                        :src="`http://localhost:8000${product.images[0].image}`"
                        :alt="product.name"
                        class="w-full h-full object-cover group-hover:scale-110 transition duration-300"
                      />
                      <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                        <span class="text-5xl">📦</span>
                      </div>

                      <div v-if="product.on_sale" class="absolute top-3 right-3 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold shadow-lg">
                        -{{ salePercent(product.price, product.sale_price) }}%
                      </div>
                    </div>

                    <div class="p-5 flex-1 flex flex-col">
                      <p class="text-xs text-[#1565c0] font-semibold mb-1">{{ product.category_name }}</p>
                      <h3 class="font-bold text-gray-900 mb-2 text-lg line-clamp-2">{{ product.name }}</h3>
                      <p class="text-sm text-gray-600 mb-4 line-clamp-2">{{ product.description }}</p>

                      <div class="mt-auto">
                        <div class="flex items-center justify-between mb-3">
                          <div>
                            <p v-if="product.on_sale" class="text-sm text-gray-400 line-through">{{ formatPrice(product.price) }}</p>
                            <p class="text-xl font-bold" :class="product.on_sale ? 'text-red-600' : 'text-green-700'">
                              {{ formatPrice(getProductPrice(product)) }}
                            </p>
                          </div>
                        </div>

                        <!-- Variant Dropdown -->
                        <div v-if="product.variants && product.variants.length > 0" class="mb-3" @click.stop>
                          <label class="block text-xs text-gray-600 mb-1">Dimenzija:</label>
                          <select
                            :value="getSelectedVariant(product)?.id"
                            @change="setSelectedVariant(product.id, product.variants.find(v => v.id == $event.target.value))"
                            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-[#1976d2] focus:border-[#1976d2]"
                          >
                            <option
                              v-for="variant in product.variants"
                              :key="variant.id"
                              :value="variant.id"
                            >
                              {{ variant.name }}
                              <template v-if="variant.price_adjustment !== 0">
                                ({{ variant.price_adjustment > 0 ? '+' : '' }}{{ formatPrice(variant.price_adjustment) }})
                              </template>
                            </option>
                          </select>
                        </div>

                        <!-- Quantity Selector -->
                        <div class="flex items-center gap-2 mb-3" @click.stop>
                          <span class="text-sm text-gray-600">Količina:</span>
                          <div class="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
                            <button
                              @click="setQuantity(product.id, getQuantity(product.id) - 1)"
                              class="w-7 h-7 bg-white rounded hover:bg-gray-200 transition text-sm font-semibold"
                            >
                              -
                            </button>
                            <span class="w-8 text-center text-sm font-semibold">{{ getQuantity(product.id) }}</span>
                            <button
                              @click="setQuantity(product.id, getQuantity(product.id) + 1)"
                              class="w-7 h-7 bg-white rounded hover:bg-gray-200 transition text-sm font-semibold"
                            >
                              +
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="px-5 pb-5 flex-shrink-0">
                    <button
                      @click.stop="addToCartFromCard(product)"
                      :disabled="cartStore.isInCart(product.id, getSelectedVariant(product)?.id)"
                      class="w-full bg-[#1976d2] hover:bg-[#1565c0] text-white font-semibold py-3 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {{ cartStore.isInCart(product.id, getSelectedVariant(product)?.id) ? '✓ Već u korpi' : '+ Dodaj u korpu' }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else class="text-center py-20">
                <span class="text-6xl text-gray-300 mb-4 block">🔍</span>
                <p class="text-xl text-gray-600">Nema proizvoda koji odgovaraju filterima</p>
                <button
                  @click="selectedCategory = null; searchQuery = ''; showOnlyOnSale = false"
                  class="mt-4 text-[#1565c0] hover:underline"
                >
                  Resetuj filtere
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>

    </main>

    <TheFooter />
  </div>
</template>
