import api from "./axios";

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    if (err.response?.status === 401) {
      try {
        await api.get("/auth/refresh");
        return api(err.config);
      } catch (refreshError) {
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(err);
  }
);
