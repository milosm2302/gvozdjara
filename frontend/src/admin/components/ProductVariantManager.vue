<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  productId: Number
})

const emit = defineEmits(['updated'])

const variants = ref([])
const showForm = ref(false)
const editing = ref(null)

const form = ref({
  name: '',
  price_adjustment: 0,
  sku: '',
  in_stock: true,
  stock_quantity: 0
})

const fetchVariants = async () => {
  if (!props.productId) return
  try {
    const response = await axios.get(`/api/product-variants/?product_id=${props.productId}`)
    variants.value = response.data
  } catch (error) {
    console.error('Error fetching variants:', error)
  }
}

const openForm = (variant = null) => {
  if (variant) {
    editing.value = variant.id
    form.value = { ...variant }
  } else {
    editing.value = null
    form.value = {
      name: '',
      price_adjustment: 0,
      sku: '',
      in_stock: true,
      stock_quantity: 0
    }
  }
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  editing.value = null
}

const saveVariant = async () => {
  try {
    const data = {
      product: props.productId,
      ...form.value
    }

    if (editing.value) {
      await axios.patch(`/api/product-variants/${editing.value}/`, data)
    } else {
      await axios.post('/api/product-variants/', data)
    }

    await fetchVariants()
    emit('updated')
    closeForm()
  } catch (error) {
    console.error('Save error:', error)
    alert('Greška pri čuvanju varijante')
  }
}

const deleteVariant = async (id) => {
  if (!confirm('Obrisati varijantu?')) return
  try {
    await axios.delete(`/api/product-variants/${id}/`)
    await fetchVariants()
    emit('updated')
  } catch (error) {
    console.error('Delete error:', error)
  }
}

// Fetch na mount
if (props.productId) {
  fetchVariants()
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h4 class="font-semibold text-lg">Varijante (Dimenzije)</h4>
      <button
        @click="openForm()"
        class="px-4 py-2 bg-green-600 text-white rounded text-sm"
      >
        + Dodaj varijantu
      </button>
    </div>

    <!-- Lista varijanti -->
    <div class="space-y-2">
      <div
        v-for="variant in variants"
        :key="variant.id"
        class="flex items-center justify-between border rounded-lg p-3 bg-gray-50"
      >
        <div>
          <p class="font-medium">{{ variant.name }}</p>
          <p class="text-sm text-gray-600">
            SKU: {{ variant.sku || 'N/A' }} |
            Dodatna cena: {{ variant.price_adjustment >= 0 ? '+' : '' }}{{ variant.price_adjustment }} RSD
          </p>
          <p class="text-xs" :class="variant.in_stock ? 'text-green-600' : 'text-red-600'">
            {{ variant.in_stock ? `Na stanju: ${variant.stock_quantity}` : 'Nije na stanju' }}
          </p>
        </div>

        <div class="flex gap-2">
          <button
            @click="openForm(variant)"
            class="px-3 py-1 bg-blue-500 text-white rounded text-sm"
          >
            Izmeni
          </button>
          <button
            @click="deleteVariant(variant.id)"
            class="px-3 py-1 bg-red-500 text-white rounded text-sm"
          >
            Obriši
          </button>
        </div>
      </div>
    </div>

    <p v-if="variants.length === 0" class="text-gray-400 text-center py-8">
      Nema varijanti. Dodaj dimenzije/varijacije proizvoda.
    </p>

    <!-- MODAL za dodavanje/izmenu -->
    <div
      v-if="showForm"
      @click.self="closeForm"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-[2000]"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-xl font-semibold mb-4">
          {{ editing ? 'Izmeni varijantu' : 'Nova varijanta' }}
        </h3>

        <form @submit.prevent="saveVariant" class="space-y-4">
          <div>
            <label class="block font-medium mb-1">Naziv (dimenzije) *</label>
            <input
              v-model="form.name"
              required
              placeholder="npr. 180×135×18mm"
              class="w-full px-3 py-2 border rounded"
            />
          </div>

          <div>
            <label class="block font-medium mb-1">SKU (šifra)</label>
            <input
              v-model="form.sku"
              placeholder="npr. TACNA-70-180"
              class="w-full px-3 py-2 border rounded"
            />
          </div>

          <div>
            <label class="block font-medium mb-1">Dodatna cena (+/-)</label>
            <input
              v-model.number="form.price_adjustment"
              type="number"
              step="0.01"
              class="w-full px-3 py-2 border rounded"
            />
            <p class="text-xs text-gray-500 mt-1">Npr: +50 za veću dimenziju, -20 za manju</p>
          </div>

          <div>
            <label class="block font-medium mb-1">Količina na stanju</label>
            <input
              v-model.number="form.stock_quantity"
              type="number"
              class="w-full px-3 py-2 border rounded"
            />
          </div>

          <div class="flex items-center gap-2">
            <input
              v-model="form.in_stock"
              type="checkbox"
              id="variant-in-stock"
            />
            <label for="variant-in-stock">Na stanju</label>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button
              type="button"
              @click="closeForm"
              class="px-5 py-2 bg-gray-300 rounded"
            >
              Otkaži
            </button>
            <button
              type="submit"
              class="px-5 py-2 bg-blue-600 text-white rounded"
            >
              Sačuvaj
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
