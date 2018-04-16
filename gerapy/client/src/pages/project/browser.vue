<template>
  <div class="panel" id="browser" v-if="show">
    <panel-title :title="$lang[$store.state.lang].columns.url">
      <el-button type="primary" size="mini" @click="createProjectDialog=true">
        <i class="fa fa-close" @click="hide"></i>
      </el-button>
    </panel-title>
    <div class="panel-body">
      <el-form :inline="true">
        <el-form-item :label="$lang[$store.state.lang].columns.url">
          <el-input v-model="url" placeholder="请输入链接" size="small"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="render" size="small">{{ $lang[$store.state.lang].buttons.render }}
          </el-button>
        </el-form-item>
      </el-form>
      <el-row class="m-b-sm">
        <el-col span="1">
          <el-button type="primary" size="mini">XPath</el-button>
        </el-col>
        <el-col span="10">
          {{ xpathSelector }}
        </el-col>
        <el-col span="1">
          <el-button type="primary" size="mini" v-clipboard:copy="xpathSelector" v-clipboard:success="onCopy"
                     v-clipboard:error="onError">{{ $lang[$store.state.lang].buttons.copy }}
          </el-button>
        </el-col>
      </el-row>
      <el-row>
        <el-col span="1">
          <el-button type="primary" size="mini">CSS</el-button>
        </el-col>
        <el-col span="10">
          {{ cssSelector }}
        </el-col>
        <el-col span="1">
          <el-button type="primary" size="mini" v-clipboard:copy="cssSelector" v-clipboard:success="onCopy"
                     v-clipboard:error="onError">{{ $lang[$store.state.lang].buttons.copy }}
          </el-button>
        </el-col>
      </el-row>
      <div v-html="html" class="m-t-md" id="render-result" @click="select">
      </div>
    </div>
  </div>
</template>

<script>
  import xpathGenerator from 'assets/js/generator.xpath'
  import cssGenerator from 'assets/js/generator.css'
  import {panelTitle, bottomToolBar} from 'components'
  import ElRow from "element-ui/packages/row/src/row";
  import ElCol from "element-ui/packages/col/src/col";
  import Vue from 'vue';
  import VueClipboard from 'vue-clipboard2';
  Vue.use(VueClipboard)

  export default{
    props: {
      show: Boolean
    },
    data(){
      return {
        url: 'http://www.baidu.com',
        html: null,
        cssSelector: null,
        xpathSelector: null,
        gerapy_selected: [],
      }
    },
    created() {
      console.log(xpathGenerator)
      console.log(cssGenerator)
    },
    methods: {
      onCopy: function (e) {
        this.$message.success(this.$lang[this.$store.state.lang].messages.successCopy)
      },
      onError: function (e) {
        this.$message.error(this.$lang[this.$store.state.lang].messages.errorCopy)
      },
      hide(){
        // this.show = false
        this.$emit('hide', false)
      },
      render() {
        this.$fetch.apiUtil.render({
          url: this.url
        }).then(({data: {data: html}}) => {
          this.html = html
        }).catch(() => {
          this.$message.error(this.$lang[this.$store.state.lang].messages.errorLoad)
        })
      },
      select(event) {
        this.gerapy_selected.forEach(element => {
          element.target.style.borderStyle = ''
          element.target.style.borderColor = ''
        });
        this.gerapy_selected = []
        event.target.style.borderStyle = 'solid'
        event.target.style.borderColor = 'red'
        this.gerapy_selected.push(event)
        this.cssSelector = cssGenerator.getSelector(event.target)
        this.xpathSelector = xpathGenerator.getElementXPath(event.target)
        console.log('css-selector', this.cssSelector)
        console.log('xpath-selector', this.xpathSelector)
        if (event.target.href) {
          console.log(event.target.href)
          event.target.href = '#'
        }
      },
    },
    components: {
      ElCol,
      ElRow,
      panelTitle,
      bottomToolBar,
    },

  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  $height: 600px;
  #browser {
    position: fixed;
    top: 100px;
    min-width: 1175px;
    min-height: $height;
    box-shadow: 10px 10px 15px #EEE;
    #render-result {
      width: 100%;
      height: $height;
      overflow-y: scroll;
      border: 1px dashed #CCC;
    }
  }

</style>
