<template>
  <div class="panel">
    <panel-title :title="$route.meta.title"></panel-title>
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
                {{ $lang[$store.state.lang].buttons.update }}
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
        routeId: this.$route.params.id,
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
              pattern: port,
              message: this.$lang[this.$store.state.lang].columns.port + ' ' + this.$lang[this.$store.state.lang].messages.notValid,
              trigger: 'blur'
            }
            ,
          ]
        }

      }
    },
    created(){
      console.log('RouterID', this.routeId)
      this.routeId !== null && this.getFormData()
    },
    methods: {
      getFormData(){
        this.loadData = true
        this.$fetch.apiClient.show({
          id: this.routeId
        }).then(({data: data}) => {
          this.form = data
          this.form.auth = data.auth ? true : false
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
            this.$message.success(this.$lang[this.$store.state.lang].messages.successSave)
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
