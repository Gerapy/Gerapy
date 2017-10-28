<template>
  <div class="header-section">
    <div class="search">
      <el-input
        size="small"
        placeholder="请输入内容">
      </el-input>
    </div>
    <lang></lang>
  </div>
</template>
<script type="text/javascript">
  import lang from '../lang'

  export default{
    components: {
      lang,
    }
  }
</script>
