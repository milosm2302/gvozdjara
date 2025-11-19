<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCategoryStore } from '@/admin/store/categories'
import { useSubcategoryStore } from '@/admin/store/subcategories'
import ConfirmModal from '@/components/ConfirmModal.vue'

const emit = defineEmits(['update-count'])

const categoryStore = useCategoryStore()
const subcategoryStore = useSubcategoryStore()

// Confirm modal
const showConfirm = ref(false)
const confirmMessage = ref("")
const confirmAction = ref(null)

const openConfirm = (msg, action) => {
  confirmMessage.value = msg
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

// Data
const subcategories = computed(() => subcategoryStore.list)
const categories = computed(() => categoryStore.list)

// Modal — Add
const openAddModal = () => {
  if (categories.value.length === 0) {
    openConfirm("Prvo dodaj kategoriju!", null)
    return
  }

  isEditing.value = false
  form.value = { id: null, name: '', category: '', description: '' }
  showModal.value = true
  error.value = ''
}

// Modal — Edit
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

// Delete — using ConfirmModal
const deleteSubcategory = (sub) => {
  openConfirm(
    `Obrisati podkategoriju "${sub.name}"?`,
    async () => {
      try {
        await subcategoryStore.remove(sub.id)
        emit('update-count')
      } catch (err) {
        console.error(err)
        openConfirm(
          "Ne može da se obriše podkategorija! Moguće da postoje proizvodi u njoj.",
          null
        )
      }
    }
  )
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
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-2xl font-bold">Podkategorije</h2>

      <button
        @click="openAddModal"
        class="px-6 py-3 bg-gradient-to-r from-[#3555e4] to-[#64b5f6] text-white rounded-md font-semibold hover:-translate-y-0.5 transition"
      >
        + Dodaj Podkategoriju
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-10 text-gray-600 text-lg">
      Učitavanje...
    </div>

    <!-- List -->
    <div v-else-if="subcategories.length > 0" class="flex flex-col gap-5">
      <div
        v-for="sub in subcategories"
        :key="sub.id"
        class="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-lg transition flex justify-between items-center"
      >
        <div class="flex-1">
          <h3 class="text-xl font-semibold">{{ sub.name }}</h3>
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

    <!-- Empty -->
    <div v-else class="py-16 text-center text-gray-400">
      <p v-if="categories.length === 0">Prvo dodaj kategorije.</p>
      <p v-else>Nema podkategorija. Dodaj prvu podkategoriju!</p>
    </div>

    <!-- Modal -->
   <!-- MODAL -->
<!-- MODAL -->
<div
  v-if="showModal"
  @click.self="closeModal"
  class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center p-4 z-[1000]
         transition-opacity duration-300 animate-fadeIn"
>

  <div
    class="bg-white rounded-3xl w-full max-w-[820px] shadow-[0_20px_60px_rgba(0,0,0,0.15)]
           overflow-hidden animate-slideUp"
  >

    <!-- HEADER -->
    <div class="px-10 py-7 bg-gradient-to-r from-blue-600 to-blue-500 flex justify-between items-center">
      <h3 class="text-2xl font-semibold text-white tracking-wide">
        {{ isEditing ? "Izmeni Podkategoriju" : "Nova Podkategorija" }}
      </h3>

      <button
        @click="closeModal"
        class="text-white text-4xl leading-none hover:scale-125 transition cursor-pointer"
      >
        &times;
      </button>
    </div>

    <!-- FORM -->
    <form @submit.prevent="saveSubcategory" class="px-10 py-8 space-y-7">

      <!-- CATEGORY -->
      <div>
        <label class="block mb-2 font-medium text-gray-800">Kategorija *</label>
        <select
          v-model="form.category"
          required
          class="w-full px-4 py-3 rounded-xl bg-gray-100 border border-gray-200
                 focus:ring-2 focus:ring-blue-400 focus:outline-none transition cursor-pointer shadow-sm"
        >
          <option value="">Izaberi kategoriju</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>

      <!-- NAME -->
      <div>
        <label class="block mb-2 font-medium text-gray-800">Naziv *</label>
        <input
          v-model="form.name"
          required
          class="w-full px-4 py-3 rounded-xl bg-gray-100 border border-gray-200
                 focus:ring-2 focus:ring-blue-400 focus:outline-none transition shadow-sm"
        />
      </div>

      <!-- DESCRIPTION -->
      <div>
        <label class="block mb-2 font-medium text-gray-800">Opis</label>
        <textarea
          v-model="form.description"
          rows="3"
          class="w-full px-4 py-3 rounded-xl bg-gray-100 border border-gray-200
                 focus:ring-2 focus:ring-blue-400 focus:outline-none transition shadow-sm resize-none"
        ></textarea>
      </div>

      <!-- ERROR -->
      <p v-if="error" class="text-red-600 font-medium">{{ error }}</p>

      <!-- BUTTONS -->
      <div class="flex justify-end gap-4 pt-6">
        <button
          type="button"
          @click="closeModal"
          class="px-7 py-3 rounded-xl bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold
                 transition cursor-pointer"
        >
          Otkaži
        </button>

        <button
          type="submit"
          :disabled="saving"
          class="px-7 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold
                 transition cursor-pointer disabled:opacity-60"
        >
          {{ saving ? "Čuvanje..." : "Sačuvaj" }}
        </button>
      </div>

    </form>

  </div>
</div>


<!-- ANIMATIONS -->




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
@keyframes fadeIn {
  from { opacity: 0 }
  to   { opacity: 1 }
}
.animate-fadeIn {
  animation: fadeIn 0.25s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(25px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.animate-slideUp {
  animation: slideUp 0.28s ease-out;
}
</style>