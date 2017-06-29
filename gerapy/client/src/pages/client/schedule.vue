<template>
  <div>
    <div class="panel" v-for="project in projects" :key="project">
      <panel-title :title="project">
        <el-button @click.stop="onRefresh" size="small">
          <i class="fa fa-refresh"></i>
        </el-button>
      </panel-title>
      <div class="panel-body" v-loading="projectsLoadData">
        <el-table
          :data="spiders[project]"
          v-loading="spidersLoadData[project]"
          element-loading-text="拼命加载中"
          style="width: 100%;">
          <el-table-column
            prop="id"
            label="ID"
            width="200">
          </el-table-column>
          <el-table-column
            prop="name"
            label="爬虫名称"
            width="400">
          </el-table-column>
          <el-table-column
            label="操作">
            <template scope="props">
              <el-button type="success" size="small" icon="arrow-right" @click="startSpider(project, props.row.name)">运行
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-collapse accordion @change="getLog">
          <el-collapse-item v-for="job in jobs[project]" :name="job.id">
            <template slot="title">
              <span class="wrapper">
                <el-button :type="jobStatusClass[job.status]" size="mini">
                  {{ jobStatusText[job.status] }}
                </el-button>
              </span>
              <span v-if="job.spider">
                <i class="fa fa-bug"></i>
                爬虫名称：
                {{ job.spider }}
              </span>
              <span v-if="job.spider" class="m-l-md">
                <i class="fa fa-key"></i>
                任务代号：{{ job.id }}
              </span>
              <span v-if="job.start_time" class="m-l-md">
                <i class="el-icon-time"></i>
                开始时间：
                {{ job.start_time.substring(0, 16) }}
              </span>
              <span v-if="job.end_time" class="m-l-md">
                <i class="el-icon-time"></i>
                结束时间：
                {{ job.end_time.substring(0, 16) }}
              </span>
            </template>
            <div v-loading="logLoadData" :element-loading-text="logLoadDataText">
              <pre>{{ logs[job.id] }}</pre>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  export default{
    data(){
      return {
        projects: [],
        spiders: {},
        jobs: {},
        projectsLoadData: true,
        spidersLoadData: {},
        logLoadData: true,
        logLoadDataText: '日志加载中',
        logLoadDataInterval: null,
        logLoadDataActive: null,
        jobStatuses: ['finished', 'running', 'pending'],
        jobStatusClass: {
          finished: 'info',
          running: 'success',
          pending: 'warning'
        },
        jobStatusText: {
          finished: '已完成',
          running: '运行中',
          pending: '等待中'
        },
        jobsInfo: {},
        logs: {},
        routeId: this.$route.params.id,
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getProjects()
    },
    methods: {
      getProjects() {
        this.$fetch.apiClient.projects({
          id: this.routeId
        }).then(({data: data}) => {
          this.projects = data
          this.projectsLoadData = false
          this.projects.forEach((project) => {
            this.getSpiders(project)
            this.getJobs(project)
            this.$set(this.spidersLoadData, project, true)
          })
        }).catch(() => {
          this.projectsLoadData = false
        })
      },
      getSpiders(project) {
        this.$fetch.apiClient.listSpiders({
          id: this.routeId,
          project: project
        }).then(({data: data}) => {
          this.$set(this.spiders, project, data)
          this.$set(this.spidersLoadData, project, false)
        }).catch(() => {
          this.$set(this.spidersLoadData, project, false)
        })
      },
      getJobs(project) {
        this.$fetch.apiClient.listJobs({
          id: this.routeId,
          project: project
        }).then(({data: data}) => {
          this.$set(this.jobs, project, data)
          console.log('JJJJJobs', this.jobs)
          for (let project in this.jobs) {
            let jobs = this.jobs[project]
            console.log(jobs)
            jobs.forEach((job) => {
              console.log(job)
              this.$set(this.jobsInfo, job.id, {project: project, spider: job['spider']})
            })
          }
        }).catch(() => {
        })
      },
      startSpider(project, spider){
        console.log(project, spider)
        this.$fetch.apiClient.startSpider({
          id: this.routeId,
          project: project,
          spider: spider,
        }).then(({data: data}) => {
          console.log('Re', data)
        }).catch(() => {
        })
      },

      getLog(job){
        // 如果展开日志
        if (job) {
          //设置活跃日志
          this.logLoadDataActive = job
          // 正在加载
          this.logLoadData = true
          // 请求日志
          this.$fetch.apiClient.getLog({
            id: this.routeId,
            project: this.jobsInfo[this.logLoadDataActive]['project'],
            spider: this.jobsInfo[this.logLoadDataActive]['spider'],
            job: this.logLoadDataActive,
            random: Math.random()
          }).then(({data: data}) => {
            //设置日志字典
            this.$set(this.logs, this.logLoadDataActive, data)
            // 加载日志完成
            this.logLoadData = false
            // 如果不存在定时任务
            if (!this.logLoadDataInterval) {
              // 设置定时任务，调度当前活跃日志
              this.logLoadDataInterval = setInterval(() => {
                this.getLog(this.logLoadDataActive)
              }, 2000)
            }
          }).catch(() => {
            //如果错误
            this.logLoadData = false
          })
        } else {
          //闭合之后停止加载日志
          clearInterval(this.logLoadDataInterval)
          this.logLoadDataInterval = null
        }
      }
    }
  }
</script>
<style>
  .el-collapse-item__content {
    padding: 15px 15px;
  }
</style>
