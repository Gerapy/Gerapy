<template>
  <div class="main-content ofh">
    <h-section></h-section>
    <div class="wrapper">
      <div class="pageContent">
        <el-row>
          <el-col :span="24">
            <el-breadcrumb separator="/" class="m-b-md m-t-sm">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ $route.meta.title }}</el-breadcrumb-item>
            </el-breadcrumb>
            <slot></slot>
          </el-col>
        </el-row>
      </div>
    </div>
    <v-footer></v-footer>
  </div>
</template>
<script type="text/javascript">
  import hSection from './headerSection'
  import vFooter from './footer'

  export default{
    name: 'content',
    components: {
      hSection,
      vFooter
    }
  }
</script>
