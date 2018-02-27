<template>
  <div class="panel">
    <panel-title :title="$lang[$store.state.lang].titles.createTask"></panel-title>
    <div class="panel-body"
         v-loading="loadData"
         :element-loading-text="$lang[$store.state.lang].messages.loading">
      <el-row>
        <el-col :span="10">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <el-form-item :label="$lang[$store.state.lang].columns.name" prop="name">
              <el-input v-model="form.name"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.name"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.clients" prop="clients">
              <el-select v-model="form.clients" multiple :placeholder="$lang[$store.state.lang].messages.select"
                         size="small">
                <el-option
                  v-for="item in clientOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.project" prop="project">
              <el-input v-model="form.project"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.project"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.spider" prop="spider">
              <el-input v-model="form.spider"
                        :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.spider"
                        size="small"></el-input>
            </el-form-item>
            <el-form-item :label="$lang[$store.state.lang].columns.trigger" prop="trigger">
              <el-select v-model="form.trigger" :placeholder="$lang[$store.state.lang].messages.select" size="small">
                <el-option
                  v-for="item in triggerOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <div v-if="form.trigger=='date'">
              <el-form-item :label="$lang[$store.state.lang].columns.runDate">
                <el-date-picker v-model="form.configuration.run_date"
                                type="datetime" size="small" :picker-options="dateOptions"
                                :placeholder="$lang[$store.state.lang].descriptions.chooseDateTime">
                </el-date-picker>
              </el-form-item>
            </div>
            <div v-if="form.trigger=='interval'">
              <el-form-item :label="$lang[$store.state.lang].columns.runDate">
                <el-input v-model="form.configuration.months"
                          :placeholder="$lang[$store.state.lang].columns.months"
                          class="inline width-100" type="number"
                          size="small"></el-input>
                <el-input v-model="form.configuration.weeks"
                          :placeholder="$lang[$store.state.lang].columns.weeks"
                          class="inline width-100" type="number"
                          size="small"></el-input>
                <el-input v-model="form.configuration.days"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.days"
                          size="small"></el-input>
                <el-input v-model="form.configuration.hours"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.hours"
                          size="small"></el-input>
                <el-input v-model="form.configuration.minutes"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.minutes"
                          size="small"></el-input>
                <el-input v-model="form.configuration.seconds"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.seconds"
                          size="small"></el-input>
                <el-date-picker
                  v-model="form.configuration.start_date"
                  type="datetime" size="small" :picker-options="dateOptions"
                  :placeholder="$lang[$store.state.lang].columns.startDate">
                </el-date-picker>
                <el-date-picker
                  v-model="form.configuration.end_date" :picker-options="dateOptions"
                  type="datetime" size="small"
                  :placeholder="$lang[$store.state.lang].columns.endDate">
                </el-date-picker>
              </el-form-item>
            </div>
            <div v-if="form.trigger=='cron'">
              <el-form-item :label="$lang[$store.state.lang].columns.runDate">
                <el-input v-model="form.configuration.year"
                          :placeholder="$lang[$store.state.lang].columns.year"
                          class="inline width-100" type="number"
                          size="small"></el-input>
                <el-input v-model="form.configuration.month"
                          :placeholder="$lang[$store.state.lang].columns.month"
                          class="inline width-100" type="number"
                          size="small"></el-input>
                <el-input v-model="form.configuration.day"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.day"
                          size="small"></el-input>
                <el-input v-model="form.configuration.week"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.week"
                          size="small"></el-input>
                <el-input v-model="form.configuration.day_of_week"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.dayOfWeek"
                          size="small"></el-input>
                <el-input v-model="form.configuration.hour"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.hour"
                          size="small"></el-input>
                <el-input v-model="form.configuration.minute"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.minute"
                          size="small"></el-input>
                <el-input v-model="form.configuration.second"
                          class="inline width-100" type="number"
                          :placeholder="$lang[$store.state.lang].columns.second"
                          size="small"></el-input>
                <el-date-picker
                  v-model="form.configuration.start_date"
                  type="datetime" size="small" :picker-options="dateOptions"
                  :placeholder="$lang[$store.state.lang].columns.startDate">
                </el-date-picker>
                <el-date-picker
                  v-model="form.configuration.end_date" :picker-options="dateOptions"
                  type="datetime" size="small"
                  :placeholder="$lang[$store.state.lang].columns.endDate">
                </el-date-picker>
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
        form: {
          name: null,
          clients: [],
          trigger: null,
          project: null,
          spider: null,
          configuration: {
            run_date: null,
            months: null,
            weeks: null,
            days: null,
            hours: null,
            minutes: null,
            seconds: null,
            start_date: null,
            end_date: null,
            month: null,
            week: null,
            day: null,
            hour: null,
            minute: null,
            second: null,
            year: null,
            day_of_week: null,
          }
        },
        clientOptions: [],
        dateOptions: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7
          }
        },
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
          project: [
            {
              required: true,
              message: this.$lang[this.$store.state.lang].columns.project + ' ' + this.$lang[this.$store.state.lang].messages.isNull,
              trigger: 'blur'
            }
          ],
          spider: [
            {
              required: true,
              message: this.$lang[this.$store.state.lang].columns.spider + ' ' + this.$lang[this.$store.state.lang].messages.isNull,
              trigger: 'blur'
            }
          ]
        }

      }
    },
    created() {
      this.getClientData()
    },
    methods: {
      getClientData(){
        this.$fetch.apiClient.index(
        ).then(({data: clients}) => {
          clients.forEach((item) => {
            this.clientOptions.push({
              value: item.pk,
              label: item.fields.name
            })
          })
        }).catch(() => {
          this.clients = []
          this.$message.error(this.$lang[this.$store.state.lang].messages.loadError)
        })
      },
      onSubmitForm(){
        this.$refs.form.validate((valid) => {
          if (!valid)
            return false
          this.onSubmitLoading = true
          this.$fetch.apiTask.create(this.form).then(() => {
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
    },
    computed: {}
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
