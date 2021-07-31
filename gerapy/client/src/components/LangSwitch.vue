<template>
  <div id="lang">
    <span
      :class="state.lang === 'zh' ? 'active' : ''"
      @click="onChangeLang('zh')"
      >中文</span
    >
    <span> / </span>
    <span
      :class="state.lang === 'en' ? 'active' : ''"
      @click="onChangeLang('en')"
      >En</span
    >
  </div>
</template>

<script>
import store from "../store";

export default {
  name: "LangSwitch",
  data() {
    return {
      state: store.state,
    };
  },
  methods: {
    onChangeLang(lang) {
      store.commit("setLang", lang);
    },
  },
};
</script>
<style scoped>
#lang {
  display: inline-block;
  margin-bottom: 15px;
  margin-right: 10px;
  cursor: pointer;
  font-size: 14px;
}

.active {
  color: #28ccaa;
}
</style>
