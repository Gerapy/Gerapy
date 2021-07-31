import Vue from "vue";
import Router from "vue-router";
import Layout from "./layout/Index.vue";
import store from "./store";

Vue.use(Router);

const router = new Router({
  // mode: 'history',
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("./views/login/Login.vue"),
    },
    {
      path: "/",
      redirect: "/home",
      name: "layout",
      component: Layout,
      children: [
        {
          path: "/home",
          name: "home",
          component: () => import("./views/home/Index.vue"),
        },
        {
          path: "/client",
          name: "clientIndex",
          component: () => import("./views/client/Index.vue"),
        },
        {
          path: "/client/create",
          name: "clientCreate",
          component: () => import("./views/client/Create.vue"),
        },
        {
          path: "/client/:id/edit",
          name: "clientEdit",
          component: () => import("./views/client/Edit.vue"),
        },
        {
          path: "/client/:id/schedule",
          name: "clientSchedule",
          component: () => import("./views/client/Schedule.vue"),
        },
        {
          path: "/project",
          name: "projectIndex",
          component: () => import("./views/project/Index.vue"),
        },
        {
          path: "/project/:name/edit",
          name: "projectEdit",
          component: () => import("./views/project/Edit.vue"),
        },
        {
          path: "/project/:name/deploy",
          name: "projectDeploy",
          component: () => import("./views/project/Deploy.vue"),
        },
        {
          path: "/project/:name/configure",
          name: "projectConfigure",
          component: () => import("./views/project/Configure.vue"),
        },
        // task management
        {
          path: "/task",
          name: "taskIndex",
          component: () => import("./views/task/Index.vue"),
        },
        {
          path: "/task/create",
          name: "taskCreate",
          component: () => import("./views/task/Create.vue"),
        },
        {
          path: "/task/:id/edit",
          name: "taskEdit",
          component: () => import("./views/task/Edit.vue"),
        },
        {
          path: "/task/:id/status",
          name: "taskStatus",
          component: () => import("./views/task/Status.vue"),
        },
      ],
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  },
});

const whiteList = ["/login"];

router.beforeEach((to, from, next) => {
  let token = store.getters.token;
  if (token) {
    if (to.path === "/login") {
      // 如果登录过，直接跳转到首页
      next({ path: "/" });
    } else {
      next();
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next();
    } else {
      next({ path: `/login` });
    }
  }
});

// 每次跳出之后清除定时任务
router.afterEach(() => {
  router.app.$store.commit("clearIntervals");
  router.app.$store.commit("clearTimeout");
});

export default router;
