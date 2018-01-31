<template>
  <div class="panel">
    <panel-title :title="$lang[$store.state.lang].titles.createTask"></panel-title>
    <div class="panel-body"
         v-loading="loadData"
         :element-loading-text="$lang[$store.state.lang].messages.loading">
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" label-width="100px">
            <el-form-item :label="$lang[$store.state.lang].columns.name" prop="name">
              <el-input v-model="form.name"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.name"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.clients">
              <el-select v-model="clients" multiple placeholder="请选择" size="small">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.project" prop="project">
              <el-input v-model="project"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.project"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.spider" prop="project">
              <el-input v-model="project"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.spider"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.trigger" prop="trigger">
              <el-select v-model="trigger" placeholder="请选择" size="small">
                <el-option
                  v-for="item in triggerOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <div v-if="trigger=='date'">
              <el-form-item label="Rundate" prop="timezone">
                <el-date-picker v-model="configuration.run_date" type="date"
                                placeholder="选择日期" size="small"
                                :picker-options="dateOptions">
                </el-date-picker>
                <el-time-picker v-model="configuration.run_time"
                                :picker-options="timeOptions"
                                size="small"></el-time-picker>
              </el-form-item>
            </div>
            <div v-if="trigger=='interval'">
              <el-form-item label="run_date" prop="timezone" class="line-run-date">
                <el-input v-model="configuration.weeks"
                          placeholder="weeks"
                          class="inline" type="number"
                          size="small"></el-input>
                <el-input v-model="configuration.days"
                          class="inline" type="number"
                          placeholder="days"
                          size="small"></el-input>
                <el-input v-model="configuration.hours"
                          class="inline" type="number"
                          placeholder="hours"
                          size="small"></el-input>
                <el-input v-model="configuration.minutes"
                          class="inline" type="number"
                          placeholder="minutes"
                          size="small"></el-input>
                <el-input v-model="configuration.seconds"
                          class="inline" type="number"
                          placeholder="seconds"
                          size="small"></el-input>
                <el-date-picker
                  v-model="configuration.start_date"
                  type="datetime" size="small"
                  placeholder="Start date">
                </el-date-picker>
                <el-date-picker
                  v-model="configuration.end_date"
                  type="datetime" size="small"
                  placeholder="end date">
                </el-date-picker>
              </el-form-item>
            </div>
            <div v-if="trigger=='cron'">
              <el-form-item label="run_date" prop="timezone">
                <el-input v-model="configuration.run_time"
                          :picker-options="timeOptions"
                          size="small"></el-input>
              </el-form-item>
              <el-form-item label="timezone" prop="timezone">
                <el-input v-model="configuration.timezone"
                          size="small"></el-input>
              </el-form-item>
            </div>
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
        clients: [],
        trigger: null,
        configuration: {
          run_date: null,
          run_time: null,
          weeks: null,
          days: null,
          hours: null,
          minutes: null,
          seconds: null,
          start_date: null,
          end_date: null,
        },
        dateOptions: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7
          }
        },
        timeOptions: {
          selectableRange: '00:00:00 - 23:59:59'
        },
        options: [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '黄金糕2'
        }],
        triggerOptions: [{
          value: 'date',
          label: 'Date',
        }, {
          value: 'interval',
          label: 'Interval'
        }, {
          value: 'cron',
          label: 'Crontab'
        }],
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
      }
    },
    methods: {
      //提交
      onSubmitForm(){
        this.$refs.form.validate((valid) => {
          if (!valid)
            return false
          this.onSubmitLoading = true
          this.$fetch.apiTask.create(
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
<style>
  .line-run-date {
    width: 1000px
  }

  .line-run-date .inline {
    width: 200px
  }
</style>
