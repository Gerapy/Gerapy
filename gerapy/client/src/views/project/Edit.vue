<template>
  <el-row>
    <el-col :span="4">
      <div class="panel" id="tree">
        <panel-title :title="projectName"> </panel-title>
        <div class="panel-body">
          <el-tree
            :data="tree"
            :props="defaultProps"
            @node-click="onNodeClick"
          ></el-tree>
        </div>
      </div>
    </el-col>
    <el-col :span="20">
      <div class="panel m-l-md">
        <panel-title :title="basename(activeFile)">
          <el-button
            @click="onRenameFile"
            size="mini"
            type="primary"
            v-if="activeFile"
          >
            <i class="fa fa-edit"></i>
            {{ $lang.buttons.rename }}
          </el-button>
          <el-button
            @click="onCreateFile"
            size="mini"
            type="info"
            v-if="activeFile"
          >
            <i class="fa fa-plus"></i>
            {{ $lang.buttons.create }}
          </el-button>
          <el-button
            @click="onDeleteFile"
            size="mini"
            type="danger"
            v-if="activeFile"
          >
            <i class="fa fa-close"></i>
            {{ $lang.buttons.delete }}
          </el-button>
        </panel-title>
        <div class="panel-body">
          <codemirror
            v-model="code"
            :options="editorOptions"
            @input="onEditorCodeChange"
          >
          </codemirror>
        </div>
      </div>
    </el-col>
  </el-row>
</template>
<script>
import PanelTitle from "../../components/PanelTitle";
import { codemirror } from "vue-codemirror";

// Theme
import "codemirror/theme/monokai.css";

// Base Style
import "codemirror/lib/codemirror.css";

// Extra Keys
import "codemirror/addon/hint/show-hint";
import "codemirror/addon/hint/javascript-hint";
import "codemirror/addon/hint/sql-hint";
import "codemirror/addon/hint/html-hint";
import "codemirror/addon/hint/xml-hint";
import "codemirror/addon/hint/anyword-hint";
import "codemirror/addon/hint/css-hint";
import "codemirror/addon/hint/show-hint";

// Key Map
import "codemirror/keymap/sublime";

// CloseBrackets
import "codemirror/addon/edit/closebrackets";

// Active Line
import "codemirror/addon/selection/active-line";

// StyleSelectedText
import "codemirror/addon/selection/mark-selection";
import "codemirror/addon/search/searchcursor";

// Hint
import "codemirror/addon/hint/show-hint";
import "codemirror/addon/hint/show-hint.css";
import "codemirror/addon/hint/anyword-hint";

// foldGutter
import "codemirror/addon/fold/foldgutter.css";
import "codemirror/addon/fold/brace-fold";
import "codemirror/addon/fold/comment-fold";
import "codemirror/addon/fold/foldcode";
import "codemirror/addon/fold/foldgutter";
import "codemirror/addon/fold/indent-fold";
import "codemirror/addon/fold/markdown-fold";
import "codemirror/addon/fold/xml-fold";

// Mode
import "codemirror/mode/css/css";
import "codemirror/mode/dockerfile/dockerfile";
import "codemirror/mode/htmlmixed/htmlmixed";
import "codemirror/mode/markdown/markdown";
import "codemirror/mode/php/php";
import "codemirror/mode/python/python";
import "codemirror/mode/sass/sass";
import "codemirror/mode/javascript/javascript";
import "codemirror/mode/sql/sql";
import "codemirror/mode/vue/vue";

