<template>

  <div class="panel">
    <panel-title title="项目创建">
    </panel-title>
    <div class="panel-body">
      <el-row>
        <el-col :span="24">
          <el-form ref="form" :model="configuration" label-width="100px">
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
            <div class="hr-line-dashed"></div>
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
                  <div v-for="(value, key, index) in rule" :key="value">
                    <h5 class="inline m-v-sm">{{ key }}</h5>
                    <el-button type="primary" size="mini" class="inline" v-if="value instanceof Array"
                               @click="onAddInput(configuration.rules[ruleKey][key])">
                      <i class="fa fa-plus"></i>
                      添加
                    </el-button>
                    <el-form-item>
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
                      <div v-if="typeof value == 'string'">
                        <el-input
                          v-model="configuration.rules[ruleKey][key]" class="inline"
                          size="small"></el-input>
                        <el-button type="danger" size="mini" @click="onDeleteInput(configuration.rules[ruleKey], key)">
                          <i class="fa fa-remove"></i>
                          删除
                        </el-button>
                      </div>
                    </el-form-item>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </el-form-item>

            Extractors:
            <div v-for="(extractor, extractorKey, extractorIndex) in configuration.extractors" :key="extractorKey">
              Callback:
              <el-input
                v-model="extractor.callback" class="inline" placeholder="callback"
                size="small"></el-input>
              <div v-for="(value, key, index) in extractor.attrs" :key="key">
                {{ key }}:
                <el-button type="primary" size="mini" @click="onAddInput(extractor.attrs[key], {method: 'xpath'})">
                  <i class="fa fa-plus"></i>
                  添加
                </el-button>
                <el-button type="danger" size="mini"
                           @click="onDeleteInput(extractor.attrs, key)">
                  <i class="fa fa-remove"></i>
                  删除
                </el-button>
                <div v-for="(v, k, i) in value" :key="k">
                  <el-select v-model="v['method']" placeholder="请选择" size="small" class="inline">
                    <el-option
                      v-for="item in methods"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                  <el-input
                    v-model="v['arg']" class="inline" placeholder="arg"
                    size="small"></el-input>
                  <el-input
                    v-model="v['re']" class="inline" placeholder="re"
                    size="small"></el-input>
                  <el-button type="danger" size="mini"
                             @click="onDeleteInput(value, k)">
                    <i class="fa fa-remove"></i>
                    删除
                  </el-button>
                </div>
              </div>
            </div>
            Items:
            <div v-for="(item, itemKey, itemIndex) in configuration.items" :key="itemKey">
              Name:
              <el-input
                v-model="item['name']" class="inline" placeholder="callback"
                size="small"></el-input>
              <div v-for="(attr, attrKey, attrIndex) in item.attrs" :key="attrKey">
                {{ attrKey }}
                Input:
                <el-input
                  v-model="attr['inProcessor']" class="inline" placeholder="inProcessor"
                  size="small"></el-input>
                Output:
                <el-input
                  v-model="attr['outProcessor']" class="inline" placeholder="outProcessor"
                  size="small"></el-input>
              </div>
            </div>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>

</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  import ElCollapseItem from "../../../node_modules/element-ui/packages/collapse/src/collapse-item";
  export default{
    data(){
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
        addRuleItem: false,
        activeRule: null,
        methods: [{
          value: 'xpath',
          label: 'XPath'
        }, {
          value: 'css',
          label: 'CSS'
        }, {
          value: 'attr',
          label: 'Attr'
        }],
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
                title: [
                  {
                    inProcessor: 'dssdf',
                    outProcessor: 'sdfsdf',
                  }
                ],
                url: [
                  {
                    inProcessor: 'dssdf',
                    outProcessor: 'sdfsdf',
                  }
                ]
              }
            }
          ]
        },
        projects: [],
        //请求时的loading效果
        loadData: false,
        //批量选择数组
        batchSelect: [],
        buildInfos: {}
      }
    },
    components: {
      ElCollapseItem,
      panelTitle,
      bottomToolBar
    },
    created(){
      this.getProjectData()
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
        console.log(array)
        array.push(arg)
      },
      onAddRuleItem() {
        this.$set(this.configuration.rules[this.activeRule], this.ruleItem, [])
        this.addRuleItem = false
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

  .el-form-item__content {
    margin-left: 10px !important;
  }

  .el-collapse-item__wrap {
    background-color: white !important;
  }

  h4, h5 {
    font-weight: 200;
  }
</style>
