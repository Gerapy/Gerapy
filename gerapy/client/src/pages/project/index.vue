<template>
  <el-row>
    <el-col :span="3">
      <div class="panel">
        <panel-title title="项目目录">
        </panel-title>
        <div class="panel-body">
          <el-tree :data="tree" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
        </div>
      </div>
    </el-col>
    <el-col :span="21">
      <div class="panel m-l-md">
        <panel-title title="代码">
          <el-button @click="saveCode" size="small" type="success">
            <i class="fa fa-check"></i>
            保存
          </el-button>
          <el-button @click="deleteFile" size="small" type="danger">
            <i class="fa fa-close"></i>
            删除
          </el-button>
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

  // Mode

  import 'codemirror/mode/css/css'
  import 'codemirror/mode/dockerfile/dockerfile'
  import 'codemirror/mode/htmlmixed/htmlmixed'
  import 'codemirror/mode/markdown/markdown'
  import 'codemirror/mode/php/php'
  import 'codemirror/mode/python/python'
  import 'codemirror/mode/sass/sass'
  import 'codemirror/mode/javascript/javascript'
  import 'codemirror/mode/sql/sql'
  import 'codemirror/mode/vue/vue'

  export default{
    data(){
      return {
        clientData: null,
        //请求时的loading效果
        loadData: true,
        //批量选择数组
        batchSelect: [],
        tree: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        activeNode: null,
        code: '',
        modeMap: {
          'py': 'text/x-python',
          'js': 'text/javascript',
          'html': 'text/html',
          'vue': 'text/x-vue',
          'md': 'text/x-markdown',
          'scss': 'text/x-sass',
          'css': 'text/x-css',
          'php': 'application/x-httpd-php',
        },
        editorOptions: {
          tabSize: 4,
          mode: 'text/javascript',
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
      this.getProjectTree()
    },
    methods: {
      getProjectTree() {
        // 获取目录树
        this.$fetch.apiProject.projectTree()
          .then(({data: tree}) => {
            console.log(tree)
            this.tree = tree
          })
          .catch(() => {
          })
      },
      handleNodeClick(data) {
        this.activeNode = data
        this.changeCode(data)
      },
      // 呈现代码
      changeCode(data) {
        // 获取后缀
        let group = this.activeNode.label.split('.')
        let extension = group[group.length - 1]
        // 设置Mode
        this.editorOptions.mode = this.modeMap[extension]
        // 加载文件
        if (!data.children) {
          this.$fetch.apiProject.projectFile(
            data
          ).then(({data: code}) => {
            this.code = code
          }).catch(() => {
            this.$message.error('加载失败')
          })
        }
      },
      // 保存代码
      saveCode(){
        this.onEditorCodeChange(this.code, () => {
          this.$message.success('保存成功')
        })
      },
      deleteFile() {
        this.$confirm('此操作将批量删除选择数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // 删除文件
          this.$fetch.apiProject.projectFileDelete({
            path: this.activeNode['path'],
            label: this.activeNode['label']
          }).then(() => {
            this.$message.success('删除成功')
            this.getProjectTree()
          }).catch(() => {
            this.$message.error('删除失败')
          })
        }).catch((error) => {
          console.log(error)
        })
      },
      onEditorCodeChange(code, callback) {
        //更新文件
        this.$fetch.apiProject.projectFileUpdate({
          code: code,
          path: this.activeNode['path'],
          label: this.activeNode['label']
        }).then(() => {
          if (callback) {
            callback()
          }
        }).catch(() => {
          this.$message.error('修改失败')
        })
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
