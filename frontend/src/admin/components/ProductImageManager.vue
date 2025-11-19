<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  productId: Number
})

const emit = defineEmits(['updated'])

const images = ref([])
const uploading = ref(false)
const selectedFile = ref(null)

const fetchImages = async () => {
  if (!props.productId) return
  try {
    const response = await axios.get(`/api/product-images/?product_id=${props.productId}`)
    images.value = response.data
  } catch (error) {
    console.error('Error fetching images:', error)
  }
}

const handleFileSelect = (event) => {
  selectedFile.value = event.target.files[0]
}

const uploadImage = async () => {
  if (!selectedFile.value) return

  uploading.value = true
  const formData = new FormData()
  formData.append('image', selectedFile.value)
  formData.append('product', props.productId)
  formData.append('is_primary', images.value.length === 0) // Prva slika je primary

  try {
    await axios.post('/api/product-images/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    selectedFile.value = null
    await fetchImages()
    emit('updated')
  } catch (error) {
    console.error('Upload error:', error)
    alert('Greška pri upload-u slike')
  } finally {
    uploading.value = false
  }
}

const setPrimary = async (imageId) => {
  try {
    await axios.patch(`/api/product-images/${imageId}/`, { is_primary: true })
    await fetchImages()
  } catch (error) {
    console.error('Error setting primary:', error)
  }
}

const deleteImage = async (imageId) => {
  if (!confirm('Obrisati sliku?')) return
  try {
    await axios.delete(`/api/product-images/${imageId}/`)
    await fetchImages()
    emit('updated')
  } catch (error) {
    console.error('Delete error:', error)
  }
}

// Fetch na mount
if (props.productId) {
  fetchImages()
}
</script>

<template>
  <div class="space-y-4">
    <h4 class="font-semibold text-lg">Slike proizvoda</h4>

    <!-- Upload forma -->
    <div class="flex gap-3 items-center">
      <input
        type="file"
        @change="handleFileSelect"
        accept="image/*"
        class="flex-1 border rounded px-3 py-2"
      />
      <button
        @click="uploadImage"
        :disabled="!selectedFile || uploading"
        class="px-5 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {{ uploading ? 'Upload...' : 'Dodaj sliku' }}
      </button>
    </div>

    <!-- Galerija -->
    <div class="grid grid-cols-3 gap-4">
      <div
        v-for="img in images"
        :key="img.id"
        class="relative border rounded-lg overflow-hidden group"
      >
        <img
          :src="`http://localhost:8000${img.image}`"
          :alt="img.alt_text"
          class="w-full h-40 object-cover"
        />

        <div v-if="img.is_primary" class="absolute top-2 left-2 bg-green-500 text-white px-2 py-1 text-xs rounded">
          Glavna
        </div>

        <div class="absolute bottom-0 left-0 right-0 bg-black/70 p-2 flex gap-2 opacity-0 group-hover:opacity-100 transition">
          <button
            v-if="!img.is_primary"
            @click="setPrimary(img.id)"
            class="flex-1 px-2 py-1 bg-green-600 text-white text-xs rounded"
          >
            Postavi kao glavnu
          </button>
          <button
            @click="deleteImage(img.id)"
            class="px-2 py-1 bg-red-600 text-white text-xs rounded"
          >
            Obriši
          </button>
        </div>
      </div>
    </div>

    <p v-if="images.length === 0" class="text-gray-400 text-center py-8">
      Nema slika. Dodaj prvu sliku proizvoda.
    </p>
  </div>
</template>
