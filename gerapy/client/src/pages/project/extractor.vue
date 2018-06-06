<template>
  <div>
    <el-form-item>
      <h5 class="inline m-v-sm">{{ $lang[$store.state.lang].titles.callback }}</h5>
      <el-input
        v-model="extractor.callback" class="inline"
        :placeholder="$lang[$store.state.lang].titles.callback"
        size="small">
      </el-input>
    </el-form-item>
    <el-form-item>
      <h5 class="inline m-v-sm">{{ $lang[$store.state.lang].titles.item }}</h5>
      <el-select v-model="extractor.item" :placeholder="$lang[$store.state.lang].titles.item"
                 size="small" class="inline inline-first">
        <el-option
          v-for="item in items"
          :key="item.name"
          :label="item.name"
          :value="item.name">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item>
      <div v-if="Object.keys(extractor.attrs).length">
        <div v-for="(value, key, index) in extractor.attrs" :key="key">
          {{ key }}
          <el-button type="primary" size="mini"
                     @click="onAddInput(extractor.attrs[key], {method: 'xpath'})">
            <i class="fa fa-plus"></i>
            {{ $lang[$store.state.lang].buttons.addRule }}
          </el-button>
          <div v-for="(v, k, i) in value" :key="k" class="extractor-rule">
            <el-select v-model="v['method']" :placeholder="$lang[$store.state.lang].columns.method"
                       size="small"
                       class="inline inline-first">
              <el-option
                v-for="item in extractorMethods"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            <el-input
              v-model="v['arg']" class="inline inline-second"
              :placeholder="$lang[$store.state.lang].columns.value"
              size="small"></el-input>
            <el-input
              v-model="v['processor']" class="inline inline-third"
              :placeholder="$lang[$store.state.lang].columns.processors"
              size="small"></el-input>
            <el-input
              v-model="v['re']" class="inline inline-fourth"
              :placeholder="$lang[$store.state.lang].columns.regex"
              size="small"></el-input>
            <el-button type="danger" size="mini"
                       @click="onDeleteInput(extractor.attrs, key, k)">
              <i class="fa fa-remove"></i>
              {{ $lang[$store.state.lang].buttons.delete }}
            </el-button>
          </div>
        </div>
      </div>
      <div v-else>
        <h5>{{ $lang[$store.state.lang].messages.addColumn }}</h5>
      </div>
    </el-form-item>
  </div>
</template>

<script>

  export default {
    name: 'Extractor',
    props: {
      extractor: {
        type: Object,
      },
      items: {
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
        extractorMethods: [
          {
            value: 'xpath',
            label: 'XPath'
          }, {
            value: 'css',
            label: 'CSS'
          }, {
            value: 'attr',
            label: 'Attr'
          }, {
            value: 'value',
            label: 'Value'
          }
        ],
      }
    }
  }
</script>
