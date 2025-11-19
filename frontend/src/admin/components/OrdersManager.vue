<script setup>
import { ref, onMounted } from 'vue'
import { useOrderStore } from '../store/orders'

const emit = defineEmits(['update-count'])
const orderStore = useOrderStore()

// Status boje i nazivi ostaju u komponenti
const statusColors = {
  pending: 'bg-yellow-100 text-yellow-800',
  confirmed: 'bg-blue-100 text-blue-800',
  processing: 'bg-purple-100 text-purple-800',
  completed: 'bg-green-100 text-green-800',
  cancelled: 'bg-red-100 text-red-800'
}

const statusLabels = {
  pending: 'Na čekanju',
  confirmed: 'Potvrđena',
  processing: 'U obradi',
  completed: 'Završena',
  cancelled: 'Otkazana'
}

const showDetailModal = ref(false)

const openDetailModal = (order) => {
  orderStore.selectOrder(order)
  showDetailModal.value = true
}

const closeDetailModal = () => {
  showDetailModal.value = false
  orderStore.clearSelected()
}

// format funkcije ostaju ovde
const formatPrice = (price) =>
  new Intl.NumberFormat('sr-RS', { style: 'currency', currency: 'RSD' }).format(price)

const formatDate = (dateString) =>
  new Date(dateString).toLocaleString('sr-RS')

// onMounted → samo fetch
onMounted(() => {
  orderStore.fetchAll()
})
</script>


