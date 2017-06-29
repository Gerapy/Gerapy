<template>
  <div>
    <div class="panel" v-for="project in projects">
      <panel-title :title="project">
        <el-button @click.stop="onRefresh" size="small">
          <i class="fa fa-refresh"></i>
        </el-button>
      </panel-title>
      <div class="panel-body">

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
        //请求时的loading效果
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
        }).catch(() => {
          this.loadData = false
        })
      }
    }
  }
</script>
