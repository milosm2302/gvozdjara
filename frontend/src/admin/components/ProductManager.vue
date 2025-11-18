<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProductStore } from '@/admin/store/products'
import { useCategoryStore } from '@/admin/store/categories'
import { useSubcategoryStore } from '@/admin/store/subcategories'

const emit = defineEmits(['update-count'])

const productStore = useProductStore()
const categoryStore = useCategoryStore()
const subcategoryStore = useSubcategoryStore()

// UI
const showModal = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const error = ref('')
const loading = ref(false)

const filterCategory = ref('')
const searchQuery = ref('')

// Form
const form = ref({
  id: null,
  name: '',
  description: '',
  price: '',
  category: '',
  subcategory: '',
  on_sale: false,
  sale_price: ''
})

// Filtered subcategories
const filteredSubcategories = computed(() => {
  if (!form.value.category) return []
  return subcategoryStore.list.filter(s => s.category === form.value.category)
})

// Filtered products
const filteredProducts = computed(() => {
  let result = [...productStore.list]

  if (filterCategory.value) {
    result = result.filter(p => Number(p.category) === Number(filterCategory.value))
  }

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(
      p =>
        p.name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q)
    )
  }

  return result
})

// Price formatting
const formatPrice = price =>
  new Intl.NumberFormat('sr-RS', {
    style: 'currency',
    currency: 'RSD'
  }).format(price)

// Modal
const openAddModal = () => {
  if (categoryStore.list.length === 0) {
    alert('Najpre dodaj kategoriju!')
    return
  }

  isEditing.value = false
  form.value = {
    id: null,
    name: '',
    description: '',
    price: '',
    category: '',
    subcategory: '',
    on_sale: false,
    sale_price: ''
  }

  showModal.value = true
}

const openEditModal = product => {
  isEditing.value = true
  form.value = { ...product }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  error.value = ''
}

// Save
const saveProduct = async () => {
  saving.value = true
  error.value = ''

  try {
    const data = {
      name: form.value.name,
      description: form.value.description,
      price: parseFloat(form.value.price),
      category: form.value.category,
      subcategory: form.value.subcategory || null,
      on_sale: form.value.on_sale,
      sale_price:
        form.value.on_sale && form.value.sale_price
          ? parseFloat(form.value.sale_price)
          : null
    }

    if (isEditing.value) {
      await productStore.update(form.value.id, data)
    } else {
      await productStore.create(data)
    }

    emit('update-count')
    closeModal()
  } catch (err) {
    console.error(err)
    error.value = 'Greška pri čuvanju proizvoda.'
  } finally {
    saving.value = false
  }
}

// Delete
const deleteProduct = async product => {
  if (!confirm(`Obrisati proizvod "${product.name}"?`)) return
  await productStore.remove(product.id)
  emit('update-count')
}

