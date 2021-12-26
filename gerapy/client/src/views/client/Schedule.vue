<template>
  <div>
    <div class="panel" v-if="projectsLoading">
      <div class="panel-body" v-loading="projectsLoading">
        <el-table empty-text=""></el-table>
      </div>
    </div>
    <div class="panel" v-for="project in projects" :key="project">
      <panel-title :title="project"> </panel-title>
      <div class="panel-body" v-loading="projectsLoading">
        <el-table
          :data="spiders[project]"
          v-loading="spidersLoading[project]"
          :style="{ width: '100%' }"
        >
          <el-table-column prop="id" :label="$lang.columns.id" width="200">
          </el-table-column>

          <el-table-column prop="name" :label="$lang.columns.name" width="400">
          </el-table-column>
          <el-table-column :label="$lang.columns.operations">
            <template slot-scope="props">
              <el-button
                type="success"
                size="mini"
                @click="onStartSpider(project, props.row.name)"
              >
                <i class="fa fa-caret-right"></i>
                {{ $lang.buttons.run }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-collapse accordion @change="getLog">
          <el-collapse-item
            v-for="job in jobs[project]"
            :name="job.id"
            :key="job.id"
          >
            <template slot="title">
              <span
                v-if="job.spider"
                class="m-l-xs"
                :style="{ minWidth: '120px' }"
              >
                <i class="fa fa-bug"></i>
                {{ $lang.columns.spiderName }}:
                {{ job.spider }}
              </span>
              <span
                v-if="job.spider"
                class="m-l-md"
                :style="{ minWidth: '290px' }"
              >
                <i class="fa fa-key"></i>
                {{ $lang.columns.jobID }}:
                {{ job.id }}
              </span>
              <span
                v-if="job.start_time"
                class="m-l-md"
                :style="{ minWidth: '190px' }"
              >
                <i class="el-icon-time"></i>
                {{ $lang.columns.startTime }}:
                {{ job.start_time.substring(0, 16) }}
              </span>
              <span
                v-if="job.end_time"
                class="m-l-md"
                :style="{ minWidth: '190px' }"
              >
                <i class="el-icon-time"></i>
                {{ $lang.columns.endTime }}:
                {{ job.end_time.substring(0, 16) }}
              </span>
              <span class="m-l-md">
                <el-button
                  :type="jobStatusClass[job.status]"
                  size="mini"
                  class="pull-right m-r-md"
                >
                  <i
                    v-if="['pending'].includes(job.status)"
                    class="fa fa-circle-thin"
                  ></i>
                  <i
                    v-if="['running'].includes(job.status)"
                    class="fa fa-spin fa-spinner"
                  ></i>
                  <i
                    v-if="['finished'].includes(job.status)"
                    class="fa fa-check"
                  ></i>
                  {{ jobStatusText[job.status] }}
                </el-button>
                <el-button
                  type="danger"
                  size="mini"
                  class="pull-right m-r-md"
                  v-if="['pending', 'running'].includes(job.status)"
                  @click.stop="onCancelJob(job.id)"
                >
                  <i class="fa fa-remove"></i>
                  <span v-if="['pending'].includes(job.status)">
                    {{ $lang.buttons.cancel }}
                  </span>
                  <span v-if="['running'].includes(job.status)">
                    {{ $lang.buttons.stop }}
                  </span>
                </el-button>
              </span>
            </template>
            <div v-loading="logLoading" :element-loading-text="logLoadingText">
              <pre>{{ logs[job.id] }}</pre>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
  </div>
</template>
<script>
import PanelTitle from "../../components/PanelTitle";

export default {
  data() {
    return {
      // 连续获取错误次数
      errorCount: 0,
      // 所有项目
      projects: [],
      // 加载projects标志
      projectsLoading: true,
      // 所有爬虫 {'project1': ['spider1', 'spider2'], 'project2': ['spider1']}
      spiders: {},
      // 加载spiders标志
      spidersLoading: {},
      // 所有任务 {'project1': [{'id': '', 'spider': '', 'status': ''}]}
      jobs: {},
      // 任务状态
      jobStatuses: ["finished", "running", "pending"],
      // 任务状态class
      jobStatusClass: {
        finished: "info",
        running: "success",
        pending: "warning",
      },
      // 任务状态文本
      jobStatusText: {
        finished: this.$store.getters.$lang.buttons.finished,
        running: this.$store.getters.$lang.buttons.running,
        pending: this.$store.getters.$lang.buttons.pending,
      },
      // 任务信息 {'jobid': {'spider': 'spider1', 'project': 'project1'}}
      jobsInfo: {},
      // 日志信息 {'logid': 'text'}
      logs: {},
      // 加载logs标志
      logLoading: true,
      // 加载log提示语
      logLoadingText: this.$store.getters.$lang.messages.loading,
      // 定时刷新log指针
      logLoadingInterval: null,
      // 标记正在加载哪个log
      logLoadingActive: null,
      // 路由信息
      routeId: this.$route.params.id,
    };
  },
  components: {
    PanelTitle,
  },
  created() {
    this.getProjects();
    this.$store.commit(
      "addInterval",
      setInterval(() => {
        this.getJobs();
      }, 5000)
    );
  },
  methods: {
    //获取所有项目
    getProjects() {
      this.projectsLoading = true;
      this.$http
        .get(
          this.formatString(this.$store.state.url.client.projects, {
            id: this.routeId,
          })
        )
        .then(({ data: data }) => {
          this.projects = data;
          if (this.projects && this.projects.length === 0) {
            this.$message.info(this.$store.getters.$lang.messages.noProjects);
          }
          this.projectsLoading = false;
          this.projects.forEach((project) => {
            this.$set(this.spidersLoading, project, true);
          });
          this.errorCount = 0;
          // 获取所有爬虫
          this.getSpiders();
          // 获取所有任务
          this.getJobs();
        })
        .catch(() => {
          this.projectsLoading = false;
          this.errorCount += 1;
          if (this.errorCount >= 3) {
            this.$message.error(this.$store.getters.$lang.messages.errorLoad);
          } else {
            // 定时任务
            this.$store.commit(
              "setTimeout",
              setTimeout(() => {
                this.getProjects();
              }, 500)
            );
          }
        });
    },
    // 获取所有爬虫
    getSpiders() {
      this.projects.forEach((project) => {
        this.$http
          .get(
            this.formatString(this.$store.state.url.client.listSpiders, {
              id: this.routeId,
              project: project,
            })
          )
          .then(({ data: data }) => {
            this.$set(this.spiders, project, data);
            this.$set(this.spidersLoading, project, false);
          })
          .catch(() => {
            this.$set(this.spidersLoading, project, false);
          });
      });
    },
    // 获取所有任务
    getJobs() {
      this.projects.forEach((project) => {
        this.$http
          .get(
            this.formatString(this.$store.state.url.client.listJobs, {
              id: this.routeId,
              project: project,
            })
          )
          .then(({ data: data }) => {
            this.$set(this.jobs, project, data);
            for (let project in this.jobs) {
              let jobs = this.jobs[project];
              jobs.forEach((job) => {
                this.$set(this.jobsInfo, job.id, {
                  project: project,
                  spider: job["spider"],
                });
              });
            }
          });
      });
    },
    // 启动任务
    onStartSpider(project, spider) {
      this.$http
        .get(
          this.formatString(this.$store.state.url.client.startSpider, {
            id: this.routeId,
            project: project,
            spider: spider,
          })
        )
        .then(() => {
          this.$message.success(this.$store.getters.$lang.messages.successRun);
          this.getJobs();
        })
        .catch(() => {
          this.$message.error(this.$store.getters.$lang.messages.errorRun);
        });
    },
    // 获取日志
    getLog(job) {
      // 如果展开日志
      if (job) {
        //设置活跃日志
        this.logLoadingActive = job;
        // 正在加载
        this.logLoading = true;
        // 请求日志
        this.$http
          .get(
            this.formatString(this.$store.state.url.client.getLog, {
              id: this.routeId,
              project: this.jobsInfo[this.logLoadingActive]["project"],
              spider: this.jobsInfo[this.logLoadingActive]["spider"],
              job: this.logLoadingActive,
              random: Math.random(),
            })
          )
          .then(({ data: data }) => {
            //设置日志字典
            this.$set(this.logs, this.logLoadingActive, data);
            // 加载日志完成
            this.logLoading = false;
            // 定时任务获取最新爬取日志
            this.$store.commit(
              "setTimeout",
              setTimeout(() => {
                this.getLog(job);
              }, 2000)
            );
          })
          .catch(() => {
            this.logLoading = false;
          });
      } else {
        //闭合之后停止加载日志
        this.$store.commit("clearTimeout");
      }
    },
    onCancelJob(job) {
      this.$http
        .get(
          this.formatString(this.$store.state.url.client.cancelJob, {
            id: this.routeId,
            project: this.jobsInfo[job]["project"],
            job: job,
          })
        )
        .then(() => {
          this.$message.success(this.$store.getters.$lang.messages.canceling);
          this.getJobs();
        })
        .catch(() => {
          this.$message.error(this.$store.getters.$lang.messages.errorCancel);
        });
    },
  },
};
</script>
<style>
.el-collapse-item__content {
  padding: 15px 15px;
}
</style>
