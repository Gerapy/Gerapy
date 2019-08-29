<template>
  <div class="panel">
    <panel-title :title="$lang[$store.state.lang].objects.tasks">
      <router-link :to="{name: 'taskCreate'}" tag="span">
        <el-button type="success" size="mini">
          <i class="fa fa-plus"></i>
          {{ $lang[$store.state.lang].buttons.create }}
        </el-button>
      </router-link>
    </panel-title>
    <div class="panel-body">
      <el-table
        :empty-text="$lang[$store.state.lang].messages.noData"
        :data="tasks"
        v-loading="loadData"
        :element-loading-text="$lang[$store.state.lang].messages.loading"
        @selection-change="onBatchSelect">
        <el-table-column
          align="center"
          type="selection"
          width="50">
        </el-table-column>
        <el-table-column
          align="center"
          prop="id"
          :label="$lang[$store.state.lang].columns.id"
          width="60">
        </el-table-column>
        <el-table-column
          align="center"
          prop="name"
          :label="$lang[$store.state.lang].columns.name"
          width="200">
        </el-table-column>
        <el-table-column
          align="center"
          prop="project"
          :label="$lang[$store.state.lang].columns.project"
          width="200">
        </el-table-column>
        <el-table-column
          align="center"
          prop="spider"
          :label="$lang[$store.state.lang].columns.spider">
        </el-table-column>
        <el-table-column
          align="center"
          :label="$lang[$store.state.lang].columns.operations">
          <template slot-scope="props">
            <router-link :to="{name: 'taskStatus', params: {id: props.row.id }}" tag="span">
              <el-button type="success" size="mini">
                <i class="fa fa-sitemap"></i>
                {{ $lang[$store.state.lang].buttons.status }}
              </el-button>
            </router-link>
            <router-link :to="{name: 'taskEdit', params: {id: props.row.id }}" tag="span">
              <el-button type="info" size="mini">
                <i class="fa fa-edit"></i>
                {{ $lang[$store.state.lang].buttons.edit }}
              </el-button>
            </router-link>
            <el-button type="danger" size="mini" @click="onSingleDelete(props.row.id)">
              <i class="fa fa-remove"></i>
              {{ $lang[$store.state.lang].buttons.delete }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <bottom-tool-bar>
        <el-button
          type="danger"
          icon="delete"
          size="mini"
          :disabled="batchSelect.length === 0"
          @click="onBatchDelete"
          slot-scope="handler">
          <span>{{ $lang[$store.state.lang].buttons.batchDelete }}</span>
        </el-button>
      </bottom-tool-bar>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'

  export default {
    data() {
      return {
        tasks: null,
        //请求时的loading效果
        loadData: true,
        //批量选择数组
        batchSelect: [],
        statusText: {
          '1': this.$lang[this.$store.state.lang].buttons.normal,
          '0': this.$lang[this.$store.state.lang].buttons.connecting,
          '-1': this.$lang[this.$store.state.lang].buttons.error,
        }
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created() {
      this.getTaskData()
    },
    methods: {
      onBatchSelect(val) {
        this.batchSelect = val
      },
      onRefresh() {
        this.getTaskData()
      },
      changeFilter() {
        this.lastIds = {}
        this.getTaskData()
      },
      //获取数据
      getTaskData() {
        this.loadData = true
        this.$fetch.apiTask.index(
        ).then(({data: {data: tasks}}) => {
          this.tasks = tasks
          this.loadData = false
        }).catch(() => {
          this.loadData = false
        })
      },
      deleteTask(id) {
        this.$fetch.apiTask.remove({
          id: id
        }).then(() => {
          this.$message.success(this.$lang[this.$store.state.lang].messages.successDelete)
          this.loadData = false
          this.getTaskData()
        }).catch(() => {
          this.$message.error(this.$lang[this.$store.state.lang].messages.errorDelete)
          this.loadData = false
        })
      },
      onSingleDelete(id) {
        this.$confirm(this.$lang[this.$store.state.lang].messages.confirm, this.$lang[this.$store.state.lang].buttons.confirm, {
          confirmButtonText: this.$lang[this.$store.state.lang].buttons.yes,
          cancelButtonText: this.$lang[this.$store.state.lang].buttons.no,
          type: 'warning'
        }).then(() => {
          this.deleteTask(id)
        })
      },
      //批量删除
      onBatchDelete() {
        this.$confirm(this.$lang[this.$store.state.lang].messages.confirm, this.$lang[this.$store.state.lang].buttons.confirm, {
          confirmButtonText: this.$lang[this.$store.state.lang].buttons.yes,
          cancelButtonText: this.$lang[this.$store.state.lang].buttons.no,
          type: 'warning'
        }).then(() => {
          this.loadData = true
          console.log(this.batchSelect)
          this.batchSelect.forEach((item) => {
            this.deleteTask(item.pk)
          })
        }).catch(() => {
        })
      }
    }
  }
</script>
