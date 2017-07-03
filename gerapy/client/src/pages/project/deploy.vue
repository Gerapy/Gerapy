<template>

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
          label="最新版本">
          <template scope="props">
            <span>{{ projectVersions[props.row.pk]}}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作">
          <template scope="props">
            <el-button type="success" size="mini" @click="onDeploy(props.row.pk, props.row.fields.name)">部署</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  export default{
    data(){
      return {
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

    },
    methods: {
      //获取数据
      getClientData(){
        this.loadData = true
        this.$fetch.apiClient.index(
        ).then(({data: clients}) => {
          this.clients = clients
          this.loadData = false
          this.clients.forEach(({pk: id}) => {
            console.log(id)
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
        }).then(({data: versions}) => {
          console.log(versions)
          let version = null
          if (versions.length > 0) {
            version = versions[0]
          }
          this.$set(this.projectVersions, id, version)
          this.loadData = false
        }).catch(() => {
          this.loadData = false
        })
      },
      onDeploy(id, name) {
        console.log(name)
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">

</style>
