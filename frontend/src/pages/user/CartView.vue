<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import ShopHeader from '../../components/ShopHeader.vue'
import { useCartStore } from '../../store/cart'
import { useFilters } from '../../composables/useFilters'

const router = useRouter()
const cartStore = useCartStore()
const { formatPrice } = useFilters()

// Derived values
const cart = computed(() => cartStore.items)
const cartCount = computed(() => cartStore.count)
const subtotal = computed(() => cartStore.subtotal)
const shipping = computed(() => cartStore.shipping)
const total = computed(() => cartStore.total)
const totalItems = computed(() => cartStore.count)

const increaseQuantity = (item) => cartStore.increase(item)
const decreaseQuantity = (item) => cartStore.decrease(item)
const removeFromCart = (item) => {
  if (confirm(`Da li želite da uklonite "${item.name}" iz korpe?`)) {
    cartStore.remove(item)
  }
}
const clearCart = () => {
  if (confirm('Da li ste sigurni da želite da ispraznite korpu?')) {
    cartStore.clear()
  }
}

const goToCheckout = () => {
  alert('Checkout stiže uskoro 🚀')
}

onMounted(() => {
  cartStore.load()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <ShopHeader :cart-count="cartCount" @search="() => {}" />

    <div class="max-w-7xl mx-auto px-5 py-10">

      <router-link 
        to="/" 
        class="inline-flex items-center text-[#3555e4] no-underline font-semibold mb-5 transition-colors hover:text-[#64b5f6]"
      >
        ← Nazad na kupovinu
      </router-link>

      <h1 class="text-4xl font-bold text-gray-800 mb-8">Vaša Korpa</h1>

      <!-- Empty -->
      <div v-if="cart.length === 0" class="text-center py-20 bg-white rounded-xl">
        <span class="text-[100px] block mb-5">🛒</span>
        <h2 class="text-3xl font-bold mb-2.5">Korpa je prazna</h2>
        <p class="text-gray-600 text-lg mb-8">Dodajte proizvode da biste nastavili</p>

        <router-link 
          to="/" 
          class="inline-block px-10 py-4 bg-gradient-to-r from-[#3555e4] to-[#64b5f6] text-white rounded-full font-semibold transition-transform hover:scale-105 no-underline"
        >
          Pogledaj Proizvode
        </router-link>
      </div>

      <!-- Not empty -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-[1fr_400px] gap-8">

        <!-- Items -->
        <div class="flex flex-col gap-5">
          <div 
            v-for="item in cart" 
            :key="item.id"
            class="bg-white rounded-xl p-5 grid grid-cols-[100px_1fr_auto_auto_auto] gap-5 items-center"
          >
            <div class="w-[100px] h-[100px] rounded-lg overflow-hidden bg-gray-100">
              <img 
                :src="item.image || 'https://via.placeholder.com/100x100?text=Proizvod'"
                class="w-full h-full object-cover"
              />
            </div>

            <div>
              <h3 class="text-lg font-semibold text-gray-800 mb-1">{{ item.name }}</h3>
              <p class="text-[#3555e4] font-semibold">{{ formatPrice(item.price) }}</p>
            </div>

            <div class="flex items-center gap-2.5 bg-gray-100 rounded-full p-1">
              <button 
                @click="decreaseQuantity(item)"
                :disabled="item.quantity <= 1"
                class="w-8 h-8 bg-white rounded-full text-[#3555e4] hover:bg-[#3555e4] hover:text-white disabled:opacity-30"
              >-</button>

              <span class="min-w-[30px] text-center font-semibold">
                {{ item.quantity }}
              </span>

              <button 
                @click="increaseQuantity(item)"
                class="w-8 h-8 bg-white rounded-full text-[#3555e4] hover:bg-[#3555e4] hover:text-white"
              >+</button>
            </div>

            <div class="min-w-[120px] text-right">
              <p class="text-xl font-bold text-green-700">
                {{ formatPrice(item.price * item.quantity) }}
              </p>
            </div>

            <button 
              @click="removeFromCart(item)"
              class="w-10 h-10 bg-red-50 hover:bg-[#e74c3c] rounded-lg text-xl hover:text-white"
            >
              🗑️
            </button>
          </div>
        </div>

        <!-- Summary -->
        <div class="bg-white rounded-xl p-8 h-fit sticky top-[100px]">
          <h2 class="text-2xl font-bold text-gray-800 mb-5">Rezime narudžbine</h2>

          <div class="flex justify-between text-gray-600 mb-4">
            <span>Proizvodi ({{ totalItems }})</span>
            <span>{{ formatPrice(subtotal) }}</span>
          </div>

          <div class="flex justify-between text-gray-600 mb-4">
            <span>Dostava</span>
            <span :class="shipping === 0 ? 'text-green-600 font-semibold' : ''">
              {{ shipping === 0 ? 'Besplatno' : formatPrice(shipping) }}
            </span>
          </div>

         

          <div class="border-t my-5"></div>

          <div class="flex justify-between text-2xl font-bold text-gray-800 mb-5">
            <span>Ukupno</span>
            <span>{{ formatPrice(total) }}</span>
          </div>

          <button 
            @click="goToCheckout"
            class="w-full py-4 bg-gradient-to-r from-[#3555e4] to-[#64b5f6] text-white rounded-lg text-lg font-semibold hover:-translate-y-0.5"
          >
            Nastavi ka poručivanju
          </button>

          <button 
            @click="clearCart"
            class="w-full py-3 mt-3 bg-gray-100 hover:bg-gray-200 rounded-lg font-semibold text-gray-600"
          >
            Isprazni korpu
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
