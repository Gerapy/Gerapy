<template>

  <div class="panel">
    <panel-title title="项目创建">
    </panel-title>
    <div class="panel-body" id="project-create">
      <el-row>
        <el-col :span="24">
          <el-form ref="form" :model="configuration" label-width="100px">
            <!-- 起始链接开始 -->
            <el-form-item>
              <h4 class="inline">起始链接</h4>
              <el-button type="primary" class="inline" size="mini" @click="onAddInput(configuration.startUrls)">
                <i class="fa fa-plus"></i>
                添加
              </el-button>
              <div v-for="(value, key, index) in configuration.startUrls" :key="key">
                <el-input
                  v-model="configuration.startUrls[key]" class="inline" placeholder="请输入起始链接"
                  size="small"></el-input>
                <el-button type="danger" size="mini" @click="onDeleteInput(configuration.startUrls, key)">
                  <i class="fa fa-remove"></i>
                  删除
                </el-button>
              </div>
            </el-form-item>
            <!-- 起始链接结束 -->

            <div class="hr-line-dashed"></div>
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
              <el-button type="primary" class="inline" size="mini" @click="onAddInput(configuration.rules, {})">
                <i class="fa fa-plus"></i>
                添加
              </el-button>
              <el-collapse accordion>
                <el-collapse-item v-for="(rule, ruleKey, ruleIndex) in configuration.rules">
                  <!-- 每条规则标题及操作配置 -->
                  <template slot="title">
                    <span>
                      规则{{ ruleKey + 1 }}
                    </span>
                    <span class="pull-right">
                      <el-button type="primary" class="inline" size="mini"
                                 @click.stop="addRuleItem=true,activeRule=ruleKey">
                        <i class="fa fa-plus"></i>
                        添加
                      </el-button>
                      <el-button type="danger" size="mini" class="m-r-md"
                                 @click="onDeleteInput(configuration.rules, ruleKey)">
                          <i class="fa fa-remove"></i>
                          删除
                      </el-button>
                    </span>
                  </template>
                  <!-- 每条规则标题及操作配置 -->
                  <!-- 每条规则配置选项 -->
                  <div v-for="(value, key, index) in rule" :key="value">
                    <h5 class="inline m-v-sm">{{ key }}</h5>
                    <el-button type="primary" size="mini" class="inline" v-if="value instanceof Array"
                               @click="onAddInput(configuration.rules[ruleKey][key])">
                      <i class="fa fa-plus"></i>
                      添加
                    </el-button>
                    <el-form-item>
                      <!-- 列表类型，如 allow, deny -->
                      <div v-if="value instanceof Array">
                        <div v-for="(v, k, i) in value">
                          <el-input
                            v-model="configuration.rules[ruleKey][key][k]" class="inline"
                            size="small"></el-input>
                          <el-button type="danger" size="mini"
                                     @click="onDeleteInput(configuration.rules[ruleKey], key, k)">
                            <i class="fa fa-remove"></i>
                            删除
                          </el-button>
                        </div>
                      </div>
                      <!-- 列表类型 -->
                      <!-- 字符串类型，如 callback, process_request -->
                      <div v-if="typeof value == 'string'">
                        <el-input
                          v-model="configuration.rules[ruleKey][key]" class="inline"
                          size="small"></el-input>
                        <el-button type="danger" size="mini" @click="onDeleteInput(configuration.rules[ruleKey], key)">
                          <i class="fa fa-remove"></i>
                          删除
                        </el-button>
                      </div>
                      <!-- 字符串类型 -->
                      <!-- 布尔类型，如 follow -->
                      <div v-if="typeof value == 'boolean'">
                        <el-radio class="radio" v-model="configuration.rules[ruleKey][key]" :label="true">True
                        </el-radio>
                        <el-radio class="radio" v-model="configuration.rules[ruleKey][key]" :label="false">False
                        </el-radio>
                        <el-button type="danger" size="mini" class="pull-right m-r-lg"
                                   @click="onDeleteInput(configuration.rules[ruleKey], key)">
                          <i class="fa fa-remove"></i>
                          删除
                        </el-button>
                      </div>
                      <!-- 布尔类型 -->
                    </el-form-item>
                  </div>
                  <!-- 每条规则配置选项 -->
                </el-collapse-item>
              </el-collapse>
            </el-form-item>
            <!-- 爬取规则结束 -->

            <div class="hr-line-dashed"></div>

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
              <el-collapse accordion>
                <el-collapse-item v-for="(item, itemKey, itemIndex) in configuration.items">
                  <!-- 每个对象配置 -->
                  <template slot="title">
                    <span>
                      对象{{ itemKey + 1 }}
                    </span>
                    <span class="pull-right">
                      <el-button type="primary" class="inline" size="mini"
                                 @click.stop="addItem=true,activeItem=itemKey">
                        <i class="fa fa-plus"></i>
                        添加
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
                    名称
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


            <!-- 提取规则开始 -->
            <el-form-item>
              <h4 class="inline">提取规则</h4>
              <!-- 添加规则配置浮窗 -->
              <el-dialog :visible.sync="addExtractorItem" size="tiny">
                <el-form>
                  <el-form-item label="选择规则配置">
                    <el-select v-model="extractorItem" placeholder="请选择" size="small">
                      <el-option
                        v-for="item in extractorItemOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                      </el-option>
                    </el-select>
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
              <el-collapse accordion>
                <el-collapse-item v-for="(extractor, extractorKey, extractorIndex) in configuration.extractors">
                  <!-- 每条规则标题及操作配置 -->
                  <template slot="title">
                    <span>
                      规则{{ extractorKey + 1 }}
                    </span>
                    <span class="pull-right">
                      <el-button type="danger" size="mini" class="m-r-md"
                                 @click="onDeleteInput(configuration.extractors, extractorKey)">
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
                    <div v-for="(value, key, index) in extractor.attrs" :key="key">
                      {{ key }}
                      <el-button type="primary" size="mini"
                                 @click="onAddInput(extractor.attrs[key], {method: 'xpath'})">
                        <i class="fa fa-plus"></i>
                        添加规则
                      </el-button>
                      <div v-for="(v, k, i) in value" :key="k" class="extractor-rule">
                        <el-select v-model="v['method']" placeholder="提取方式" size="small" class="inline inline-first">
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
                          v-model="v['re']" class="inline inline-third" placeholder="正则表达式"
                          size="small"></el-input>
                        <el-button type="danger" size="mini"
                                   @click="onDeleteInput(extractor.attrs, key, k)">
                          <i class="fa fa-remove"></i>
                          删除
                        </el-button>
                      </div>
                    </div>
                  </el-form-item>
                </el-collapse-item>
              </el-collapse>
            </el-form-item>
            <!-- 提取规则结束 -->


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
          }],

        addItem: false,
        activeItem: null,
        item: null,

        configuration: {
          startUrls: [
            "http://www.baidu.com",
            "http://www.bing.com"
          ],
          rules: [
            {
              allow: ['/subject/', '/allow'],
              deny: ['/subjects/', 'sd', 'vvv'],
            },
//            {
//              allow: ['/subject/', '/allow'],
//              deny: ['/subjects/', 'sd', 'vvv'],
//              allow_domains: ['www.baidu.com'],
//              deny_domains: ['www.bing.com'],
//              deny_extensions: ['s'],
//              restrict_xpaths: ['s'],
//              restrict_css: ['ddd'],
//              callback: 'xc',
//              cb_kwargs: ['sd'],
//              follow: ['s'],
//              process_links: 'sd',
//              process_request: ['sd'],
//              tags: ['sdds'],
//              attrs: ['ssddsds'],
//              canonicalize: ['sd'],
//              unique: ['sd'],
//              process_value: ['sd'],
//              strip: ['s'],
//            }
          ],
          extractors: [
            {
              callback: 'parse_item',
              item: 'NewsItem',
              attrs: {
                title: [
                  {
                    method: 'xpath',
                    arg: '//div[@class="h-news"]//div[@class="h-title"]/text()',
                    re: 'rrrr'
                  }
                ],
                url: [
                  {
                    method: 'attr',
                    arg: 'url'
                  }
                ],
              }
            }
          ],
          items: [
            {
              name: 'NewsItem',
              attrs: {
                title: {
                  inProcessor: 'dssdf',
                  outProcessor: 'sdfsdf',
                },
                url: {
                  inProcessor: 'dssdf',
                  outProcessor: 'sdfsdf',
                }

              }
            }
          ]
        },
        projects: [],
      }
    },
    components: {
      ElInput,
      ElFormItem,
      ElCollapseItem,
      panelTitle,
      bottomToolBar
    },
    created(){
    },
    methods: {
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
      onAddInput(array, arg = '') {
        array.push(arg)
      },
      onAddRuleItem() {
        this.$set(this.configuration.rules[this.activeRule], this.ruleItem, this.ruleItemInit[this.ruleItem])
        this.addRuleItem = false
      },
      onAddItem() {
        this.$set(this.configuration.items[this.activeItem]['attrs'], this.item, {})
        this.addItem = false
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  .inline {
    display: inline-block;
    max-width: calc(100% - 80px);
  }

  .wrap {
    border: 1px dashed #EEE;
    padding: 20px;
  }

  #project-create {
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
      .inline-third {
        width: 200px;
      }
    }
    .item {
      .inline-first {
        min-width: 16px;
      }
      .inline-second {
        width: 60px;
        text-align: center;
      }
      .inline-third, .inline-fourth {
        width: calc((100% - 200px) / 2);
      }
    }
  }


</style>
