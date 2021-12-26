import Vue from "vue";
import Vuex from "vuex";
import VuexPersist from "vuex-persist";
import { en, zh } from "./langs/index";
import zhLocale from "element-ui/lib/locale/lang/zh-CN";
import enLocale from "element-ui/lib/locale/lang/en";
import locale from "element-ui/lib/locale";

Vue.use(Vuex);

const vuexPersist = new VuexPersist({
  key: "gerapy",
  storage: localStorage,
});

export default new Vuex.Store({
  state: {
    lang: "zh",
    i18n: {
      zh: zh,
      en: en,
    },
    auth: {
      user: null,
      token: null,
    },
    color: {
      primary: "#35CBAA",
      success: "#35CBAA",
      warning: "#F6B93D",
      danger: "#EF6372",
      error: "#EF6372",
      info: "#60BCFE",
    },
    timeout: null,
    intervals: [],
    dateFormat: "yyyy-MM-dd hh:mm:ss",
    dateFormat24: "yyyy-MM-dd HH:mm:ss",
    url: {
      user: {
        auth: "api/user/auth",
      },
      home: {
        status: "/api/index/status",
      },
      project: {
        index: "/api/project/index",
        create: "/api/project/create",
        upload: "/api/project/upload",
        clone: "/api/project/clone",
        remove: "/api/project/{name}/remove",
        build: "/api/project/{name}/build",
        configure: "/api/project/{name}/configure",
        generate: "/api/project/{name}/generate",
        parse: "/api/project/{name}/parse",
        tree: "/api/project/{name}/tree",
        fileRead: "/api/project/file/read",
        fileUpdate: "/api/project/file/update",
        fileDelete: "/api/project/file/delete",
        fileRename: "/api/project/file/rename",
        fileCreate: "/api/project/file/create",
      },
      task: {
        index: "/api/task",
        create: "/api/task/create",
        info: "/api/task/{id}/info",
        update: "/api/task/{id}/update",
        remove: "/api/task/{id}/remove",
        status: "/api/task/{id}/status",
      },
      client: {
        index: "/api/client",
        show: "/api/client/{id}",
        status: "/api/client/{id}/status",
        update: "/api/client/{id}/update",
        remove: "/api/client/{id}/remove",
        create: "/api/client/create",
        projects: "/api/client/{id}/projects",
        listSpiders: "/api/client/{id}/project/{project}/spiders",
        startSpider: "/api/client/{id}/project/{project}/spider/{spider}",
        listJobs: "/api/client/{id}/project/{project}/jobs",
        getLog:
          "/api/client/{id}/project/{project}/spider/{spider}/job/{job}/log/{random}",
        cancelJob: "/api/client/{id}/project/{project}/job/{job}/cancel",
        projectVersion: "/api/client/{id}/project/{name}/version",
        projectDeploy: "/api/client/{id}/project/{name}/deploy",
      },
      util: {
        render: "/api/render",
      },
    },
  },
  mutations: {
    setLang(state, lang) {
      state.lang = lang;
      if (lang === "zh") {
        locale.use(zhLocale);
      }
      if (lang === "en") {
        locale.use(enLocale);
      }
    },
    // auth
    setToken(state, token) {
      state.auth.token = token;
    },
    clearToken(state) {
      state.auth.token = null;
    },
    // user
    setUser(state, user) {
      state.auth.user = user;
    },
    clearUser(state) {
      state.auth.user = null;
    },
    // timeout
    setTimeout: (state, timeout) => {
      if (state.timeout) {
        clearTimeout(state.timeout);
      }
      state.timeout = timeout;
    },
    clearTimeout: (state) => {
      clearTimeout(state.timeout);
    },
    addInterval: (state, interval) => {
      state.intervals.push(interval);
    },
    clearIntervals: (state) => {
      state.intervals.forEach((interval) => {
        clearInterval(interval);
      });
      state.intervals = [];
    },
  },
  getters: {
    $lang: (state) => {
      return state.i18n[state.lang];
    },
    token: (state) => {
      return state.auth.token;
    },
    user: (state) => {
      return state.auth.user;
    },
  },
  plugins: [vuexPersist.plugin],
});
