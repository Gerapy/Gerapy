<template>
  <div>
    <el-form-item :label="$lang.titles.extractors">
      <el-button
        type="primary"
        class="inline"
        size="mini"
        @click="onAddInput(extractors, { callback: '', item: '', attrs: {} })"
      >
        <i class="fa fa-plus"></i>
        {{ $lang.buttons.addExtractor }}
      </el-button>
    </el-form-item>
    <!-- 添加规则配置浮窗 -->
    <el-dialog :visible.sync="addExtractorItem" size="tiny">
      <el-form>
        <el-form-item :label="$lang.titles.selectConfig">
          <el-cascader
            expand-trigger="hover"
            :options="extractorItemOptions"
            v-model="extractorItem"
          >
          </el-cascader>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="addExtractorItem = false" size="small">
          {{ $lang.buttons.cancel }}
        </el-button>
        <el-button @click="onAddExtractorItem()" type="primary" size="small"
          >{{ $lang.buttons.add }}
        </el-button>
      </div>
    </el-dialog>
    <!-- 添加规则配置浮窗 -->

    <el-form-item label-width="100px">
      <el-collapse
        :value="parseInt(extractors.length - 1)"
        v-if="extractors.length"
      >
        <el-collapse-item
          v-for="(extractor, extractorIndex) in extractors"
          :name="extractorIndex"
          :key="extractorIndex"
        >
          <!-- 每条规则标题及操作配置 -->
          <template slot="title">
            <el-form-item class="inline">
              <el-button class="inline m-r-sm" type="primary" size="mini">
                {{ extractorIndex + 1 }}
              </el-button>
            </el-form-item>
            <el-form-item class="inline">
              {{ $lang.titles.extractor }} {{ extractorIndex + 1 }}
            </el-form-item>
            <el-form-item class="inline">
              <el-button
                type="primary"
                class="inline"
                size="mini"
                @click.stop="
                  (addExtractorItem = true),
                    (activeExtractorItem = extractorIndex)
                "
              >
                <i class="fa fa-plus"></i>
                {{ $lang.buttons.addColumn }}
              </el-button>
            </el-form-item>
            <el-form-item class="inline">
              <el-button
                type="danger"
                size="mini"
                class="m-r-md"
                @click="onDeleteInput(extractors, extractorIndex)"
              >
                <i class="fa fa-remove"></i>
                {{ $lang.buttons.delete }}
              </el-button>
            </el-form-item>
          </template>
          <extractor
            :extractor="extractor"
            :items="items"
            :onAddInput="onAddInput"
            :onDeleteInput="onDeleteInput"
          ></extractor>
          <!-- 每条规则标题及操作配置 -->
        </el-collapse-item>
      </el-collapse>
    </el-form-item>
  </div>
</template>

<script>
import Extractor from "./Extractor";

export default {
  name: "Extractors",
  props: {
    extractors: {
      type: Array,
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
      // 提取规则
      addExtractorItem: false,
      extractorItem: null,
      activeExtractorItem: null,
    };
  },
  components: {
    Extractor,
  },
  methods: {
    onAddExtractorItem() {
      this.$set(
        this.extractors[this.activeExtractorItem]["attrs"],
        this.extractorItem.slice(-1),
        []
      );
      this.addExtractorItem = false;
    },
  },
  computed: {
    extractorItemOptions() {
      let array = [];
      this.items.forEach((item) => {
        let attrs = [];
        for (let attr in item["attrs"]) {
          attrs.push({
            value: attr,
            label: attr,
          });
        }
        array.push({
          value: item["name"],
          label: item["name"],
          children: attrs,
        });
      });
      return array;
    },
  },
};
</script>
