<template>
  <div>
    <div class="panel">
      <panel-title title="项目打包">
      </panel-title>
      <div class="panel-body">
        <el-form ref="form" :model="buildInfo" label-width="80px">
          <el-form-item label="活动名称">
            <el-input></el-input>
          </el-form-item>
          <el-form-item label="活动区域">
            <el-select placeholder="请选择活动区域">
              <el-option label="区域一" value="shanghai"></el-option>
              <el-option label="区域二" value="beijing"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="活动性质">
            <el-checkbox-group>
              <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>
              <el-checkbox label="地推活动" name="type"></el-checkbox>
              <el-checkbox label="线下主题活动" name="type"></el-checkbox>
              <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>
            </el-checkbox-group>
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
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">

</style>
