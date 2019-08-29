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
            :label="$lang[$store.state.lang].columns.id"
            width="200">
          </el-table-column>
          <el-table-column
            prop="name"
            :label="$lang[$store.state.lang].columns.name"
            width="400">
          </el-table-column>
          <el-table-column
            :label="$lang[$store.state.lang].columns.operations">
            <template slot-scope="props">
              <el-button type="success" size="mini" @click="startSpider(project, props.row.name)">
                <i class="fa fa-caret-right"></i>
                {{ $lang[$store.state.lang].buttons.run }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-collapse accordion @change="getLog">
          <el-collapse-item v-for="job in jobs[project]" :name="job.id" :key="job.id">
            <template slot-scope="title">
              <span v-if="job.spider">
                <i class="fa fa-bug"></i>
                {{ $lang[$store.state.lang].columns.spiderName }}:
                {{ job.spider }}
              </span>
              <span v-if="job.spider" class="m-l-md">
                <i class="fa fa-key"></i>
                {{ $lang[$store.state.lang].columns.jobID }}:
                {{ job.id }}
              </span>
              <span v-if="job.start_time" class="m-l-md">
                <i class="el-icon-time"></i>
                {{ $lang[$store.state.lang].columns.startTime }}:
                {{ job.start_time.substring(0, 16) }}
              </span>
              <span v-if="job.end_time" class="m-l-md">
                <i class="el-icon-time"></i>
                {{ $lang[$store.state.lang].columns.endTime }}:
                {{ job.end_time.substring(0, 16) }}
              </span>
              <span class="wrapper">
                <el-button :type="jobStatusClass[job.status]" size="mini" class="pull-right m-t-sm m-r-md">
                  {{ jobStatusText[job.status] }}
                </el-button>
                <el-button type="danger" size="mini" class="pull-right m-t-sm m-r-md"
                           v-if="['pending', 'running'].includes(job.status)" @click.stop="cancelJob(job.id)">
                  <i class="fa fa-remove"></i>
                  <span v-if="['pending'].includes(job.status)">
                    {{ $lang[$store.state.lang].buttons.cancel }}
                  </span>
                  <span v-if="['running'].includes(job.status)">
                    {{ $lang[$store.state.lang].buttons.stop }}
                  </span>
                </el-button>
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
import { panelTitle, bottomToolBar } from "components";
export default {
  data() {
    return {
      // 所有项目
      projects: [],
      // 加载projects标志
      projectsLoadData: true,
      // 所有爬虫 {'project1': ['spider1', 'spider2'], 'project2': ['spider1']}
      spiders: {},
      // 加载spiders标志
      spidersLoadData: {},
      // 所有任务 {'project1': [{'id': '', 'spider': '', 'status': ''}]}
      jobs: {},
      // 任务状态
      jobStatuses: ["finished", "running", "pending"],
      // 任务状态class
      jobStatusClass: {
        finished: "info",
        running: "success",
        pending: "warning"
      },
      // 任务状态文本
      jobStatusText: {
        finished: this.$lang[this.$store.state.lang].buttons.finished,
        running: this.$lang[this.$store.state.lang].buttons.running,
        pending: this.$lang[this.$store.state.lang].buttons.pending
      },
      // 任务信息 {'jobid': {'spider': 'spider1', 'project': 'project1'}}
      jobsInfo: {},
      // 日志信息 {'logid': 'text'}
      logs: {},
      // 加载logs标志
      logLoadData: true,
      // 加载log提示语
      logLoadDataText: this.$lang[this.$store.state.lang].messages.loading,
      // 定时刷新log指针
      logLoadDataInterval: null,
      // 标记正在加载哪个log
      logLoadDataActive: null,
      // 路由信息
      routeId: this.$route.params.id
    };
  },
  components: {
    panelTitle,
    bottomToolBar
  },
  created() {
    this.getProjects();
    this.$store.dispatch(
      "addInterval",
      setInterval(() => {
        this.getJobs();
      }, 5000)
    );
  },
  methods: {
    //获取所有项目
    getProjects() {
      this.$fetch.apiClient
        .projects({
          id: this.routeId
        })
        .then(({ data: data }) => {
          this.projects = data;
          this.projectsLoadData = false;
          this.projects.forEach(project => {
            this.$set(this.spidersLoadData, project, true);
          });
          // 获取所有爬虫
          this.getSpiders();
          // 获取所有任务
          this.getJobs();
        })
        .catch(() => {
          //this.$message.error('获取项目失败，正在重试')
          this.projectsLoadData = false;
          this.getProjects();
        });
    },
    // 获取所有爬虫
    getSpiders() {
      this.projects.forEach(project => {
        this.$fetch.apiClient
          .listSpiders({
            id: this.routeId,
            project: project
          })
          .then(({ data: data }) => {
            this.$set(this.spiders, project, data);
            this.$set(this.spidersLoadData, project, false);
          })
          .catch(() => {
            this.$set(this.spidersLoadData, project, false);
          });
      });
    },
    // 获取所有任务
    getJobs() {
      this.projects.forEach(project => {
        this.$fetch.apiClient
          .listJobs({
            id: this.routeId,
            project: project
          })
          .then(({ data: data }) => {
            this.$set(this.jobs, project, data);
            for (let project in this.jobs) {
              let jobs = this.jobs[project];
              jobs.forEach(job => {
                this.$set(this.jobsInfo, job.id, {
                  project: project,
                  spider: job["spider"]
                });
              });
            }
          })
          .catch(() => {
            //this.$message.error('获取任务失败')
          });
      });
    },
    // 启动任务
    startSpider(project, spider) {
      this.$fetch.apiClient
        .startSpider({
          id: this.routeId,
          project: project,
          spider: spider
        })
        .then(() => {
          this.$message.success(
            this.$lang[this.$store.state.lang].messages.successRun
          );
          this.getJobs();
        })
        .catch(() => {
          this.$message.error(
            this.$lang[this.$store.state.lang].messages.errorRun
          );
        });
    },
    // 获取日志
    getLog(job) {
      // 如果展开日志
      if (job) {
        //设置活跃日志
        this.logLoadDataActive = job;
        // 正在加载
        this.logLoadData = true;
        // 请求日志
        this.$fetch.apiClient
          .getLog({
            id: this.routeId,
            project: this.jobsInfo[this.logLoadDataActive]["project"],
            spider: this.jobsInfo[this.logLoadDataActive]["spider"],
            job: this.logLoadDataActive,
            random: Math.random()
          })
          .then(({ data: data }) => {
            //设置日志字典
            this.$set(this.logs, this.logLoadDataActive, data);
            // 加载日志完成
            this.logLoadData = false;
            // 定时任务
            this.$store.dispatch(
              "setTimeout",
              setTimeout(() => {
                this.getLog(job);
              }, 2000)
            );
          })
          .catch(() => {
            // 如果错误
            this.logLoadData = false;
          });
      } else {
        //闭合之后停止加载日志
        this.$store.dispatch("clearTimeout");
      }
    },
    cancelJob(job) {
      this.$fetch.apiClient
        .cancelJob({
          id: this.routeId,
          project: this.jobsInfo[job]["project"],
          job: job
        })
        .then(() => {
          this.$message.success(
            this.$lang[this.$store.state.lang].messages.canceling
          );
          this.getJobs();
        })
        .catch(() => {
          //如果错误
          this.$message.error(
            this.$lang[this.$store.state.lang].messages.errorCancel
          );
        });
    }
  }
};
</script>
<style>
.el-collapse-item__content {
  padding: 15px 15px;
}
</style>
