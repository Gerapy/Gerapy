<template>
  <div>
    <el-row class="m-b-md">
      <el-col :span="24" id="console" class="p-md">
        <el-form-item label-width="80px">
          <template slot="label">
            <el-button type="primary" size="mini">project</el-button>
          </template>
          {{ projectName }}
        </el-form-item>
        <el-form-item label-width="80px">
          <template slot="label">
            <el-button type="primary" size="mini">spider</el-button>
          </template>
          {{ spider.name }}
        </el-form-item>

        <el-form-item label-width="80px" v-if="active.request">
          <template slot="label">
            <el-button type="primary" size="mini">start</el-button>
          </template>
          {{ !!active.request.start }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="active.request && !active.request.start"
        >
          <template slot="label">
            <el-button type="primary" size="mini">url</el-button>
          </template>
          {{ active.request.url }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="active.request && !active.request.start"
        >
          <template slot="label">
            <el-button type="primary" size="mini">method</el-button>
          </template>
          {{ active.request.method }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="active.request && !active.request.start"
        >
          <template slot="label">
            <el-button type="primary" size="mini">dont_filter</el-button>
          </template>
          {{ active.request.dont_filter }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="active.request && !active.request.start"
        >
          <template slot="label">
            <el-button type="primary" size="mini">priority</el-button>
          </template>
          {{ active.request.priority }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="
            active.request &&
              !active.request.start &&
              active.request.method.toLowerCase() !== 'get'
          "
        >
          <template slot="label">
            <el-button type="primary" size="mini">body</el-button>
          </template>
          {{ active.request.body }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="active.request && !active.request.start"
        >
          <template slot="label">
            <el-button type="primary" size="mini">cookies</el-button>
          </template>
          {{ active.request.cookies }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="active.request && !active.request.start"
        >
          <template slot="label">
            <el-button type="primary" size="mini">headers</el-button>
          </template>
          {{ active.request.headers }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="active.request && !active.request.start"
        >
          <template slot="label">
            <el-button type="primary" size="mini">meta</el-button>
          </template>
          {{ active.request.meta }}
        </el-form-item>
        <el-form-item
          label-width="80px"
          v-if="active.request && !active.request.start"
        >
          <template slot="label">
            <el-button type="primary" size="mini">callback</el-button>
          </template>
          {{ active.request.callback }}
        </el-form-item>
        <el-form-item class="text-right">
          <el-button-group class="btn-group-bf">
            <el-button
              @click="onBackward"
              size="mini"
              type="primary"
              :disabled="!canBackward"
            >
              <i class="fa fa-step-backward"></i>
            </el-button>
            <el-button
              @click="onForward"
              size="mini"
              type="primary"
              :disabled="!canForward"
            >
              <i class="fa fa-step-forward"></i>
            </el-button>
          </el-button-group>
          <el-button
            @click="onRun"
            size="mini"
            type="primary"
            :style="{ width: '30px' }"
          >
            <i class="fa fa-play"></i>
          </el-button>
        </el-form-item>
      </el-col>
      <el-col :span="24" id="error" v-if="error" class="m-t-md">
        <el-alert :title="$lang.titles.error" type="error" :closable="false">
          <template slot>
            <pre>
              {{ error }}
            </pre>
          </template>
        </el-alert>
      </el-col>
      <el-col :span="24" id="follows">
        <el-tabs v-model="active.tab">
          <el-tab-pane label="Follows" name="follows">
            <el-col
              :span="24"
              id="follow-requests"
              class="p-md"
              v-loading="fetching"
            >
              <p :class="follow.requests.length ? 'm-b-sm' : '' + 'm-l-xs'">
                Follow Requests
                <el-button type="primary" size="mini">{{
                  follow.requests.length
                }}</el-button>
              </p>
              <div v-for="(request, requestIndex) in follow.requests">
                <div class="follow-request">
                  <el-form-item class="inline">
                    <el-button type="primary" size="mini">{{
                      requestIndex + 1
                    }}</el-button>
                    <el-button type="primary" size="mini">{{
                      request.method
                    }}</el-button>
                    <span :style="{ fontSize: '13px' }">{{ request.url }}</span>
                    <el-button
                      type="primary"
                      size="mini"
                      v-if="request.callback"
                    >
                      <i class="fa fa-angle-right"></i>
                      {{ request.callback }}
                    </el-button>
                  </el-form-item>
                  <el-form-item
                    class="inline pull-right"
                    :style="{ height: '40px' }"
                  >
                    <el-button
                      :style="{ marginTop: '10px', width: '30px' }"
                      @click="onFollow(request)"
                      size="mini"
                      type="primary"
                    >
                      <i class="fa fa-play"></i>
                    </el-button>
                  </el-form-item>
                </div>
              </div>
            </el-col>
            <el-col
              :span="24"
              id="follow-items"
              class="m-t p-md"
              v-loading="fetching"
            >
              <p :class="follow.items.length ? 'm-b-sm' : '' + 'm-l-xs'">
                Follow Items
                <el-button type="primary" size="mini">{{
                  follow.items.length
                }}</el-button>
              </p>
              <div class="follow-item" v-for="item in follow.items">
                <el-form-item
                  v-for="(value, key) in item"
                  :key="key"
                  label-width="80px"
                >
                  <template slot="label">
                    <el-button
                      type="primary"
                      size="mini"
                      :style="{ width: '100%' }"
                      >{{ key }}</el-button
                    >
                  </template>
                  {{ value }}
                </el-form-item>
              </div>
            </el-col>
          </el-tab-pane>
          <el-tab-pane label="Web" name="web">
            <div id="follow-web">
              <web :html="active.response.html"></web>
            </div>
          </el-tab-pane>
          <el-tab-pane label="HTML" name="html">
            <div id="follow-html">
              <pre>{{ active.response.html }}</pre>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import Web from "./Web";

export default {
  name: "Parser",
  components: {
    Web,
  },
  props: {
    projectName: {
      type: String,
    },
    spider: {
      type: Object,
    },
  },
  data() {
    return {
      active: {
        response: {},
        request: {
          url: null,
          start: true,
        },
        index: null,
        requests: [],
        tab: "follows",
      },
      follow: {
        requests: [],
        items: [],
      },
      fetching: false,
      error: null,
    };
  },
  computed: {
    canBackward() {
      if (!this.active.request || !this.active.requests) {
        return false;
      }
      return this.active.index >= 1 && this.active.requests.length >= 2;
    },
    canForward() {
      if (!this.active.request || !this.active.requests) {
        return false;
      }
      return (
        this.active.index >= 0 &&
        this.active.index < this.active.requests.length - 1
      );
    },
  },
  methods: {
    onRun() {
      this.onFetch();
    },
    onBackward() {
      this.$set(this.active, "index", this.active.index - 1);
      this.$set(
        this.active,
        "request",
        this.active.requests[this.active.index]
      );
    },
    onForward() {
      this.$set(this.active, "index", this.active.index + 1);
      this.$set(
        this.active,
        "request",
        this.active.requests[this.active.index]
      );
    },
    onFollow(request) {
      this.$set(this.active, "request", request);
      this.onFetch();
    },
    // 添加 request 到调试台历史记录中
    addActiveRequest() {
      this.active.requests.push(this.active.request);
      this.$set(this.active, "index", this.active.requests.length - 1);
    },
    onFetch() {
      this.addActiveRequest();
      this.fetching = true;
      this.error = null;
      let postData = {
        spider: this.spider.name,
        url: this.active.request.url,
        start: this.active.request.start,
        callback: this.active.request.callback,
        cookies: this.active.request.cookies,
        headers: this.active.request.headers,
        method: this.active.request.method,
        meta: this.active.request.meta,
        dont_filter: this.active.request.dont_filter,
        priority: this.active.request.priority,
      };
      // 如果不是 GET 类型的请求，增加请求体
      if (postData.method && postData.method.toLowerCase() !== "get") {
        postData.body = this.active.request.body;
      }
      // 模拟请求
      this.$http
        .post(
          this.formatString(this.$store.state.url.project.parse, {
            name: this.projectName,
          }),
          postData
        )
        .then(({ data: data }) => {
          if (data.status === true) {
            let result = data.result;
            this.fetching = false;
            // 后续跟进请求
            let requests = result.requests;
            if (requests) {
              this.$set(this.follow, "requests", requests);
            }
            // 后续跟进结果
            let items = result.items;
            if (items) {
              this.$set(this.follow, "items", items);
            }
            // 当前页面响应结果
            let response = result.response;
            if (response) {
              this.$set(this.active, "response", response);
            }
          }
          if (data.status === false) {
            // 执行出现错误
            this.fetching = false;
            this.error = data.message;
          }
        })
        .catch((error) => {
          this.fetching = false;
          this.$message.error(
            this.$store.getters.$lang.messages.errorParse + error
          );
        });
    },
  },
};
</script>

<style lang="scss">
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
  label {
    .el-button {
      width: 100%;
    }
  }
}

#follows {
  $max-height: 400px;
  #follow-requests,
  #follow-items {
    border: 1px solid rgb(223, 230, 236);
    overflow-y: scroll;
    max-height: $max-height;
    .el-loading-mask {
      height: 10000px;
    }
  }
  #follow-items {
    .follow-item {
      border-bottom: 1px solid rgb(223, 230, 236);
      .key {
        width: 10%;
      }
      .value {
        width: 90%;
      }
    }
  }
  #follow-requests {
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
  }

  #follow-web {
    iframe {
      border: 1px solid #dfe6ec;
      min-height: 500px;
    }
  }

  #follow-html {
    max-height: 500px;
    overflow: scroll;
    border: 1px solid #dfe6ec;
    padding: 15px;
  }
}

.el-tabs__item.is-active {
  color: #28ccaa !important;
}

.el-tabs__active-bar {
  background-color: #28ccaa !important;
}
</style>
