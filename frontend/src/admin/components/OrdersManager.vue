<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const emit = defineEmits(['update-count'])

const orders = ref([])
const loading = ref(false)
const selectedOrder = ref(null)
const showDetailModal = ref(false)

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

const fetchOrders = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/orders/')
    orders.value = response.data
  } catch (error) {
    console.error('Error fetching orders:', error)
    alert('Greška pri učitavanju narudžbina')
  } finally {
    loading.value = false
  }
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('sr-RS', {
    style: 'currency',
    currency: 'RSD'
  }).format(price)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('sr-RS')
}

const openDetailModal = (order) => {
  selectedOrder.value = order
  showDetailModal.value = true
}

const closeDetailModal = () => {
  showDetailModal.value = false
  selectedOrder.value = null
}

const updateOrderStatus = async (orderId, newStatus) => {
  try {
    await axios.post(`/api/orders/${orderId}/update_status/`, { status: newStatus })
    await fetchOrders()
  } catch (error) {
    console.error('Status update error:', error)
    alert('Greška pri ažuriranju statusa')
  }
}

onMounted(() => {
  fetchOrders()
})
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-2xl font-bold">Narudžbine</h2>
      <button
        @click="fetchOrders"
        class="px-5 py-2.5 bg-blue-600 text-white rounded-md hover:bg-blue-700"
      >
        Osveži
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-10 text-gray-600">
      Učitavanje narudžbina...
    </div>

    <!-- Orders table -->
    <div v-else-if="orders.length > 0" class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">#</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Kupac</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Telefon</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Ukupno</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Datum</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Akcije</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="order in orders"
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
            <td class="px-4 py-3 text-sm font-semibold">{{ formatPrice(order.total_amount) }}</td>
            <td class="px-4 py-3 text-sm">
              <span :class="statusColors[order.status]" class="px-2 py-1 rounded-full text-xs font-medium">
                {{ statusLabels[order.status] }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-600">{{ formatDate(order.created_at) }}</td>
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

    <!-- Empty state -->
    <div v-else class="py-16 text-center text-gray-400">
      Nema narudžbina.
    </div>

    <!-- Detail Modal -->
    <div
      v-if="showDetailModal && selectedOrder"
      @click.self="closeDetailModal"
      class="fixed inset-0 bg-black/60 flex items-center justify-center p-5 z-[1500]"
    >
      <div class="bg-white rounded-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">

        <!-- Header -->
        <div class="p-6 border-b bg-gradient-to-r from-blue-600 to-blue-500 text-white flex justify-between items-start">
          <div>
            <h3 class="text-2xl font-bold">Narudžbina #{{ selectedOrder.id }}</h3>
            <p class="text-sm opacity-90">{{ formatDate(selectedOrder.created_at) }}</p>
          </div>
          <button @click="closeDetailModal" class="text-3xl hover:bg-white/20 rounded px-2">&times;</button>
        </div>

        <div class="p-6 space-y-6">

          <!-- Informacije o kupcu -->
          <div>
            <h4 class="font-semibold text-lg mb-3">Kupac</h4>
            <div class="space-y-2 bg-gray-50 p-4 rounded">
              <p><strong>Ime:</strong> {{ selectedOrder.customer_name }}</p>
              <p>
                <strong>Telefon:</strong>
                <a :href="`tel:${selectedOrder.customer_phone}`" class="text-blue-600 hover:underline ml-2">
                  {{ selectedOrder.customer_phone }}
                </a>
              </p>
              <p v-if="selectedOrder.customer_email">
                <strong>Email:</strong>
                <a :href="`mailto:${selectedOrder.customer_email}`" class="text-blue-600 hover:underline ml-2">
                  {{ selectedOrder.customer_email }}
                </a>
              </p>
              <p v-if="selectedOrder.delivery_address">
                <strong>Adresa:</strong> {{ selectedOrder.delivery_address }}
              </p>
            </div>
          </div>

          <!-- Stavke narudžbine -->
          <div>
            <h4 class="font-semibold text-lg mb-3">Stavke</h4>
            <div class="space-y-2">
              <div
                v-for="item in selectedOrder.items"
                :key="item.id"
                class="flex justify-between items-center bg-gray-50 p-3 rounded"
              >
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
          </div>

          <!-- Total -->
          <div class="border-t pt-4">
            <div class="flex justify-between items-center text-xl font-bold">
              <span>Ukupno:</span>
              <span class="text-green-700">{{ formatPrice(selectedOrder.total_amount) }}</span>
            </div>
          </div>

          <!-- Napomene -->
          <div v-if="selectedOrder.notes">
            <h4 class="font-semibold text-lg mb-2">Napomena kupca</h4>
            <p class="bg-yellow-50 p-3 rounded text-sm">{{ selectedOrder.notes }}</p>
          </div>

          <!-- Status update -->
          <div>
            <h4 class="font-semibold text-lg mb-3">Ažuriraj status</h4>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="(label, status) in statusLabels"
                :key="status"
                @click="updateOrderStatus(selectedOrder.id, status)"
                :class="selectedOrder.status === status ? 'ring-2 ring-blue-500' : ''"
                class="px-4 py-2 rounded text-sm font-medium transition hover:scale-105"
                :style="{
                  backgroundColor: selectedOrder.status === status ? '#3b82f6' : '#e5e7eb',
                  color: selectedOrder.status === status ? 'white' : '#374151'
                }"
              >
                {{ label }}
              </button>
            </div>
          </div>

          <!-- Notifikacije -->
          <div class="bg-gray-50 p-4 rounded text-sm space-y-1">
            <p>
              <span :class="selectedOrder.email_sent ? 'text-green-600' : 'text-gray-400'">
                {{ selectedOrder.email_sent ? '✓' : '✗' }} Email poslat
              </span>
            </p>
            <p>
              <span :class="selectedOrder.sms_sent ? 'text-green-600' : 'text-gray-400'">
                {{ selectedOrder.sms_sent ? '✓' : '✗' }} SMS poslat
              </span>
            </p>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>
