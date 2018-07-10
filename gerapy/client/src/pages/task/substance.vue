<template>
  <el-form ref="form" :model="formData" :rules="rules" label-width="100px">
    <el-form-item :label="$lang[$store.state.lang].columns.name" prop="name">
      <el-input v-model="formData.name"
                :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.name"
                size="small"></el-input>
    </el-form-item>
    <el-form-item :label="$lang[$store.state.lang].columns.clients" prop="clients">
      <el-select v-model="formData.clients" multiple :placeholder="$lang[$store.state.lang].messages.select"
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
      <el-input v-model="formData.project"
                :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.project"
                size="small"></el-input>
    </el-form-item>
    <el-form-item :label="$lang[$store.state.lang].columns.spider" prop="spider">
      <el-input v-model="formData.spider"
                :placeholder="$lang[$store.state.lang].messages.enter + ' ' + $lang[$store.state.lang].columns.spider"
                size="small"></el-input>
    </el-form-item>
    <el-form-item :label="$lang[$store.state.lang].columns.trigger" prop="trigger">
      <el-select v-model="formData.trigger" :placeholder="$lang[$store.state.lang].messages.select" size="small">
        <el-option
          v-for="item in triggerOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </el-form-item>
    <div v-if="formData.trigger=='date'">
      <el-form-item :label="$lang[$store.state.lang].columns.runDate">
        <el-date-picker v-model="formData.configuration.run_date"
                        type="datetime" size="small" :picker-options="dateOptions"
                        :placeholder="$lang[$store.state.lang].descriptions.chooseDateTime">
        </el-date-picker>
        <el-input v-model="formData.configuration.timezone"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.timezone"
                  size="small"></el-input>
      </el-form-item>
    </div>
    <div v-if="formData.trigger=='interval'">
      <el-form-item :label="$lang[$store.state.lang].columns.runDate">
        <el-input v-model.number="formData.configuration.weeks"
                  :placeholder="$lang[$store.state.lang].columns.weeks"
                  class="inline width-100" type="number"
                  size="small"></el-input>
        <el-input v-model.number="formData.configuration.days"
                  class="inline width-100" type="number"
                  :placeholder="$lang[$store.state.lang].columns.days"
                  size="small"></el-input>
        <el-input v-model.number="formData.configuration.hours"
                  class="inline width-100" type="number"
                  :placeholder="$lang[$store.state.lang].columns.hours"
                  size="small"></el-input>
        <el-input v-model.number="formData.configuration.minutes"
                  class="inline width-100" type="number"
                  :placeholder="$lang[$store.state.lang].columns.minutes"
                  size="small"></el-input>
        <el-input v-model.number="formData.configuration.seconds"
                  class="inline width-100" type="number"
                  :placeholder="$lang[$store.state.lang].columns.seconds"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.timezone"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.timezone"
                  size="small"></el-input>
        <el-date-picker
          v-model="formData.configuration.start_date"
          type="datetime" size="small" :picker-options="dateOptions"
          :placeholder="$lang[$store.state.lang].columns.startDate">
        </el-date-picker>
        <el-date-picker
          v-model="formData.configuration.end_date" :picker-options="dateOptions"
          type="datetime" size="small"
          :placeholder="$lang[$store.state.lang].columns.endDate">
        </el-date-picker>
      </el-form-item>
    </div>
    <div v-if="formData.trigger=='cron'">
      <el-form-item :label="$lang[$store.state.lang].columns.runDate">
        <el-input v-model="formData.configuration.year"
                  :placeholder="$lang[$store.state.lang].columns.year"
                  class="inline width-100"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.month"
                  :placeholder="$lang[$store.state.lang].columns.month"
                  class="inline width-100"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.day"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.day"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.week"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.week"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.day_of_week"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.dayOfWeek"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.hour"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.hour"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.minute"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.minute"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.second"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.second"
                  size="small"></el-input>
        <el-input v-model="formData.configuration.timezone"
                  class="inline width-100"
                  :placeholder="$lang[$store.state.lang].columns.timezone"
                  size="small"></el-input>
        <el-date-picker
          v-model="formData.configuration.start_date"
          type="datetime" size="small" :picker-options="dateOptions"
          :placeholder="$lang[$store.state.lang].columns.startDate">
        </el-date-picker>
        <el-date-picker
          v-model="formData.configuration.end_date" :picker-options="dateOptions"
          type="datetime" size="small"
          :placeholder="$lang[$store.state.lang].columns.endDate">
        </el-date-picker>
      </el-form-item>
    </div>
    <div>
      <el-form-item>
        <slot name="submit"></slot>
        <el-button @click="$router.back()" size="small">
          <i class="fa fa-reply"></i>
          {{ $lang[$store.state.lang].buttons.return }}
        </el-button>
      </el-form-item>
    </div>
  </el-form>
</template>

<script>
  export default {
    props: {
      id: {
        type: String,
        default: null
      }
    },
    data() {
      return {
        formData: {
          name: null,
          clients: [],
          trigger: null,
          project: null,
          spider: null,
          configuration: {
            run_date: null,
            weeks: null,
            days: null,
            hours: null,
            minutes: null,
            seconds: null,
            month: null,
            week: null,
            day: null,
            hour: null,
            minute: null,
            second: null,
            year: null,
            day_of_week: null,
            timezone: null,
            start_date: null,
            end_date: null,
          }
        },
        clientOptions: [],
        dateOptions: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7
          }
        },
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
      }
    },
    mounted() {
      this.getClientData()
      this.getTaskData()
    },
    methods: {
      getClientData() {
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
      getTaskData() {
        if (this.id) {
          this.$fetch.apiTask.info({
            id: this.id
          }).then(({data: {data: client}}) => {
            this.formData = client
          }).catch(() => {
            this.$message.error(this.$lang[this.$store.state.lang].messages.loadError)
          })
        }
      },
    }
  }
</script>

<style scoped>
  .el-date-editor.el-input {
    width: 152px;
  }
</style>
