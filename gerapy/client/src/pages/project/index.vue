<template>
  <el-row>
    <el-col :span="3">
      <div class="panel">
        <panel-title title="项目目录">
        </panel-title>
        <div class="panel-body">
          <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
        </div>
      </div>
    </el-col>
    <el-col :span="21">
      <div class="panel m-l-md">
        <panel-title title="代码">
        </panel-title>
        <div class="panel-body">
          <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
        </div>
      </div>
    </el-col>
  </el-row>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  export default{
    data(){
      return {
        clientData: null,
        //请求时的loading效果
        loadData: true,
        //批量选择数组
        batchSelect: [],
        data: [{
          label: '一级 1',
          children: [{
            label: '二级 1-1',
            children: [{
              label: '三级 1-1-1'
            }]
          }]
        }, {
          label: '一级 2',
          children: [{
            label: '二级 2-1',
            children: [{
              label: '三级 2-1-1'
            }]
          }, {
            label: '二级 2-2',
            children: [{
              label: '三级 2-2-1'
            }]
          }]
        }, {
          label: '一级 3',
          children: [{
            label: '二级 3-1',
            children: [{
              label: '三级 3-1-1'
            }]
          }, {
            label: '二级 3-2',
            children: [{
              label: '三级 3-2-1'
            }]
          }]
        }],
        defaultProps: {
          children: 'children',
          label: 'label'
        }
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created(){

    },
    methods: {
      handleNodeClick(data) {
        console.log(data);
      }
    }

  }
</script>
