<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

import CategoryManager from '../components/CategoryManager.vue'
import SubcategoryManager from '../components/SubcategoryManager.vue'
import ProductManager from '../components/ProductManager.vue'

import { useAdminNav } from '../composables/useAdminNav'
import { useAdminStatsStore } from '../store/adminStats'

const router = useRouter()
const authStore = useAuthStore()

const { activeView, setView, views } = useAdminNav()
const statsStore = useAdminStatsStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/admin/login')
}

onMounted(() => {
  statsStore.refresh()
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">

    <!-- Header -->
    <header class="bg-white px-10 py-5 shadow-md flex justify-between items-center sticky top-0 z-[100]">
      <h1 class="text-2xl font-bold text-gray-800">Gvozdara Shop - Admin Panel</h1>

      <div class="flex items-center gap-4">
        <span class="font-semibold text-gray-800">{{ authStore.user?.username }}</span>
        <button 
          @click="handleLogout"
          class="px-5 py-2.5 bg-red-600 text-white rounded-md font-semibold hover:bg-red-700"
        >
          Logout
        </button>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden flex-col md:flex-row">

      <!-- Sidebar -->
      <aside class="w-full md:w-[280px] bg-white border-r border-gray-200 overflow-y-auto md:sticky md:top-[72px] md:h-[calc(100vh-72px)]">
        <nav class="p-5">

          <h3 class="text-xs uppercase text-gray-400 font-bold mb-3 ml-2.5">
            Katalog
          </h3>

          <!-- Dinamička navigacija -->
          <button
            v-for="v in views"
            :key="v.id"
            @click="setView(v.id)"
            :class="activeView === v.id 
              ? 'bg-gradient-to-r from-[#3555e4] to-[#64b5f6] text-white' 
              : 'bg-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-800'"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer mb-1"
          >
            <span class="text-xl">{{ v.icon }}</span>
            <span>{{ v.label }}</span>

            <span 
              class="ml-auto px-2 py-0.5 rounded-full text-xs font-semibold"
              :class="activeView === v.id ? 'bg-white/30' : 'bg-black/10'"
            >
              {{
                v.id === 'categories' ? statsStore.categories :
                v.id === 'subcategories' ? statsStore.subcategories :
                statsStore.products
              }}
            </span>
          </button>

          <!-- Statistika -->
          <div class="mt-8 bg-gradient-to-r from-[#3555e4] to-[#64b5f6] p-5 rounded-xl text-white">
            <div class="flex justify-between mb-3">
              <span class="text-xs opacity-90">Ukupno proizvoda</span>
              <span class="text-2xl font-bold">{{ statsStore.products }}</span>
            </div>

            <div class="flex justify-between">
              <span class="text-xs opacity-90">Kategorija</span>
              <span class="text-2xl font-bold">{{ statsStore.categories }}</span>
            </div>
          </div>

        </nav>
      </aside>
        
      <!-- Main content -->
      <main class="flex-1 overflow-y-auto p-8 max-w-[1400px] mx-auto">

        <CategoryManager 
          v-if="activeView === 'categories'"
          @update-count="statsStore.refresh"
        />

        <SubcategoryManager 
          v-if="activeView === 'subcategories'"
          @update-count="statsStore.refresh"
        />

        <ProductManager 
          v-if="activeView === 'products'"
          @update-count="statsStore.refresh"
        />

      </main>
    </div>
  </div>
</template>
