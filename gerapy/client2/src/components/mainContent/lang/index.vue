<template>
  <div class="lang">
    <span :class="$store.state.lang == 'zhCN'? 'active': '' " @click="changeLang('zhCN')">中文</span>
    <span>/</span>
    <span :class="$store.state.lang == 'en'? 'active': ''" @click="changeLang('en')">En</span>
  </div>
</template>

<script>
  export default{
    methods: {
      changeLang(lang) {
        console.log(lang)
        this.$store.dispatch('setLang', lang)
        if (typeof(Storage) !== "undefined") {
          localStorage.setItem("gerapy-lang", lang)
        }else {
          console.log('您的浏览器不支持localStorage')
        }
      }
    }
  }
</script>
<style>
  .lang {
    float: right;
    margin-top: 15px;
    margin-right: 240px;
    cursor: pointer;
  }

  .active {
    color: #28ccaa;
  }
</style>
