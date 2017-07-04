<template>
  <div class="panel">
    <panel-title :title="$route.meta.title">
      <el-button @click.stop="onRefresh" size="mini">
        <i class="fa fa-refresh"></i>
      </el-button>
      <router-link :to="{name: 'clientCreate'}" tag="span">
        <el-button type="primary" icon="plus" size="mini">添加主机</el-button>
      </router-link>
    </panel-title>
    <div class="panel-body">
      <el-table
        :data="clients"
        v-loading="loadData"
        element-loading-text="拼命加载中"
        @selection-change="onBatchSelect"
        style="width: 100%;">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column
          prop="pk"
          label="ID"
          width="60">
        </el-table-column>
        <el-table-column
          prop="fields.name"
          label="名称"
          width="200">
        </el-table-column>
        <el-table-column
          prop="fields.ip"
          label="IP"
          width="200">
        </el-table-column>
        <el-table-column
          prop="fields.port"
          label="端口"
          width="200">
        </el-table-column>
        <el-table-column
          prop="fields.port"
          label="描述"
          width="200">
        </el-table-column>
        <el-table-column
          label="操作">
          <template scope="props">
            <router-link :to="{name: 'clientEdit', params: {id: props.row.pk}}" tag="span">
              <el-button type="info" size="mini">
                <i class="fa fa-edit"></i>
                编辑
              </el-button>
            </router-link>
            <router-link :to="{name: 'clientSchedule', params: {id: props.row.pk}}" tag="span">
              <el-button type="success" size="mini">
                <i class="fa fa-sitemap"></i>
                调度
              </el-button>
            </router-link>
            <el-button type="danger" size="mini" @click="onSingleDel(props.row.pk)">
              <i class="fa fa-remove"></i>
              删除
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
          @click="onBatchDel"
          slot="handler">
          <span>批量删除</span>
        </el-button>
      </bottom-tool-bar>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  export default{
    data(){
      return {
        clients: null,
        //请求时的loading效果
        loadData: true,
        //批量选择数组
        batchSelect: [],
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getClientData()
    },
    methods: {
      onBatchSelect(val){
        this.batchSelect = val
      },
      onRefresh(){
        this.getClientData()
      },
      changeFilter () {
        this.lastIds = {}
        this.getClientData()
      },
      //获取数据
      getClientData(){
        this.loadData = true
        this.$fetch.apiClient.index(
        ).then(({data: clients}) => {
          this.clients = clients
          this.loadData = false
        }).catch(() => {
          this.loadData = false
        })
      },
      deleteClient(id) {
        this.$fetch.apiClient.remove({
          id: id
        }).then(() => {
          this.$message.success('删除成功')
          this.loadData = false
          this.getClientData()
        }).catch(() => {
          this.$message.error('删除失败')
          this.loadData = false
        })
      },
      onSingleDel(id) {
        this.$confirm('此操作将批量删除选择数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.deleteClient(id)
        })
      },
      //批量删除
      onBatchDel(){
        this.$confirm('此操作将批量删除选择数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.loadData = true
          console.log(this.batchSelect)
          this.batchSelect.forEach((item) => {
            this.deleteClient(item.pk)
          })
        }).catch(() => {
        })
      }
    }
  }
</script>
