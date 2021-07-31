<template>
  <div>
    <h4 class="inline">{{ $lang.titles.proxy }}</h4>
    <el-collapse>
      <el-collapse-item v-if="proxy">
        <template slot="title">
          <span>
            {{ proxy.uri }}
          </span>
          <span class="pull-right m-r-md">
            <el-switch v-model="proxy.enable"> </el-switch>
          </span>
        </template>

        <el-form ref="form" label-width="100px">
          <el-form-item :label="$lang.columns.proxyPool">
            <el-input
              v-model="proxy.uri"
              class="inline"
              :placeholder="$lang.columns.proxyPool"
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$lang.columns.failTimes">
            <el-input
              v-model="proxy.failTimes"
              class="inline"
              :placeholder="$lang.columns.failTimes"
              size="small"
            ></el-input>
          </el-form-item>
        </el-form>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
export default {
  name: "Proxy",
  props: {
    proxy: {
      type: Object,
    },
    onAddInput: {
      type: Function,
    },
    onDeleteInput: {
      type: Function,
    },
  },
};
</script>
