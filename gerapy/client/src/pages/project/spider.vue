<template>
  <div>
    <el-form-item>
      <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.name }}</h4>
      <el-input v-model="spider.name" class="inline" size="small"
                :placeholder="$lang[$store.state.lang].columns.name"></el-input>
    </el-form-item>

    <el-form-item>
      <h4 class="inline m-r-sm m-b-md">{{ $lang[$store.state.lang].columns.customSettings }}</h4>
      <el-input type="textarea" v-model="spider.custom_settings" class="inline" size="small"
                :placeholder="$lang[$store.state.lang].columns.customSettings"></el-input>
    </el-form-item>

    <el-form-item>
      <h4 class="inline m-r-sm m-b-md">{{ $lang[$store.state.lang].columns.innerCode }}</h4>
      <el-input type="textarea" v-model="spider.code.in_class" class="inline" size="small"
                :placeholder="$lang[$store.state.lang].columns.innerCode"></el-input>
    </el-form-item>

    <el-form-item>
      <h4 class="inline m-r-sm m-b-md">{{ $lang[$store.state.lang].columns.outerCode }}</h4>
      <el-input type="textarea" v-model="spider.code.out_class" class="inline" size="small"
                :placeholder="$lang[$store.state.lang].columns.innerCode"></el-input>
    </el-form-item>

    <!-- 起始链接开始 -->
    <el-form-item>
      <h4 class="inline">{{ $lang[$store.state.lang].columns.classAttrs }}</h4>
      <el-button type="primary" class="inline" size="mini"
                 @click="onAddInput(spider.attrs, {'key': null, 'value': null})">
        <i class="fa fa-plus"></i>
        {{ $lang[$store.state.lang].buttons.addAttr }}
      </el-button>
      <div v-for="(value, key, index) in spider.attrs" :key="key">
        <el-input
          v-model="value['key']" class="inline inline-short"
          :placeholder="$lang[$store.state.lang].columns.attrName"
          size="small"></el-input>
        <el-input
          v-model="value['value']" class="inline inline-long"
          :placeholder="$lang[$store.state.lang].columns.attrValue"
          size="small"></el-input>
        <el-button type="danger" size="mini" @click="onDeleteInput(spider.attrs, key)">
          <i class="fa fa-remove"></i>
          {{ $lang[$store.state.lang].buttons.delete }}
        </el-button>
      </div>
    </el-form-item>
    <!-- 起始链接结束 -->

    <!-- 起始链接开始 -->
    <el-form-item>
      <h4 class="inline">{{ $lang[$store.state.lang].columns.startUrls }}</h4>
      <el-button type="primary" v-if="spider.start_urls.mode == 'list'" class="inline" size="mini"
                 @click="onAddInput(spider.start_urls.list)">
        <i class="fa fa-plus"></i>
        {{ $lang[$store.state.lang].buttons.addUrl }}
      </el-button>
      <div>
        <el-radio class="radio" v-model="spider.start_urls.mode" label="list">
          {{ $lang[$store.state.lang].columns.list }}
        </el-radio>
        <!--<el-radio class="radio" v-model="spider.start_urls.mode" label="file">文件</el-radio>-->
        <el-radio class="radio" v-model="spider.start_urls.mode" label="code">
          {{ $lang[$store.state.lang].columns.code }}
        </el-radio>
      </div>
      <div v-if="spider.start_urls.mode == 'list'">
        <div v-for="(value, key, index) in spider.start_urls.list" :key="key">
          <el-input
            v-model="spider.start_urls.list[key]" class="inline"
            :placeholder="$lang[$store.state.lang].columns.startUrls"
            size="small"></el-input>
          <el-button type="danger" size="mini" @click="onDeleteInput(spider.start_urls.list, key)">
            <i class="fa fa-remove"></i>
            {{ $lang[$store.state.lang].buttons.delete }}
          </el-button>
        </div>
      </div>
      <div v-if="spider.start_urls.mode == 'code'">
        <el-input type="textarea"
                  v-model="spider.start_urls.code" class="inline"
                  :placeholder="$lang[$store.state.lang].columns.code"
                  size="small"></el-input>
      </div>
    </el-form-item>
    <!-- 起始链接结束 -->

    <!-- 合法域名 -->
    <el-form-item>
      <h4 class="inline">{{ $lang[$store.state.lang].columns.allowedDomains }}</h4>
      <el-button type="primary" class="inline" size="mini" @click="onAddInput(spider.allowed_domains)">
        <i class="fa fa-plus"></i>
        {{ $lang[$store.state.lang].buttons.addDomain }}
      </el-button>
      <div v-for="(value, key, index) in spider.allowed_domains" :key="key">
        <el-input
          v-model="spider.allowed_domains[key]" class="inline"
          :placeholder="$lang[$store.state.lang].columns.allowedDomains"
          size="small"></el-input>
        <el-button type="danger" size="mini" @click="onDeleteInput(spider.allowed_domains, key)">
          <i class="fa fa-remove"></i>
          {{ $lang[$store.state.lang].buttons.delete }}
        </el-button>
      </div>
    </el-form-item>
    <!-- 合法域名结束 -->

    <!-- 爬取规则开始 -->
    <el-form-item>
      <h4 class="inline">{{ $lang[$store.state.lang].titles.rules }}</h4>
      <!-- 添加规则配置浮窗 -->
      <el-dialog :visible.sync="addRuleItem" size="tiny">
        <el-form>
          <el-form-item :label="$lang[$store.state.lang].titles.selectConfig">
            <el-select v-model="ruleItem" :placeholder="$lang[$store.state.lang].titles.selectConfig"
                       size="small">
              <el-option
                v-for="item in ruleItemOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer">
          <el-button @click="addRuleItem=false" size="small">{{ $lang[$store.state.lang].buttons.cancel }}
          </el-button>
          <el-button @click="onAddRuleItem()"
                     type="primary" size="small">{{ $lang[$store.state.lang].buttons.add }}
          </el-button>
        </div>
      </el-dialog>
      <!-- 添加规则配置浮窗 -->
      <el-button type="primary" class="inline" size="mini" @click="onAddInput(spider.rules, {})">
        <i class="fa fa-plus"></i>
        {{ $lang[$store.state.lang].buttons.addRule }}
      </el-button>
      <el-collapse :accordion="accordion" :value="parseInt(spider.rules.length-1)"
                   v-if="spider.rules.length">
        <el-collapse-item v-for="(rule, ruleKey, ruleIndex) in spider.rules" :name="ruleKey"
                          :key="ruleKey">
          <!-- 每条规则标题及操作配置 -->
          <template slot="title">
            <span>
              {{ $lang[$store.state.lang].titles.rule }} {{ ruleKey + 1 }}
            </span>
            <span class="pull-right">
              <el-button type="primary" class="inline" size="mini"
                         @click.stop="addRuleItem=true,activeRule=ruleKey">
                <i class="fa fa-plus"></i>
                {{ $lang[$store.state.lang].buttons.addColumn }}
              </el-button>
              <el-button type="danger" size="mini" class="m-r-md"
                         @click="onDeleteInput(spider.rules, ruleKey)">
                  <i class="fa fa-remove"></i>
                  {{ $lang[$store.state.lang].buttons.delete }}
              </el-button>
            </span>
          </template>
          <!-- 每条规则标题及操作配置 -->
          <!-- 每条规则配置选项 -->
          <rule :rule="rule" :onAddInput="onAddInput" :onDeleteInput="onDeleteInput"></rule>
          <!-- 每条规则配置选项 -->
        </el-collapse-item>
      </el-collapse>
    </el-form-item>
    <!-- 爬取规则结束 -->

    <!-- 提取规则开始 -->
    <el-form-item>
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
                 @click="onAddInput(spider.extractors, {callback:'', item: '', attrs:{}})">
        <i class="fa fa-plus"></i>
        {{ $lang[$store.state.lang].buttons.addExtractor }}
      </el-button>
      <el-collapse :accordion="accordion" :value="parseInt(spider.extractors.length-1)"
                   v-if="spider.extractors.length">
        <el-collapse-item v-for="(extractor, extractorKey, extractorIndex) in spider.extractors"
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
                         @click="onDeleteInput(spider.extractors, extractorKey)">
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
    </el-form-item>
    <!-- 提取规则结束 -->

    <!-- 存储开始 -->
    <el-form-item>
      <h4 class="inline">{{ $lang[$store.state.lang].titles.storage }}</h4>
      <div>
        <h5 class="inline m-v-sm">MySQL</h5>
        <el-switch
          v-model="spider.storage.mysql.enable">
        </el-switch>
      </div>
      <div v-if="spider.storage.mysql.enable">

        <el-form-item>
          <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.host }}</h4>
          <el-input
            v-model="spider.storage.mysql.host" class="inline"
            :placeholder="$lang[$store.state.lang].columns.host"
            size="small"></el-input>
        </el-form-item>

        <el-form-item>
          <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.port }}</h4>
          <el-input
            v-model="spider.storage.mysql.port" class="inline"
            :placeholder="$lang[$store.state.lang].columns.port"
            size="small"></el-input>
        </el-form-item>

        <el-form-item>
          <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.user }}</h4>
          <el-input
            v-model="spider.storage.mysql.user" class="inline"
            :placeholder="$lang[$store.state.lang].columns.user"
            size="small"></el-input>
        </el-form-item>

        <el-form-item>
          <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.password }}</h4>
          <el-input
            v-model="spider.storage.mysql.password" class="inline"
            :placeholder="$lang[$store.state.lang].columns.password"
            size="small"></el-input>
        </el-form-item>

        <el-form-item>
          <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.database }}</h4>
          <el-input
            v-model="spider.storage.mysql.database" class="inline"
            :placeholder="$lang[$store.state.lang].columns.database"
            size="small"></el-input>
        </el-form-item>
      </div>
    </el-form-item>
    <!-- 存储结束 -->
  </div>
