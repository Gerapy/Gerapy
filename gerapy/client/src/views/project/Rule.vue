<template>
  <div>
    <div v-if="Object.keys(rule).length">
      <div v-for="(value, key) in rule" :key="key">
        <el-form-item class="inline">
          {{ key }}
        </el-form-item>
        <el-form-item class="inline">
          <el-button
            type="primary"
            size="mini"
            class="inline"
            v-if="value instanceof Array"
            @click="onAddInput(rule[key])"
          >
            <i class="fa fa-plus"></i>
            {{ $lang.buttons.add }}
          </el-button>
        </el-form-item>
        <el-form-item>
          <!-- 列表类型，如 allow, deny -->
          <div v-if="value instanceof Array">
            <div v-for="(arrayValue, arrayIndex) in value" :key="arrayIndex">
              <el-form-item class="inline" :style="{ width: '500px' }">
                <el-input
                  v-if="isNaN(rule[key][arrayIndex])"
                  v-model="rule[key][arrayIndex]"
                  class="inline"
                  size="small"
                ></el-input>
                <el-input
                  v-else
                  v-model.number="rule[key][arrayIndex]"
                  class="inline"
                  size="small"
                ></el-input>
              </el-form-item>
              <el-form-item class="inline">
                <el-button
                  type="danger"
                  size="mini"
                  @click="onDeleteInput(rule, key, arrayIndex)"
                >
                  <i class="fa fa-remove"></i>
                  {{ $lang.buttons.delete }}
                </el-button>
              </el-form-item>
            </div>
          </div>
          <!-- 列表类型 -->
          <!-- 字符串类型，如 callback, process_request -->
          <div v-if="typeof value === 'string' || value === null">
            <el-form-item class="inline" :style="{ width: '500px' }">
              <el-input
                v-model="rule[key]"
                class="inline"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item class="inline">
              <el-button
                type="danger"
                size="mini"
                @click="onDeleteInput(rule, key)"
              >
                <i class="fa fa-remove"></i>
                {{ $lang.buttons.delete }}
              </el-button>
            </el-form-item>
          </div>
          <!-- 字符串类型 -->

          <!-- 布尔类型，如 follow -->
          <div v-if="typeof value === 'boolean'">
            <el-form-item class="inline" :style="{ width: '500px' }">
              <el-radio class="radio" v-model="rule[key]" :label="true"
                >True
              </el-radio>
              <el-radio class="radio" v-model="rule[key]" :label="false"
                >False
              </el-radio>
            </el-form-item>
            <el-form-item class="inline">
              <el-button
                type="danger"
                size="mini"
                @click="onDeleteInput(rule, key)"
              >
                <i class="fa fa-remove"></i>
                {{ $lang.buttons.delete }}
              </el-button>
            </el-form-item>
          </div>
          <!-- 布尔类型 -->
        </el-form-item>
      </div>
    </div>
    <div v-else>
      <h5>{{ $lang.messages.addColumn }}</h5>
    </div>
  </div>
</template>

<script>
export default {
  name: "Rule",
  props: {
    rule: {
      type: Object,
    },
    onAddInput: {
      type: Function,
    },
    onDeleteInput: {
      type: Function,
    },
  },
};
</script>
