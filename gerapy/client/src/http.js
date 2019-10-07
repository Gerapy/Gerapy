import axios from 'axios';

import router from './router'

import { getToken, removeToken } from './utils/auth'

/* eslint-disable */



axios.defaults.timeout = 8000;

axios.interceptors.request.use(
    config => {
        console.log("设置 Header")
        if (getToken()){
            config.headers.Authorization = 'Token ' + getToken()

        }

        return config
    },

    error => {
        return Promise.reject(error)
    }
)

axios.interceptors.response.use(
    response => {
        if (response.status === 401) {
            removeToken()
            router.push({path: '/login'});
            console.log("Token Error");
        }else if (response.status === 403) {
            router.push({path: '/home'});
            console.log("No Permission");
        }
        return response;
    },
    error => {
        return Promise.reject(error);
    }
);


export default axios