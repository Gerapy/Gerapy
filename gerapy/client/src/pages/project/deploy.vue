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
                <template slot-scope="props">
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
                <template slot-scope="props">
                  <span>{{ projectDescriptions[props.row.pk]}}</span>
                </template>
              </el-table-column>
              <el-table-column
                align="center"
                :label="$lang[$store.state.lang].columns.deployedAt">
                <template slot-scope="props">
                  <span>{{ projectDateTimes[props.row.pk]}}</span>
                </template>
              </el-table-column>
              <el-table-column
                align="center"
                :label="$lang[$store.state.lang].columns.operations">
                <template slot-scope="props">
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
                slot-scope="handler">
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
      <el-col :span="12">
        <div class="panel">
          <panel-title :title="$lang[$store.state.lang].objects.project">
          </panel-title>
          <div class="panel-body">
            <el-form :model="buildInfo" label-width="120px">
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
      <el-col :span="12">
        <div class="panel">
          <panel-title :title="$lang[$store.state.lang].titles.buildProject">
          </panel-title>
          <div class="panel-body">
            <el-form ref="form" :model="buildInfo" :rules="rules" label-width="120px">
              <el-form-item :label="$lang[$store.state.lang].columns.name">
                {{ buildInfo.name }}
              </el-form-item>
              <el-form-item :label="$lang[$store.state.lang].columns.description"
                            prop="description"
                            class="description">
                <el-input v-model="buildInfo.description" size="small"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" @click="onBuild">
                  <i class="fa fa-codepen"></i>
                  <span v-if="buildInfo.egg">{{ $lang[$store.state.lang].buttons.re
                    }}</span>{{ $lang[$store.state.lang].buttons.build }}
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
        notBuildText: this.$lang[this.$store.state.lang].messages.notBuilt,
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
          '1': this.$lang[this.$store.state.lang].buttons.normal,
          '0': this.$lang[this.$store.state.lang].buttons.connecting,
          '-1': this.$lang[this.$store.state.lang].buttons.error,
        },
        rules: {
          description: [
            {required: true, message: this.$lang[this.$store.state.lang].messages.emptyDescription, trigger: 'blur'},
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
            this.$message.success(this.$lang[this.$store.state.lang].titles.client + ' ' + id + ' ' +
              this.$lang[this.$store.state.lang].messages.successDeploy
            )
            this.getProjectVersion(id)
            this.loadData = false
          }).catch((data) => {
            this.$message.error(this.$lang[this.$store.state.lang].titles.client + ' ' + id + ' ' + this.$lang[this.$store.state.lang].messages.errorDeploy)
            this.loadData = false
          })
        } else {
          this.$message.error(this.$lang[this.$store.state.lang].titles.client + ' ' + id + ' ' + this.$lang[this.$store.state.lang].messages.errorDeploy)
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
        this.$confirm(this.$lang[this.$store.state.lang].messages.confirm, this.$lang[this.$store.state.lang].buttons.confirm, {
          confirmButtonText: this.$lang[this.$store.state.lang].buttons.yes,
          cancelButtonText: this.$lang[this.$store.state.lang].buttons.no,
          type: 'warning'
        }).then(() => {
          this.loadData = true
          console.log(this.batchSelect)
          this.batchSelect.forEach(({pk: id}) => {
            this.deploy(id)
          })
        }).catch(() => {
          this.$message.error(this.$lang[this.$store.state.lang].messages.errorDeploy)
        })
      },
      onDeploy(id) {
        if (this.buildInfo.egg) {
          this.deploy(id)
        } else {
          this.$message.error(this.$lang[this.$store.state.lang].messages.buildFirst)
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
            this.$message.success(this.$lang[this.$store.state.lang].messages.successBuild)
          }).catch(() => {
            this.loadData = false
            this.$message.error(this.$lang[this.$store.state.lang].messages.errorBuild)
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
