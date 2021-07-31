<template>
  <div>
    <el-form-item :label="$lang.titles.rules">
      <el-button
        type="primary"
        class="inline"
        size="mini"
        @click="onAddInput(rules, {})"
      >
        <i class="fa fa-plus"></i>
        {{ $lang.buttons.addRule }}
      </el-button>
    </el-form-item>

    <!-- 添加规则项配置浮窗 -->
    <el-dialog :visible.sync="addRuleItem" size="tiny">
      <el-form>
        <el-form-item :label="$lang.titles.selectConfig">
          <el-select
            v-model="ruleItem"
            :placeholder="$lang.titles.selectConfig"
            size="small"
          >
            <el-option
              v-for="item in ruleItemOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="addRuleItem = false" size="small"
          >{{ $lang.buttons.cancel }}
        </el-button>
        <el-button @click="onAddRuleItem()" type="primary" size="small"
          >{{ $lang.buttons.add }}
        </el-button>
      </div>
    </el-dialog>
    <!-- 添加规则项配置浮窗 -->
    <el-form-item label-width="100px">
      <el-collapse :value="parseInt(rules.length - 1)" v-if="rules.length">
        <el-collapse-item
          v-for="(rule, ruleIndex) in rules"
          :name="'rule' + ruleIndex"
          :key="'rule' + ruleIndex"
        >
          <!-- 每条规则标题及操作配置 -->
          <template slot="title">
            <el-form-item class="inline">
              <el-button class="inline m-r-sm" type="primary" size="mini">
                {{ ruleIndex + 1 }}
              </el-button>
            </el-form-item>
            <el-form-item class="inline">
              {{ $lang.titles.rule }} {{ ruleIndex + 1 }}
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                class="inline"
                size="mini"
                @click.stop="(addRuleItem = true), (activeRule = ruleIndex)"
              >
                <i class="fa fa-plus"></i>
                {{ $lang.buttons.addColumn }}
              </el-button>
            </el-form-item>
            <el-form-item>
              <el-button
                type="danger"
                size="mini"
                class="m-r-md"
                @click="onDeleteInput(rules, ruleIndex)"
              >
                <i class="fa fa-remove"></i>
                {{ $lang.buttons.delete }}
              </el-button>
            </el-form-item>
          </template>
          <!-- 每条规则标题及操作配置 -->

          <!-- 每条规则配置选项 -->
          <rule
            :rule="rule"
            :onAddInput="onAddInput"
            :onDeleteInput="onDeleteInput"
          ></rule>
          <!-- 每条规则配置选项 -->
        </el-collapse-item>
      </el-collapse>
    </el-form-item>
  </div>
</template>

<script>
import { ruleItemOptions, ruleItemInit } from "../../utils/rule";
import Rule from "./Rule";
import clone from "clone";

export default {
  name: "Rules",
  props: {
    rules: {
      type: Array,
    },
    onAddInput: {
      type: Function,
    },
    onDeleteInput: {
      type: Function,
    },
  },
  data() {
    return {
      // 爬取规则
      ruleItem: null,
      ruleItemOptions: ruleItemOptions,
      ruleItemInit: ruleItemInit,
      addRuleItem: false,
      activeRule: null,
    };
  },
  components: {
    Rule,
  },
  methods: {
    onAddRuleItem() {
      this.$set(
        this.rules[this.activeRule],
        this.ruleItem,
        clone(this.ruleItemInit[this.ruleItem])
      );
      this.addRuleItem = false;
    },
  },
};
</script>
