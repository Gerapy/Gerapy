<template>
  <div class="panel">
    <panel-title :title="$route.meta.title"></panel-title>
    <div class="panel-body"
         v-loading="load_data"
         element-loading-text="拼命加载中">
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <el-form-item label="环境标志:" prop="envTag">
              <el-input v-model="form.envTag" placeholder="请输入内容"></el-input>
            </el-form-item>
            <el-form-item label="环境描述:" prop="envDescription">
              <el-input v-model="form.envDescription" placeholder="请输入环境描述"></el-input>
            </el-form-item>
            <el-form-item label="规则:" prop="addressPattern">
              <el-input v-model="form.addressPattern" placeholder="请输入规则"></el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="on_submit_form" :loading="on_submit_loading">立即提交</el-button>
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
  import {phone, dateTime as dt} from '../../common/tools/regex'

  export default{
    data(){
      return {
        form: {
          envTag: '',
          envDescription: '',
          addressPattern: '',
        },
        route_id: this.$route.params.id,
        load_data: false,
        on_submit_loading: false,
        rules: {
          envTag: [
            {required: true, message: '环境标志不能为空', trigger: 'blur'},
          ],
          addressPattern: [
            {required: true, message: '规则为空', trigger: 'blur'},
          ]
        }
      }
    },
    created(){
      this.route_id && this.get_form_data()
    },
    methods: {
      //获取数据
      get_form_data(){
        this.load_data = true
        this.$fetch.api_pattern.get({
          id: this.route_id
        }).then(({data}) => {
          this.form = data
        this.load_data = false
      }).catch(() => {
          this.load_data = false
      })
      },
      //提交
      on_submit_form(){
        this.$refs.form.validate((valid) => {
          if (!valid)
            return false
        this.on_submit_loading = true
        this.$fetch.api_pattern.save(this.form).then(() => {
          this.$message.success('添加成功')
          this.on_submit_loading = false
        }).
        catch(() => {
          this.on_submit_loading = false
        })
      })
      }
    },
    components: {
      panelTitle
    }
  }
</script>
