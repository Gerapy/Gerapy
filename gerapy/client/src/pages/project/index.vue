<template>
  <el-row>
    <el-col :span="3">
      <div class="panel">
        <panel-title title="项目目录">
        </panel-title>
        <div class="panel-body">
          <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
        </div>
      </div>
    </el-col>
    <el-col :span="21">
      <div class="panel m-l-md">
        <panel-title title="代码">
        </panel-title>
        <div class="panel-body">
          <codemirror v-model="code" :options="editorOptions" @change="onEditorCodeChange">
          </codemirror>
        </div>
      </div>
    </el-col>
  </el-row>
</template>
<script type="text/javascript">
  import {panelTitle, bottomToolBar} from 'components'
  import {codemirror, CodeMirror} from 'vue-codemirror'

  // Key Map
  import 'codemirror/mode/clike/clike'
  import 'codemirror/addon/edit/matchbrackets'
  import 'codemirror/addon/comment/comment'
  import 'codemirror/addon/dialog/dialog'
  import 'codemirror/addon/dialog/dialog.css'
  import 'codemirror/addon/search/searchcursor'
  import 'codemirror/addon/search/search'
  import 'codemirror/keymap/sublime'

  // CloseBrackets
  import 'codemirror/addon/edit/closebrackets'

  // Active Line
  import 'codemirror/addon/selection/active-line'

  // StyleSelectedText
  import 'codemirror/addon/selection/mark-selection'
  import 'codemirror/addon/search/searchcursor'

  // Hint
  import 'codemirror/addon/hint/show-hint'
  import 'codemirror/addon/hint/show-hint.css'
  import 'codemirror/addon/hint/anyword-hint'

  // foldGutter
  import 'codemirror/addon/fold/foldgutter.css'
  import 'codemirror/addon/fold/brace-fold'
  import 'codemirror/addon/fold/comment-fold'
  import 'codemirror/addon/fold/foldcode'
  import 'codemirror/addon/fold/foldgutter'
  import 'codemirror/addon/fold/indent-fold'
  import 'codemirror/addon/fold/markdown-fold'
  import 'codemirror/addon/fold/xml-fold'

  export default{
    data(){
      return {
        clientData: null,
        //请求时的loading效果
        loadData: true,
        //批量选择数组
        batchSelect: [],
        data: [{
          label: '一级 1',
          children: [{
            label: '二级 1-1',
            children: [{
              label: '三级 1-1-1'
            }]
          }]
        }, {
          label: '一级 2',
          children: [{
            label: '二级 2-1',
            children: [{
              label: '三级 2-1-1'
            }]
          }, {
            label: '二级 2-2',
            children: [{
              label: '三级 2-2-1'
            }]
          }]
        }, {
          label: '一级 3',
          children: [{
            label: '二级 3-1',
            children: [{
              label: '三级 3-1-1'
            }]
          }, {
            label: '二级 3-2',
            children: [{
              label: '三级 3-2-1'
            }]
          }]
        }],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        code: 'const a = 10',
        editorOptions: {
          tabSize: 4,
          mode: 'text/x-python',
          theme: 'monokai',
          lineNumbers: true,
          styleActiveLine: true,
          line: true,
          // sublime、emacs、vim三种键位模式
          keyMap: 'sublime',
          // 按键映射，比如Ctrl键映射autocomplete，autocomplete是hint代码提示事件
          extraKeys: {
            'Tab': 'autocomplete'
          },
          // 代码折叠
          foldGutter: true,
          gutters: [
            'CodeMirror-linenumbers', 'CodeMirror-foldgutter'
          ],
          // 选中文本自动高亮，及高亮方式
          styleSelectedText: true,
          highlightSelectionMatches: {
            showToken: /\w/,
            annotateScrollbar: true
          },
        }
      }
    },
    components: {
      panelTitle,
      bottomToolBar,
      codemirror
    },
    created(){

    },
    methods: {
      handleNodeClick(data) {
        console.log(data);
      },
      onEditorCodeChange(newCode) {
        console.log('this is new code', newCode)
      }
    }
  }
</script>

<style lang="scss" type="text/scss" rel="stylesheet/scss">
  .CodeMirror {
    font-size: 16px;
    min-height: 600px;
  }
</style>
