<template>
  <div>
    <el-row class="m-b-sm">
      <el-col :span="3">
        <el-button type="primary" size="mini">XPath Selector</el-button>
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
    <el-row class="m-b-md">
      <el-col :span="3">
        <el-button type="primary" size="mini">CSS Selector</el-button>
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
    <iframe
      sandbox="allow-same-origin allow-scripts"
      scrolling="yes"
      width="100%"
      :srcdoc="html"
      class="iframe-box"
      id="iframe-box"
      frameborder="0"
    ></iframe>
  </div>
</template>
<script>
import $ from "jquery";

$.fn.extend({
  getCSSSelector: function() {
    var path,
      node = this;
    while (node.length) {
      var realNode = node[0],
        name = realNode.localName;
      var classes = $(realNode).attr("class");
      var cls = "";
      if (classes) {
        classes = classes.split(" ");
        for (let i = 0; i < classes.length; i++) {
          if (classes[i]) {
            cls += "." + classes[i];
          }
        }
      }

      if (!name) break;
      name = name.toLowerCase();

      if (cls) {
        name = name + cls;
      }

      var parent = node.parent();

      var sameTagSiblings = parent.children(name);
      if (sameTagSiblings.length > 1) {
        var allSiblings = parent.children();
        var index = allSiblings.index(realNode) + 1;
        if (index > 1) {
          name += ":nth-child(" + index + ")";
        }
      }

      if (name !== "html" && name !== "body") {
        path = name + (path ? " > " + path : "");
      }
      node = parent;
    }
    return path;
  },
  getXPathSelector: function() {
    var path,
      node = this;
    if (node.id) return "//*[@id='" + node.id + "']";
    var position,
      $node = this.first(),
      nodeName = $node.prop("nodeName"),
      $sibSameNameAndSelf = $node.siblings(nodeName).addBack(),
      steps = [],
      $parent = $node.parent(),
      parentName = $parent.prop("nodeName");

    position =
      $sibSameNameAndSelf.length > 1
        ? "[" + ($sibSameNameAndSelf.index($node) + 1) + "]"
        : "";
    steps.push(nodeName + position);

    while (
      $parent.length == 1 &&
      parentName !== node &&
      parentName.toLowerCase() !== "#document" &&
      parentName.toLowerCase() !== "html" &&
      parentName.toLowerCase() !== "body"
    ) {
      $sibSameNameAndSelf = $parent.siblings(parentName).addBack();
      position =
        $sibSameNameAndSelf.length > 1
          ? "[" + ($sibSameNameAndSelf.index($parent) + 1) + "]"
          : "";
      steps.push(parentName + position);
      $parent = $parent.parent();
      parentName = $parent.prop("nodeName");
    }
    return (
      "//" +
      steps
        .reverse()
        .join("/")
        .toLowerCase()
    );
  },
});

function getCSSSelector(element) {
  return $(element).getCSSSelector();
}

function getXPathSelector(element) {
  return $(element).getXPathSelector();
}

export default {
  name: "Web",
  data() {
    return {
      xpathSelector: null,
      cssSelector: null,
    };
  },
  props: {
    html: {
      type: String,
    },
  },
  methods: {
    onCopy: function() {
      this.$message.success(this.$store.getters.$lang.messages.successCopy);
    },
    onError: function() {
      this.$message.error(this.$store.getters.$lang.messages.errorCopy);
    },
  },
  mounted() {
    let that = this;
    let iframe_id = "iframe-box";
    $("#" + iframe_id).on("load", function() {
      document.getElementById(
        iframe_id
      ).contentWindow.document.body.onclick = function(event) {
        event.preventDefault();
        event.stopPropagation();
        let target = $(event.target);
        console.log(getCSSSelector(target));
        that.cssSelector = getCSSSelector(target);
        that.xpathSelector = getXPathSelector(target);

        $(document.getElementById(iframe_id).contentWindow.document.body)
          .find(".gerapy-selected")
          .remove();
        $(document.getElementById(iframe_id).contentWindow.document.body)
          .find(getCSSSelector(target))
          .each(function() {
            $("<div></div>")
              .css($(this).offset())
              .css({
                width: target.width(),
                height: target.height(),
                position: "absolute",
                border: "2px solid red",
                "pointer-events": "none",
                "z-index": 10000,
              })
              .addClass("gerapy-selected")
              .appendTo(
                $(
                  document.getElementById(iframe_id).contentWindow.document.body
                )
              );
          });
      };
    });
  },
};
</script>
<style scoped>
iframe html {
  cursor: pointer;
}
</style>
