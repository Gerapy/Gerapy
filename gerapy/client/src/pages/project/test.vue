<template>
  <el-collapse-item :name="index">
    <p>
      hello {{ index }}
    </p>
  </el-collapse-item>
</template>
<script>
  export default {
    props: {
      index: {
        type: Number
      }
    },
    data() {
      return {
        array: [1, 2, 3]
      }
    },
    computed: {
      isActive() {
        return this.$parent.activeNames.indexOf(this.name) > -1;
      }
    },
  }
</script>
