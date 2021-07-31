<template>
  <div>
    <el-form-item :label="$lang.columns.uri">
      <el-input
        v-model="config.uri"
        class="inline"
        :placeholder="$lang.columns.uri"
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
    <el-form-item :label="$lang.columns.collections">
      <el-button
        type="primary"
        class="inline"
        size="mini"
        @click="onAddCollection"
      >
        <i class="fa fa-plus"></i>
        {{ $lang.buttons.addCollection }}
      </el-button>
      <div v-if="config.collections && config.collections.length">
        <div v-for="(collectionMap, collectionMapKey) in config.collections">
          <el-form-item class="inline">
            <el-select
              :placeholder="$lang.titles.selectConfig"
              size="small"
              v-model="collectionMap.item"
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
              v-model="collectionMap.collection"
              size="small"
              :placeholder="$lang.columns.collection"
            >
            </el-input>
          </el-form-item>
          <el-form-item class="inline">
            <el-button
              type="danger"
              size="mini"
              class="m-l-sm"
              @click="onDeleteInput(config.collections, collectionMapKey)"
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
  name: "Mongodb",
  props: {
    config: {
      type: Object,
      default: {
        enable: false,
        collections: [],
        uri: null,
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
    onAddCollection() {
      if (!this.config.collections) {
        this.config.collections = [];
      }
      this.config.collections.push({});
      this.$set(this.config, "collections", this.config.collections);
    },
  },
};
</script>
