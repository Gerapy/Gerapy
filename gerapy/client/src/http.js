import axios from "axios";
import router from "./router";
import store from "./store";

axios.defaults.timeout = 8000;

// set global authorization token
axios.interceptors.request.use(
  (config) => {
    let token = store.getters.token;
    if (token) {
      config.headers.Authorization = "Token " + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 401) {
      store.commit("clearToken");
      router.push({ path: "/login" });
    } else if (error.response.status === 403) {
      router.push({ path: "/home" });
    }
    return Promise.reject(error);
  }
);

export default axios;
