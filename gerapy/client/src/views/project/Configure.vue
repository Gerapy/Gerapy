<template>
  <div id="project-configure">
    <div class="panel" id="info">
      <panel-title :title="$lang.titles.project"> </panel-title>
      <el-form label-width="140px" label-position="left">
        <el-form-item :label="$lang.columns.projectName">
          {{ projectName }}
        </el-form-item>

        <el-form-item :label="$lang.columns.generateCode">
          <span>{{
            projectGeneratedAt
              ? projectGeneratedAt
              : $lang.descriptions.notGenerated
          }}</span>
          <span v-if="projectGeneratedAt">
            <router-link
              :to="{ name: 'projectEdit', params: { name: projectName } }"
              tag="span"
            >
              <el-button type="primary" size="mini">
                <i class="fa fa-edit"></i>
                {{ $lang.buttons.edit }}
              </el-button>
            </router-link>
          </span>
        </el-form-item>
      </el-form>
    </div>
    <!-- 实体配置 -->
    <div class="panel" id="items">
      <panel-title :title="$lang.titles.items"> </panel-title>
      <el-form label-width="100px">
        <el-form-item label-width="0px">
          <el-button
            type="primary"
            class="inline"
            size="mini"
            @click="onAddInput(configuration.items, { name: '', attrs: {} })"
          >
            <i class="fa fa-plus"></i>
            {{ $lang.buttons.addItem }}
          </el-button>
        </el-form-item>

        <!-- 添加规则配置浮窗 -->
        <el-dialog :visible.sync="addItem" size="tiny">
          <el-form>
            <el-form-item :label="$lang.columns.column">
              <el-input
                size="small"
                v-model="column"
                class="inline"
                :placeholder="$lang.columns.column"
              >
              </el-input>
            </el-form-item>
          </el-form>
          <div slot="footer">
            <el-button @click="addItem = false" size="small"
              >{{ $lang.buttons.cancel }}
            </el-button>
            <el-button @click="onAddItem()" type="primary" size="small"
              >{{ $lang.buttons.add }}
            </el-button>
          </div>
        </el-dialog>
        <!-- 添加规则配置浮窗结束 -->

        <el-form-item label-width="0px">
          <el-collapse
            :accordion="accordion"
            :value="parseInt(configuration.items.length - 1)"
            v-if="configuration.items.length"
          >
            <el-collapse-item
              v-for="(item, itemIndex) in configuration.items"
              :name="'item' + itemIndex"
              :key="'item' + itemIndex"
            >
              <template slot="title">
                <el-form-item label-width="0" class="inline">
                  <el-button type="primary" size="mini" class="m-r-xs">
                    {{ itemIndex + 1 }}
                  </el-button>
                </el-form-item>
                <el-form-item label-width="0" class="inline">
                  {{ item.name }}
                </el-form-item>
                <el-form-item label-width="0" class="inline">
                  <el-button
                    type="primary"
                    class="inline"
                    size="mini"
                    @click.stop="
                      (addItem = true),
                        (activeItem = itemIndex),
                        (column = null)
                    "
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
                    @click="$delete(configuration.items, itemIndex)"
                  >
                    <i class="fa fa-remove"></i>
                    {{ $lang.buttons.delete }}
                  </el-button>
                </el-form-item>
              </template>
              <item :item="item"></item>
            </el-collapse-item>
          </el-collapse>
        </el-form-item>
      </el-form>
    </div>
    <!-- 实体配置结束 -->

    <!-- 爬虫配置 -->
    <div class="panel" id="spiders">
      <panel-title :title="$lang.titles.listSpider"> </panel-title>

      <el-form label-width="100px">
        <el-form-item label-width="0">
          <el-button
            type="primary"
            class="inline"
            size="mini"
            @click="onAddSpider"
          >
            <i class="fa fa-plus"></i>
            {{ $lang.buttons.addSpider }}
          </el-button>
        </el-form-item>
        <el-form-item label-width="0">
          <el-collapse
            v-model="activeSpider"
            accordion
            v-if="configuration.spiders.length"
          >
            <el-collapse-item
              v-for="(spider, spiderIndex) in configuration.spiders"
              :name="spiderIndex"
              :key="spiderIndex"
            >
              <spider
                :projectName="projectName"
                :spider="spider"
                :spiderIndex="spiderIndex"
                :items="configuration.items"
                :onAddInput="onAddInput"
                :onDeleteInput="onDeleteInput"
              ></spider>
              <template slot="title">
                <el-form-item label-width="0" class="inline">
                  <el-button class="inline m-r-sm" type="primary" size="mini">
                    {{ spiderIndex + 1 }}
                  </el-button>
                </el-form-item>
                <el-form-item label-width="0" class="inline">
                  {{ spider.name }}
                </el-form-item>
                <el-form-item label-width="0" class="inline">
                  <el-button
                    type="danger"
                    size="mini"
                    class="m-r-md"
                    @click="onDeleteInput(configuration.spiders, spiderIndex)"
                  >
                    <i class="fa fa-remove"></i>
                    {{ $lang.buttons.delete }}
                  </el-button>
                </el-form-item>
              </template>
            </el-collapse-item>
          </el-collapse>
        </el-form-item>
      </el-form>
    </div>
    <!-- 爬虫配置结束 -->

    <el-button @click="saveProject" type="primary" id="save">
      <i class="fa fa-spin fa-circle-o-notch" v-if="savingProject"></i>
      <i class="fa fa-save" v-else></i>
    </el-button>
  </div>