export default {
  name: "projectEdit",
  data() {
    return {
      projectName: this.$route.params.name,
      clientData: null,
      loading: true,
      tree: [],
      defaultProps: {
        children: "children",
        label: "label",
      },
      activeFile: null,
      activeNode: null,
      code: "Please Choose File from Left to Edit.",
      modeMap: {
        py: "text/x-python",
        js: "text/javascript",
        html: "text/html",
        vue: "text/x-vue",
        md: "text/x-markdown",
        scss: "text/x-sass",
        css: "text/x-css",
        php: "application/x-httpd-php",
      },
      editorOptions: {
        tabSize: 4,
        mode: "text/javascript",
        theme: "monokai",
        lineNumbers: true,
        styleActiveLine: true,
        line: true,
        keyMap: "sublime",
        // 按键映射，比如Ctrl键映射autocomplete，autocomplete是hint代码提示事件
        extraKeys: {
          Tab: "autocomplete",
        },
        // 代码折叠
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        // 选中文本自动高亮，及高亮方式
        styleSelectedText: true,
        highlightSelectionMatches: {
          showToken: /\w/,
          annotateScrollbar: true,
        },
      },
    };
  },
  components: {
    PanelTitle,
    codemirror,
  },
  created() {
    this.getProjectTree(this.projectName);
  },
  methods: {
    getProjectTree(name) {
      // 获取目录树
      this.$http
        .get(
          this.formatString(this.$store.state.url.project.tree, {
            name: name,
          })
        )
        .then(({ data: tree }) => {
          this.tree = tree;
          if (this.tree.length > 0) {
            let lastNode = this.tree[this.tree.length - 1];
            this.onNodeClick(lastNode);
          }
        })
        .catch(() => {
          this.$message.error(this.$store.getters.$lang.messages.errorLoad);
        });
    },
    onNodeClick(data) {
      this.activeNode = data;
      this.onChangeCode(data);
      this.activeFile = this.join(this.activeNode.path, this.activeNode.label);
    },
    // 呈现代码
    onChangeCode(data) {
      // 获取后缀
      let group = this.activeNode.label.split(".");
      let extension = group[group.length - 1];
      // 设置Mode
      this.editorOptions.mode = this.modeMap[extension];
      // 加载文件
      if (!data.children) {
        this.$http
          .post(this.$store.state.url.project.fileRead, data)
          .then(({ data: code }) => {
            this.code = code;
          })
          .catch(() => {
            this.$message.error(this.$store.getters.$lang.messages.errorLoad);
          });
      }
    },
    onRenameFile() {
      this.$prompt(
        this.$store.getters.$lang.titles.renameFile,
        this.$store.getters.$lang.buttons.confirm,
        {
          confirmButtonText: this.$store.getters.$lang.buttons.yes,
          cancelButtonText: this.$store.getters.$lang.buttons.no,
          inputValue: this.activeNode.label,
          inputPattern: /[^/\s]/,
          inputErrorMessage: this.$store.getters.$lang.messages.errorFormat,
        }
      ).then(({ value }) => {
        this.$http
          .post(this.$store.state.url.project.fileRename, {
            path: this.activeNode.path,
            pre: this.activeNode.label,
            new: value,
          })
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.messages.successSave
            );
            this.getProjectTree(this.projectName);
          })
          .catch(() => {
            this.$message.error(this.$store.getters.$lang.messages.errorSave);
          });
      });
    },
    onCreateFile() {
      this.$prompt(
        this.$store.getters.$lang.titles.createFile,
        this.$store.getters.$lang.buttons.confirm,
        {
          confirmButtonText: this.$store.getters.$lang.buttons.yes,
          cancelButtonText: this.$store.getters.$lang.buttons.no,
          inputValue: this.activeNode.label,
          inputPattern: /[^/\s]/,
          inputErrorMessage: this.$store.getters.$lang.messages.errorFormat,
        }
      ).then(({ value }) => {
        this.$http
          .post(this.$store.state.url.project.fileCreate, {
            path: this.activeNode.path,
            name: value,
          })
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.messages.successSave
            );
            this.getProjectTree(this.projectName);
          })
          .catch(() => {
            this.$message.error(this.$store.getters.$lang.messages.errorSave);
          });
      });
    },
    onDeleteFile() {
      this.$confirm(
        this.$store.getters.$lang.messages.confirm,
        this.$store.getters.$lang.buttons.confirm,
        {
          confirmButtonText: this.$store.getters.$lang.buttons.yes,
          cancelButtonText: this.$store.getters.$lang.buttons.no,
          type: "warning",
        }
      ).then(() => {
        this.$http
          .post(this.$store.state.url.project.fileDelete, {
            path: this.activeNode.path,
            label: this.activeNode.label,
          })
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.messages.successDelete
            );
            this.getProjectTree(this.projectName);
          })
          .catch(() => {
            this.$message.error(this.$store.getters.$lang.messages.errorDelete);
          });
      });
    },
    onEditorCodeChange(code, callback) {
      this.$http
        .post(this.$store.state.url.project.fileUpdate, {
          code: code,
          path: this.activeNode["path"],
          label: this.activeNode["label"],
        })
        .then(() => {
          if (callback) {
            callback();
          }
        })
        .catch(() => {
          this.$message.error(this.$store.getters.$lang.messages.errorDelete);
        });
    },
  },
};
</script>

<style lang="scss">
.CodeMirror {
  font-size: 16px;
  height: 76vh;
  z-index: 0;
}

#tree {
  .panel-body {
    overflow: hidden;
  }
  .el-tree {
    overflow-x: scroll;
    height: 76vh;
    border: none;
    div[role="treeitem"] {
      .el-tree-node__content {
        height: 35px;
      }
    }
  }
}

.el-tree-node.is-current {
  background: #eee;
}
</style>
