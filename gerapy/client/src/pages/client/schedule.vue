<template>
  <div>
    <div class="panel" v-for="project in projects" :key="project">
      <panel-title :title="project">
        <el-button @click.stop="onRefresh" size="small">
          <i class="fa fa-refresh"></i>
        </el-button>
      </panel-title>
      <div class="panel-body">
        <el-table
          :data="spiders[project]"
          v-loading="loadData"
          element-loading-text="拼命加载中"
          style="width: 100%;">
          <el-table-column
            type="selection"
            width="55">
          </el-table-column>
          <el-table-column
            prop="name"
            label="名称"
            width="100">
          </el-table-column>
          <el-table-column
            label="操作">
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
        projects: [],
        spiders: {},
        loadData: true,
        routeId: this.$route.params.id,
      }
    },
    components: {
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getProjects()
    },
    methods: {
      getProjects() {
        this.$fetch.apiClient.projects({
          id: this.routeId
        }).then(({data: data}) => {
          this.projects = data
          this.loadData = false
          this.projects.forEach((project) => {
            this.getSpiders(project)
          })
        }).catch(() => {
          this.loadData = false
        })
      },
      getSpiders(project) {
        this.$fetch.apiClient.projectSpiders({
          id: this.routeId,
          project: project
        }).then(({data: data}) => {
          this.$set(this.spiders, project, data)
        }).catch(() => {
        })
      }
    }
  }
</script>
