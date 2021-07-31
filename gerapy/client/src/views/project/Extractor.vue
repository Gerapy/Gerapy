<template>
  <div>
    <el-form-item :label="$lang.titles.column">
      <div v-if="Object.keys(extractor.attrs).length">
        <div v-for="(value, key) in extractor.attrs" :key="key">
          <el-form-item class="inline">
            {{ key }}
          </el-form-item>
          <el-form-item class="inline">
            <el-button
              type="primary"
              size="mini"
              @click="onAddInput(extractor.attrs[key], { method: 'xpath' })"
            >
              <i class="fa fa-plus"></i>
              {{ $lang.buttons.addRule }}
            </el-button>
          </el-form-item>
          <div v-for="(v, k) in value" :key="k" class="label-center">
            <el-form-item class="inline">
              <el-select
                v-model="v['method']"
                :placeholder="$lang.columns.method"
                size="small"
                class="inline inline-first"
              >
                <el-option
                  v-for="item in extractorMethods"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item class="inline" :label="$lang.columns.value">
              <el-input
                v-model="v['arg']"
                class="inline inline-second"
                :placeholder="$lang.columns.value"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item class="inline" :label="$lang.columns.processors">
              <el-input
                v-model="v['processor']"
                class="inline inline-third"
                :placeholder="$lang.columns.processors"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item class="inline" :label="$lang.columns.regex">
              <el-input
                v-model="v['re']"
                class="inline inline-fourth"
                :placeholder="$lang.columns.regex"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item class="inline">
              <el-button
                type="danger"
                size="mini"
                @click="onDeleteInput(extractor.attrs, key, k)"
              >
                <i class="fa fa-remove"></i>
                {{ $lang.buttons.delete }}
              </el-button>
            </el-form-item>
          </div>
        </div>
      </div>
      <div v-else>
        <p>{{ $lang.messages.addColumn }}</p>
      </div>
    </el-form-item>
    <el-form-item :label="$lang.titles.callback" class="inline">
      <el-input
        v-model="extractor.callback"
        :placeholder="$lang.titles.callback"
        size="small"
      >
      </el-input>
    </el-form-item>
    <el-form-item :label="$lang.titles.item">
      <el-select
        v-model="extractor.item"
        :placeholder="$lang.titles.item"
        size="small"
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
  </div>
</template>

<script>
export default {
  name: "Extractor",
  props: {
    extractor: {
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
  data() {
    return {
      extractorMethods: [
        {
          value: "xpath",
          label: "XPath",
        },
        {
          value: "css",
          label: "CSS",
        },
        {
          value: "attr",
          label: "Attr",
        },
        {
          value: "value",
          label: "Value",
        },
      ],
    };
  },
};
</script>
