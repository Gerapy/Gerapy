<template>

  <div class="panel" id="browser" v-if="show">
    <panel-title title="Browser">
      <el-button type="primary" size="mini" @click="createProjectDialog=true">
        <i class="fa fa-close" @click="hide"></i>
      </el-button>
    </panel-title>
    <div class="panel-body">
      <el-form :inline="true">
        <el-form-item label="链接">
          <el-input v-model="url" placeholder="请输入链接" size="small"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="render" size="small">加载</el-button>
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
          <el-button type="primary" size="mini" @click="copy(xpathSelector)">复制</el-button>
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
          <el-button type="primary" size="mini" @click="copy(cssSelector)">复制</el-button>
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
      }
    },
    created() {
      console.log('666')
      console.log(xpathGenerator)
      console.log(cssGenerator)
    },
    methods: {
      hide(){
        this.show = false
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
        let selected = document.getElementsByClassName('gerapy-selected')
        for (let index = 0; index < selected.length; index++) {
          let element = selected[index]
          element.classList.remove('gerapy-selected')
          element.style.borderStyle = null
          element.style.borderColor = null
        }
        event.target.className += ' gerapy-selected'
        event.target.style.borderStyle = 'solid'
        event.target.style.borderColor = 'red'
        this.cssSelector = cssGenerator.getSelector(event.target)
        this.xpathSelector = xpathGenerator.getElementXPath(event.target)
        console.log('css-selector', this.cssSelector)
        console.log('xpath-selector', this.xpathSelector)
      },
      copy(value) {
        console.log(value)
      }
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
