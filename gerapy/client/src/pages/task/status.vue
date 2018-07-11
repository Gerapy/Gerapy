<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="panel">
          <panel-title :title="$lang[$store.state.lang].objects.task">
          </panel-title>
          <div class="panel-body">
            <div class="m-b">
              <el-button type="primary" size="mini">{{ task.trigger }}</el-button>
              <span class="text">{{ task.configuration }}</span>
            </div>
            <div class="m-b">
              <el-button type="primary" size="mini">
                {{ $lang[$store.state.lang].objects.project }}
              </el-button>
              <span class="text">{{ task.project }}</span>
            </div>
            <div class="m-b">
              <el-button type="primary" size="mini">
                {{ $lang[$store.state.lang].objects.spider }}
              </el-button>
              <span class="text">{{ task.spider }}</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="8" v-for="job in jobs">
        <div class="panel">
          <panel-title :title="$lang[$store.state.lang].objects.job">
          </panel-title>
          <div class="panel-body" v-loading="loadingJob">
            <div class="m-b">
              <el-button type="primary" size="mini" class="m-r-xs">
                {{ $lang[$store.state.lang].objects.client }}
              </el-button>
              <span class="text">{{ job.client.name }}</span>
            </div>
            <div class="m-b">
              <el-button type="primary" size="mini" class="m-r-xs">
                {{ $lang[$store.state.lang].buttons.nextTime }}
              </el-button>
              <span class="text">{{ job.next }}</span>
            </div>
            <el-row class="text-center m-t-md">
              <el-col :span="12">
                <h1 class="number">{{ executedJobs(job) }}</h1>
                <small> {{ $lang[$store.state.lang].descriptions.executedJobs }}</small>
              </el-col>
              <el-col :span="12">
                <h1 class="number">{{ errorJobs(job) }}</h1>
                <small> {{ $lang[$store.state.lang].descriptions.errorJobs }}</small>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {panelTitle} from 'components'

  export default {
    data() {
      return {
        id: this.$route.params.id,
        jobs: [],
        task: null,
        loadingJob: false,
      }
    },
    computed: {},
    mounted() {
      setInterval(() => {
        this.getJobsData()
      }, 2000)
      this.getTaskData()
    },
    methods: {
      getJobsData() {
        this.$fetch.apiTask.status({
          id: this.id
        }).then(({data: {data: data}}) => {
          this.jobs = data
        }).catch(() => {
          this.$message.error(this.$lang[this.$store.state.lang].messages.loadError)
        })
      },
      getTaskData() {
        if (this.id) {
          this.$fetch.apiTask.info({
            id: this.id
          }).then(({data: {data: data}}) => {
            this.task = data
          }).catch(() => {
            this.$message.error(this.$lang[this.$store.state.lang].messages.loadError)
          })
        }
      },
      executedJobs(job) {
        let count = 0
        job.executions.forEach((execution) => {
          console.log('eee', execution)
          if (execution.fields.status === 'Started execution') {
            count += 1
          }
        })
        return count
      },
      errorJobs(job) {
        let count = 0
        job.executions.forEach((execution) => {
          if (execution.fields.status === 'Error!') {
            count += 1
          }
        })
        return count
      }
    },
    components: {
      panelTitle,
    },
  }
</script>

<style scoped>
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
