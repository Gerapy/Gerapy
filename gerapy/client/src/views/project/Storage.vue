<template>
  <div>
    <el-form-item :label="$lang.titles.storage">
      <el-collapse>
        <el-collapse-item>
          <template slot="title">
            <el-form-item class="inline" label-width="80px" label="MongoDB">
              <el-switch v-model="storage.mongodb.enable"> </el-switch>
            </el-form-item>
          </template>
          <mongodb
            :config="storage.mongodb"
            :items="items"
            :onAddInput="onAddInput"
            :onDeleteInput="onDeleteInput"
          ></mongodb>
        </el-collapse-item>
        <el-collapse-item>
          <template slot="title">
            <el-form-item class="inline" label-width="80px" label="MySQL">
              <el-switch v-model="storage.mysql.enable"> </el-switch>
            </el-form-item>
          </template>
          <mysql
            :config="storage.mysql"
            :items="items"
            :onAddInput="onAddInput"
            :onDeleteInput="onDeleteInput"
          ></mysql>
        </el-collapse-item>
      </el-collapse>
    </el-form-item>
  </div>
</template>

<script>
import Mysql from "./Mysql";
import Mongodb from "./Mongodb";

export default {
  name: "Storage",
  props: {
    storage: {
      type: Object,
    },
    items: {
      type: Array,
    },
    onAddInput: {
      type: Function,
    },
    onDeleteInput: {
      type: Function,
    },
  },
  components: {
    Mysql,
    Mongodb,
  },
};
</script>
