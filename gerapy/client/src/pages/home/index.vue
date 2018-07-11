<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="panel">
          <panel-title :title="$lang[$store.state.lang].objects.client">
            <el-button size="mini" type="primary">
              {{ $lang[$store.state.lang].buttons.normal }}
            </el-button>
          </panel-title>
          <div class="panel-body" v-loading="loading">
            <h1 class="number">{{ status.success}}</h1>
            <small> {{ $lang[$store.state.lang].descriptions.normalClients }}</small>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="panel">
          <panel-title :title="$lang[$store.state.lang].objects.client">
            <el-button size="mini" type="danger">
              {{ $lang[$store.state.lang].buttons.error }}
            </el-button>
          </panel-title>
          <div class="panel-body" v-loading="loading">
            <h1 class="number">{{ status.error}}</h1>
            <small> {{ $lang[$store.state.lang].descriptions.errorClients }}</small>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="panel" id="tree">
          <panel-title :title="$lang[$store.state.lang].objects.project">
            <el-button size="mini" type="success">
              {{ $lang[$store.state.lang].buttons.normal }}
            </el-button>
          </panel-title>
          <div class="panel-body" v-loading="loading">
            <h1 class="number">{{ status.project }}</h1>
            <small>{{ $lang[$store.state.lang].descriptions.countProjects }}</small>
          </div>
        </div>
      </el-col>
    </el-row>
    <!--<el-button type="primary" class="float-circle" @click="monitorFormVisible = true">-->
      <!--<span>+</span>-->
    <!--</el-button>-->
    <el-dialog title="添加监控" :visible.sync="monitorFormVisible">
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="名称:" prop="name">
          <el-input v-model="form.name" placeholder="请输入名称" size="small"></el-input>
        </el-form-item>
        <el-form-item label="描述:" prop="description">
          <el-input v-model="form.description" placeholder="请输入描述" size="small"></el-input>
        </el-form-item>
        <el-form-item label="类型:" prop="type">
          <el-radio size="small" class="radio" v-model="form.type" label="MongoDB">MongoDB</el-radio>
          <el-radio size="small" class="radio" v-model="form.type" label="Redis">Redis</el-radio>
        </el-form-item>
        <div v-if="form.type == 'MongoDB'">
          <el-form-item label="连接信息:" prop="configuration.url">
            <el-input v-model="form.configuration.url" :placeholder="urlPlaceholder[form.type]" size="small"
                      @change="getMongoDBs"></el-input>
          </el-form-item>
          <el-form-item label="数据库:">
            <el-select size="small" v-model="form.configuration.db" allow-create filterable
                       placeholder="选择数据库" @change="getMongoCollections">
              <el-option
                v-for="item in mongoDBs"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="集合:">
            <el-select size="small" v-model="form.configuration.collections" allow-create filterable
                       multiple placeholder="请选择" @visible-change="getMongoDBs" remote
                       :loading="loadingMongoDBs">
              <el-option
                v-for="item in mongoCollections"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </div>
        <div v-if="form.type == 'Redis'">

        </div>
        <el-form-item>
          <el-button type="primary" size="small" @click="onCreateMonitor">
            <i class="fa fa-check"></i>
            创建
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle} from 'components'
  import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item";

  export default{
    data(){
      return {
        radio: '1',
        status: {},
        loading: true,
        monitorFormVisible: false,
        urlPlaceholder: {
          MongoDB: 'mongodb://[username:password@]host[:port][/[database][?options]]',
          Redis: 'redis[s]://[:password]@host:port/db'
        },
        mongoCollections: [],
        mongoDBs: [],
        form: {
          type: 'MongoDB',
          configuration: {
            db: null,
            collections: []
          }
        },
        formLabelWidth: '120px',
        rules: {
          name: [
            {required: true, message: '名称不能为空', trigger: 'blur'},
          ],
          'configuration.url': [
            {required: true, message: '连接信息不能为空', trigger: 'blur'},
          ]
        }
      }
    },
    components: {
      ElFormItem,
      panelTitle
    },
    created(){
      this.getHomeStatus()
    },
    methods: {
      getHomeStatus() {
        this.$fetch.apiHome.status(
        ).then(({data: status}) => {
          console.log(status)
          this.status = status
          this.loading = false
        })
      },
      getMongoDBs() {
        this.mongoDBs = []
        this.$fetch.apiMonitor.getDBList({
          'url': this.form.configuration.url,
          'type': 'MongoDB'
        }).then(({data: dbs}) => {
          this.loadingMongoDBs = false
          dbs.forEach((db) => {
            this.mongoDBs.push({
              'label': db,
              'value': db
            })
          })
        })
      },
      getMongoCollections() {
        this.mongoCollections = []
        this.$fetch.apiMonitor.getCollectionList({
          'url': this.form.configuration.url,
          'type': 'MongoDB',
          'db': this.form.configuration.db
        }).then(({data: dbs}) => {
          dbs.forEach((db) => {
            this.mongoCollections.push({
              'label': db,
              'value': db
            })
          })
        })
      },
      onCreateMonitor() {
        this.$fetch.apiMonitor.create({
          'form': this.form
        }).then(() => {
          this.$message.success('创建成功')
          this.monitorFormVisible = false
        })
      }
    }
  }
</script>

<style scoped>
  h1.number {
    font-weight: 100;
    margin: 10px 0;
    margin-top: 0;
  }

  .float-circle {
    position: fixed;
    bottom: 50px;
    right: 26px;
    z-index: 100;
    height: 38px;
    width: 38px;
    display: block;
    padding: 9px 8px;
    text-align: center;
    border-radius: 50%;
    font-weight: 100;
    font-size: 18px;
  }
</style>
