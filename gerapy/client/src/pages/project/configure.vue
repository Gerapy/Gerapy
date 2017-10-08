<template>

  <div class="panel">
    <panel-title title="项目配置">
      <el-button type="primary" size="mini" @click="saveProject()">
        <i class="fa fa-check"></i>
        保存
      </el-button>
    </panel-title>
    <div class="panel-body" id="project-create">
      <el-row>
        <el-col :span="24">
          <el-form ref="form" :model="configuration" label-width="100px">

            <el-form-item>
              <h4 class="inline m-r-sm">项目名称</h4>
              {{ projectName }}
            </el-form-item>

            <!-- 提取对象 -->
            <el-form-item>
              <h4 class="inline">提取对象</h4>
              <!-- 添加规则配置浮窗 -->
              <el-dialog :visible.sync="addItem" size="tiny">
                <el-form>
                  <el-form-item label="字段名称">
                    <el-input size="small" v-model="item" class="inline" placeholder="字段名称">
                    </el-input>
                  </el-form-item>
                </el-form>
                <div slot="footer">
                  <el-button @click="addItem=false" size="small">取消</el-button>
                  <el-button @click="onAddItem()"
                             type="primary" size="small">添加
                  </el-button>
                </div>
              </el-dialog>
              <!-- 添加规则配置浮窗 -->
              <el-button type="primary" class="inline" size="mini"
                         @click="onAddInput(configuration.items, {name:'', attrs:{}})">
                <i class="fa fa-plus"></i>
                添加对象
              </el-button>
              <el-collapse :accordion="accordion" :value="parseInt(configuration.items.length-1)"
                           v-if="configuration.items.length">
                <el-collapse-item v-for="(item, itemKey, itemIndex) in configuration.items" :name="itemKey">
                  <!-- 每个对象配置 -->
                  <template slot="title">
                    <span>
                      对象{{ itemKey + 1 }}
                    </span>
                    <span class="pull-right">
                      <el-button type="primary" class="inline" size="mini"
                                 @click.stop="addItem=true,activeItem=itemKey">
                        <i class="fa fa-plus"></i>
                        添加字段
                      </el-button>
                      <el-button type="danger" size="mini" class="m-r-md"
                                 @click="onDeleteInput(configuration.items, itemKey)">
                          <i class="fa fa-remove"></i>
                          删除
                      </el-button>
                    </span>
                  </template>
                  <!-- 每个对象配置 -->
                  <el-form-item>
                    <h4 class="inline m-r-sm">名称</h4>
                    <el-input
                      v-model="item['name']" class="inline" placeholder="名称"
                      size="small"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <div v-for="(attr, attrKey, attrIndex) in item.attrs" :key="attrKey" class="item">
                      <el-button class="inline inline-first m-r-sm" type="primary" size="mini">
                        {{ attrIndex + 1 }}
                      </el-button>
                      <span class="inline inline-second">{{ attrKey }}</span>
                      <el-input
                        v-model="attr['inProcessor']" class="inline inline-third" placeholder="输入处理"
                        size="small"></el-input>
                      <el-input
                        v-model="attr['outProcessor']" class="inline inline-fourth" placeholder="输出处理"
                        size="small"></el-input>
                      <el-button type="danger" size="mini" class="m-r-md"
                                 @click="onDeleteInput(item.attrs, attrKey)">
                        <i class="fa fa-remove"></i>
                        删除
                      </el-button>
                    </div>
                  </el-form-item>
                </el-collapse-item>
              </el-collapse>
            </el-form-item>
            <!-- 提取对象结束 -->

            <div class="hr-line-dashed"></div>

            <h4 class="inline m-b-sm">爬虫列表</h4>

            <el-button type="primary" class="inline" size="mini"
                       @click="onAddInput(configuration.spiders, {name:null, extractors:[], rules: [], startUrls:[], allowedDomains: []})">
              <i class="fa fa-plus"></i>
              添加爬虫
            </el-button>

            <el-collapse v-model="activeSpider" accordion v-if="configuration.spiders.length">
              <el-collapse-item v-for="(spider, spiderKey, spiderIndex) in configuration.spiders" :name="spiderKey">
                <template slot="title">
                  <span>
                    <el-button class="inline m-r-sm" type="primary" size="mini">
                        {{ spiderKey + 1 }}
                    </el-button>
                  </span>
                  <span>
                    {{ spider.name }}
                  </span>
                  <span class="pull-right">
                    <el-button type="danger" size="mini" class="m-r-md"
                               @click="onDeleteInput(configuration.spiders, spiderKey)">
                        <i class="fa fa-remove"></i>
                        删除
                    </el-button>
                  </span>
                </template>

                <el-form-item>
                  <h4 class="inline m-r-sm">爬虫名称</h4>
                  <el-input v-model="spider.name" class="inline" size="small" placeholder="爬虫名称"></el-input>
                </el-form-item>

                <!-- 起始链接开始 -->
                <el-form-item>
                  <h4 class="inline">起始链接</h4>
                  <el-button type="primary" class="inline" size="mini" @click="onAddInput(spider.startUrls)">
                    <i class="fa fa-plus"></i>
                    添加链接
                  </el-button>
                  <div v-for="(value, key, index) in spider.startUrls" :key="key">
                    <el-input
                      v-model="spider.startUrls[key]" class="inline" placeholder="请输入起始链接"
                      size="small"></el-input>
                    <el-button type="danger" size="mini" @click="onDeleteInput(spider.startUrls, key)">
                      <i class="fa fa-remove"></i>
                      删除
                    </el-button>
                  </div>
                </el-form-item>
                <!-- 起始链接结束 -->

                <!-- 合法域名 -->
                <el-form-item>
                  <h4 class="inline">合法域名</h4>
                  <el-button type="primary" class="inline" size="mini" @click="onAddInput(spider.allowedDomains)">
                    <i class="fa fa-plus"></i>
                    添加域名
                  </el-button>
                  <div v-for="(value, key, index) in spider.allowedDomains" :key="key">
                    <el-input
                      v-model="spider.allowedDomains[key]" class="inline" placeholder="请输入合法域名"
                      size="small"></el-input>
                    <el-button type="danger" size="mini" @click="onDeleteInput(spider.allowedDomains, key)">
                      <i class="fa fa-remove"></i>
                      删除
                    </el-button>
                  </div>
                </el-form-item>
                <!-- 合法域名结束 -->

                <!-- 爬取规则开始 -->
                <el-form-item>
                  <h4 class="inline">爬取规则</h4>
                  <!-- 添加规则配置浮窗 -->
                  <el-dialog :visible.sync="addRuleItem" size="tiny">
                    <el-form>
                      <el-form-item label="选择规则配置">
                        <el-select v-model="ruleItem" placeholder="请选择" size="small">
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
                      <el-button @click="addRuleItem=false" size="small">取消</el-button>
                      <el-button @click="onAddRuleItem()"
                                 type="primary" size="small">添加
                      </el-button>
                    </div>
                  </el-dialog>
                  <!-- 添加规则配置浮窗 -->
                  <el-button type="primary" class="inline" size="mini" @click="onAddInput(spider.rules, {})">
                    <i class="fa fa-plus"></i>
                    添加规则
                  </el-button>
                  <el-collapse :accordion="accordion" :value="parseInt(spider.rules.length-1)"
                               v-if="spider.rules.length">
                    <el-collapse-item v-for="(rule, ruleKey, ruleIndex) in spider.rules" :name="ruleKey">
                      <!-- 每条规则标题及操作配置 -->
                      <template slot="title">
                        <span>
                          规则{{ ruleKey + 1 }}
                        </span>
                        <span class="pull-right">
                          <el-button type="primary" class="inline" size="mini"
                                     @click.stop="addRuleItem=true,activeRule=ruleKey">
                            <i class="fa fa-plus"></i>
                            添加字段
                          </el-button>
                          <el-button type="danger" size="mini" class="m-r-md"
                                     @click="onDeleteInput(spider.rules, ruleKey)">
                              <i class="fa fa-remove"></i>
                              删除
                          </el-button>
                        </span>
                      </template>
                      <!-- 每条规则标题及操作配置 -->
                      <!-- 每条规则配置选项 -->
                      <div v-if="Object.keys(rule).length">
                        <div v-for="(value, key, index) in rule" :key="value">
                          <h5 class="inline m-v-sm">{{ key }}</h5>
                          <el-button type="primary" size="mini" class="inline" v-if="value instanceof Array"
                                     @click="onAddInput(spider.rules[ruleKey][key])">
                            <i class="fa fa-plus"></i>
                            添加
                          </el-button>
                          <el-form-item>
                            <!-- 列表类型，如 allow, deny -->
                            <div v-if="value instanceof Array">
                              <div v-for="(v, k, i) in value">
                                <el-input
                                  v-model="spider.rules[ruleKey][key][k]" class="inline"
                                  size="small"></el-input>
                                <el-button type="danger" size="mini"
                                           @click="onDeleteInput(spider.rules[ruleKey], key, k)">
                                  <i class="fa fa-remove"></i>
                                  删除
                                </el-button>
                              </div>
                            </div>
                            <!-- 列表类型 -->
                            <!-- 字符串类型，如 callback, process_request -->
                            <div v-if="typeof value == 'string'">
                              <el-input
                                v-model="spider.rules[ruleKey][key]" class="inline"
                                size="small"></el-input>
                              <el-button type="danger" size="mini"
                                         @click="onDeleteInput(spider.rules[ruleKey], key)">
                                <i class="fa fa-remove"></i>
                                删除
                              </el-button>
                            </div>
                            <!-- 字符串类型 -->
                            <!-- 布尔类型，如 follow -->
                            <div v-if="typeof value == 'boolean'">
                        <span class="inline">
                          <el-radio class="radio" v-model="spider.rules[ruleKey][key]" :label="true">True
                          </el-radio>
                          <el-radio class="radio" v-model="spider.rules[ruleKey][key]" :label="false">False
                          </el-radio>
                        </span>
                              <el-button type="danger" size="mini"
                                         @click="onDeleteInput(spider.rules[ruleKey], key)">
                                <i class="fa fa-remove"></i>
                                删除
                              </el-button>
                            </div>
                            <!-- 布尔类型 -->
                          </el-form-item>
                        </div>
                      </div>
                      <div v-else>
                        <h5>请添加字段</h5>
                      </div>
                      <!-- 每条规则配置选项 -->
                    </el-collapse-item>
                  </el-collapse>
                </el-form-item>
                <!-- 爬取规则结束 -->


                <!-- 提取规则开始 -->
                <el-form-item>
                  <h4 class="inline">解析器</h4>
                  <!-- 添加规则配置浮窗 -->
                  <el-dialog :visible.sync="addExtractorItem" size="tiny">
                    <el-form>
                      <el-form-item label="选择规则配置">
                        <el-cascader
                          expand-trigger="hover"
                          :options="extractorItemOptions"
                          v-model="extractorItem">
                        </el-cascader>
                      </el-form-item>
                    </el-form>
                    <div slot="footer">
                      <el-button @click="addExtractorItem=false" size="small">取消</el-button>
                      <el-button @click="onAddExtractorItem()"
                                 type="primary" size="small">添加
                      </el-button>
                    </div>
                  </el-dialog>
                  <!-- 添加规则配置浮窗 -->
                  <el-button type="primary" class="inline" size="mini"
                             @click="onAddInput(spider.extractors, {callback:'', item: '', attrs:{}})">
                    <i class="fa fa-plus"></i>
                    添加解析器
                  </el-button>
                  <el-collapse :accordion="accordion" :value="parseInt(spider.extractors.length-1)"
                               v-if="spider.extractors.length">
                    <el-collapse-item v-for="(extractor, extractorKey, extractorIndex) in spider.extractors"
                                      :name="extractorKey">
                      <!-- 每条规则标题及操作配置 -->
                      <template slot="title">
                        <span>
                          规则{{ extractorKey + 1 }}
                        </span>
                        <span class="pull-right">
                          <el-button type="primary" class="inline" size="mini"
                                     @click.stop="addExtractorItem=true,activeExtractorItem=extractorKey">
                            <i class="fa fa-plus"></i>
                            添加字段
                          </el-button>
                          <el-button type="danger" size="mini" class="m-r-md"
                                     @click="onDeleteInput(spider.extractors, extractorKey)">
                              <i class="fa fa-remove"></i>
                              删除
                          </el-button>
                        </span>
                      </template>
                      <!-- 每条规则标题及操作配置 -->
                      <el-form-item>
                        <h5 class="inline m-v-sm">处理函数</h5>
                        <el-input
                          v-model="extractor.callback" class="inline" placeholder="处理函数名称"
                          size="small">
                        </el-input>
                      </el-form-item>
                      <el-form-item>
                        <h5 class="inline m-v-sm">提取对象</h5>
                        <el-select v-model="extractor.item" placeholder="提取对象" size="small" class="inline inline-first">
                          <el-option
                            v-for="item in extractorItemOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                          </el-option>
                        </el-select>
                      </el-form-item>
                      <el-form-item>
                        <div v-if="Object.keys(extractor.attrs).length">
                          <div v-for="(value, key, index) in extractor.attrs" :key="key">
                            {{ key }}
                            <el-button type="primary" size="mini"
                                       @click="onAddInput(extractor.attrs[key], {method: 'xpath'})">
                              <i class="fa fa-plus"></i>
                              添加规则
                            </el-button>
                            <div v-for="(v, k, i) in value" :key="k" class="extractor-rule">
                              <el-select v-model="v['method']" placeholder="提取方式" size="small"
                                         class="inline inline-first">
                                <el-option
                                  v-for="item in extractorMethods"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                              </el-select>
                              <el-input
                                v-model="v['arg']" class="inline inline-second" placeholder="提取规则"
                                size="small"></el-input>
                              <el-input
                                v-model="v['processor']" class="inline inline-third" placeholder="处理器"
                                size="small"></el-input>
                              <el-input
                                v-model="v['re']" class="inline inline-fourth" placeholder="正则表达式"
                                size="small"></el-input>
                              <el-button type="danger" size="mini"
                                         @click="onDeleteInput(extractor.attrs, key, k)">
                                <i class="fa fa-remove"></i>
                                删除
                              </el-button>
                            </div>
                          </div>
                        </div>
                        <div v-else>
                          <h5>请添加字段</h5>
                        </div>
                      </el-form-item>
                    </el-collapse-item>
                  </el-collapse>
                </el-form-item>
                <!-- 提取规则结束 -->

              </el-collapse-item>
            </el-collapse>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>

