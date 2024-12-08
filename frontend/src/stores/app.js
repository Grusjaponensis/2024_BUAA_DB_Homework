// Utilities
import { defineStore } from 'pinia'
import { reactive } from 'vue'

export const useAppStore = defineStore('app', {
  state: () => ({
    //
  }),
})

export const snackbar = reactive({
  show: false,
  text: "",
  color: "green",
  timeout: 3000
})