</template>
<script>
import PanelTitle from "../../components/PanelTitle";
import Spider from "./Spider";
import Item from "./Item";

export default {
  name: "ProjectConfigure",
  data() {
    return {
      error: null,
      showBrowser: false,
      savingProject: false,
      projectName: this.$route.params.name,
      projectDescription: null,
      projectGeneratedAt: null,
      projectBuiltAt: null,
      activeSpider: 0,
      accordion: false,
      // 提取实体
      addItem: false,
      activeItem: null,
      column: null,
      configuration: {
        spiders: [],
        items: [],
      },
    };
  },
  computed: {
    extractorItemOptions() {
      let array = [];
      this.configuration.items.forEach((item) => {
        let attrs = [];
        for (let attr in item["attrs"]) {
          attrs.push({
            value: attr,
            label: attr,
          });
        }
        array.push({
          value: item["name"],
          label: item["name"],
          children: attrs,
        });
      });
      return array;
    },
  },
  components: {
    PanelTitle,
    Spider,
    Item,
  },
  created() {
    this.getProject();
  },
  methods: {
    hideBrowser() {
      this.showBrowser = false;
    },
    getProject() {
      this.$http
        .get(
          this.formatString(this.$store.state.url.project.configure, {
            name: this.projectName,
          })
        )
        .then(({ data: data }) => {
          this.projectDescription = data.description;
          this.projectGeneratedAt = data.generated_at;
          this.projectBuiltAt = data.built_at;
          this.configuration = data.configuration || this.configuration;
          this.loadData = false;
        });
    },
    saveProject() {
      this.savingProject = true;
      this.$http
        .post(
          this.formatString(this.$store.state.url.project.configure, {
            name: this.projectName,
          }),
          {
            configuration: this.configuration,
          }
        )
        .then(({ data: { status: status, message: message } }) => {
          if (status === "1") {
            this.$message.success(
              this.$store.getters.$lang.messages.successSave
            );
          } else {
            this.error = message;
          }
          this.savingProject = false;
        })
        .catch(({ data: { message: message } }) => {
          this.$message.error(this.$store.getters.$lang.messages.errorSave);
          this.savingProject = false;
        });
    },
    onDeleteInput(array, ...keys) {
      if (keys.length === 2) {
        // 二维字典
        this.$delete(array[keys[0]], keys[1]);
        if (array[keys[0]].length === 0) {
          this.$delete(array, keys[0]);
        }
      } else if (keys.length === 1) {
        // 一维字典
        this.$delete(array, keys[0]);
      }
    },
    onAddInput(array, arg = "") {
      if (!array) {
        array = [];
      }
      array.push(arg);
    },
    onAddItem() {
      this.$set(
        this.configuration.items[this.activeItem]["attrs"],
        this.column,
        {}
      );
      this.addItem = false;
    },
    onGenerate() {
      if (this.projectBuiltAt) {
        this.$confirm(
          this.$store.getters.$lang.messages.reGenerate,
          this.$store.getters.$lang.buttons.confirm,
          {
            confirmButtonText: this.$store.getters.$lang.buttons.yes,
            cancelButtonText: this.$store.getters.$lang.buttons.no,
            type: "warning",
          }
        )
          .then(() => {
            this.generateProject();
          })
          .catch(() => {
            this.$message.error(this.$store.getters.$lang.messages.errorDelete);
          });
      } else {
        this.generateProject();
      }
    },
    onAddSpider() {
      this.onAddInput(this.configuration.spiders, {
        name: null,
        custom_settings: [],
        code: {},
        extractors: [],
        rules: [],
        proxy: {},
        cookies: {},
        storage: {
          mysql: {
            enable: false,
            tables: [],
          },
          mongodb: {
            enable: false,
            collections: [],
          },
        },
        start_urls: {
          mode: "list",
          list: [],
          code: null,
          file: null,
        },
        attrs: [],
        allowed_domains: [],
      });
    },
  },
};
</script>

<style lang="scss">
#project-configure {
  #info,
  #items,
  #spiders {
    .el-form {
      padding: 20px 30px;
    }
  }
  #info {
    .el-form {
      .el-form-item {
        margin-bottom: 0;
      }
    }
  }
}

.inline {
  display: inline-block;
  &.short {
    max-width: 100px !important;
  }
  &.medium {
    max-width: 200px !important;
  }
  &.long {
    max-width: 400px !important;
  }
}

#save {
  position: fixed;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
  font-size: 12px;
  padding-left: 15px;
}
</style>