<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-2xl font-bold">Narudžbine</h2>
      <button
        @click="orderStore.fetchAll"
        class="px-5 py-2.5 bg-blue-600 text-white rounded-md hover:bg-blue-700"
      >
        Osveži
      </button>
    </div>

    <!-- Loading -->
    <div v-if="orderStore.loading" class="text-center py-10 text-gray-600">
      Učitavanje narudžbina...
    </div>

    <!-- Orders table -->
    <div v-else-if="orderStore.list.length > 0" class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-semibold">#</th>
            <th class="px-4 py-3 text-left text-sm font-semibold">Kupac</th>
            <th class="px-4 py-3 text-left text-sm font-semibold">Telefon</th>
            <th class="px-4 py-3 text-left text-sm font-semibold">Ukupno</th>
            <th class="px-4 py-3 text-left text-sm font-semibold">Status</th>
            <th class="px-4 py-3 text-left text-sm font-semibold">Datum</th>
            <th class="px-4 py-3 text-left text-sm font-semibold">Akcije</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="order in orderStore.list"
            :key="order.id"
            class="border-t hover:bg-gray-50 transition"
          >
            <td class="px-4 py-3 text-sm font-medium">#{{ order.id }}</td>

            <td class="px-4 py-3 text-sm">{{ order.customer_name }}</td>

            <td class="px-4 py-3 text-sm">
              <a :href="`tel:${order.customer_phone}`" class="text-blue-600 hover:underline">
                {{ order.customer_phone }}
              </a>
            </td>

            <td class="px-4 py-3 text-sm font-semibold">
              {{ formatPrice(order.total_amount) }}
            </td>

            <td class="px-4 py-3 text-sm">
              <span
                :class="statusColors[order.status]"
                class="px-2 py-1 rounded-full text-xs font-medium"
              >
                {{ statusLabels[order.status] }}
              </span>
            </td>

            <td class="px-4 py-3 text-sm text-gray-600">
              {{ formatDate(order.created_at) }}
            </td>

            <td class="px-4 py-3 text-sm">
              <button
                @click="openDetailModal(order)"
                class="px-3 py-1.5 bg-blue-600 text-white rounded text-xs hover:bg-blue-700"
              >
                Detalji
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty -->
    <div v-else class="py-16 text-center text-gray-400">
      Nema narudžbina.
    </div>

    <!-- DETAIL MODAL -->
    <div
      v-if="showDetailModal && orderStore.selected"
      @click.self="closeDetailModal"
      class="fixed inset-0 bg-black/60 flex items-center justify-center p-5 z-[1500]"
    >
      <div class="bg-white rounded-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">

        <!-- Modal Header -->
        <div class="p-6 border-b bg-gradient-to-r from-blue-600 to-blue-500 text-white flex justify-between">
          <div>
            <h3 class="text-2xl font-bold">
              Narudžbina #{{ orderStore.selected.id }}
            </h3>
            <p class="text-sm opacity-90">{{ formatDate(orderStore.selected.created_at) }}</p>
          </div>

          <button @click="closeDetailModal" class="text-3xl hover:bg-white/20 rounded px-2">
            &times;
          </button>
        </div>

        <div class="p-6 space-y-6">

          <!-- Kupac -->
          <div>
            <h4 class="font-semibold text-lg mb-3">Kupac</h4>
            <div class="space-y-2 bg-gray-50 p-4 rounded">
              <p><strong>Ime:</strong> {{ orderStore.selected.customer_name }}</p>

              <p>
                <strong>Telefon:</strong>
                <a
                  :href="`tel:${orderStore.selected.customer_phone}`"
                  class="text-blue-600 hover:underline ml-2"
                >
                  {{ orderStore.selected.customer_phone }}
                </a>
              </p>

              <p v-if="orderStore.selected.customer_email">
                <strong>Email:</strong>
                <a
                  :href="`mailto:${orderStore.selected.customer_email}`"
                  class="text-blue-600 hover:underline ml-2"
                >
                  {{ orderStore.selected.customer_email }}
                </a>
              </p>

              <p v-if="orderStore.selected.delivery_address">
                <strong>Adresa:</strong> {{ orderStore.selected.delivery_address }}
              </p>
            </div>
          </div>

          <!-- Items -->
          <div>
            <h4 class="font-semibold text-lg mb-3">Stavke</h4>

            <div v-for="item in orderStore.selected.items" :key="item.id" class="bg-gray-50 p-3 rounded mb-2 flex justify-between">
              <div>
                <p class="font-medium">{{ item.product_name }}</p>
                <p v-if="item.variant_name" class="text-sm text-gray-600">{{ item.variant_name }}</p>
                <p class="text-sm text-gray-600">Količina: {{ item.quantity }}</p>
              </div>

              <div class="text-right">
                <p class="font-semibold">{{ formatPrice(item.total_price) }}</p>
                <p class="text-sm text-gray-600">{{ formatPrice(item.unit_price) }} / kom</p>
              </div>
            </div>
          </div>

          <!-- Total -->
          <div class="border-t pt-4">
            <div class="flex justify-between text-xl font-bold">
              <span>Ukupno:</span>
              <span class="text-green-700">{{ formatPrice(orderStore.selected.total_amount) }}</span>
            </div>
          </div>

          <!-- Napomena -->
          <div v-if="orderStore.selected.notes">
            <h4 class="font-semibold text-lg mb-2">Napomena kupca</h4>
            <p class="bg-yellow-50 p-3 rounded text-sm">{{ orderStore.selected.notes }}</p>
          </div>

          <!-- UPDATE STATUS -->
          <div>
            <h4 class="font-semibold text-lg mb-3">Ažuriraj status</h4>

            <div class="flex flex-wrap gap-2">
              <button
                v-for="(label, status) in statusLabels"
                :key="status"
                @click="orderStore.updateStatus(orderStore.selected.id, status)"
                :class="orderStore.selected.status === status ? 'ring-2 ring-blue-500' : ''"
                class="px-4 py-2 rounded text-sm font-medium transition hover:scale-105"
                :style="{
                  backgroundColor: orderStore.selected.status === status ? '#3b82f6' : '#e5e7eb',
                  color: orderStore.selected.status === status ? 'white' : '#374151'
                }"
              >
                {{ label }}
              </button>
            </div>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>
