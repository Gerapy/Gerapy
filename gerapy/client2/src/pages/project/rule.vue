<template>
  <div>
    <div v-if="Object.keys(rule).length">
      <div v-for="(value, key, index) in rule" :key="key">
        <h5 class="inline m-v-sm">{{ key }}</h5>
        <el-button type="primary" size="mini" class="inline" v-if="value instanceof Array"
                   @click="onAddInput(rule[key])">
          <i class="fa fa-plus"></i>
          {{ $lang[$store.state.lang].buttons.add }}
        </el-button>
        <el-form-item>
          <!-- 列表类型，如 allow, deny -->
          <div v-if="value instanceof Array">
            <div v-for="(arrayValue, arrayKey, arrayIndex) in value" :key="arrayKey">
              <el-input v-if="isNaN(rule[key][arrayKey])"
                v-model="rule[key][arrayKey]" class="inline"
                size="small"></el-input>
              <el-input v-else
                v-model.number="rule[key][arrayKey]" class="inline"
                size="small"></el-input>
              <el-button type="danger" size="mini"
                         @click="onDeleteInput(rule, key, arrayKey)">
                <i class="fa fa-remove"></i>
                {{ $lang[$store.state.lang].buttons.delete }}
              </el-button>
            </div>
          </div>
          <!-- 列表类型 -->
          <!-- 字符串类型，如 callback, process_request -->
          <div v-if="typeof value === 'string'">
            <el-input
              v-model="rule[key]" class="inline"
              size="small"></el-input>
            <el-button type="danger" size="mini"
                       @click="onDeleteInput(rule, key)">
              <i class="fa fa-remove"></i>
              {{ $lang[$store.state.lang].buttons.delete }}
            </el-button>
          </div>
          <!-- 字符串类型 -->
          <!-- 布尔类型，如 follow -->
          <div v-if="typeof value === 'boolean'">
            <span class="inline">
              <el-radio class="radio" v-model="rule[key]" :label="true">True
              </el-radio>
              <el-radio class="radio" v-model="rule[key]" :label="false">False
              </el-radio>
            </span>
            <el-button type="danger" size="mini"
                       @click="onDeleteInput(rule, key)">
              <i class="fa fa-remove"></i>
              {{ $lang[$store.state.lang].buttons.delete }}
            </el-button>
          </div>
          <!-- 布尔类型 -->
        </el-form-item>
      </div>
    </div>
    <div v-else>
      <h5>{{ $lang[$store.state.lang].messages.addColumn }}</h5>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Rule',
    props: {
      rule: {
        type: Object
      },
      onAddInput: {
        type: Function
      },
      onDeleteInput: {
        type: Function
      }
    }
  }
</script>
