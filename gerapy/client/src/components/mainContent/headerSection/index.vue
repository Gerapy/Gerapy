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
  import search from 'components/search'

  export default{
    components: {
    },
    methods: {
      submit_search(value) {
        this.$message.success(value)
      }
    }
  }
</script>
