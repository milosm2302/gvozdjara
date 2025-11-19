<template>
  <transition name="modal-fade">
    <div
      v-if="show"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-[2000]"
      @click.self="$emit('cancel')"
    >
      <div
        class="bg-white rounded-3xl shadow-2xl w-full max-w-xl p-10 
               transform transition-all duration-200 modal-animation"
      >
        <!-- Title -->
        <h2 class="text-3xl font-bold text-gray-900 text-center mb-6">
          {{ title }}
        </h2>

        <!-- Message -->
        <p class="text-gray-600 text-center mb-10 leading-relaxed text-lg">
          {{ message }}
        </p>

        <!-- Buttons -->
        <div class="flex gap-4 justify-center">
          <button
            @click="$emit('confirm')"
            class="px-8 py-3 rounded-xl bg-[#1976d2] text-white font-semibold 
                   shadow hover:bg-[#1565c0] active:scale-95 transition"
          >
            {{ confirmText }}
          </button>

          <button
            @click="$emit('cancel')"
            class="px-8 py-3 rounded-xl bg-gray-200 text-gray-800 font-semibold
                   shadow hover:bg-gray-300 active:scale-95 transition"
          >
            {{ cancelText }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: { type: String, default: "Potvrda" },
  message: String,
  confirmText: { type: String, default: "Da" },
  cancelText: { type: String, default: "Odustani" },
})
</script>

<style scoped>
/* Fade za pozadinu */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Scale animacija za modal */
.modal-animation {
  opacity: 1;
  transform: scale(1);
}

.modal-fade-enter-from .modal-animation {
  transform: scale(0.9);
  opacity: 0;
}

.modal-fade-leave-to .modal-animation {
  transform: scale(0.95);
  opacity: 0;
}
</style>
