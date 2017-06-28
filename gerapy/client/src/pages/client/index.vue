<template>
  <div class="panel">
    <panel-title :title="$route.meta.title">
      <span class="inline">
        <div class="filter">
          <el-input v-model="minutesToNow" placeholder="MinutesToNow" size="small" min="0" @change="changeFilter">
            <template slot="prepend">最近</template>
            <template slot="append">分钟</template>
          </el-input>
        </div>
      </span>
      <el-button @click.stop="onRefresh" size="small">
        <i class="fa fa-refresh"></i>
      </el-button>
      <router-link :to="{name: 'taskAdd'}" tag="span">
        <el-button type="primary" icon="plus" size="small">添加数据</el-button>
      </router-link>
    </panel-title>
    <div class="panel-body">
      <el-table
        :data="taskData"
        v-loading="loadData"
        element-loading-text="拼命加载中"
        border
        style="width: 100%;">
        <el-table-column
          prop="id"
          label="id"
          width="250">
        </el-table-column>
        <el-table-column
          prop="destAddress"
          label="目标地址"
          width="200">
        </el-table-column>
        <el-table-column
          prop="sessionData.topic"
          label="话题"
          width="200">
        </el-table-column>
        <el-table-column
          prop="sessionData.greetingWord"
          label="问候语"
          width="400">
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          width="80">
        </el-table-column>
        <el-table-column
          prop="envTag"
          label="环境"
          width="80">
        </el-table-column>
        <el-table-column
          prop="dateTime"
          label="时间">
        </el-table-column>
        <el-table-column
          label="操作"
          width="180">
          <template scope="props">
            <el-button v-if="props.row.status=='Scheduled'" type="danger" size="small" icon="delete" @click="cancel(props.row)">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
      <bottom-tool-bar>
        <div slot="page">
          <span class="inline">
            <div class="filter">
              <el-input v-model="pageSize" placeholder="currentPage" size="small" @change="changeFilter">
                <template slot="prepend">每页</template>
                <template slot="append">条</template>
              </el-input>
            </div>
          </span>
          <el-pagination
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-size="10"
            layout="total, prev, pager, next"
            :total="total">
          </el-pagination>
        </div>
      </bottom-tool-bar>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  export default{
    data(){
      return {
        taskData: null,
        // 最后一条数据
        lastId: null,
        //数据总条目
        pageSize: 20,
        //请求时的loading效果
        loadData: true,
        // 距离现在时间（分钟）
        minutesToNow: 1000,
        // 当前页面
        currentPage: 1,
        //批量选择数组
        batchSelect: [],
        // 总页数
        total: null,
        // 每页起始ID数组
        lastIds: {},
        // 状态选项
        statusOptions: [{
          value: 'Scheduled',
          label: 'Scheduled'
        }, {
          value: 'Trying',
          label: 'Trying'
        }, {
          value: 'Calling',
          label: 'Calling'
        }, {
          value: 'Failed',
          label: 'Failed'
        }, {
          value: 'Finished',
          label: 'Finished'
        }, {
          value: 'Canceled',
          label: 'Canceled'
        }],
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getTaskData()
    },
    methods: {
      //刷新
      onRefresh(){
        this.getTaskData()
      },
      changeFilter () {
        this.lastIds = {}
        this.getTaskData()
      },
      //获取数据
      getTaskData(){
        this.loadData = true
        this.$fetch.apiClient.index({
          minutesToNow: this.minutesToNow,
          pageSize: this.pageSize,
          lastId: this.lastIds[this.currentPage - 1]
        })
          .then(({data: taskData}) => {
            this.taskData = taskData
            this.loadData = false
            this.lastIds[this.currentPage] = taskData[this.pageSize - 1].id
          })
          .catch(() => {
            this.loadData = false
          })
      },
      //页码选择
      handleCurrentChange(val) {
        this.currentPage = val
        this.getTaskData()
      },
      cancel(row) {
        this.$fetch.api_task.cancel(row)
          .then(() => {
            row.status = 'Canceled'
            this.$message.success('取消成功')
          })
          .catch(() => {
            row.status = 'Canceled'
          })
      }
    }
  }
</script>
<style lang="scss" type="text/scss" rel="stylesheet/scss">
  .inline {
    display: inline-block;
    word-break: inherit;
  }

  .filter {
    width: 150px;
    text-align: center;
    input {
      text-align: center;
    }
  }

  .el-pagination {
    display: inline-block;
    position: relative;
    top: -4px;
  }
</style>
