<template>
  <el-form
    ref="form"
    :model="formData"
    :rules="rules"
    label-width="100px"
    label-position="right"
  >
    <el-form-item :label="$lang.columns.name" prop="name">
      <el-input
        v-model="formData.name"
        :placeholder="$lang.messages.enter + ' ' + $lang.columns.name"
        size="small"
      ></el-input>
    </el-form-item>
    <el-form-item :label="$lang.columns.project" prop="project">
      <el-input
        v-model="formData.project"
        :placeholder="$lang.messages.enter + ' ' + $lang.columns.project"
        size="small"
      ></el-input>
    </el-form-item>

    <el-form-item :label="$lang.columns.spider" prop="spider">
      <el-input
        v-model="formData.spider"
        :placeholder="$lang.messages.enter + ' ' + $lang.columns.spider"
        size="small"
      ></el-input>
    </el-form-item>
    <el-form-item :label="$lang.columns.clients" prop="clients">
      <el-select
        v-model="formData.clients"
        multiple
        :placeholder="$lang.messages.select"
        size="small"
      >
        <el-option
          v-for="item in clientOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item :label="$lang.columns.trigger" prop="trigger">
      <el-select
        v-model="formData.trigger"
        :placeholder="$lang.messages.select"
        size="small"
      >
        <el-option
          v-for="item in triggerOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
    </el-form-item>
    <div v-if="formData.trigger === 'date'">
      <el-form-item :label="$lang.columns.runDate">
        <el-date-picker
          v-model="formData.configuration.run_date"
          class="inline width-200"
          type="datetime"
          size="small"
          :value-format="$store.state.dateFormat24"
          :picker-options="dateOptions"
          :placeholder="$lang.descriptions.chooseDateTime"
        >
        </el-date-picker>
      </el-form-item>
      <el-form-item :label="$lang.columns.timezone">
        <el-select
          v-model="formData.configuration.timezone"
          size="small"
          filterable
          :placeholder="$lang.columns.timezone"
          class="inline width-200"
        >
          <el-option
            v-for="item in timeZones"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </el-form-item>
    </div>
    <div v-if="formData.trigger === 'interval'">
      <el-form-item :label="$lang.columns.runDate">
        <el-form-item :label="$lang.columns.weeks">
          <el-input
            v-model.number="formData.configuration.weeks"
            :placeholder="$lang.columns.weeks"
            class="inline width-100"
            type="number"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.days">
          <el-input
            v-model.number="formData.configuration.days"
            class="inline width-100"
            type="number"
            :placeholder="$lang.columns.days"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.hours">
          <el-input
            v-model.number="formData.configuration.hours"
            class="inline width-100"
            type="number"
            :placeholder="$lang.columns.hours"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.minutes">
          <el-input
            v-model.number="formData.configuration.minutes"
            class="inline width-100"
            type="number"
            :placeholder="$lang.columns.minutes"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.seconds">
          <el-input
            v-model.number="formData.configuration.seconds"
            class="inline width-100"
            type="number"
            :placeholder="$lang.columns.seconds"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.timezone">
          <el-select
            v-model="formData.configuration.timezone"
            filterable
            :placeholder="$lang.columns.timezone"
            size="small"
            class="inline width-200"
          >
            <el-option
              v-for="item in timeZones"
              :key="item"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item :label="$lang.columns.startDate">
          <el-date-picker
            v-model="formData.configuration.start_date"
            :format="$store.state.dateFormat24"
            :value-format="$store.state.dateFormat24"
            type="datetime"
            size="small"
            :picker-options="dateOptions"
            class="inline width-200"
            :placeholder="$lang.columns.startDate"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item :label="$lang.columns.endDate">
          <el-date-picker
            v-model="formData.configuration.end_date"
            :picker-options="dateOptions"
            class="inline width-200"
            type="datetime"
            size="small"
            :format="$store.state.dateFormat24"
            :value-format="$store.state.dateFormat24"
            :placeholder="$lang.columns.endDate"
          >
          </el-date-picker>
        </el-form-item>
      </el-form-item>
    </div>
    <div v-if="formData.trigger === 'cron'">
      <el-form-item :label="$lang.columns.runDate">
        <el-form-item :label="$lang.columns.year">
          <el-input
            v-model="formData.configuration.year"
            :placeholder="$lang.columns.year"
            class="inline width-100"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.month">
          <el-input
            v-model="formData.configuration.month"
            :placeholder="$lang.columns.month"
            class="inline width-100"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.week">
          <el-input
            v-model="formData.configuration.week"
            class="inline width-100"
            :placeholder="$lang.columns.week"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.dayOfWeek">
          <el-input
            v-model="formData.configuration.day_of_week"
            class="inline width-100"
            :placeholder="$lang.columns.dayOfWeek"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.day">
          <el-input
            v-model="formData.configuration.day"
            class="inline width-100"
            :placeholder="$lang.columns.day"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.hour">
          <el-input
            v-model="formData.configuration.hour"
            class="inline width-100"
            :placeholder="$lang.columns.hour"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.minute">
          <el-input
            v-model="formData.configuration.minute"
            class="inline width-100"
            :placeholder="$lang.columns.minute"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.second">
          <el-input
            v-model="formData.configuration.second"
            class="inline width-100"
            :placeholder="$lang.columns.second"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item :label="$lang.columns.timezone">
          <el-select
            v-model="formData.configuration.timezone"
            size="small"
            filterable
            :placeholder="$lang.columns.timezone"
            class="inline width-200"
          >
            <el-option
              v-for="item in timeZones"
              :key="item"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item :label="$lang.columns.startDate">
          <el-date-picker
            v-model="formData.configuration.start_date"
            :format="$store.state.dateFormat24"
            :value-format="$store.state.dateFormat24"
            type="datetime"
            size="small"
            :picker-options="dateOptions"
            class="inline width-200"
            :placeholder="$lang.columns.startDate"
          >
          </el-date-picker>
        </el-form-item>
        <el-form-item :label="$lang.columns.endDate">
          <el-date-picker
            v-model="formData.configuration.end_date"
            :format="$store.state.dateFormat24"
            :value-format="$store.state.dateFormat24"
            type="datetime"
            size="small"
            :picker-options="dateOptions"
            class="inline width-200"
            :placeholder="$lang.columns.endDate"
          >
          </el-date-picker>
        </el-form-item>
      </el-form-item>
    </div>
    <div>
      <el-form-item>
        <slot name="submit"></slot>
        <el-button @click="$router.back()" size="small">
          <i class="fa fa-reply"></i>
          {{ $lang.buttons.return }}
        </el-button>
      </el-form-item>
    </div>
  </el-form>
