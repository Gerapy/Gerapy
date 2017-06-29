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
          <el-collapse-item :name="job.id" v-for="job in jobs[project]">
            <template slot="title">
                <span class="wrapper">
                  <el-button :type="jobStatusClass[job.status]" size="mini">
                    {{ jobStatusText[job.status] }}
                  </el-button>
                </span>
              <span>{{ job.id }}</span>
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
            <div>{{ logs[job.id] }}</div>
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
        logs:{},
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
      getLog(activeName){
        console.log(activeName)
      }
    }
  }
</script>
