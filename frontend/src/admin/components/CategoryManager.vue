<script setup>
import { ref, onMounted } from 'vue'
import { useCategoryStore } from '@/admin/store/categories'
import ConfirmModal from '@/components/ConfirmModal.vue'

const emit = defineEmits(['update-count'])

const categoryStore = useCategoryStore()

// Confirm modal
const showConfirm = ref(false)
const confirmMessage = ref("")
const confirmAction = ref(null)

const openConfirm = (message, action) => {
  confirmMessage.value = message
  confirmAction.value = action
  showConfirm.value = true
}

const closeConfirm = () => {
  showConfirm.value = false
  confirmMessage.value = ""
  confirmAction.value = null
}

const doConfirm = () => {
  if (confirmAction.value) confirmAction.value()
  closeConfirm()
}

// Form modal
const showModal = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const error = ref('')

const form = ref({
  id: null,
  name: '',
  description: ''
})

const openAddModal = () => {
  isEditing.value = false
  form.value = { id: null, name: '', description: '' }
  showModal.value = true
  error.value = ''
}

const openEditModal = (cat) => {
  isEditing.value = true
  form.value = {
    id: cat.id,
    name: cat.name,
    description: cat.description || ''
  }
  showModal.value = true
  error.value = ''
}

const closeModal = () => {
  showModal.value = false
  form.value = { id: null, name: '', description: '' }
  error.value = ''
}

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
    error.value = 'Greška pri čuvanju kategorije.'
  } finally {
    saving.value = false
  }
}

const deleteCategory = (cat) => {
  openConfirm(
    `Da li želiš da obrišeš "${cat.name}"?`,
    async () => {
      try {
        await categoryStore.remove(cat.id)
        emit('update-count')
      } catch {
        openConfirm("Ne može da se obriše kategorija jer ima proizvode!", null)
      }
    }
  )
}

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

      <button
        @click="openAddModal"
        class="px-6 py-3 bg-gradient-to-r from-[#3555e4] to-[#64b5f6]
               text-white rounded-lg shadow hover:shadow-md active:scale-95 transition cursor-pointer"
      >
        + Dodaj Kategoriju
      </button>
    </div>

    <!-- Loading -->
    <div v-if="categoryStore.loading" class="text-center py-10 text-gray-600">
      Učitavanje...
    </div>

    <!-- List -->
    <div v-else-if="categoryStore.list.length > 0" class="flex flex-col gap-5">
      <div
        v-for="cat in categoryStore.list"
        :key="cat.id"
        class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm 
               hover:shadow-lg transition flex justify-between items-center"
      >
        <div class="flex-1">
          <h3 class="text-xl font-semibold">{{ cat.name }}</h3>

          <p v-if="cat.description" class="text-gray-600 text-sm mt-1">
            {{ cat.description }}
          </p>

          <span
            class="inline-block mt-3 px-3 py-1 bg-green-50 text-green-700 rounded-full
                   text-xs font-semibold"
          >
            {{ cat.product_count || 0 }} proizvoda
          </span>
        </div>

        <div class="flex gap-3 cursor-pointer">
          <button
            @click="openEditModal(cat)"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700
                   transition cursor-pointer"
          >
            Izmeni
          </button>

          <button
            @click="deleteCategory(cat)"
            class="px-4 py-2 bg-red-600 text-white rounded-lg shadow hover:bg-red-700
                   transition cursor-pointer"
          >
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
    <div
      v-if="showModal"
      @click.self="closeModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center p-4
             z-[1000] animate-fade-in"
    >
      <div
        class="bg-white rounded-3xl w-full max-w-[650px] shadow-2xl overflow-hidden 
               animate-slide-up"
      >
        <!-- HEADER -->
        <div class="px-10 py-7 bg-gradient-to-r from-blue-600 to-blue-500 flex justify-between items-center">
          <h3 class="text-2xl font-semibold text-white">
            {{ isEditing ? 'Izmeni Kategoriju' : 'Nova Kategorija' }}
          </h3>

          <button
            @click="closeModal"
            class="text-white text-4xl leading-none hover:scale-125 transition cursor-pointer"
          >
            &times;
          </button>
        </div>

        <!-- FORM -->
        <form @submit.prevent="saveCategory" class="px-10 py-8 space-y-6">
          <div>
            <label class="block mb-2 font-medium text-gray-800">Naziv *</label>
            <input
              v-model="form.name"
              required
              class="w-full px-4 py-3 rounded-xl bg-gray-100 border border-gray-200
                     focus:ring-2 focus:ring-blue-400 focus:outline-none transition shadow-sm"
            />
          </div>

          <div>
            <label class="block mb-2 font-medium text-gray-800">Opis</label>
            <textarea
              v-model="form.description"
              rows="3"
              class="w-full px-4 py-3 rounded-xl bg-gray-100 border border-gray-200
                     focus:ring-2 focus:ring-blue-400 focus:outline-none transition shadow-sm resize-none"
            ></textarea>
          </div>

          <p v-if="error" class="text-red-600 font-medium">{{ error }}</p>

          <!-- BUTTONS -->
          <div class="flex justify-end gap-4 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-6 py-3 bg-gray-300 rounded-xl font-semibold hover:bg-gray-400
                     transition cursor-pointer"
            >
              Otkaži
            </button>

            <button
              type="submit"
              :disabled="saving"
              class="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow
                     hover:bg-blue-700 transition cursor-pointer disabled:opacity-60"
            >
              {{ saving ? 'Čuvanje...' : 'Sačuvaj' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirm Modal -->
    <ConfirmModal
      :show="showConfirm"
      :message="confirmMessage"
      title="Potvrda"
      confirmText="Obriši"
      cancelText="Odustani"
      @confirm="doConfirm"
      @cancel="closeConfirm"
    />
  </div>
</template>

<style>
@layer utilities {
  .animate-fade-in {
    animation: fadeIn 0.25s ease-out;
  }
  .animate-slide-up {
    animation: slideUp 0.3s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0 }
    to   { opacity: 1 }
  }

  @keyframes slideUp {
    from { opacity: 0; transform: translateY(25px); }
    to   { opacity: 1; transform: translateY(0); }
  }
}
</style>