</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  import ElCollapseItem from "../../../node_modules/element-ui/packages/collapse/src/collapse-item";
  import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item";
  import ElInput from "../../../node_modules/element-ui/packages/input/src/input";
  export default{
    data(){
      return {
        projectName: this.$route.params.name,
        projectDescription: null,
        activeSpider: 0,

        accordion: false,
        // 规则配置
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

        // 提取规则
        addExtractorItem: false,
        extractorItem: null,
        activeExtractorItem: null,
        extractorMethods: [
          {
            value: 'xpath',
            label: 'XPath'
          }, {
            value: 'css',
            label: 'CSS'
          }, {
            value: 'attr',
            label: 'Attr'
          }, {
            value: 'value',
            label: 'Value'
          }
        ],
        // 提取对象
        addItem: false,
        activeItem: null,
        item: null,

        configuration: {
          spiders: [],
          items: []
        }
      }
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
    components: {
      ElInput,
      ElFormItem,
      ElCollapseItem,
      panelTitle,
      bottomToolBar
    },
    created() {
      this.getProject()
    },
    methods: {
      getProject() {
        this.$fetch.apiProject.projectGetConfiguration({
          name: this.projectName
        }).then(({data: data}) => {
          console.log(data)
          this.projectDescription = data.description
          this.configuration = data.configuration || this.configuration
          this.loadData = false
        }).catch(() => {
          this.$message.error('获取配置失败')
        })
      },
      saveProject() {
        this.$fetch.apiProject.projectSaveConfiguration({
          name: this.projectName
        }, {
          configuration: this.configuration
        }).then(({data: data}) => {
          console.log(data.configuration)
          this.$message.success('保存配置成功')
        }).catch(() => {
          this.$message.error('保存配置失败')
        })
      },
      onDeleteInput(array, ...keys) {
        if (keys.length == 2) {
          // 二维字典
          this.$delete(array[keys[0]], keys[1])
          if (array[keys[0]].length == 0) {
            this.$delete(array, keys[0])
          }
        } else if (keys.length == 1) {
          // 一维字典
          this.$delete(array, keys[0])
        }
      },
      onAddItem() {
        this.$set(this.configuration.items[this.activeItem]['attrs'], this.item, {})
        this.addItem = false
      },
      onAddInput(array, arg = '') {
        array.push(arg)
      },
      onAddRuleItem() {
        this.$set(this.configuration.spiders[this.activeSpider].rules[this.activeRule], this.ruleItem, this.ruleItemInit[this.ruleItem])
        this.addRuleItem = false
      },
      onAddExtractorItem() {
        this.$set(this.configuration.spiders[this.activeSpider].extractors[this.activeExtractorItem]['attrs'], this.extractorItem.slice(-1), [])
        this.addExtractorItem = false
      }
    },
    watch: {
      configuration: {
        handler() {
          this.saveProject()
        },
        deep: true
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  .inline {
    display: inline-block;
    max-width: calc(100% - 80px);
  }

  .inline-long {
    max-width: 400px !important;
  }

  .wrap {
    border: 1px dashed #EEE;
    padding: 20px;
  }

  #project-create {
    .inline {
      max-width: 200px;
    }
    .el-form-item__content {
      margin-left: 10px !important;
    }

    .el-collapse-item__wrap {
      background-color: white !important;
    }
    h4, h5 {
      font-weight: 200;
    }
    .extractor-rule {
      .inline-first {
        width: 100px;
      }
      .inline-second {
        width: calc(100% - 380px);
      }
      .inline-third, .inline-third {
        width: 200px;
      }
    }
    .item {
      .inline-first {
        min-width: 16px;
      }
      .inline-second {
        width: 80px;
        text-align: center;
      }
      .inline-third, .inline-fourth {
        width: calc((100% - 200px) / 2);
      }
    }
  }
</style>
