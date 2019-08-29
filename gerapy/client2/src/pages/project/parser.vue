<template>
  <div>
    <el-row class="m-b-md">
      <el-col :span="24" id="console" class="p-md">
        <p>
          <el-button type="primary" size="mini">project</el-button>
          {{ projectName }}
        </p>
        <p>
          <el-button type="primary" size="mini">url</el-button>
          <a :href="activeRequest.url">{{ activeRequest.url }}</a>
        </p>
        <p>
          <el-button type="primary" size="mini">method</el-button>
          {{ activeRequest.method }}
        </p>
        <p>
          <el-button type="primary" size="mini">callback</el-button>
          {{ activeRequest.callback }}
        </p>
        <el-button class="pull-right btn-run" @click="onRun" size="mini" type="primary">
          <i class="fa fa-play"></i>
        </el-button>
        <span class="pull-right m-r-md">
          <el-button-group class="btn-group-bf">
            <el-button @click="onBackward" size="mini" type="primary" :disabled="!canBackward">
              <i class="fa fa-step-backward"></i>
            </el-button>
            <el-button @click="onForward" size="mini" type="primary" :disabled="!canForward">
              <i class="fa fa-step-forward"></i>
            </el-button>
          </el-button-group>
        </span>
      </el-col>
      <el-col :span="24" v-if="error" class="m-t-md">
        <el-alert
          :title="$lang[$store.state.lang].titles.error"
          type="error"
          :closable="false">
          <template slot-scope="description">
            <pre>
              {{ error }}
            </pre>
          </template>
        </el-alert>
      </el-col>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="Follows" name="follows">
          <el-col :span="24" id="follow-requests" class="p-md" v-loading="fetching">
            <h4 :class="followRequests.length?'m-b-sm':''+ 'm-l-xs'">Follow Requests</h4>
            <div v-for="followRequest in followRequests">
              <div class="follow-request">
              <span :span="24">
                {{ followRequest.url }}
              </span>
                <el-button class="pull-right btn-follow" @click="onFollow(followRequest)" size="mini" type="primary">
                  <i class="fa fa-play"></i>
                </el-button>
              </div>
            </div>
          </el-col>
          <el-col :span="24" id="follow-items" class="m-t p-md" v-loading="fetching">
            <h4 :class="followItems.length?'m-b-sm':'' + 'm-l-xs'">Follow Items</h4>
            <div>
              <div class="follow-item" v-for="followItem in followItems">
                <p :span="24" v-for="(value, key) in followItem" :key="key" class="m-v-sm">
                  <span class="key m-r-sm">
                    <el-button type="primary" size="mini">{{ key }}</el-button>
                  </span>
                  <span class="value">
                    {{ value }}
                  </span>
                </p>
              </div>
            </div>
          </el-col>
        </el-tab-pane>
        <el-tab-pane label="Web" name="web">
          <div id="parser-web">
            <web :html="activeResponseHtml"></web>
          </div>
        </el-tab-pane>
        <el-tab-pane label="HTML" name="html">
          <div id="parser-html">
            <pre>{{ activeResponseHtml }}</pre>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-row>
  </div>
</template>
<script>

  import web from 'pages/project/web.vue'

  export default {
    components: {web},
    props: {
      projectName: {
        type: String
      },
      spider: {
        type: Object
      }
    },
    data() {
      return {
        fetching: false,
        activeResponseHtml: null,
        activeTab: 'follows',
        start: true,
        activeRequest: {
          url: null,
          start: 1
        },
        error: null,
        followRequests: [],
        followItems: [],
        activeRequests: [],
        activeRequestIndex: null,
      }
    },
    computed: {
      canBackward() {
        return this.activeRequestIndex >= 1 && this.activeRequests.length >= 2
      },
      canForward() {
        return this.activeRequestIndex >= 0 && this.activeRequestIndex < this.activeRequests.length - 1
      }
    },
    methods: {
      onRun() {
        this.onFetch()
      },
      onBackward() {
        this.activeRequestIndex -= 1
        this.activeRequest = this.activeRequests[this.activeRequestIndex]
      },
      onForward() {
        this.activeRequestIndex += 1
        this.activeRequest = this.activeRequests[this.activeRequestIndex]
      },
      onFollow(request) {
        this.activeRequest = request
        this.onFetch()
      },
      addActiveRequest() {
        this.activeRequests.push(this.activeRequest)
        this.activeRequestIndex = this.activeRequests.length - 1
      },
      onFetch() {
        this.addActiveRequest()
        this.fetching = true
        this.error = null
        this.$fetch.apiProject.projectParse({
          name: this.projectName,
        }, {
          url: this.activeRequest.url,
          start: this.activeRequest.start,
          callback: this.activeRequest.callback,
          spider: this.spider.name
        }).then(({data: data}) => {
          if (data.status === '1') {
            let result = data.result
            this.fetching = false
            this.followRequests = []
            let requests = result.requests
            if (requests) {
              requests.forEach((request) => {
                this.followRequests.push({
                  url: request.url,
                  method: request.method,
                  callback: request.callback,
                })
              })
            }
            let items = result.items
            if (items) {
              this.followItems = []
              items.forEach((item) => {
                this.followItems.push(item)
              })
            }
            let response = result.response
            if (response) {
              this.activeResponseHtml = response.html
            }
          }
          if (data.status === '0') {
            this.fetching = false
            this.error = data.message
          }

        }).catch((error) => {
          this.fetching = false
          this.$message.error(this.$lang[this.$store.state.lang].messages.errorParse + error)
        })
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  #console {
    height: auto;
    border: 1px solid rgb(223, 230, 236);
    p {
      margin-top: 5px;
      margin-bottom: 5px;
      button {
        margin-right: 5px;
      }
      a {
        color: rgb(72, 87, 106);
        font-weight: 400;
      }
    }
  }

  .follow-request {
    position: relative;
    height: 40px;
    line-height: 40px;
    padding-left: 5px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    cursor: pointer;
    border-bottom: 1px solid rgb(223, 230, 236);
  }

  .follow-item {
    border-bottom: 1px solid rgb(223, 230, 236);
  }

  .btn-group-bf {
    button {
      min-width: 30px;
    }
  }

  .btn-run {
    margin-top: 2px;
    min-width: 30px;
  }

  .btn-follow {
    width: 30px;
    height: 20px;
    margin-top: 10px;
  }

  #follow-requests, #follow-items {
    border: 1px solid rgb(223, 230, 236);
    overflow-y: scroll;
    max-height: 200px;
  }

  #follow-items {
    .follow-item {
      .key {
        width: 10%;
      }
      .value {
        width: 90%;
      }
    }
  }

  .el-tabs__item.is-active {
    color: #28ccaa !important;
  }

  .el-tabs__active-bar {
    background-color: #28ccaa !important;
  }

  #parser-web {
    iframe {
      border: 1px solid #dfe6ec;
    }
  }

  #parser-html {
    max-height: 500px;
    overflow: scroll;
    border: 1px solid #dfe6ec;
    padding: 15px;
  }
</style>
