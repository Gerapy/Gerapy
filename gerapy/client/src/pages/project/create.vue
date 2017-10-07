<template>

  <div class="panel">
    <panel-title title="项目创建">
    </panel-title>
    <div class="panel-body">
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="configuration" label-width="100px">
            <el-form-item label="起始链接:" prop="name">
              <div v-for="(value, key, index) in configuration.startUrls" :key="key">
                <el-input
                  v-model="configuration.startUrls[key]" class="inline start-urls" placeholder="请输入起始链接"
                  size="small"></el-input>
                <el-button type="danger" size="mini" @click="onDeleteInput(configuration.startUrls, key)">
                  <i class="fa fa-remove"></i>
                  删除
                </el-button>
              </div>
              Rule:
              <div v-for="(rule, ruleKey, ruleIndex) in configuration.rules" :key="ruleKey">
                <div class="wrap">
                  <div v-for="(value, key, index) in rule" :key="value">
                    {{ key }}:
                    <div v-if="value instanceof Array">
                      <el-button type="primary" size="mini" @click="onAddInput(configuration.rules[ruleKey][key])">
                        <i class="fa fa-plus"></i>
                        添加
                      </el-button>
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

                  </div>
                </div>
              </div>
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
                  {{  attrKey }}
                </div>
              </div>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>

</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  export default{
    data(){
      return {
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
//            },
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
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  .inline {
    display: inline-block;
    max-width: 30%;
  }

  .start-urls {
    max-width: 70%;
  }

  .wrap {
    border: 1px dashed #EEE;
    padding: 20px;
  }
</style>
