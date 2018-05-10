<template>
  <div>
    <el-row>
      <el-col :span="24" id="console">
        <p>{{ project }}</p>
        <el-button class="pull-right">
          <i class="fa fa-magic"></i>
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  export default {
    props: {
      project: {
        type: String
      }
    },
    data() {
      return {
        request: {
          url: null,
          html: null,
        }
      }
    },
    methods: {
      onParse() {
        this.$fetch.apiProject.projectGenerate({
          name: this.projectName
        }).then(({data: data}) => {
          this.$message.success(this.$lang[this.$store.state.lang].messages.successGenerate)
          this.getProject()
        }).catch(() => {
          this.$message.error(this.$lang[this.$store.state.lang].messages.errorGenerate)
        })
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  #console {
    height: auto;
    background: #c7e6c7;
  }
</style>
