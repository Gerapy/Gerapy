<template>
  <form @submit.prevent="submit_form">
    <el-input
      :placeholder="placeholder"
      v-model="formValue">
    </el-input>
  </form>
</template>
<script type="text/javascript">
  export default{
    props: {
      placeholder: {
        type: String,
        default: "Search here..."
      }
    },
    data(){
      return {
        formValue: ''
      }
    },
    computed: {
      valueIsNull () {
        return this.formValue.trim() === ''
      }
    },
    methods: {
      submit_form() {
        !this.valueIsNull && this.$emit('search', this.formValue)
        return false
      }
    }
  }
</script>
