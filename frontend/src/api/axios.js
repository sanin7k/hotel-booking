import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL; // your FastAPI backend

const api = axios.create({
  baseURL: BASE_URL,
  withCredentials: true, // for cookies if needed
});

export default api;
