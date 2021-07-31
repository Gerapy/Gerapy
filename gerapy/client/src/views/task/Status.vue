<template>
  <div id="task-status">
    <el-row :gutter="20">
      <el-col :span="6">
        <div class="panel">
          <panel-title :title="$lang.objects.task">
            <el-button
              type="primary"
              size="mini"
              @click="$router.push({ name: 'taskEdit', params: { id: id } })"
            >
              <i class="fa fa-edit"></i>
              {{ $lang.buttons.edit }}
            </el-button>
          </panel-title>
          <div class="panel-body" v-if="task">
            <el-form label-width="80px">
              <el-form-item :label="$lang.columns.trigger">
                <el-button size="mini" type="primary">{{
                  task.trigger
                }}</el-button>
              </el-form-item>
              <div v-if="task.configuration">
                <!-- date -->
                <div v-if="task.trigger === 'date'">
                  <el-form-item :label="$lang.columns.runDate">
                    <el-button size="mini" type="primary">{{
                      task.configuration.run_date
                    }}</el-button>
                  </el-form-item>
                  <el-form-item :label="$lang.columns.timezone">
                    <el-button size="mini" type="primary">{{
                      task.configuration.timezone
                    }}</el-button>
                  </el-form-item>
                </div>
                <!-- end date -->
                <!-- interval -->
                <div v-if="task.trigger === 'interval'">
                  <el-form-item
                    :label="$lang.columns.weeks"
                    v-if="task.configuration.weeks !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.weeks
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.days"
                    v-if="task.configuration.days !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.days
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.hours"
                    v-if="task.configuration.hours !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.hours
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.minutes"
                    v-if="task.configuration.minutes !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.minutes
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.seconds"
                    v-if="task.configuration.seconds !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.seconds
                    }}</el-button>
                  </el-form-item>
                  <el-form-item :label="$lang.columns.timezone">
                    <el-button size="mini" type="primary">{{
                      task.configuration.timezone
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.startDate"
                    v-if="task.configuration.start_date !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.start_date
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.endDate"
                    v-if="task.configuration.end_date !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.end_date
                    }}</el-button>
                  </el-form-item>
                </div>
                <!-- end interval -->
                <!-- cron -->
                <div v-if="task.trigger === 'cron'">
                  <el-form-item
                    :label="$lang.columns.year"
                    v-if="task.configuration.year !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.year
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.month"
                    v-if="task.configuration.month !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.month
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.week"
                    v-if="task.configuration.week !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.week
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.dayOfWeek"
                    v-if="task.configuration.day_of_week !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.day_of_week
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.day"
                    v-if="task.configuration.day !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.day
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.hour"
                    v-if="task.configuration.hour !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.hour
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.minute"
                    v-if="task.configuration.minute !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.minute
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.second"
                    v-if="task.configuration.second !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.second
                    }}</el-button>
                  </el-form-item>
                  <el-form-item :label="$lang.columns.timezone">
                    <el-button size="mini" type="primary">{{
                      task.configuration.timezone
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.startDate"
                    v-if="task.configuration.start_date !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.start_date
                    }}</el-button>
                  </el-form-item>
                  <el-form-item
                    :label="$lang.columns.endDate"
                    v-if="task.configuration.end_date !== null"
                  >
                    <el-button size="mini" type="primary">{{
                      task.configuration.end_date
                    }}</el-button>
                  </el-form-item>
                </div>
                <!-- end interval -->
              </div>
            </el-form>
          </div>
        </div>
      </el-col>
      <el-col :span="18" v-loading="loadingJob">
        <el-row v-if="jobs.length === 0">
          <el-col :span="24">
            <!--<el-alert-->
            <!--:title="$lang.messages.noTask"-->
            <!--type="info"-->
            <!--:closable="false">-->
            <!--</el-alert>-->
            <div class="panel">
              <panel-title :title="$lang.objects.task"> </panel-title>
              <div class="panel-body">
                <el-form>
                  <el-form-item :label="$lang.messages.noTask"> </el-form-item>
                </el-form>
              </div>
            </div>
          </el-col>
        </el-row>
        <el-row v-for="job in jobs">
          <el-col :span="24">
            <div class="panel">
              <panel-title :title="job.client.name">
                <el-button
                  type="primary"
                  size="mini"
                  @click="
                    $router.push({
                      name: 'clientSchedule',
                      params: { id: job.client.id },
                    })
                  "
                >
                  <i class="fa fa-sitemap"></i>
                  {{ $lang.buttons.schedule }}
                </el-button>
              </panel-title>
              <div class="panel-body">
                <el-row>
                  <el-col :span="8">
                    <el-form label-width="80px">
                      <el-form-item :label="$lang.objects.client">
                        <el-button type="primary" size="mini">
                          {{ job.client.name }}
                        </el-button>
                      </el-form-item>
                      <el-form-item :label="$lang.columns.lastTime">
                        <el-button
                          type="primary"
                          size="mini"
                          v-if="getLastRunTime(job)"
                        >
                          {{ getLastRunTime(job) }}
                        </el-button>
                      </el-form-item>
                      <el-form-item
                        :label="$lang.columns.nextTime"
                        v-if="getNextTunTime(job)"
                      >
                        <el-button type="primary" size="mini">
                          {{ getNextTunTime(job) }}
                        </el-button>
                      </el-form-item>
                    </el-form>
                  </el-col>
                  <el-col :span="5">
                    <div class="text-center">
                      <el-progress
                        type="circle"
                        :color="$store.state.color.primary"
                        :percentage="getRunPercent(job)"
                      ></el-progress>
                      <p class="description m-t-sm">
                        {{ $lang.descriptions.toNextTask }}
                      </p>
                    </div>
                  </el-col>
                  <el-col :span="4">
                    <div class="text-center">
                      <v-chart
                        :options="getRunStatusPieData(job)"
                        :style="{ width: '100%', height: '170px' }"
                        class="pie"
                      ></v-chart>
                      <p class="description m-t-n-lg">
                        {{ $lang.descriptions.successRate }}
                        {{ getSuccessRate(job) }}%
                      </p>
                    </div>
                  </el-col>
                  <el-col :span="4">
                    <el-form label-width="80px" class="m-t-md">
                      <el-form-item :label="$lang.columns.success">
                        <h1
                          class="number"
                          :style="{ color: $store.state.color.primary }"
                        >
                          {{ getSuccessExecutions(job).length }}
                        </h1>
                      </el-form-item>
                      <el-form-item :label="$lang.columns.error">
                        <h1
                          class="number"
                          :style="{ color: $store.state.color.error }"
                        >
                          {{ getErrorExecutions(job).length }}
                        </h1>
                      </el-form-item>
                    </el-form>
                  </el-col>
                </el-row>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PanelTitle from "../../components/PanelTitle";
