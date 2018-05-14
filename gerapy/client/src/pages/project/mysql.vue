<template>
  <div>
    <el-form ref="form" label-width="90px">
      <el-form-item :label="$lang[$store.state.lang].columns.host">
        <el-input
          v-model="config.host" class="inline"
          :placeholder="$lang[$store.state.lang].columns.host"
          size="small"></el-input>
      </el-form-item>

      <el-form-item :label="$lang[$store.state.lang].columns.port">
        <el-input
          v-model="config.port" class="inline"
          :placeholder="$lang[$store.state.lang].columns.port"
          size="small"></el-input>
      </el-form-item>

      <el-form-item :label="$lang[$store.state.lang].columns.user">
        <el-input
          v-model="config.user" class="inline"
          :placeholder="$lang[$store.state.lang].columns.user"
          size="small"></el-input>
      </el-form-item>

      <el-form-item :label="$lang[$store.state.lang].columns.password">
        <el-input
          v-model="config.password" class="inline"
          :placeholder="$lang[$store.state.lang].columns.password"
          size="small"></el-input>
      </el-form-item>

      <el-form-item :label="$lang[$store.state.lang].columns.database">
        <el-input
          v-model="config.database" class="inline"
          :placeholder="$lang[$store.state.lang].columns.database"
          size="small"></el-input>
      </el-form-item>
      <el-form-item :label="$lang[$store.state.lang].columns.tables">
        <el-button type="primary" class="inline" size="mini" @click="onAddTable">
          <i class="fa fa-plus"></i>
          {{ $lang[$store.state.lang].buttons.addTable }}
        </el-button>
        <div v-if="config.tables && config.tables.length">
          <div v-for="(tableMap, tableMapKey, tableMapIndex) in config.tables">
            <el-row style="padding-left: 80px">
              <el-col :span="3">
                <el-select :placeholder="$lang[$store.state.lang].titles.selectItem"
                           size="small" v-model="tableMap.item">
                  <el-option
                    v-for="item in items"
                    :key="item.name"
                    :label="item.name"
                    :value="item.name">
                  </el-option>
                </el-select>
              </el-col>
              <el-col :span="1" class="text-center">=></el-col>
              <el-col :span="3">
                <el-input v-model="tableMap.table" size="small" :placeholder="$lang[$store.state.lang].columns.table">
                </el-input>
              </el-col>
              <el-col :span="2">
                <el-button type="danger" size="mini" class="m-l-sm"
                           @click="onDeleteInput(config.tables, tableMapKey)">
                  <i class="fa fa-remove"></i>
                  {{ $lang[$store.state.lang].buttons.delete }}
                </el-button>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-form-item>

    </el-form>

  </div>
</template>

<script>
  import ElInput from "../../../node_modules/element-ui/packages/input/src/input";
  import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item";
  export default {
    components: {
      ElFormItem,
      ElInput
    },
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
        }
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
    methods: {
      onAddTable() {
        console.log(this.config.tables)
        this.config.tables.push({})
        this.$set(this.config, 'tables', this.config.tables)
      },
    }
  }
</script>
