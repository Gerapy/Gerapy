<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="panel">
          <panel-title title="主机">
            <el-button size="mini" type="primary">
              正常
            </el-button>
          </panel-title>
          <div class="panel-body" v-loading="loading">
            <h1 class="number">{{ status.success}}</h1>
            <small>主机正常运行</small>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="panel">
          <panel-title title="主机">
            <el-button size="mini" type="danger">
              错误
            </el-button>
          </panel-title>
          <div class="panel-body" v-loading="loading">
            <h1 class="number">{{ status.error}}</h1>
            <small>主机连接失败</small>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="panel" id="tree">
          <panel-title title="项目">
            <el-button size="mini" type="success">
              正常
            </el-button>
          </panel-title>
          <div class="panel-body" v-loading="loading">
            <h1 class="number">{{ status.project }}</h1>
            <small>个项目</small>
          </div>
        </div>
      </el-col>
    </el-row>

  </div>
</template>
<script type="text/javascript">
  import {panelTitle} from 'components'

  export default{
    data(){
      return {
        status: {},
        loading: true
      }
    },
    components: {
      panelTitle
    },
    created(){
      this.getHomeStatus()
    },
    methods: {
      getHomeStatus() {
        this.$fetch.apiHome.status(
        ).then(({data: status}) => {
          console.log(status)
          this.status = status
          this.loading = false
        })
      },
    }
  }
</script>

<style>
  h1.number {
    font-weight: 100;
    margin: 10px 0;
    margin-top: 0;
  }
</style>
