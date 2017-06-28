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
              {{ form.fields.name }}
            </el-form-item>
            <el-form-item label="IP:" prop="ip">
              <el-input v-model="form.fields.ip" placeholder="请输入IP"></el-input>
            </el-form-item>
            <el-form-item label="端口:" prop="port">
              <el-input v-model="form.fields.port" placeholder="请输入端口"></el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="on_submit_form" :loading="onSubmitLoading">立即提交</el-button>
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
          fields: {
            name: '',
            ip: '',
            port: '',
            description: ''
          }
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
      //获取数据
      getFormData(){
        this.loadData = true
        this.$fetch.apiClient.show({
          pk: this.routeId
        }).then(({data}) => {
          this.form = data
          this.form.envTag = this.form.envTag.toString()
          this.loadData = false
        }).catch(() => {
          this.loadData = false
        })
      },
      //提交
      on_submit_form(){
        this.$refs.form.validate((valid) => {
          if (!valid)
            return false
          this.onSubmitLoading = true
          this.$fetch.api_pattern.update(this.form).then(() => {
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
