<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/store/cart'

const router = useRouter()
const cartStore = useCartStore()

const mobileMenuOpen = ref(false)

const cartItemCount = computed(() => cartStore.itemCount)

const navigateTo = (route) => {
  router.push(route)
  mobileMenuOpen.value = false
}
</script>

<template>
  <header class="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white sticky top-0 z-50 shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-20">

        <!-- Logo -->
        <div class="flex items-center gap-3 cursor-pointer" @click="navigateTo('/')">
          <img src="/logo.png" alt="Beta Pack Logo" class="h-12 w-auto" />
          <div class="text-xl font-bold text-white">
            BETA PACK
          </div>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center gap-8">
          <button
            @click="navigateTo('/')"
            class="text-gray-300 hover:text-white hover:bg-white/10 px-4 py-2 rounded-lg transition font-medium"
          >
            Prodavnica
          </button>
          <button
            @click="navigateTo('/o-nama')"
            class="text-gray-300 hover:text-white hover:bg-white/10 px-4 py-2 rounded-lg transition font-medium"
          >
            O nama
          </button>
          <button
            @click="navigateTo('/kontakt')"
            class="text-gray-300 hover:text-white hover:bg-white/10 px-4 py-2 rounded-lg transition font-medium"
          >
            Kontakt
          </button>
        </nav>

        <!-- Cart & Actions -->
        <div class="flex items-center gap-4">
          <!-- Cart -->
          <button
            @click="navigateTo('/cart')"
            class="relative flex items-center gap-2 bg-[#1976d2] hover:bg-[#1565c0] px-5 py-2.5 rounded-lg transition font-semibold"
          >
            <span class="text-xl">🛒</span>
            <span class="hidden sm:inline">Korpa</span>
            <span
              v-if="cartItemCount > 0"
              class="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center"
            >
              {{ cartItemCount }}
            </span>
          </button>

          <!-- Mobile menu button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden text-gray-300 hover:text-white p-2"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <div
      v-if="mobileMenuOpen"
      class="md:hidden bg-gray-800 border-t border-gray-700"
    >
      <nav class="px-4 py-4 space-y-2">
        <button
          @click="navigateTo('/')"
          class="block w-full text-left text-gray-300 hover:text-white hover:bg-white/10 px-4 py-3 rounded-lg transition font-medium"
        >
          Prodavnica
        </button>
        <button
          @click="navigateTo('/o-nama')"
          class="block w-full text-left text-gray-300 hover:text-white hover:bg-white/10 px-4 py-3 rounded-lg transition font-medium"
        >
          O nama
        </button>
        <button
          @click="navigateTo('/kontakt')"
          class="block w-full text-left text-gray-300 hover:text-white hover:bg-white/10 px-4 py-3 rounded-lg transition font-medium"
        >
          Kontakt
        </button>
      </nav>
    </div>
  </header>
</template>
