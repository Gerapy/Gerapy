<template>
  <div class="panel">
    <panel-title :title="$route.meta.title"></panel-title>
    <div class="panel-body"
         v-loading="loadData"
         element-loading-text="拼命加载中">
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <el-form-item label="名称:" prop="name">
              <el-input v-model="form.name" placeholder="请输入名称"></el-input>
            </el-form-item>
            <el-form-item label="IP:" prop="ip">
              <el-input v-model="form.ip" placeholder="请输入IP"></el-input>
            </el-form-item>
            <el-form-item label="端口:" prop="port">
              <el-input v-model="form.port" placeholder="请输入端口"></el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="onSubmitForm" :loading="onSubmitLoading">修改</el-button>
              <el-button @click="$router.back()">取消</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle} from 'components'
  export default{
    data(){
      return {
        form: {
          name: '',
          ip: '',
          port: '',
          description: ''
        },
        routeId: this.$route.params.id,
        loadData: false,
        onSubmitLoading: false,
        rules: {
          name: [
            {required: true, message: '名称不能为空', trigger: 'blur'}
          ]
        }
      }
    },
    created(){
      this.routeId !== null && this.getFormData()
    },
    methods: {
      getFormData(){
        this.loadData = true
        this.$fetch.apiClient.show({
          id: this.routeId
        }).then(({data: data}) => {
          this.form = data
          this.loadData = false
        }).catch(() => {
          this.loadData = false
        })
      },
      //提交
      onSubmitForm(){
        this.$refs.form.validate((valid) => {
          if (!valid)
            return false
          this.onSubmitLoading = true
          this.$fetch.apiClient.update({
              id: this.form.id
            }, this.form
          ).then(() => {
            this.$message.success('修改成功')
            this.onSubmitLoading = false
          }).catch(() => {
            this.onSubmitLoading = false
          })
        })
      }
    },
    components: {
      panelTitle
    }
  }
</script>
