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
              <el-input v-model="form.name" placeholder="请输入名称" size="small"></el-input>
            </el-form-item>
            <el-form-item label="IP:" prop="ip">
              <el-input v-model="form.ip" placeholder="请输入IP" size="small"></el-input>
            </el-form-item>
            <el-form-item label="端口:" prop="port">
              <el-input v-model="form.port" placeholder="请输入端口" size="small"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" @click="onSubmitForm" :loading="onSubmitLoading">
                <i class="fa fa-check"></i>
                创建
              </el-button>
              <el-button @click="$router.back()" size="small">
                <i class="fa fa-reply"></i>
                返回
              </el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle} from 'components'
  import {ip, port} from '../../common/tools/regex'
  import regex from '../../common/tools/regex'
  console.log(regex)
  console.log(ip, port)
  export default{
    data(){
      return {
        form: {
          name: '',
          ip: '',
          port: '',
          description: ''
        },
        loadData: false,
        onSubmitLoading: false,
        rules: {
          name: [
            {required: true, message: '名称不能为空', trigger: 'blur'},
          ],
          ip: [
            {required: true, message: 'IP不能为空', trigger: 'blur'},
            {pattern: ip, message: 'IP不正确', trigger: 'blur'},
          ],
          port: [
            {required: true, message: '端口不能为空', trigger: 'blur'},
            {pattern: port, message: '端口不正确', trigger: 'blur'},
          ]
        }
      }
    },
    methods: {
      //提交
      onSubmitForm(){
        this.$refs.form.validate((valid) => {
          if (!valid)
            return false
          this.onSubmitLoading = true
          this.$fetch.apiClient.create(
            this.form
          ).then(() => {
            this.$message.success('创建成功')
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