import "echarts/lib/chart/pie";
import "echarts/lib/component/tooltip";

const dateFormat = require("date-format");

export default {
  data() {
    return {
      id: this.$route.params.id,
      jobs: [],
      task: null,
      loadingJob: false,
      errorSymbol: "error",
      openDate: dateFormat.asString(this.$store.state.dateFormat, new Date()),
    };
  },
  computed: {},
  mounted() {
    this.$store.commit(
      "addInterval",
      setInterval(() => {
        this.getJobsData();
      }, 3000)
    );
    this.getTaskData();
  },
  methods: {
    getJobsData() {
      this.$http
        .get(
          this.formatString(this.$store.state.url.task.status, {
            id: this.id,
          })
        )
        .then(({ data: { data: data } }) => {
          this.jobs = data;
        })
        .catch(() => {
          this.$message.error(this.$store.getters.$lang.messages.loadError);
        });
    },
    getTaskData() {
      this.$message.info(this.$store.getters.$lang.messages.gettingTaskData);
      if (this.id) {
        this.$http
          .get(
            this.formatString(this.$store.state.url.task.info, {
              id: this.id,
            })
          )
          .then(({ data: { data: data } }) => {
            this.task = data;
          })
          .catch(() => {
            this.$message.error(this.$store.getters.$lang.messages.loadError);
          });
      }
    },
    // next run time
    getNextTunTime(job) {
      if (!job || !job.next) return null;
      return dateFormat.asString(
        this.$store.state.dateFormat,
        new Date(Date.parse(job.next))
      );
    },
    // last turn time
    getLastRunTime(job) {
      if (!job || !job.executions || !job.executions.length > 0) return null;
      let lastExecution = job.executions[0];
      if (
        !lastExecution ||
        !lastExecution.fields ||
        !lastExecution.fields.run_time
      )
        return null;
      let runTime = lastExecution.fields.run_time;
      return dateFormat.asString(
        this.$store.state.dateFormat,
        new Date(Date.parse(runTime))
      );
    },
    getRunPercent(job) {
      if (!job) return 0;
      let lastRunTime = Date.parse(this.getLastRunTime(job));
      if (!lastRunTime || isNaN(lastRunTime))
        lastRunTime = Date.parse(this.openDate);
      let nextRunTime = Date.parse(this.getNextTunTime(job));
      if (!nextRunTime) return 0;
      let nowTime = Date.parse(new Date());
      let percent = parseInt(
        ((nowTime - lastRunTime) * 100) / (nextRunTime - lastRunTime)
      );
      return percent;
    },
    getSuccessExecutions(job) {
      if (!job || !job.executions || !job.executions.length > 0) return [];
      return job.executions.filter(
        (execution) =>
          execution.fields.status.toLowerCase().indexOf(this.errorSymbol) === -1
      );
    },
    getErrorExecutions(job) {
      if (!job || !job.executions || !job.executions.length > 0) return [];
      return job.executions.filter(
        (execution) =>
          execution.fields.status.toLowerCase().indexOf(this.errorSymbol) >= 0
      );
    },
    getSuccessRate(job) {
      if (!job) return 0;
      let successes = this.getSuccessExecutions(job);
      let errors = this.getErrorExecutions(job);
      if (successes.length + errors.length === 0) return 0;
      let rate = parseInt(
        (successes.length * 100) / (successes.length + errors.length)
      );
      return rate;
    },
    getRunStatusPieData(job) {
      let successes = this.getSuccessExecutions(job);
      let errors = this.getErrorExecutions(job);
      return {
        color: [this.$store.state.color.primary, this.$store.state.color.error],
        tooltip: {
          show: true,
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        series: [
          {
            name: this.$lang.descriptions.successRate,
            type: "pie",
            data: [
              { value: successes.length, name: this.$lang.columns.success },
              { value: errors.length, name: this.$lang.columns.error },
            ],
          },
        ],
      };
    },
  },
  components: {
    PanelTitle,
  },
};
</script>

<style scoped lang="scss">
#task-status {
  .el-form {
    .el-form-item {
      margin-bottom: 5px;
    }
  }
  .description {
    font-size: 14px;
    color: #606266;
  }
  .pie {
    position: relative;
    top: -20px;
  }
}

h1.number {
  font-weight: 100;
  margin: 10px 0;
  margin-top: 0;
}

.text {
  font-size: 14px;
  color: #535351;
}
</style>
