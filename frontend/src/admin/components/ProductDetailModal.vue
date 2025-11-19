<script setup>
import { ref, computed } from 'vue'
import ProductVariantManager from './ProductVariantManager.vue'
import ProductImageManager from './ProductImageManager.vue'

const props = defineProps({
  product: Object,
  show: Boolean
})

const emit = defineEmits(['close', 'updated'])

const activeTab = ref('variants')

const tabs = [
  { id: 'variants', label: 'Varijante' },
  { id: 'images', label: 'Slike' }
]

const close = () => {
  emit('close')
}

const handleUpdate = () => {
  emit('updated')
}
</script>

<template>
  <div
    v-if="show && product"
    @click.self="close"
    class="fixed inset-0 bg-black/60 flex items-center justify-center p-5 z-[1500]"
  >
    <div class="bg-white rounded-xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">

      <!-- Header -->
      <div class="p-6 border-b flex justify-between items-center bg-gradient-to-r from-blue-600 to-blue-500 text-white">
        <div>
          <h2 class="text-2xl font-bold">{{ product.name }}</h2>
          <p class="text-sm opacity-90">{{ product.category_name }}</p>
        </div>
        <button @click="close" class="text-3xl hover:bg-white/20 rounded px-2">&times;</button>
      </div>

      <!-- Tabs -->
      <div class="flex border-b bg-gray-50">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="activeTab === tab.id
            ? 'bg-white text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-600 hover:bg-gray-100'"
          class="px-6 py-3 font-medium transition"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto p-6">
        <ProductVariantManager
          v-if="activeTab === 'variants'"
          :product-id="product.id"
          @updated="handleUpdate"
        />

        <ProductImageManager
          v-if="activeTab === 'images'"
          :product-id="product.id"
          @updated="handleUpdate"
        />
      </div>

    </div>
  </div>
</template>
