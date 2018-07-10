<template>
  <div class="panel">
    <panel-title :title="$lang[$store.state.lang].objects.clients">
      <!--<el-button @click.stop="onRefresh" size="mini">-->
      <!--<i class="fa fa-refresh"></i>-->
      <!--刷新-->
      <!--</el-button>-->
      <router-link :to="{name: 'clientCreate'}" tag="span">
        <el-button type="success" size="mini">
          <i class="fa fa-plus"></i>
          {{ $lang[$store.state.lang].buttons.create }}
        </el-button>
      </router-link>
    </panel-title>
    <div class="panel-body">
      <el-table
        :empty-text="$lang[$store.state.lang].messages.noData"
        :data="clients"
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
          width="200">
        </el-table-column>
        <el-table-column
          align="center"
          prop="fields.ip"
          :label="$lang[$store.state.lang].columns.ip"
          width="200">
        </el-table-column>
        <el-table-column
          align="center"
          prop="fields.port"
          :label="$lang[$store.state.lang].columns.port">
        </el-table-column>
        <el-table-column
          align="center"
          prop="fields.auth"
          width="80"
          :label="$lang[$store.state.lang].columns.auth">
          <template slot-scope="props">
            <span>
              {{ props.row.fields.auth ? '✓' : '✗'  }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          :label="$lang[$store.state.lang].columns.operations">
          <template slot-scope="props">
            <router-link :to="{name: 'clientEdit', params: {id: props.row.pk }}" tag="span">
              <el-button type="info" size="mini">
                <i class="fa fa-edit"></i>
                {{ $lang[$store.state.lang].buttons.edit }}
              </el-button>
            </router-link>
            <router-link :to="{name: 'clientSchedule', params: {id: props.row.pk }}" tag="span">
              <el-button type="success" size="mini">
                <i class="fa fa-sitemap"></i>
                {{ $lang[$store.state.lang].buttons.schedule }}
              </el-button>
            </router-link>
            <el-button type="danger" size="mini" @click="onSingleDelete(props.row.pk)">
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
  export default{
    data(){
      return {
        clients: null,
        //请求时的loading效果
        loadData: true,
        //批量选择数组
        batchSelect: [],
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
        }
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
      getClientsStatus() {
        this.clients.forEach((client) => {
          this.getClientStatus(client.pk)
        })
      },
      getClientStatus(id) {
        this.$set(this.clientsStatus, id, 0)
        this.$fetch.apiClient.status({
          id: id
        }).then(({data: {result: result}}) => {
          this.$set(this.clientsStatus, id, result)
        }).catch(() => {
          this.$set(this.clientsStatus, id, -1)
        })
      },
      //获取数据
      getClientData(){
        this.loadData = true
        this.$fetch.apiClient.index(
        ).then(({data: clients}) => {
          this.clients = clients
          this.loadData = false
          this.getClientsStatus()
        }).catch(() => {
          this.loadData = false
        })
      },
      deleteClient(id) {
        this.$fetch.apiClient.remove({
          id: id
        }).then(() => {
          this.$message.success(this.$lang[this.$store.state.lang].messages.successDelete)
          this.loadData = false
          this.getClientData()
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
          this.deleteClient(id)
        })
      },
      //批量删除
      onBatchDelete(){
        this.$confirm(this.$lang[this.$store.state.lang].messages.confirm, this.$lang[this.$store.state.lang].buttons.confirm, {
          confirmButtonText: this.$lang[this.$store.state.lang].buttons.yes,
          cancelButtonText: this.$lang[this.$store.state.lang].buttons.no,
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
