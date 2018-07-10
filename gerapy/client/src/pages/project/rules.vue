<template>
  <div>
    <h4 class="inline">{{ $lang[$store.state.lang].titles.rules }}</h4>
    <!-- 添加规则项配置浮窗 -->
    <el-dialog :visible.sync="addRuleItem" size="tiny">
      <el-form>
        <el-form-item :label="$lang[$store.state.lang].titles.selectConfig">
          <el-select v-model="ruleItem" :placeholder="$lang[$store.state.lang].titles.selectConfig"
                     size="small">
            <el-option
              v-for="item in ruleItemOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="addRuleItem=false" size="small">{{ $lang[$store.state.lang].buttons.cancel }}
        </el-button>
        <el-button @click="onAddRuleItem()"
                   type="primary" size="small">{{ $lang[$store.state.lang].buttons.add }}
        </el-button>
      </div>
    </el-dialog>
    <!-- 添加规则项配置浮窗 -->
    <el-button type="primary" class="inline" size="mini" @click="onAddInput(rules, {})">
      <i class="fa fa-plus"></i>
      {{ $lang[$store.state.lang].buttons.addRule }}
    </el-button>
    <el-collapse :value="parseInt(rules.length-1)"
                 v-if="rules.length">
      <el-collapse-item v-for="(rule, ruleKey, ruleIndex) in rules" :name="ruleKey"
                        :key="ruleKey">
        <!-- 每条规则标题及操作配置 -->
        <template slot="title">
            <span>
              {{ $lang[$store.state.lang].titles.rule }} {{ ruleKey + 1 }}
            </span>
          <span class="pull-right">
              <el-button type="primary" class="inline" size="mini"
                         @click.stop="addRuleItem=true,activeRule=ruleKey">
                <i class="fa fa-plus"></i>
                {{ $lang[$store.state.lang].buttons.addColumn }}
              </el-button>
              <el-button type="danger" size="mini" class="m-r-md"
                         @click="onDeleteInput(rules, ruleKey)">
                  <i class="fa fa-remove"></i>
                  {{ $lang[$store.state.lang].buttons.delete }}
              </el-button>
            </span>
        </template>
        <!-- 每条规则标题及操作配置 -->
        <!-- 每条规则配置选项 -->
        <rule :rule="rule" :onAddInput="onAddInput" :onDeleteInput="onDeleteInput"></rule>
        <!-- 每条规则配置选项 -->
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
  import {ruleItemOptions, ruleItemInit} from 'common/project/rule'
  import rule from 'pages/project/rule'
  import clone from 'clone'

  export default {
    name: 'Rules',
    props: {
      rules: {
        type: Array
      },
      onAddInput: {
        type: Function
      },
      onDeleteInput: {
        type: Function
      }
    },
    data() {
      return {
        // 爬取规则
        ruleItem: null,
        ruleItemOptions: ruleItemOptions,
        ruleItemInit: ruleItemInit,
        addRuleItem: false,
        activeRule: null,
      }
    },
    components: {
      rule
    },
    methods: {
      onAddRuleItem() {
        this.$set(this.rules[this.activeRule], this.ruleItem, clone(this.ruleItemInit[this.ruleItem]))
        this.addRuleItem = false
      },
    }
  }
</script>
