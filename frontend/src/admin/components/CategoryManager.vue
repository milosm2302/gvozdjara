<script setup>
import { ref, onMounted } from 'vue'
import { useCategoryStore } from '@/admin/store/categories'

const emit = defineEmits(['update-count'])

const categoryStore = useCategoryStore()

// Modal state
const showModal = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const error = ref('')

const form = ref({
  id: null,
  name: '',
  description: ''
})

// Modal kontrola
const openAddModal = () => {
  isEditing.value = false
  form.value = { id: null, name: '', description: '' }
  showModal.value = true
  error.value = ''
}

const openEditModal = (category) => {
  isEditing.value = true
  form.value = {
    id: category.id,
    name: category.name,
    description: category.description || ''
  }
  showModal.value = true
  error.value = ''
}

const closeModal = () => {
  showModal.value = false
  form.value = { id: null, name: '', description: '' }
  error.value = ''
}

// Save
const saveCategory = async () => {
  saving.value = true
  error.value = ''

  try {
    const payload = {
      name: form.value.name,
      description: form.value.description
    }

    if (isEditing.value) {
      await categoryStore.update(form.value.id, payload)
    } else {
      await categoryStore.create(payload)
    }

    emit('update-count')
    closeModal()

  } catch (err) {
    console.error(err)
    error.value = 'Greška pri čuvanju kategorije'
  } finally {
    saving.value = false
  }
}

// Delete
const deleteCategory = async (category) => {
  if (!confirm(`Da li želiš da obrišeš "${category.name}"?`)) return

  try {
    await categoryStore.remove(category.id)
    emit('update-count')
  } catch (err) {
    console.error(err)
    alert('Greška pri brisanju kategorije (možda ima proizvoda).')
  }
}

// Fetch on mount
onMounted(() => {
  categoryStore.fetch()
  emit('update-count')
})
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-2xl font-bold text-gray-800">Kategorije</h2>
      <button @click="openAddModal"
        class="px-6 py-3 bg-gradient-to-r from-[#3555e4] to-[#64b5f6] text-white rounded-md">
        + Dodaj Kategoriju
      </button>
    </div>

    <!-- Loading -->
    <div v-if="categoryStore.loading" class="text-center py-10 text-gray-600">
      Učitavanje...
    </div>

    <!-- Lista -->
    <div v-else-if="categoryStore.list.length > 0" class="flex flex-col gap-5">
      <div v-for="category in categoryStore.list" :key="category.id"
        class="bg-white border border-gray-200 rounded-lg p-5 flex justify-between items-center">

        <div class="flex-1">
          <h3 class="text-xl font-semibold">{{ category.name }}</h3>
          <p v-if="category.description" class="text-gray-600 text-sm">
            {{ category.description }}
          </p>
          <span class="inline-block px-3 py-1 bg-green-50 text-green-800 rounded-full text-xs font-semibold">
            {{ category.product_count || 0 }} proizvoda
          </span>
        </div>

        <div class="flex gap-2.5">
          <button @click="openEditModal(category)"
            class="px-4 py-2 bg-blue-600 text-white rounded-md">
            Izmeni
          </button>

          <button @click="deleteCategory(category)"
            class="px-4 py-2 bg-red-600 text-white rounded-md">
            Obriši
          </button>
        </div>
      </div>
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-16 text-gray-400">
      <p class="text-lg">Nema kategorija. Dodaj prvu!</p>
    </div>

    <!-- Modal -->
    <div v-if="showModal" @click.self="closeModal"
      class="fixed inset-0 bg-black/50 flex justify-center items-center p-5">

      <div class="bg-white rounded-xl w-full max-w-[500px] shadow-2xl">
        <div class="flex justify-between items-center px-8 py-5 border-b">
          <h3 class="text-xl font-semibold">
            {{ isEditing ? 'Izmeni Kategoriju' : 'Nova Kategorija' }}
          </h3>
          <button @click="closeModal" class="text-4xl text-gray-400 hover:text-gray-800">
            &times;
          </button>
        </div>

        <form @submit.prevent="saveCategory" class="p-8">
          <div class="mb-5">
            <label class="block mb-2">Naziv*</label>
            <input v-model="form.name" required class="w-full px-3 py-3 border rounded-md" />
          </div>

          <div class="mb-5">
            <label class="block mb-2">Opis</label>
            <textarea v-model="form.description" rows="3" class="w-full px-3 py-3 border rounded-md"></textarea>
          </div>

          <p v-if="error" class="text-red-600 my-4">{{ error }}</p>

          <div class="flex justify-end gap-2.5">
            <button type="button" @click="closeModal" class="px-6 py-3 bg-gray-500 text-white rounded-md">
              Otkaži
            </button>

            <button type="submit" :disabled="saving"
              class="px-6 py-3 bg-gradient-to-r from-[#3555e4] to-[#64b5f6] text-white rounded-md">
              {{ saving ? 'Čuvanje...' : 'Sačuvaj' }}
            </button>
          </div>
        </form>

      </div>

    </div>
  </div>
</template>
