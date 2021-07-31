<template>
  <div>
    <el-form-item :label="$lang.columns.host">
      <el-input
        v-model="config.host"
        class="inline"
        :placeholder="$lang.columns.host"
        size="small"
      ></el-input>
    </el-form-item>

    <el-form-item :label="$lang.columns.port">
      <el-input
        v-model="config.port"
        class="inline"
        :placeholder="$lang.columns.port"
        size="small"
      ></el-input>
    </el-form-item>

    <el-form-item :label="$lang.columns.user">
      <el-input
        v-model="config.user"
        class="inline"
        :placeholder="$lang.columns.user"
        size="small"
      ></el-input>
    </el-form-item>

    <el-form-item :label="$lang.columns.password">
      <el-input
        v-model="config.password"
        class="inline"
        :placeholder="$lang.columns.password"
        size="small"
      ></el-input>
    </el-form-item>

    <el-form-item :label="$lang.columns.database">
      <el-input
        v-model="config.database"
        class="inline"
        :placeholder="$lang.columns.database"
        size="small"
      ></el-input>
    </el-form-item>
    <el-form-item :label="$lang.columns.tables">
      <el-button type="primary" class="inline" size="mini" @click="onAddTable">
        <i class="fa fa-plus"></i>
        {{ $lang.buttons.addTable }}
      </el-button>
      <div v-if="config.tables && config.tables.length">
        <div v-for="(tableMap, tableMapKey, tableMapIndex) in config.tables">
          <el-form-item class="inline">
            <el-select
              :placeholder="$lang.titles.selectItem"
              size="small"
              v-model="tableMap.item"
            >
              <el-option
                v-for="item in items"
                :key="item.name"
                :label="item.name"
                :value="item.name"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="inline" label-width="20px">
            =>
          </el-form-item>
          <el-form-item class="inline" label-width="20px">
            <el-input
              v-model="tableMap.table"
              size="small"
              :placeholder="$lang.columns.table"
            >
            </el-input>
          </el-form-item>
          <el-form-item class="inline" label-width="20px">
            <el-button
              type="danger"
              size="mini"
              class="m-l-sm"
              @click="onDeleteInput(config.tables, tableMapKey)"
            >
              <i class="fa fa-remove"></i>
              {{ $lang.buttons.delete }}
            </el-button>
          </el-form-item>
        </div>
      </div>
    </el-form-item>
  </div>
</template>

<script>
export default {
  name: "Mysql",
  props: {
    config: {
      type: Object,
      default: {
        enable: false,
        tables: [],
        host: null,
        port: null,
        user: null,
        password: null,
        database: null,
      },
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
  methods: {
    onAddTable() {
      this.config.tables.push({});
      this.$set(this.config, "tables", this.config.tables);
    },
  },
};
</script>
