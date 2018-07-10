<template>
  <div class="panel">
    <panel-title :title="$lang[$store.state.lang].titles.createTask"></panel-title>
    <div class="panel-body"
         v-loading="loadData"
         :element-loading-text="$lang[$store.state.lang].messages.loading">
      <el-row>
        <el-col :span="10">
          <substance ref="substance" :id="routeId">
            <template slot="submit">
              <el-button type="primary" size="small" @click="onSubmitForm" :loading="onSubmitLoading">
                <i class="fa fa-check"></i>
                {{ $lang[$store.state.lang].buttons.update }}
              </el-button>
            </template>
          </substance>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle} from 'components'
  import substance from 'pages/task/substance'

  export default {
    data() {
      return {
        onSubmitLoading: false,
        loadData: false,
        routeId: this.$route.params.id,
      }
    },
    methods: {
      onSubmitForm() {
        this.$refs.substance.$refs.form.validate((valid) => {
          if (!valid)
            return false
          this.onSubmitLoading = true
          let formData = this.$refs.substance.formData
          this.$fetch.apiTask.update({id: this.routeId}, formData).then(() => {
            this.$message.success(this.$lang[this.$store.state.lang].messages.successSave)
            this.onSubmitLoading = false
          }).catch(() => {
            this.onSubmitLoading = false
          })
        })
      }
    },
    components: {
      panelTitle,
      substance
    },
  }
</script>
<style>
  .width-100 {
    width: 100px;
  }

  .width-200 {
    width: 200px;
  }
</style>