</template>

<script>
const { listTimeZones } = require("timezone-support");
export default {
  name: "Substance",
  props: {
    id: {
      type: String,
      default: null,
    },
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
        },
      },
      clientOptions: [],
      dateOptions: {
        disabledDate(time) {
          // 设置今天及今天之后的日期
          return time.getTime() < Date.now() - 8.64e7;
        },
        shortcuts: [
          {
            text: this.$store.getters.$lang.titles.laterAtOnce,
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 5 * 1000);
              picker.$emit("pick", date);
            },
          },
          {
            text: this.$store.getters.$lang.titles.later1Min,
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 60 * 1000);
              picker.$emit("pick", date);
            },
          },
          {
            text: this.$store.getters.$lang.titles.later5Min,
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 5 * 60 * 1000);
              picker.$emit("pick", date);
            },
          },
          {
            text: this.$store.getters.$lang.titles.later10Min,
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 10 * 60 * 1000);
              picker.$emit("pick", date);
            },
          },
          {
            text: this.$store.getters.$lang.titles.laterHalfHour,
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 30 * 60 * 1000);
              picker.$emit("pick", date);
            },
          },
          {
            text: this.$store.getters.$lang.titles.later1Hour,
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 60 * 60 * 1000);
              picker.$emit("pick", date);
            },
          },
        ],
      },
      timeZones: listTimeZones(),
      rules: {
        name: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.name +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        project: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.project +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        spider: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.spider +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        timezone: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.timezone +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
      },
      triggerOptions: [
        {
          value: "date",
          label: "Date",
        },
        {
          value: "interval",
          label: "Interval",
        },
        {
          value: "cron",
          label: "Crontab",
        },
      ],
    };
  },
  mounted() {
    this.getClientData();
    this.getTaskData();
  },
  methods: {
    getClientData() {
      this.$http
        .get(this.$store.state.url.client.index)
        .then(({ data: clients }) => {
          clients.forEach((item) => {
            this.clientOptions.push({
              value: item.pk,
              label: item.fields.name,
            });
          });
        })
        .catch(() => {
          this.clients = [];
          this.$message.error(this.$store.getters.$lang.messages.loadError);
        });
    },
    getTaskData() {
      if (this.id) {
        this.$http
          .get(
            this.formatString(this.$store.state.url.task.info, {
              id: this.id,
            })
          )
          .then(({ data: { data: client } }) => {
            this.formData = client;
          })
          .catch(() => {
            this.$message.error(this.$store.getters.$lang.messages.loadError);
          });
      }
    },
  },
};
</script>

<style lang="scss">
.el-date-editor.el-input {
  width: 152px;
}

.el-tag.el-tag--info {
  color: #35cbaa;
}

.el-select .el-tag__close.el-icon-close {
  background-color: #eeeeee;
  &:hover {
    background-color: #cccccc;
  }
}

.el-picker-panel {
  .el-picker-panel__footer {
    .el-button.el-picker-panel__link-btn.el-button--text.el-button--mini {
      display: none;
    }
  }
  .el-picker-panel__sidebar {
    .el-picker-panel__shortcut {
      font-size: 12px;
    }
  }
}
</style>
