<template>
  <div class="panel" id="browser" v-show="show">
    <panel-title :title="$lang.titles.browser">
      <el-button type="primary" size="mini" @click="createProjectDialog = true">
        <i class="fa fa-close" @click="hide"></i>
      </el-button>
    </panel-title>
    <div class="panel-body">
      <el-form :inline="true">
        <el-form-item :label="$lang.columns.url">
          <el-input
            v-model="url"
            :placeholder="$lang.columns.url"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="render" size="small"
            >{{ $lang.buttons.render }}
          </el-button>
        </el-form-item>
      </el-form>
      <el-row class="m-b-sm">
        <el-col :span="1">
          <el-button type="primary" size="mini">XPath</el-button>
        </el-col>
        <el-col :span="18">
          {{ xpathSelector }}
        </el-col>
        <el-col :span="1">
          <el-button
            type="primary"
            size="mini"
            v-clipboard:copy="xpathSelector"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError"
            >{{ $lang.buttons.copy }}
          </el-button>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="1">
          <el-button type="primary" size="mini">CSS</el-button>
        </el-col>
        <el-col :span="18">
          {{ cssSelector }}
        </el-col>
        <el-col :span="1">
          <el-button
            type="primary"
            size="mini"
            v-clipboard:copy="cssSelector"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError"
            >{{ $lang.buttons.copy }}
          </el-button>
        </el-col>
      </el-row>
      <div class="m-t-md" id="render-result">
        <iframe
          sandbox="allow-same-origin allow-scripts"
          scrolling="yes"
          width="100%"
          :src="src"
          class="iframe-box"
          id="iframe-box"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script>
import PanelTitle from "../../components/PanelTitle";
import $ from "jquery";
import { Base64 } from "js-base64";

export default {
  props: {
    show: Boolean,
  },
  data() {
    return {
      url: "http://www.baidu.com",
      src: null,
      cssSelector: null,
      xpathSelector: null,
      gerapy_selected: [],
    };
  },
  methods: {
    onCopy() {
      this.$message.success(this.$store.getters.$lang.messages.successCopy);
    },
    onError() {
      this.$message.error(this.$store.getters.$lang.messages.errorCopy);
    },
    hide() {
      this.$emit("hide", false);
    },
    render() {
      this.src =
        this.$store.state.url.util.render + "?url=" + Base64.encode(this.url);
      let iframe = document.getElementById("iframe-box");
      iframe.onload = () => {
        iframe.contentDocument.onclick = () => {
          this.cssSelector = $("#iframe-box")[0].contentWindow.cssSelector;
          this.xpathSelector = $("#iframe-box")[0].contentWindow.xpathSelector;
        };
      };
    },
  },
  components: {
    PanelTitle,
  },
};
</script>

<style lang="scss">
$height: 600px;
#browser {
  position: fixed;
  top: 100px;
  min-width: 1175px;
  min-height: $height;
  box-shadow: 10px 10px 15px #eee;
  #render-result {
    width: 100%;
    height: $height;
    overflow-y: scroll;
    border: 1px dashed #ccc;
  }
}

.iframe-box {
  min-height: 500px;
}
</style>
