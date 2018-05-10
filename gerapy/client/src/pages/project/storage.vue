<template>
  <div>
    <h4 class="inline">{{ $lang[$store.state.lang].titles.storage }}</h4>

    <el-collapse>
      <el-collapse-item>
        <template slot="title">
            <span>
              MySQL
            </span>
          <span class="pull-right m-r-md">
            <el-switch
              v-model="storage.mysql.enable">
            </el-switch>
          </span>
        </template>
        <mysql :config="storage.mysql" :items="items" :onAddInput="onAddInput" :onDeleteInput="onDeleteInput"></mysql>
      </el-collapse-item>
      <el-collapse-item>
        <template slot="title">
            <span>
              MongoDB
            </span>
          <span class="pull-right m-r-md">
            <el-switch
              v-model="storage.mongodb.enable">
            </el-switch>
          </span>
        </template>
        <mongodb :config="storage.mongodb" :items="items" :onAddInput="onAddInput" :onDeleteInput="onDeleteInput"></mongodb>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
  import mysql from 'pages/project/mysql'
  import mongodb from 'pages/project/mongodb'

  export default {
    name: 'Storage',
    props: {
      storage: {
        type: Object,
      },
      items: {
        type: Array
      },
      onAddInput: {
        type: Function
      },
      onDeleteInput: {
        type: Function
      }
    },
    components: {
      mysql,
      mongodb
    }
  }
</script>
