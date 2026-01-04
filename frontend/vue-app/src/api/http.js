/**
 * OCEGS HTTP Client Configuration
 * Axios instance with interceptors for API calls
 */
import axios from 'axios'

// Create axios instance
const http = axios.create({
    baseURL: '/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor
http.interceptors.request.use(
    (config) => {
        // Add auth token when available (Step 2)
        // const token = localStorage.getItem('access_token')
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`
        // }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor
http.interceptors.response.use(
    (response) => {
        return response
    },
    (error) => {
        // Handle common errors
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // Handle unauthorized (Step 2)
                    // router.push('/login')
                    break
                case 403:
                    console.error('Access forbidden')
                    break
                case 500:
                    console.error('Server error')
                    break
            }
        }
        return Promise.reject(error)
    }
)

export default http
