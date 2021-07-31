<template>
  <codemirror
    v-model="newValue"
    :options="options"
    @input="change"
    class="code-editor"
  >
  </codemirror>
</template>
<script>
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
  props: {
    value: {
      type: String,
    },
    change: {
      type: Function,
      default() {
        return () => {};
      },
    },
  },
  components: {
    codemirror,
  },
  computed: {
    newValue: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      },
    },
  },
  data() {
    return {
      options: {
        tabSize: 4,
        mode: "text/x-python",
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
};
</script>

<style lang="scss">
$line-height: 25px;
.code-editor {
  font-size: 16px;
  .CodeMirror {
    max-height: 200px;
  }
  .CodeMirror-line {
    height: $line-height;
    line-height: $line-height !important;
  }
}
</style>
