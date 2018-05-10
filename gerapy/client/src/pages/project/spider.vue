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

    <!-- 类属性开始 -->
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
    <!-- 类属性结束 -->

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
      <rules :rules="spider.rules" :onAddInput="onAddInput" :onDeleteInput="onDeleteInput"></rules>
    </el-form-item>
    <!-- 爬取规则结束 -->

    <!-- 提取规则开始 -->
    <el-form-item>
      <extractors :extractors="spider.extractors" :items="items" :onAddInput="onAddInput" :onDeleteInput="onDeleteInput"></extractors>
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
  import rules from 'pages/project/rules'
  import extractors from 'pages/project/extractors'
  import test from 'pages/project/test'
  export default {
    name: 'Spider',
    data() {
      return {
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
      rules,
      extractors,
      test
    },

  }
</script>
