<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCategoryStore } from '@/admin/store/categories'
import { useSubcategoryStore } from '@/admin/store/subcategories'

const emit = defineEmits(['update-count'])

const categoryStore = useCategoryStore()
const subcategoryStore = useSubcategoryStore()

// UI
const showModal = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const loading = ref(false)
const error = ref('')

// Form
const form = ref({
  id: null,
  name: '',
  category: '',
  description: ''
})

// Computed — subcategories list
const subcategories = computed(() => subcategoryStore.list)
const categories = computed(() => categoryStore.list)

// Modal — open add
const openAddModal = () => {
  if (categories.value.length === 0) {
    alert("Prvo dodaj kategoriju!")
    return
  }

  isEditing.value = false
  form.value = { id: null, name: '', category: '', description: '' }
  showModal.value = true
  error.value = ''
}

// Modal — open edit
const openEditModal = (sub) => {
  isEditing.value = true
  form.value = {
    id: sub.id,
    name: sub.name,
    category: sub.category,
    description: sub.description || ''
  }
  showModal.value = true
  error.value = ''
}

// Close modal
const closeModal = () => {
  showModal.value = false
  form.value = { id: null, name: '', category: '', description: '' }
  error.value = ''
}

// Save subcategory
const saveSubcategory = async () => {
  saving.value = true
  error.value = ''

  try {
    const payload = {
      name: form.value.name,
      category: form.value.category,
      description: form.value.description
    }

    if (isEditing.value) {
      await subcategoryStore.update(form.value.id, payload)
    } else {
      await subcategoryStore.create(payload)
    }

    emit('update-count')
    closeModal()

  } catch (err) {
    console.error(err)
    error.value = 'Greška pri čuvanju. Proveri da li naziv već postoji.'
  } finally {
    saving.value = false
  }
}

// Delete subcategory
const deleteSubcategory = async (sub) => {
  if (!confirm(`Obrisati podkategoriju "${sub.name}"?`)) return

  try {
    await subcategoryStore.remove(sub.id)
    emit('update-count')
  } catch (err) {
    console.error(err)
    alert('Greška pri brisanju. Možda postoje proizvodi u ovoj podkategoriji.')
  }
}

// Load data
onMounted(async () => {
  loading.value = true
  await categoryStore.fetch()
  await subcategoryStore.fetch()
  loading.value = false
})
</script>

<template>
  <div>
    <!-- HEADER -->
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-2xl font-bold">Podkategorije</h2>

      <button
        @click="openAddModal"
        class="px-6 py-3 bg-gradient-to-r from-[#3555e4] to-[#64b5f6] text-white rounded-md font-semibold hover:-translate-y-0.5 transition"
      >
        + Dodaj Podkategoriju
      </button>
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="text-center py-10 text-gray-600 text-lg">
      Učitavanje...
    </div>

    <!-- LIST -->
    <div
      v-else-if="subcategories.length > 0"
      class="flex flex-col gap-5"
    >
      <div
        v-for="sub in subcategories"
        :key="sub.id"
        class="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-lg transition flex justify-between items-center"
      >
        <div class="flex-1">
          <h3 class="text-xl font-semibold mb-2">{{ sub.name }}</h3>

          <p class="inline-block px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold">
            {{ sub.category_name }}
          </p>

          <p v-if="sub.description" class="text-gray-600 text-sm mt-2">
            {{ sub.description }}
          </p>
        </div>

        <div class="flex gap-3 ml-5">
          <button
            @click="openEditModal(sub)"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md"
          >
            Izmeni
          </button>

          <button
            @click="deleteSubcategory(sub)"
            class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md"
          >
            Obriši
          </button>
        </div>
      </div>
    </div>

    <!-- EMPTY -->
    <div v-else class="py-16 text-center text-gray-400">
      <p v-if="categories.length === 0">
        Prvo dodaj kategorije.
      </p>
      <p v-else>
        Nema podkategorija. Dodaj prvu podkategoriju!
      </p>
    </div>

    <!-- MODAL -->
    <div
      v-if="showModal"
      @click.self="closeModal"
      class="fixed inset-0 bg-black/50 flex justify-center items-center p-5 z-[1000]"
    >
      <div class="bg-white rounded-xl w-full max-w-[500px] shadow-2xl">

        <div class="flex justify-between items-center p-6 border-b">
          <h3 class="text-xl font-semibold">
            {{ isEditing ? "Izmeni Podkategoriju" : "Nova Podkategorija" }}
          </h3>

          <button @click="closeModal" class="text-3xl text-gray-500 hover:text-gray-800">
            &times;
          </button>
        </div>

        <form @submit.prevent="saveSubcategory" class="p-6">

          <!-- CATEGORY -->
          <label class="block mb-1 font-medium">Kategorija *</label>
          <select
            v-model="form.category"
            required
            class="w-full px-3 py-2 border rounded"
          >
            <option value="">Izaberi kategoriju</option>

            <option
              v-for="cat in categories"
              :key="cat.id"
              :value="cat.id"
            >
              {{ cat.name }}
            </option>
          </select>

          <!-- NAME -->
          <label class="block mt-5 mb-1 font-medium">Naziv *</label>
          <input
            v-model="form.name"
            required
            class="w-full px-3 py-2 border rounded"
          />

          <!-- DESCRIPTION -->
          <label class="block mt-5 mb-1 font-medium">Opis</label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border rounded resize-none"
          ></textarea>

          <!-- ERROR -->
          <p v-if="error" class="text-red-600 mt-3">{{ error }}</p>

          <!-- BUTTONS -->
          <div class="flex justify-end gap-3 mt-8">
            <button
              type="button"
              @click="closeModal"
              class="px-5 py-2 bg-gray-300 rounded hover:bg-gray-400"
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