</template>

<script>
  import rule from 'pages/project/rule'
  import extractor from 'pages/project/extractor'

  export default {
    name: 'Spider',
    data() {
      return {

        ruleItem: null,
        ruleItemOptions: [
          {
            value: 'callback',
            label: 'callback'
          }, {
            value: 'allow',
            label: 'allow'
          }, {
            value: 'deny',
            label: 'deny'
          }, {
            value: 'allow_domains',
            label: 'allow_domains'
          }, {
            value: 'deny_domains',
            label: 'deny_domains'
          }, {
            value: 'restrict_xpaths',
            label: 'restrict_xpaths'
          }, {
            value: 'restrict_css',
            label: 'restrict_css'
          }, {
            value: 'cb_kwargs',
            label: 'cb_kwargs'
          }, {
            value: 'follow',
            label: 'follow'
          }, {
            value: 'process_request',
            label: 'process_request'
          }, {
            value: 'process_links',
            label: 'process_links'
          }, {
            value: 'tags',
            label: 'tags'
          }, {
            value: 'attrs',
            label: 'attrs'
          }, {
            value: 'canonicalize',
            label: 'canonicalize'
          }, {
            value: 'unique',
            label: 'unique'
          }, {
            value: 'process_value',
            label: 'process_value'
          }, {
            value: 'strip',
            label: 'strip'
          },
        ],
        ruleItemInit: {
          callback: '',
          allow: [],
          deny: [],
          allow_domains: [],
          deny_domains: [],
          deny_extensions: [],
          restrict_xpaths: [],
          restrict_css: [],
          tags: [],
          attrs: [],
          canonicalize: false,
          unique: false,
          strip: false,
          follow: false,
          process_value: '',
          process_links: '',
          process_request: '',
        },
        addRuleItem: false,
        activeRule: null,
        accordion: false,

        // 提取规则
        addExtractorItem: false,
        extractorItem: null,
        activeExtractorItem: null,

        // 提取实体
        addItem: false,
        activeItem: null,
        item: null,

        configuration: {
          spiders: [],
          items: []
        }
      }
    },
    props: {
      spider: {
        type: Object,
      },
      spiderKey: {
        type: Number
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
    components: {
      rule,
      extractor
    },
    computed: {
      extractorItemOptions() {
        let array = []
        this.configuration.items.forEach((item) => {
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
    methods: {
      onAddRuleItem() {
        this.$set(this.spider.rules[this.activeRule], this.ruleItem, this.ruleItemInit[this.ruleItem])
        this.addRuleItem = false
      },
    }
  }
</script>