// On load
onMounted(async () => {
  loading.value = true
  await categoryStore.fetch()
  await subcategoryStore.fetch()
  await productStore.fetch()
  loading.value = false
})
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-2xl font-bold">Proizvodi</h2>

      <button
        @click="openAddModal"
        class="px-6 py-3 bg-gradient-to-r from-[#3555e4] to-[#64b5f6] text-white rounded-md font-semibold hover:-translate-y-0.5 transition"
      >
        + Dodaj Proizvod
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-10 text-gray-600 text-lg">
      Učitavanje...
    </div>

    <!-- List -->
    <div
      v-else-if="Array.isArray(filteredProducts) && filteredProducts.length > 0"
      class="grid grid-cols-[repeat(auto-fill,minmax(350px,1fr))] gap-5"
    >
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-lg transition"
      >
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-semibold">{{ product.name }}</h3>

          <span
            v-if="product.on_sale"
            class="px-3 py-1 bg-red-500 text-white rounded text-xs"
          >
            AKCIJA
          </span>
        </div>

        <p class="text-sm text-blue-600">
          {{ product.category_name }}
          <span v-if="product.subcategory_name"> / {{ product.subcategory_name }}</span>
        </p>

        <p class="text-gray-600 text-sm mt-2">
          {{ product.description }}
        </p>

        <div class="mt-4 flex items-center gap-2">
          <span v-if="product.on_sale" class="line-through text-gray-400">
            {{ formatPrice(product.price) }}
          </span>

          <span class="text-green-700 font-bold text-xl">
            {{ formatPrice(product.current_price) }}
          </span>
        </div>

        <div class="flex gap-2 mt-5">
          <button
            @click="openEditModal(product)"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md"
          >
            Izmeni
          </button>

          <button
            @click="deleteProduct(product)"
            class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md"
          >
            Obriši
          </button>
        </div>
      </div>
    </div>

    <!-- Empty -->
    <div v-else class="py-16 text-center text-gray-400">
      Nema proizvoda. Dodaj prvi proizvod!
    </div>

    <!-- MODAL -->
    <div
      v-if="showModal"
      @click.self="closeModal"
      class="fixed inset-0 bg-black/50 flex justify-center items-center p-5 z-[1000]"
    >
      <div class="bg-white rounded-xl w-full max-w-[600px] shadow-xl overflow-y-auto max-h-[90vh]">
        
        <div class="p-6 border-b flex justify-between items-center">
          <h3 class="text-xl font-semibold">
            {{ isEditing ? "Izmeni proizvod" : "Novi proizvod" }}
          </h3>

          <button @click="closeModal" class="text-3xl text-gray-500">&times;</button>
        </div>

        <form @submit.prevent="saveProduct" class="p-6">
          <!-- NAME -->
          <label class="block font-medium mb-1">Naziv *</label>
          <input v-model="form.name" required class="w-full px-3 py-2 border rounded" />

          <!-- DESCRIPTION -->
          <label class="block font-medium mt-5 mb-1">Opis *</label>
          <textarea
            v-model="form.description"
            rows="4"
            class="w-full px-3 py-2 border rounded resize-none"
          ></textarea>

          <!-- PRICE -->
          <label class="block font-medium mt-5 mb-1">Cena (RSD) *</label>
          <input v-model="form.price" type="number" required class="w-full px-3 py-2 border rounded" />

          <!-- CATEGORY -->
          <label class="block font-medium mt-5 mb-1">Kategorija *</label>
          <select v-model="form.category" class="w-full px-3 py-2 border rounded" required>
            <option value="">Izaberi kategoriju</option>
            <option v-for="c in categoryStore.list" :value="c.id" :key="c.id">
              {{ c.name }}
            </option>
          </select>

          <!-- SUBCATEGORY -->
          <label class="block font-medium mt-5 mb-1">Podkategorija</label>
          <select v-model="form.subcategory" class="w-full px-3 py-2 border rounded">
            <option value="">Bez podkategorije</option>
            <option
              v-for="s in filteredSubcategories"
              :key="s.id"
              :value="s.id"
            >
              {{ s.name }}
            </option>
          </select>

          <!-- On sale -->
          <label class="flex items-center mt-5 text-sm gap-2 cursor-pointer">
            <input v-model="form.on_sale" type="checkbox" />
            <span>Proizvod je na akciji</span>
          </label>

          <div v-if="form.on_sale">
            <label class="block font-medium mt-5 mb-1">Akcijska cena *</label>
            <input
              v-model="form.sale_price"
              type="number"
              class="w-full px-3 py-2 border rounded"
            />
          </div>

          <!-- ERROR -->
          <p v-if="error" class="text-red-600 mt-3">{{ error }}</p>

          <!-- BUTTONS -->
          <div class="flex justify-end gap-3 mt-8">
            <button
              type="button"
              @click="closeModal"
              class="px-5 py-2 bg-gray-300 rounded"
            >
              Otkaži
            </button>

            <button
              type="submit"
              :disabled="saving"
              class="px-5 py-2 bg-blue-600 text-white rounded disabled:opacity-60"
            >
              {{ saving ? "Čuvanje..." : "Sačuvaj" }}
            </button>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>
