import axios from 'axios'

// Use environment variable or default to local development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export const api = axios.create({
    baseURL: API_BASE_URL
})
