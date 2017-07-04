<template>
  <div class="header-section">
    <div class="search">
      <el-input
        size="small"
        placeholder="请输入内容">
      </el-input>
    </div>
  </div>
</template>
<script type="text/javascript">
  import menuRight from './menuRight'
  import search from 'components/search'

  export default{
    components: {
      menuRight
    },
    methods: {
      submit_search(value) {
        this.$message.success(value)
      }
    }
  }
</script>
