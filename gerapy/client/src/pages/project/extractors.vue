<template>
  <div>
    <h4 class="inline">{{ $lang[$store.state.lang].titles.extractors }}</h4>
    <!-- 添加规则配置浮窗 -->
    <el-dialog :visible.sync="addExtractorItem" size="tiny">
      <el-form>
        <el-form-item :label="$lang[$store.state.lang].titles.selectConfig">
          <el-cascader
            expand-trigger="hover"
            :options="extractorItemOptions"
            v-model="extractorItem">
          </el-cascader>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="addExtractorItem=false" size="small">
          {{ $lang[$store.state.lang].buttons.cancel }}
        </el-button>
        <el-button @click="onAddExtractorItem()"
                   type="primary" size="small">{{ $lang[$store.state.lang].buttons.add }}
        </el-button>
      </div>
    </el-dialog>
    <!-- 添加规则配置浮窗 -->
    <el-button type="primary" class="inline" size="mini"
               @click="onAddInput(extractors, {callback:'', item: '', attrs:{}})">
      <i class="fa fa-plus"></i>
      {{ $lang[$store.state.lang].buttons.addExtractor }}
    </el-button>
    <el-collapse :value="parseInt(extractors.length-1)"
                 v-if="extractors.length">
      <el-collapse-item v-for="(extractor, extractorKey, extractorIndex) in extractors"
                        :name="extractorKey" :key="extractorKey">
        <!-- 每条规则标题及操作配置 -->
        <template slot="title">
            <span>
              {{ $lang[$store.state.lang].titles.extractor }} {{ extractorKey + 1 }}
            </span>
          <span class="pull-right">
              <el-button type="primary" class="inline" size="mini"
                         @click.stop="addExtractorItem=true,activeExtractorItem=extractorKey">
                <i class="fa fa-plus"></i>
                {{ $lang[$store.state.lang].buttons.addColumn }}
              </el-button>
              <el-button type="danger" size="mini" class="m-r-md"
                         @click="onDeleteInput(extractors, extractorKey)">
                  <i class="fa fa-remove"></i>
                  {{ $lang[$store.state.lang].buttons.delete }}
              </el-button>
            </span>
        </template>
        <extractor :extractor="extractor" :items="items" :onAddInput="onAddInput"
                   :onDeleteInput="onDeleteInput"></extractor>
        <!-- 每条规则标题及操作配置 -->
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
  import extractor from 'pages/project/extractor'

  export default {
    name: 'Extractors',
    props: {
      extractors: {
        type: Array
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
    data() {
      return {
        // 提取规则
        addExtractorItem: false,
        extractorItem: null,
        activeExtractorItem: null,
      }
    },
    components: {
      extractor,
    },
    methods: {
      onAddExtractorItem() {
        this.$set(this.extractors[this.activeExtractorItem]['attrs'], this.extractorItem.slice(-1), [])
        this.addExtractorItem = false
      },
    },
    computed: {
      extractorItemOptions() {
        let array = []
        this.items.forEach((item) => {
          let attrs = []
          for (let attr in item['attrs']) {
            attrs.push({
              value: attr,
              label: attr
            })
          }
          array.push({
            value: item['name'],
            label: item['name'],
            children: attrs
          })
        })
        return array
      }
    },
  }
</script>
