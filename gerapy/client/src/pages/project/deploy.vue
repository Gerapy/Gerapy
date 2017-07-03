<template>
  <div>
    <div class="panel">
      <panel-title title="项目打包">
      </panel-title>
      <div class="panel-body">
        <el-form ref="form" :model="buildInfo" label-width="80px">
          <el-form-item label="项目名称">
            {{ buildInfo.name }}
          </el-form-item>
          <el-form-item label="打包描述">
            <el-input v-model="buildInfo.description"></el-input>
          </el-form-item>
          <el-form-item label="包名">
            {{ buildInfo.egg || notBuildText }}
          </el-form-item>
          <el-form-item label="打包时间">
            {{ buildInfo.built_at || notBuildText }}
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onBuild"><span v-if="buildInfo.egg"></span>打包</el-button>
            <el-button>取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="panel">
      <panel-title title="项目部署">
      </panel-title>
      <div class="panel-body">
        <el-table
          :data="clients"
          v-loading="loadData"
          element-loading-text="拼命加载中"
          style="width: 100%;">
          <el-table-column
            prop="fields.name"
            label="主机名称"
            width="300">
          </el-table-column>
          <el-table-column
            prop="fields.ip"
            label="主机IP"
            width="300">
          </el-table-column>
          <el-table-column
            label="上次部署时间">
            <template scope="props">
              <span>{{ projectVersions[props.row.pk]}}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="操作">
            <template scope="props">
              <el-button type="success" size="mini" @click="onDeploy(props.row.pk)">部署</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>

</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  export default{
    data(){
      return {
        buildInfo: {},
        notBuildText: '未打包',
        clients: [],
        //请求时的loading效果
        loadData: false,
        projectName: this.$route.params.name,
        //批量选择数组
        batchSelect: [],
        projectVersions: {}
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getClientData()
      this.getBuildInfo()
    },
    methods: {
      getBuildInfo(){
        this.loadData = true
        this.$fetch.apiProject.buildInfo({
          name: this.projectName
        }).then(({data: data}) => {
          this.buildInfo = data
          console.log(data)
          this.loadData = false
        }).catch(() => {
          this.loadData = false
        })
      },
      getClientData(){
        this.loadData = true
        this.$fetch.apiClient.index(
        ).then(({data: clients}) => {
          this.clients = clients
          this.loadData = false
          this.clients.forEach(({pk: id}) => {
            this.getProjectVersions(id)
          })
        }).catch(() => {
          this.loadData = false
        })
      },
      getProjectVersions(id){
        this.loadData = true
        this.$fetch.apiClient.projectVersions({
          id: id,
          name: this.projectName,
        }).then(({data: version}) => {
          this.$set(this.projectVersions, id, version)
          this.loadData = false
        }).catch(() => {
          this.loadData = false
        })
      },
      onDeploy(id) {
        this.$fetch.apiClient.projectDeploy({
          id: id,
          name: this.projectName,
        }).then(() => {
          this.$message.success('部署成功')
          this.getProjectVersions(id)
          this.loadData = false
        }).catch(() => {
          this.$message.error('部署失败')
          this.loadData = false
        })
      },
      onBuild() {
        this.$fetch.apiProject.build({
          name: this.projectName
        }, {
          description: this.buildInfo['description'],
          egg: this.buildInfo['egg'],
          built_at: this.buildInfo['built_at']
        }).then(({data: data}) => {
          this.buildInfo = data
          console.log(data)
          this.loadData = false
          this.$message.success('打包成功')
        }).catch(() => {
          this.loadData = false
          this.$message.success('打包失败')
        })
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">

</style>
