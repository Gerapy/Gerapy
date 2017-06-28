<template>
  <div class="panel">
    <panel-title :title="$route.meta.title">
      <el-button @click.stop="onRefresh" size="small">
        <i class="fa fa-refresh"></i>
      </el-button>
      <router-link :to="{name: 'patternAdd'}" tag="span">
        <el-button type="primary" icon="plus" size="small">添加数据</el-button>
      </router-link>
    </panel-title>
    <div class="panel-body">
      <el-table
        :data="patternData"
        v-loading="loadData"
        element-loading-text="拼命加载中"
        border
        @selection-change="onBatchSelect"
        style="width: 100%;">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column
          prop="envTag"
          label="环境标志"
          width="200">
        </el-table-column>
        <el-table-column
          prop="envDescription"
          label="环境描述"
          width="300">
        </el-table-column>
        <el-table-column
          prop="addressPattern"
          label="规则"
          width="300">
        </el-table-column>
        <el-table-column
          label="操作"
          width="380">
          <template scope="props">
            <router-link :to="{name: 'patternUpdate', params: {id: props.row.envTag}}" tag="span">
              <el-button type="info" size="small" icon="edit">修改</el-button>
            </router-link>
            <el-button type="danger" size="small" icon="delete" @click="deleteData(props.row)">删除</el-button>
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
        patternData: null,
        //请求时的loading效果
        loadData: true,
        //批量选择数组
        batchSelect: [],
        // 总页数
        total: null,
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getPatternData()
    },
    methods: {
      //刷新
      onRefresh(){
        this.getPatternData()
      },
      changeFilter () {
        this.lastIds = {}
        this.getPatternData()
      },
      //获取数据
      getPatternData(){
        this.loadData = true
        this.$fetch.api_pattern.list({})
          .then(({data: patternData}) => {
            this.patternData = patternData
            this.loadData = false
          })
          .catch(() => {
            this.loadData = false
          })
      },
      //单个删除
      deleteData(item){
        this.$confirm('此操作将删除该数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            console.log('Item', item)
            this.loadData = true
            this.$fetch.api_pattern.del(item)
              .then(({msg}) => {
                this.getPatternData()
                this.$message.success(msg)
              })
              .catch(() => {
              })
          })
          .catch(() => {
          })
      },
      //页码选择
      handleCurrentChange(val) {
        this.currentPage = val
        this.getPatternData()
      },
      //批量选择
      onBatchSelect(val){
        this.batchSelect = val
      },
      //批量删除
      onBatchDel(){
        this.$confirm('此操作将批量删除选择数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            this.loadData = true
            console.log(this.batchSelect)
            this.batchSelect.forEach((item) => {
              this.$fetch.api_pattern.del(item)
                .then(({msg}) => {
                  this.getPatternData()
                  this.$message.success(msg)
                })
                .catch(() => {
                })
            })
          })
          .catch(() => {
          })
      }
    }
  }
</script>
<style lang="scss" type="text/scss" rel="stylesheet/scss">
  .inline {
    display: inline-block;
    word-break: inherit;
  }

  .filter {
    width: 150px;
    text-align: center;
    input {
      text-align: center;
    }
  }

  .el-pagination {
    display: inline-block;
    position: relative;
    top: -4px;
  }
</style>
