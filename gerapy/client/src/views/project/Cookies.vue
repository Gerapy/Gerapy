<template>
  <div>
    <h4 class="inline">{{ $lang.titles.cookies }}</h4>
    <el-collapse>
      <el-collapse-item>
        <template slot="title">
          <span>
            {{ cookies.uri }}
          </span>
          <span class="pull-right m-r-md">
            <el-switch v-model="cookies.enable"> </el-switch>
          </span>
        </template>
        <el-form ref="form" label-width="100px">
          <el-form-item :label="$lang.columns.cookiesPool">
            <el-input
              v-model="cookies.uri"
              class="inline"
              :placeholder="$lang.columns.cookiesPool"
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
  name: "Cookies",
  props: {
    cookies: {
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
