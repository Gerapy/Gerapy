<template>
  <div class="header-section">
    <div class="search">
      <search @search="submit_search"></search>
    </div>
    <menu-right></menu-right>
  </div>
</template>
<script type="text/javascript">
  import menuRight from './menuRight'
  import search from 'components/search'

  export default{
    components: {
      menuRight,
      search
    },
    methods: {
      submit_search(value) {
        this.$message.success(value)
      }
    }
  }
</script>
