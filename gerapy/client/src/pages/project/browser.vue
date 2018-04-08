<template>

  <div class="panel" id="browser">
    <panel-title title="Browser"></panel-title>
    <div class="panel-body">
      <div>
        <el-input v-model="url" placeholder="请输入链接"></el-input>
        <el-button type="success" plain @click="render">渲染</el-button>
      </div>
      <div v-html="html" id="render-result" @click="select">
      </div>
    </div>
  </div>
</template>

<script>
  import xpathGenerator from 'assets/js/generator.xpath'
  import cssGenerator from 'assets/js/generator.css'
  import {panelTitle, bottomToolBar} from 'components'
  export default{
    data(){
      return {
        url: 'http://www.baidu.com',
        html: '<p>ahahhaha</p><h1>6666</h1>'
      }
    },
    created() {
      console.log('666')
      console.log(xpathGenerator)
      console.log(cssGenerator)
    },
    methods: {
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
          element.style.borderStyle = ''
          element.style.borderColor = ''
        }
        event.target.className += ' gerapy-selected'
        event.target.style.borderStyle = 'solid'
        event.target.style.borderColor = 'red'
        var cssSelector = cssGenerator.getSelector(event.target)
        var xpathSelector = xpathGenerator.getElementXPath(event.target)
        console.log('css-selector', cssSelector)
        console.log('xpath-selector', xpathSelector)
      }
    },
    components: {
      panelTitle,
      bottomToolBar,
    },

  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  #browser {
    position: fixed;
    top: 100px;
    width: 100%;
    #render-result {
      max-width: 1000px;
      max-height: 600px;
      overflow: hidden;
    }
  }

</style>
