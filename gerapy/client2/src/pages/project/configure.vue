<template>
  <div>
    <div class="panel">
      <el-alert v-if="error"
        title="Error"
        type="error"
        :closable="false"
        id="error-message"
        :show-icon="false">
        <template slot-scope="description">
          <pre>
            {{ error }}
          </pre>
        </template>
      </el-alert>
      <el-button @click="saveProject" type="primary" id="save-project">
        <i class="fa fa-spin fa-circle-o-notch" v-if="savingProject"></i>
        <i class="fa fa-save" v-else></i>
      </el-button>
      <panel-title :title="$lang[$store.state.lang].titles.configureProject">
      </panel-title>
      <div class="panel-body" id="project-create">
        <el-row>
          <el-col :span="24">
            <el-form ref="form" :model="configuration" label-width="100px">
              <el-form-item>
                <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.projectName }}</h4>
                {{ projectName }}
              </el-form-item>
              <el-form-item>
                <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.generateCode }}</h4>
                {{ projectGeneratedAt ? projectGeneratedAt : $lang[$store.state.lang].descriptions.notGenerated }}
                <!--<el-button type="primary" class="inline" size="mini"-->
                <!--@click="onGenerate(projectName)">-->
                <!--<i class="fa fa-magic"></i>-->
                <!--{{ $lang[$store.state.lang].buttons.generate }}-->
                <!--</el-button>-->
              </el-form-item>
              <div class="hr-line-dashed"></div>
              <!-- 提取实体 -->
              <h4 class="inline m-v-md">{{ $lang[$store.state.lang].titles.items }}</h4>
              <!-- 添加规则配置浮窗 -->
              <el-dialog :visible.sync="addItem" size="tiny">
                <el-form>
                  <el-form-item :label="$lang[$store.state.lang].columns.column">
                    <el-input size="small" v-model="item" class="inline"
                              :placeholder="$lang[$store.state.lang].columns.column">
                    </el-input>
                  </el-form-item>
                </el-form>
                <div slot="footer">
                  <el-button @click="addItem=false" size="small">{{ $lang[$store.state.lang].buttons.cancel }}
                  </el-button>
                  <el-button @click="onAddItem()"
                             type="primary" size="small">{{ $lang[$store.state.lang].buttons.add }}
                  </el-button>
                </div>
              </el-dialog>

              <!-- 添加配置浮窗 -->
              <el-button type="primary" class="inline" size="mini"
                         @click="onAddInput(configuration.items, {name:'', attrs:{}})">
                <i class="fa fa-plus"></i>
                {{ $lang[$store.state.lang].buttons.addItem }}
              </el-button>
              <el-collapse :accordion="accordion" :value="parseInt(configuration.items.length-1)"
                           v-if="configuration.items.length">
                <el-collapse-item v-for="(item, itemKey, itemIndex) in configuration.items" :name="itemKey"
                                  :key="itemKey">
                  <!-- 每个实体配置 -->
                  <template slot="title">
                    <span>
                      {{ $lang[$store.state.lang].titles.item }} {{ itemKey + 1 }}
                    </span>
                    <span class="pull-right">
                      <el-button type="primary" class="inline" size="mini"
                                 @click.stop="addItem=true,activeItem=itemKey">
                        <i class="fa fa-plus"></i>
                        {{ $lang[$store.state.lang].buttons.addColumn }}
                      </el-button>
                      <el-button type="danger" size="mini" class="m-r-md"
                                 @click="onDeleteInput(configuration.items, itemKey)">
                          <i class="fa fa-remove"></i>
                          {{ $lang[$store.state.lang].buttons.delete }}
                      </el-button>
                    </span>
                  </template>
                  <!-- 每个实体配置 -->
                  <el-form-item>
                    <h4 class="inline m-r-sm">{{ $lang[$store.state.lang].columns.name }}</h4>
                    <el-input
                      v-model="item['name']" class="inline" :placeholder="$lang[$store.state.lang].columns.name"
                      size="small"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <div v-for="(attr, attrKey, attrIndex) in item.attrs" :key="attrKey" class="item">
                      <el-button class="inline inline-first m-r-sm" type="primary" size="mini">
                        {{ attrIndex + 1 }}
                      </el-button>
                      <span class="inline inline-second">{{ attrKey }}</span>
                      <el-input
                        v-model="attr['value']" class="inline inline-third"
                        :placeholder="$lang[$store.state.lang].columns.value"
                        size="small"></el-input>
                      <el-input
                        v-model="attr['in_processor']" class="inline inline-fourth"
                        :placeholder="$lang[$store.state.lang].columns.inProcessor"
                        size="small"></el-input>
                      <el-input
                        v-model="attr['out_processor']" class="inline inline-fifth"
                        :placeholder="$lang[$store.state.lang].columns.outProcessor"
                        size="small"></el-input>
                      <el-button type="danger" size="mini" class="m-r-md"
                                 @click="onDeleteInput(item.attrs, attrKey)">
                        <i class="fa fa-remove"></i>
                        {{ $lang[$store.state.lang].buttons.delete }}
                      </el-button>
                    </div>
                  </el-form-item>
                </el-collapse-item>
              </el-collapse>
              <!-- 提取实体结束 -->

              <!-- 爬虫配置 -->
              <h4 class="inline m-v-md">{{ $lang[$store.state.lang].titles.listSpider }}</h4>

              <el-button type="primary" class="inline" size="mini"
                         @click="onAddSpider">
                <i class="fa fa-plus"></i>
                {{ $lang[$store.state.lang].buttons.addSpider }}
              </el-button>

              <el-collapse v-model="activeSpider" accordion v-if="configuration.spiders.length">

                <el-collapse-item v-for="(spider, spiderKey, spiderIndex) in configuration.spiders" :name="spiderKey"
                                  :key="spiderKey">
                  <spider :projectName="projectName" :spider="spider" :spiderKey="spiderKey"
                          :items="configuration.items" :onAddInput="onAddInput"
                          :onDeleteInput="onDeleteInput"></spider>
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
                    {{ $lang[$store.state.lang].buttons.delete }}
                    </el-button>
                    </span>
                  </template>
                </el-collapse-item>
              </el-collapse>
              <!-- 爬虫配置结束 -->
            </el-form>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  import browser from 'pages/project/browser'
  import spider from 'pages/project/spider'
  import ElCollapseItem from "../../../node_modules/element-ui/packages/collapse/src/collapse-item";
  import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item";
  import ElInput from "../../../node_modules/element-ui/packages/input/src/input";
  import ElButton from "../../../node_modules/element-ui/packages/button/src/button";
  export default{
    data(){
      return {
        error: null,
        showBrowser: false,
        savingProject: false,
        projectName: this.$route.params.name,
        projectDescription: null,
        projectGeneratedAt: null,
        projectBuiltAt: null,
        activeSpider: 0,
        accordion: false,
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
      ElButton,
      ElInput,
      ElFormItem,
      ElCollapseItem,
      panelTitle,
      bottomToolBar,
      browser,
      spider
    },
    created() {
      this.getProject()
    },
    methods: {
      hideBrowser(){
        this.showBrowser = false
      },
      getProject() {
        this.$fetch.apiProject.projectGetConfiguration({
          name: this.projectName
        }).then(({data: data}) => {
          this.projectDescription = data.description
          this.projectGeneratedAt = data.generated_at
          this.projectBuiltAt = data.built_at
          this.configuration = data.configuration || this.configuration
          this.loadData = false
        }).catch(() => {
        })
      },
      saveProject() {
        this.savingProject = true
        this.$fetch.apiProject.projectSaveConfiguration({
          name: this.projectName
        }, {
          configuration: this.configuration
        }).then(({data: {status: status, message: message}}) => {
          if (status == '1') {
            this.$message.success(this.$lang[this.$store.state.lang].messages.successSave)
          } else {
            this.error = message
          }
          this.savingProject = false
        }).catch(({data: {message: message}}) => {
          this.$message.error(this.$lang[this.$store.state.lang].messages.errorSave)
          this.savingProject = false
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
      onAddInput(array, arg = '') {
        if (!array) {
          array = []
        }
        array.push(arg)
      },
      onAddItem() {
        this.$set(this.configuration.items[this.activeItem]['attrs'], this.item, {})
        this.addItem = false
      },
      onGenerate() {
        if (this.projectBuiltAt) {
          this.$confirm(this.$lang[this.$store.state.lang].messages.reGenerate, this.$lang[this.$store.state.lang].buttons.confirm, {
            confirmButtonText: this.$lang[this.$store.state.lang].buttons.yes,
            cancelButtonText: this.$lang[this.$store.state.lang].buttons.no,
            type: 'warning'
          }).then(() => {
            this.generateProject()
          }).catch(() => {
            this.$message.error(this.$lang[this.$store.state.lang].messages.errorDelete)
          })
        } else {
          this.generateProject()
        }
      },
      onAddSpider() {
        this.onAddInput(this.configuration.spiders,
          {
            name: null,
            custom_settings: [],
            code: {},
            extractors: [],
            rules: [],
            proxy: {},
            cookies: {},
            storage: {
              mysql: {
                enable: false,
                tables: []
              },
              mongodb: {
                enable: false,
                collections: []
              }
            },
            start_urls: {
              mode: 'list',
              list: [],
              code: null,
              file: null
            },
            attrs: [],
            allowed_domains: []
          })
      }
    },
//    watch: {
//      configuration: {
//        handler() {
//          this.saveProject()
//        },
//        deep: true
//      }
//    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  #error-message {
    position: fixed;
    bottom: 40px;
    z-index: 100;
    width: 500px;
    right: 80px;
    font-size: 13px;
  }

  .inline {
    display: inline-block;
    max-width: calc(100% - 80px);
  }

  .inline-short {
    max-width: 100px !important;
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
    .el-textarea {
      textarea {
        width: 300px;
      }
    }
    .extractor-rule {
      .inline-first {
        width: 100px;
      }
      .inline-second {
        width: calc(100% - 380px);
      }
      .inline-third, .inline-fourth, .inline-fifth {
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

  #save-project {
    position: fixed;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    right: 20px;
    bottom: 20px;
    z-index: 1000;
    font-size: 12px;
  }
</style>
