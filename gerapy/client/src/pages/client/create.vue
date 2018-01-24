<template>
  <div class="panel">
    <panel-title :title="$lang[$store.state.lang].titles.createClient"></panel-title>
    <div class="panel-body"
         v-loading="loadData"
         :element-loading-text="$lang[$store.state.lang].messages.loading">
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <el-form-item :label="$lang[$store.state.lang].columns.name" prop="name">
              <el-input v-model="form.name"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.name"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.ip" prop="ip">
              <el-input v-model="form.ip"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.ip"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.port" prop="port">
              <el-input v-model="form.port"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.port"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.auth" prop="auth">
              <el-switch
                v-model="form.auth">
              </el-switch>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.username" prop="username" v-if="form.auth">
              <el-input v-model="form.username"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.username"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.password" prop="password" v-if="form.auth">
              <el-input v-model="form.password" type="password"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.password"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" @click="onSubmitForm" :loading="onSubmitLoading">
                <i class="fa fa-check"></i>
                {{ $lang[$store.state.lang].buttons.create }}
              </el-button>
              <el-button @click="$router.back()" size="small">
                <i class="fa fa-reply"></i>
                {{ $lang[$store.state.lang].buttons.return }}
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
  import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item";
  export default{
    data(){
      return {
        form: {
          name: '',
          ip: '',
          port: '',
          description: '',
          auth: false,
          username: '',
          password: ''
        },
        loadData: false,
        onSubmitLoading: false,
        rules: {
          name: [
            {
              required: true,
              message: this.$lang[this.$store.state.lang].columns.name + ' ' + this.$lang[this.$store.state.lang].messages.isNull,
              trigger: 'blur'
            },
          ],
          ip: [
            {
              required: true,
              message: this.$lang[this.$store.state.lang].columns.ip + ' ' + this.$lang[this.$store.state.lang].messages.isNull,
              trigger: 'blur'
            }
          ],
          port: [
            {
              required: true,
              message: this.$lang[this.$store.state.lang].columns.port + ' ' + this.$lang[this.$store.state.lang].messages.isNull
              , trigger: 'blur'
            },
            {
              pattern: port,
              message: this.$lang[this.$store.state.lang].columns.port + ' ' + this.$lang[this.$store.state.lang].messages.notValid,
              trigger: 'blur'
            }
            ,
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
            this.$message.success(this.$lang[this.$store.state.lang].messages.successSave)
            this.onSubmitLoading = false
          }).catch(() => {
            this.onSubmitLoading = false
          })
        })
      }
    },
    components: {
      ElFormItem,
      panelTitle
    }
  }
</script>
