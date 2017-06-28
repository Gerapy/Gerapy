<template>
  <div class="panel">
    <panel-title :title="$route.meta.title"></panel-title>
    <div class="panel-body"
         v-loading="load_data"
         element-loading-text="拼命加载中">
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <el-form-item label="目标地址:" prop="destAddress">
              <el-input v-model="form.destAddress" placeholder="请输入内容"></el-input>
            </el-form-item>
            <el-form-item label="话题:" prop="sessionData.topic">
              <el-input v-model="form.sessionData.topic" placeholder="请输入话题"></el-input>
            </el-form-item>
            <el-form-item label="问候语:" prop="sessionData.greetingWord">
              <el-input
                type="textarea"
                :rows="3"
                placeholder="请输入问候语"
                v-model="form.sessionData.greetingWord">
              </el-input>
            </el-form-item>
            <el-form-item label="时间:" prop="dateTime">
              <el-date-picker
                v-model="form.dateTime"
                type="datetime"
                placeholder="选择日期时间"
                align="right"
                :picker-options="pickerOptions">
              </el-date-picker>
            </el-form-item>
            <el-form-item label="环境标志:" prop="envTag">
              <el-select v-model="form.envTag" clearable placeholder="请选择">
                <el-option
                  v-for="item in envTagOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
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
        envTagOptions: [],
        statusOptions: [{
          value: 1,
          label: '成功'
        }, {
          value: 2,
          label: '失败'
        }, {
          value: 3,
          label: '等待'
        }],
        pickerOptions: {
          shortcuts: [{
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date());
            }
          }, {
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          }, {
            text: '一周前',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', date);
            }
          }]
        },
        form: {
          destAddress: '',
          sessionData: {
            topic: '',
            greetingWord: ''
          },
          dateTime: '',
          envTag: ''
        },
        route_id: this.$route.params.id,
        load_data: false,
        on_submit_loading: false,
        rules: {
          destAddress: [
            {required: true, message: '目标地址不能为空', trigger: 'blur'},
            //            {pattern: phone, message: '电话号码不正确', trigger: 'blur'},
          ],
          'sessionData.topic': [
            {required: true, message: '话题不能为空', trigger: 'blur'},
          ],
          'sessionData.greetingWord': [
            {required: true, message: '问候语不能为空', trigger: 'blur'},
          ]
        }
      }
    },
    created(){
      this.get_form_data()
    },
    methods: {
      //获取数据
      get_form_data(){
        this.load_data = true
        this.$fetch.api_pattern.list({})
          .then(({data: patternData}) => {
            console.log('Pattern', patternData)
            this.envTagOptions = []
            patternData.forEach((item) => {
              this.envTagOptions.push({
                'value': item.envTag,
                'label': item.addressPattern
              })
            })
            this.load_data = false
          })
          .catch(() => {
            this.load_data = false
          })
      },
      //提交
      on_submit_form(){
        this.$refs.form.validate((valid) => {
          if (!valid)
            return false
          this.on_submit_loading = true
          this.$fetch.api_task.save(this.form).then(() => {
            this.$message.success('添加成功')
            this.on_submit_loading = false
          }).catch(() => {
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
