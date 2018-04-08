<template>
  <div>
    <div class="panel">
      <el-button @click="showBrowser=true" type="primary" class="show-browser">
        <i class="fa fa-edge"></i>
      </el-button>
      <panel-title :title="$lang[$store.state.lang].titles.configureProject">
        <el-button type="primary" size="mini" @click="saveProject()">
          <i class="fa fa-check"></i>
          {{ $lang[$store.state.lang].buttons.save }}
        </el-button>
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
                <el-button type="primary" class="inline" size="mini"
                           @click="onGenerate(projectName)">
                  <i class="fa fa-magic"></i>
                  {{ $lang[$store.state.lang].buttons.generate }}
                </el-button>
              </el-form-item>

              <!-- 提取实体 -->
              <el-form-item>
                <h4 class="inline">{{ $lang[$store.state.lang].titles.items }}</h4>
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
                <!-- 添加规则配置浮窗 -->
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
              </el-form-item>
              <!-- 提取实体结束 -->

              <div class="hr-line-dashed"></div>

              <h4 class="inline m-b-sm">{{ $lang[$store.state.lang].titles.listSpider }}</h4>

              <el-button type="primary" class="inline" size="mini"
                         @click="onAddInput(configuration.spiders, {name:null, custom_settings:null, code:{}, extractors: [], rules: [], storage: {mysql: {enable: false}}, start_urls: {mode: 'list', list:[], code: null, file: null}, attrs: [], allowed_domains: []})">
                <i class="fa fa-plus"></i>
                {{ $lang[$store.state.lang].buttons.addSpider }}
              </el-button>

              <el-collapse v-model="activeSpider" accordion v-if="configuration.spiders.length">
                <el-collapse-item v-for="(spider, spiderKey, spiderIndex) in configuration.spiders" :name="spiderKey"
                                  :key="spiderKey">
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
                        <div v-if="Object.keys(rule).length">
                          <div v-for="(value, key, index) in rule" :key="value">
                            <h5 class="inline m-v-sm">{{ key }}</h5>
                            <el-button type="primary" size="mini" class="inline" v-if="value instanceof Array"
                                       @click="onAddInput(spider.rules[ruleKey][key])">
                              <i class="fa fa-plus"></i>
                              {{ $lang[$store.state.lang].buttons.add }}
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
                                    {{ $lang[$store.state.lang].buttons.delete }}
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
                                  {{ $lang[$store.state.lang].buttons.delete }}
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
                                  {{ $lang[$store.state.lang].buttons.delete }}
                                </el-button>
                              </div>
                              <!-- 布尔类型 -->
                            </el-form-item>
                          </div>
                        </div>
                        <div v-else>
                          <h5>{{ $lang[$store.state.lang].messages.addColumn }}</h5>
                        </div>
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
                          {{ $lang[$store.state.lang].buttons.cancel
                          }}
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
                        <!-- 每条规则标题及操作配置 -->
                        <el-form-item>
                          <h5 class="inline m-v-sm">{{ $lang[$store.state.lang].titles.callback }}</h5>
                          <el-input
                            v-model="extractor.callback" class="inline"
                            :placeholder="$lang[$store.state.lang].titles.callback"
                            size="small">
                          </el-input>
                        </el-form-item>
                        <el-form-item>
                          <h5 class="inline m-v-sm">{{ $lang[$store.state.lang].titles.item }}</h5>
                          <el-select v-model="extractor.item" :placeholder="$lang[$store.state.lang].titles.item"
                                     size="small" class="inline inline-first">
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
                                {{ $lang[$store.state.lang].buttons.addRule }}
                              </el-button>
                              <div v-for="(v, k, i) in value" :key="k" class="extractor-rule">
                                <el-select v-model="v['method']" :placeholder="$lang[$store.state.lang].columns.method"
                                           size="small"
                                           class="inline inline-first">
                                  <el-option
                                    v-for="item in extractorMethods"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                  </el-option>
                                </el-select>
                                <el-input
                                  v-model="v['arg']" class="inline inline-second"
                                  :placeholder="$lang[$store.state.lang].columns.value"
                                  size="small"></el-input>
                                <el-input
                                  v-model="v['processor']" class="inline inline-third"
                                  :placeholder="$lang[$store.state.lang].columns.processors"
                                  size="small"></el-input>
                                <el-input
                                  v-model="v['re']" class="inline inline-fourth"
                                  :placeholder="$lang[$store.state.lang].columns.regex"
                                  size="small"></el-input>
                                <el-button type="danger" size="mini"
                                           @click="onDeleteInput(extractor.attrs, key, k)">
                                  <i class="fa fa-remove"></i>
                                  {{ $lang[$store.state.lang].buttons.delete }}
                                </el-button>
                              </div>
                            </div>
                          </div>
                          <div v-else>
                            <h5>{{ $lang[$store.state.lang].messages.addColumn }}</h5>
                          </div>
                        </el-form-item>
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
                          placeholder="$lang[$store.state.lang].columns.port"
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
                </el-collapse-item>
              </el-collapse>
            </el-form>
          </el-col>
        </el-row>
      </div>
    </div>
    <browser :show="showBrowser"></browser>
  </div>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  import browser from 'pages/project/browser'
  import ElCollapseItem from "../../../node_modules/element-ui/packages/collapse/src/collapse-item";
  import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item";
  import ElInput from "../../../node_modules/element-ui/packages/input/src/input";
  import ElButton from "../../../node_modules/element-ui/packages/button/src/button";
  export default{
    data(){
      return {
        showBrowser: false,
        projectName: this.$route.params.name,
        projectDescription: null,
        projectGeneratedAt: null,
        projectBuiltAt: null,
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
      browser
    },
    created() {
      this.getProject()
    },
    methods: {
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
        this.$fetch.apiProject.projectSaveConfiguration({
          name: this.projectName
        }, {
          configuration: this.configuration
        }).then(({data: data}) => {
          this.$message.success(this.$lang[this.$store.state.lang].messages.successSave)
        }).catch(() => {
          this.$message.error(this.$lang[this.$store.state.lang].messages.errorSave)
        })
      },
      generateProject() {
        this.$fetch.apiProject.projectGenerate({
          name: this.projectName
        }).then(({data: data}) => {
          this.$message.success(this.$lang[this.$store.state.lang].messages.successGenerate)
          this.getProject()
        }).catch(() => {
          this.$message.error(this.$lang[this.$store.state.lang].messages.errorGenerate)
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

  #project-browser {
    position: fixed;
    top: 100px;
    width: 80%;
  }

  .show-browser {
    position: fixed;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    right: 20px;
    bottom: 20px;
    z-index: 1000;
  }
</style>
