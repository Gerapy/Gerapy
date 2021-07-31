<template>
  <div class="label-left">
    <!-- 名称开始 -->
    <el-form-item :label="$lang.columns.name" class="inline">
      <el-input
        v-model="spider.name"
        size="small"
        :placeholder="$lang.columns.name"
      ></el-input>
    </el-form-item>
    <!-- 名称结束 -->

    <!-- 起始链接开始 -->
    <el-form-item :label="$lang.columns.startUrls">
      <el-form-item>
        <el-radio class="radio" v-model="spider.start_urls.mode" label="list">
          {{ $lang.columns.list }}
        </el-radio>

        <el-radio class="radio" v-model="spider.start_urls.mode" label="code">
          {{ $lang.columns.code }}
        </el-radio>
      </el-form-item>
      <div v-if="spider.start_urls.mode === 'list'">
        <el-form-item>
          <el-button
            type="primary"
            v-if="spider.start_urls.mode === 'list'"
            class="inline"
            size="mini"
            @click="onAddInput(spider.start_urls.list)"
          >
            <i class="fa fa-plus"></i>
            {{ $lang.buttons.addUrl }}
          </el-button>
        </el-form-item>
        <div
          v-for="(url, urlIndex) in spider.start_urls.list"
          :key="'url' + urlIndex"
        >
          <el-form-item class="inline" label-width="0">
            <el-input
              v-model="spider.start_urls.list[urlIndex]"
              class="inline"
              :placeholder="$lang.columns.startUrls"
              :style="{ width: '600px' }"
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item class="inline" label-width="0">
            <el-button
              type="danger"
              size="mini"
              @click="$delete(spider.start_urls.list, urlIndex)"
            >
              <i class="fa fa-remove"></i>
              {{ $lang.buttons.delete }}
            </el-button>
          </el-form-item>
        </div>
      </div>
      <div v-if="spider.start_urls.mode === 'code'">
        <el-form-item label-width="0">
          <code-editor v-model="spider.start_urls.code"></code-editor>
        </el-form-item>
      </div>
    </el-form-item>
    <!-- 起始链接结束 -->

    <!-- 合法域名 -->
    <el-form-item
      :label="$lang.columns.allowedDomains"
      :style="{ marginBottom: '15px' }"
    >
      <el-form-item>
        <el-button
          type="primary"
          class="inline"
          size="mini"
          @click="onAddInput(spider.allowed_domains)"
        >
          <i class="fa fa-plus"></i>
          {{ $lang.buttons.addDomain }}
        </el-button>
      </el-form-item>
      <div
        v-for="(value, key) in spider.allowed_domains"
        :key="'spider_allowed_domains' + key"
      >
        <el-form-item class="inline" :style="{ width: '400px' }">
          <el-input
            v-model="spider.allowed_domains[key]"
            class="inline"
            :placeholder="$lang.columns.allowedDomains"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item class="inline">
          <el-button
            type="danger"
            size="mini"
            @click="$delete(spider.allowed_domains, key)"
          >
            <i class="fa fa-remove"></i>
            {{ $lang.buttons.delete }}
          </el-button>
        </el-form-item>
      </div>
    </el-form-item>
    <!-- 合法域名结束 -->

    <parser :projectName="projectName" :spider="spider"></parser>

    <!-- 类属性开始 -->
    <el-form-item :label="$lang.columns.classAttrs">
      <el-form-item>
        <el-button
          type="primary"
          class="inline"
          size="mini"
          @click="onAddInput(spider.attrs, { key: null, value: null })"
        >
          <i class="fa fa-plus"></i>
          {{ $lang.buttons.addAttr }}
        </el-button>
      </el-form-item>
      <div
        v-for="(value, key) in spider.attrs"
        :key="'spider_attrs' + key"
        class="label-center"
      >
        <el-form-item class="inline" :label="$lang.columns.attrName">
          <el-input
            v-model="value['key']"
            class="inline inline-short"
            :placeholder="$lang.columns.attrName"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item class="inline" :label="$lang.columns.attrValue">
          <el-input
            v-model="value['value']"
            class="inline inline-long"
            :placeholder="$lang.columns.attrValue"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item class="inline">
          <el-button
            type="danger"
            size="mini"
            @click="$delete(spider.attrs, key)"
          >
            <i class="fa fa-remove"></i>
            {{ $lang.buttons.delete }}
          </el-button>
        </el-form-item>
      </div>
    </el-form-item>
    <!-- 类属性结束 -->

    <!-- 爬取规则开始 -->
    <el-form-item>
      <rules
        :rules="spider.rules"
        :onAddInput="onAddInput"
        :onDeleteInput="onDeleteInput"
      ></rules>
    </el-form-item>
    <!-- 爬取规则结束 -->

    <!-- 提取规则开始 -->
    <el-form-item>
      <extractors
        :extractors="spider.extractors"
        :items="items"
        :onAddInput="onAddInput"
        :onDeleteInput="onDeleteInput"
      ></extractors>
    </el-form-item>
    <!-- 提取规则结束 -->

    <!-- 存储开始 -->
    <el-form-item>
      <storage
        :storage="spider.storage"
        :items="items"
        :onAddInput="onAddInput"
        :onDeleteInput="onDeleteInput"
      ></storage>
    </el-form-item>
    <!-- 存储结束 -->

    <!-- 代理开始 -->
    <!--<el-form-item>-->
    <!--<proxy :proxy="spider.proxy" :onAddInput="onAddInput" :onDeleteInput="onDeleteInput"></proxy>-->
    <!--</el-form-item>-->
    <!-- 代理结束 -->

    <!-- Cookies开始 -->
    <!--<el-form-item>-->
    <!--<cookies :cookies="spider.cookies" :onAddInput="onAddInput" :onDeleteInput="onDeleteInput"></cookies>-->
    <!--</el-form-item>-->
    <!-- Cookies结束 -->

    <!-- 配置项开始 -->
    <el-form-item
      :label="$lang.columns.customSettings"
      :style="{ marginBottom: '15px' }"
    >
      <el-button
        type="primary"
        class="inline"
        size="mini"
        @click="onAddInput(spider.custom_settings, { key: null, value: null })"
      >
        <i class="fa fa-plus"></i>
        {{ $lang.buttons.addAttr }}
      </el-button>
      <div
        v-for="(value, key) in spider.custom_settings"
        :key="'spider_custom_settings' + key"
        class="label-center"
      >
        <el-form-item class="inline" :label="$lang.columns.attrName">
          <el-input
            v-model="value['key']"
            class="inline inline-medium"
            :placeholder="$lang.columns.attrName"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item class="inline" :label="$lang.columns.attrValue">
          <el-input
            v-model="value['value']"
            class="inline inline-long"
            :placeholder="$lang.columns.attrValue"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item class="inline">
          <el-button
            type="danger"
            size="mini"
            @click="onDeleteInput(spider.custom_settings, key)"
          >
            <i class="fa fa-remove"></i>
            {{ $lang.buttons.delete }}
          </el-button>
        </el-form-item>
      </div>
    </el-form-item>
    <!-- 配置项结束 -->

    <el-form-item
      :label="$lang.columns.innerCode"
      :style="{ marginBottom: '15px' }"
    >
      <code-editor v-model="spider.code.in_class"></code-editor>
    </el-form-item>

    <el-form-item :label="$lang.columns.outerCode">
      <!--<el-input type="textarea" v-model="spider.code.out_class" size="small"-->
      <!--:placeholder="$lang.columns.innerCode" :rows="4"></el-input>-->
      <code-editor v-model="spider.code.out_class"></code-editor>
    </el-form-item>
  </div>
</template>

<script>
import Rules from "./Rules";
import Extractors from "./Extractors";
import Storage from "./Storage";
import Parser from "./Parser";
import Proxy from "./Proxy";
import Cookies from "./Cookies";
import CodeEditor from "../../components/CodeEditor";

export default {
  name: "Spider",
  props: {
    projectName: {
      type: String,
    },
    spider: {
      type: Object,
    },
    spiderKey: {
      type: Number,
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
  components: {
    Rules,
    Extractors,
    Storage,
    Parser,
    Proxy,
    Cookies,
    CodeEditor,
  },
};
</script>
