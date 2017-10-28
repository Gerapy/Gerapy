<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="panel">
          <panel-title :title="$lang[$store.state.lang].titles.deployProject">
          </panel-title>
          <div class="panel-body">
            <el-table
              :data="clients"
              v-loading="loadData"
              :element-loading-text="$lang[$store.state.lang].messages.loading"
              @selection-change="onBatchSelect"
              style="width: 100%;">
              <el-table-column
                align="center"
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column
                align="center"
                :label="$lang[$store.state.lang].columns.status"
                width="100">
                <template scope="props">
                  <el-button :type="statusClass[clientsStatus[props.row.pk]]" size="mini">
                    {{ statusText[clientsStatus[props.row.pk]] }}
                  </el-button>
                </template>
              </el-table-column>
              <el-table-column
                align="center"
                prop="pk"
                :label="$lang[$store.state.lang].columns.id"
                width="60">
              </el-table-column>
              <el-table-column
                align="center"
                prop="fields.name"
                :label="$lang[$store.state.lang].columns.name"
                width="100">
              </el-table-column>
              <el-table-column
                align="center"
                prop="fields.ip"
                :label="$lang[$store.state.lang].columns.ip"
                width="150">
              </el-table-column>
              <el-table-column
                align="center"
                prop="fields.port"
                :label="$lang[$store.state.lang].columns.port"
                width="100">
              </el-table-column>
              <el-table-column
                align="center"
                :label="$lang[$store.state.lang].columns.description">
                <template scope="props">
                  <span>{{ projectDescriptions[props.row.pk]}}</span>
                </template>
              </el-table-column>
              <el-table-column
                align="center"
                :label="$lang[$store.state.lang].columns.deployedAt">
                <template scope="props">
                  <span>{{ projectDateTimes[props.row.pk]}}</span>
                </template>
              </el-table-column>
              <el-table-column
                align="center"
                :label="$lang[$store.state.lang].columns.operations">
                <template scope="props">
                  <el-button type="success" size="mini" @click="onDeploy(props.row.pk)"
                             v-if="clientsStatus[props.row.pk]">
                    <i class="fa fa-cloud-upload"></i>
                    {{ $lang[$store.state.lang].buttons.deploy }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <bottom-tool-bar>
              <el-button
                type="info"
                size="mini"
                :disabled="batchSelect.length === 0"
                @click="onBatchDeploy"
                slot="handler">
              <span>
                <i class="fa fa-cloud-upload"></i>
                {{ $lang[$store.state.lang].buttons.batchDeploy }}
              </span>
              </el-button>
            </bottom-tool-bar>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="panel">
          <panel-title :title="$lang[$store.state.lang].objects.project">
          </panel-title>
          <div class="panel-body">
            <el-form :model="buildInfo" label-width="80px">
              <el-form-item :label="$lang[$store.state.lang].columns.name">
                {{ buildInfo.name }}
              </el-form-item>
              <el-form-item :label="$lang[$store.state.lang].columns.packageName">
                {{ buildInfo.egg || notBuildText }}
              </el-form-item>
              <el-form-item :label="$lang[$store.state.lang].columns.builtAt">
                {{ buildInfo.built_at || notBuildText }}
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="panel">
          <panel-title title="项目打包">
          </panel-title>
          <div class="panel-body">
            <el-form ref="form" :model="buildInfo" :rules="rules" label-width="80px">
              <el-form-item label="项目名称">
                {{ buildInfo.name }}
              </el-form-item>
              <el-form-item label="版本描述" prop="description" class="description">
                <el-input v-model="buildInfo.description" size="small"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" @click="onBuild">
                  <i class="fa fa-codepen"></i>
                  <span v-if="buildInfo.egg">重新</span>打包
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  import ElRow from "element-ui/packages/row/src/row";
  import ElCol from "element-ui/packages/col/src/col";
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
        projectDescriptions: {},
        projectDateTimes: {},
        clientsStatus: {},
        statusClass: {
          '1': 'success',
          '0': 'warning',
          '-1': 'danger',
        },
        statusText: {
          '1': '运行正常',
          '0': '连接中',
          '-1': '连接失败',
        },
        rules: {
          description: [
            {required: true, message: '描述不能为空', trigger: 'blur'},
          ]
        }
      }
    },
    components: {
      ElCol,
      ElRow,
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getClientData()
      this.getBuildInfo()
    },
    methods: {
      onBatchSelect(val){
        this.batchSelect = val
        console.log(this.batchSelect)
      },
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
      getClientStatus(id) {
        this.$set(this.clientsStatus, id, 0)
        this.$fetch.apiClient.status({
          id: id
        }).then(({data: {result: data}}) => {
          this.$set(this.clientsStatus, id, data)
        }).catch(() => {
          this.$set(this.clientsStatus, id, -1)
        })
      },
      getClientData(){
        this.loadData = true
        this.$fetch.apiClient.index(
        ).then(({data: clients}) => {
          this.clients = clients
          this.loadData = false
          this.clients.forEach(({pk: id}) => {
            this.getProjectVersion(id)
            this.getClientStatus(id)
          })
        }).catch(() => {
          this.loadData = false
        })
      },
      deploy(id) {
        if (this.clientsStatus[id]) {
          this.$fetch.apiClient.projectDeploy({
            id: id,
            name: this.projectName,
          }).then(() => {
            this.$message.success('主机' + id + '部署成功')
            this.getProjectVersion(id)
            this.loadData = false
          }).catch((data) => {
            console.log('部署失败', data)
            this.$message.error('主机' + id + '部署失败')
            this.loadData = false
          })
        } else {
          this.$message.error('主机' + id + '连接失败')
          this.loadData = false
        }
      },
      getProjectVersion(id){
        this.loadData = true
        this.$fetch.apiClient.projectVersion({
          id: id,
          name: this.projectName,
        }).then(({data: version}) => {
          this.$set(this.projectDescriptions, id, version['description'])
          this.$set(this.projectDateTimes, id, version['deployed_at'])
          this.loadData = false
        }).catch(() => {
          this.loadData = false
        })
      },
      onBatchDeploy() {
        this.$confirm('此操作将花费一些时间, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.loadData = true
          console.log(this.batchSelect)
          this.batchSelect.forEach(({pk: id}) => {
            this.deploy(id)
          })
        }).catch(() => {
          this.$message.error('批量部署部分出错')
        })
      },
      onDeploy(id) {
        if (this.buildInfo.egg) {
          this.deploy(id)
        } else {
          this.$message.error('请先打包项目')
        }
      },
      onBuild() {
        this.$refs.form.validate((valid) => {
          if (!valid)
            return false
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
            this.$message.error('打包失败')
          })
        })
      }
    }
  }
</script>

<style>
  .description input {
    max-width: 200px;
  }
</style>
