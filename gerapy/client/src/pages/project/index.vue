<template>

  <div class="panel">
    <panel-title title="项目管理">
    </panel-title>
    <div class="panel-body">
      <el-table
        :data="projects"
        v-loading="loadData"
        element-loading-text="拼命加载中"
        @selection-change="onBatchSelect"
        style="width: 100%;">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column
          prop="name"
          label="项目名称"
          width="200">
        </el-table-column>
        <el-table-column
          label="项目版本"
          width="200">
          <template scope="props">
            <span v-if="buildInfos[props.row.name]">
              {{ buildInfos[props.row.name]['description'] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="已打包"
          width="100">
          <template scope="props">
            <span v-if="buildInfos[props.row.name]">
              {{ buildInfos[props.row.name]['egg']?'是':'否' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="打包名称"
          width="200">
          <template scope="props">
            <span v-if="buildInfos[props.row.name]">
              {{ buildInfos[props.row.name]['egg'] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="打包时间"
          width="200">
          <template scope="props">
            <span v-if="buildInfos[props.row.name]">
              {{ buildInfos[props.row.name]['built_at'] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作">
          <template scope="props">
            <router-link :to="{name: 'projectEdit', params: {name: props.row.name}}" tag="span">
              <el-button type="warning" size="small">
                <i class="fa fa-edit"></i>
                编辑
              </el-button>
            </router-link>
            <router-link :to="{name: 'projectDeploy', params: {name: props.row.name}}" tag="span">
              <el-button type="success" size="small">
                <i class="fa fa-cloud-upload"></i>
                部署
              </el-button>
            </router-link>
            <router-link :to="{name: 'projectMonitor', params: {name: props.row.name}}" tag="span">
              <el-button type="info" size="small">
                <i class="fa fa-podcast"></i>
                监控
              </el-button>
            </router-link>
            <el-button type="danger" size="small" @click="onSingleDel(props.row.name)">
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
          size="small"
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
        projects: [],
        //请求时的loading效果
        loadData: false,
        //批量选择数组
        batchSelect: [],
        buildInfos: {}
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getProjectData()
    },
    methods: {
      onBatchSelect(val){
        this.batchSelect = val
      },
      getBuildInfo(name){
        this.loadData = true
        this.$fetch.apiProject.buildInfo({
          name: name
        }).then(({data: data}) => {
          this.$set(this.buildInfos, name, data)
          this.loadData = false
          console.log('LLLL', this.buildInfos)
        }).catch(() => {
          this.loadData = false
        })
      },
      //获取数据
      getProjectData(){
        this.loadData = true
        this.$fetch.apiProject.projectList(
        ).then(({data: projects}) => {
          this.projects = projects
          this.loadData = false
          this.projects.forEach((project) => {
            console.log(project)
            this.getBuildInfo(project.name)
          })
        }).catch(() => {
          this.loadData = false
        })
      },
      deleteProject(name) {
        this.loadData = true
        this.$fetch.apiProject.projectRemove({
          name: name
        }).then(() => {
          this.$message.success('删除成功')
          this.loadData = false
          this.getProjectData()
        }).catch((error) => {
          console.log(error)
          this.loadData = false
          this.$message.error('删除失败')
        })
      },
      // 单个删除
      onSingleDel(name) {
        this.$confirm('此操作将批量删除选择数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.deleteProject(name)
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
          this.batchSelect.forEach(({name: name}) => {
            this.deleteProject(name)
          })
        }).catch(() => {
          this.$message.error('批量删除出错')
        })
      }
    }
  }
</script>
