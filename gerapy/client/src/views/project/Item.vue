<template>
  <div>
    <el-form-item :label="$lang.columns.name" label-width="60px" class="inline">
      <el-input
        v-model="item.name"
        :placeholder="$lang.columns.name"
        size="small"
      ></el-input>
    </el-form-item>
    <el-form-item label-width="20px">
      <div
        v-for="(attr, attrKey, attrIndex) in item.attrs"
        :key="attrKey"
        class="field"
      >
        <el-form-item class="inline" label-width="0">
          <el-button type="primary" size="mini">
            {{ attrIndex + 1 }}
          </el-button>
        </el-form-item>
        <el-form-item class="inline" label-width="0">
          <span
            :style="{
              width: '80px',
              textAlign: 'center',
              display: 'inline-block',
            }"
            >{{ attrKey }}</span
          >
        </el-form-item>
        <el-form-item
          :label="$lang.columns.value"
          class="inline"
          label-width="60px"
        >
          <el-input
            v-model="attr.value"
            :placeholder="$lang.columns.value"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          :label="$lang.columns.inProcessor"
          class="inline"
          label-width="100px"
        >
          <el-input
            v-model="attr.in_processor"
            :placeholder="$lang.columns.inProcessor"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          :label="$lang.columns.outProcessor"
          class="inline"
          label-width="110px"
        >
          <el-input
            v-model="attr.out_processor"
            :placeholder="$lang.columns.outProcessor"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item label-width="5px" class="inline">
          <el-button
            type="danger"
            size="mini"
            class="m-r-md"
            @click="$delete(item.attrs, attrKey)"
          >
            <i class="fa fa-remove"></i>
            {{ $lang.buttons.delete }}
          </el-button>
        </el-form-item>
      </div>
    </el-form-item>
  </div>
</template>

<script>
export default {
  name: "Item",
  props: {
    item: {
      type: Object,
    },
  },
};
</script>
