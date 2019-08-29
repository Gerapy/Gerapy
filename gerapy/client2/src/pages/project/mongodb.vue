<template>
  <div>
    <el-form ref="form" label-width="90px">
      <el-form-item :label="$lang[$store.state.lang].columns.uri">
        <el-input
          v-model="config.uri" class="inline"
          :placeholder="$lang[$store.state.lang].columns.uri"
          size="small"></el-input>
      </el-form-item>

      <el-form-item :label="$lang[$store.state.lang].columns.database">
        <el-input
          v-model="config.database" class="inline"
          :placeholder="$lang[$store.state.lang].columns.database"
          size="small"></el-input>
      </el-form-item>

      <el-form-item :label="$lang[$store.state.lang].columns.collections">
        <el-button type="primary" class="inline" size="mini" @click="onAddCollection">
          <i class="fa fa-plus"></i>
          {{ $lang[$store.state.lang].buttons.addCollection }}
        </el-button>
        <div v-if="config.collections && config.collections.length">
          <div v-for="(collectionMap, collectionMapKey, collectionMapIndex) in config.collections">
            <el-row style="padding-left: 80px">
              <el-col :span="3">
                <el-select :placeholder="$lang[$store.state.lang].titles.selectConfig"
                           size="small" v-model="collectionMap.item">
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
                <el-input v-model="collectionMap.collection" size="small"
                          :placeholder="$lang[$store.state.lang].columns.collection">
                </el-input>
              </el-col>
              <el-col :span="2">
                <el-button type="danger" size="mini" class="m-l-sm"
                           @click="onDeleteInput(config.collections, collectionMapKey)">
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
          collections: [],
          uri: null,
          database: null
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
      onAddCollection() {
        if (!this.config.collections) {
          this.config.collections = []
        }
        this.config.collections.push({})
        this.$set(this.config, 'collections', this.config.collections)
      },
    }
  }
</script>
