<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="panel">
          <panel-title :title="$lang.titles.deployProject"> </panel-title>
          <div class="panel-body">
            <el-table
              :data="clients"
              v-loading="loading"
              :element-loading-text="$lang.messages.loading"
              @selection-change="onBatchSelect"
              :style="{ width: '100%' }"
            >
              <el-table-column align="center" type="selection" width="55">
              </el-table-column>
              <el-table-column
                align="center"
                :label="$lang.columns.status"
                width="100"
              >
                <template slot-scope="props">
                  <el-button
                    :type="statusClass[clientsStatus[props.row.pk]]"
                    size="mini"
                  >
                    {{ statusText[clientsStatus[props.row.pk]] }}
                  </el-button>
                </template>
              </el-table-column>
              <el-table-column
                align="center"
                prop="pk"
                :label="$lang.columns.id"
                width="60"
              >
              </el-table-column>
              <el-table-column
                align="center"
                prop="fields.name"
                :label="$lang.columns.name"
                width="100"
              >
              </el-table-column>
              <el-table-column
                align="center"
                prop="fields.ip"
                :label="$lang.columns.ip"
                width="150"
              >
              </el-table-column>
              <el-table-column
                align="center"
                prop="fields.port"
                :label="$lang.columns.port"
                width="100"
              >
              </el-table-column>
              <el-table-column
                align="center"
                :label="$lang.columns.description"
              >
                <template slot-scope="props">
                  <span>{{ projectDescriptions[props.row.pk] }}</span>
                </template>
              </el-table-column>
              <el-table-column align="center" :label="$lang.columns.deployedAt">
                <template slot-scope="props">
                  <span>{{ projectDateTimes[props.row.pk] }}</span>
                </template>
              </el-table-column>
              <el-table-column align="center" :label="$lang.columns.operations">
                <template slot-scope="props">
                  <el-button
                    type="success"
                    size="mini"
                    @click="onDeploy(props.row.pk)"
                    v-if="clientsStatus[props.row.pk]"
                  >
                    <i class="fa fa-cloud-upload"></i>
                    {{ $lang.buttons.deploy }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <bottom-bar>
              <el-button
                slot="handler"
                type="primary"
                size="mini"
                :disabled="batchSelect.length === 0"
                @click="onBatchDeploy"
                slot-scope="handler"
              >
                <span>
                  <i class="fa fa-cloud-upload"></i>
                  {{ $lang.buttons.batchDeploy }}
                </span>
              </el-button>
            </bottom-bar>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="panel">
          <panel-title :title="$lang.objects.project"> </panel-title>
          <div class="panel-body">
            <el-form :model="buildInfo" label-width="120px">
              <el-form-item :label="$lang.columns.name">
                {{ buildInfo.name }}
              </el-form-item>
              <el-form-item :label="$lang.columns.packageName">
                {{ buildInfo.egg || notBuildText }}
              </el-form-item>
              <el-form-item :label="$lang.columns.builtAt">
                {{ buildInfo.built_at || notBuildText }}
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="panel">
          <panel-title :title="$lang.titles.buildProject"> </panel-title>
          <div class="panel-body">
            <el-form
              ref="form"
              :model="buildInfo"
              :rules="rules"
              label-width="120px"
            >
              <el-form-item :label="$lang.columns.name">
                {{ buildInfo.name }}
              </el-form-item>
              <el-form-item
                :label="$lang.columns.description"
                prop="description"
                class="description"
              >
                <el-input
                  v-model="buildInfo.description"
                  size="small"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" @click="onBuild">
                  <i class="fa fa-codepen"></i> 
                  <span v-if="buildInfo.egg"> {{ $lang.buttons.re }}</span>{{ $lang.buttons.build }}
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script type="text/javascript">
import PanelTitle from "../../components/PanelTitle";
import BottomBar from "../../components/BottomBar";

export default {
  data() {
    return {
      buildInfo: {},
      notBuildText: this.$store.getters.$lang.messages.notBuilt,
      clients: [],
      loading: false,
      projectName: this.$route.params.name,
      batchSelect: [],
      projectDescriptions: {},
      projectDateTimes: {},
      clientsStatus: {},
      statusClass: {
        "1": "success",
        "0": "warning",
        "-1": "danger",
      },
      statusText: {
        "1": this.$store.getters.$lang.buttons.normal,
        "0": this.$store.getters.$lang.buttons.connecting,
        "-1": this.$store.getters.$lang.buttons.error,
      },
      rules: {
        description: [
          {
            required: true,
            message: this.$store.getters.$lang.messages.emptyDescription,
            trigger: "blur",
          },
        ],
      },
    };
  },
  components: {
    PanelTitle,
    BottomBar,
  },
  created() {
    this.getClientData();
    this.getBuildInfo();
  },
  methods: {
    onBatchSelect(val) {
      this.batchSelect = val;
      console.log(this.batchSelect);
    },
    getBuildInfo() {
      this.loading = true;
      this.$http
        .get(
          this.formatString(this.$store.state.url.project.build, {
            name: this.projectName,
          })
        )
        .then(({ data: data }) => {
          this.buildInfo = data;
          console.log(data);
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    getClientStatus(id) {
      this.$set(this.clientsStatus, id, 0);
      this.$http
        .get(
          this.formatString(this.$store.state.url.client.status, {
            id: id,
          })
        )
        .then(({ data: { result: data } }) => {
          this.$set(this.clientsStatus, id, data);
        })
        .catch(() => {
          this.$set(this.clientsStatus, id, -1);
        });
    },
    getClientData() {
      this.loading = true;
      this.$http
        .get(this.$store.state.url.client.index)
        .then(({ data: clients }) => {
          this.clients = clients;
          this.loading = false;
          this.clients.forEach(({ pk: id }) => {
            this.getProjectVersion(id);
            this.getClientStatus(id);
          });
        })
        .catch(() => {
          this.loading = false;
        });
    },
    deploy(id) {
      if (this.clientsStatus[id]) {
        this.$http
          .post(
            this.formatString(this.$store.state.url.client.projectDeploy, {
              id: id,
              name: this.projectName,
            })
          )
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.titles.client +
                " " +
                id +
                " " +
                this.$store.getters.$lang.messages.successDeploy
            );
            this.getProjectVersion(id);
            this.loading = false;
          })
          .catch(() => {
            this.$message.error(
              this.$store.getters.$lang.titles.client +
                " " +
                id +
                " " +
                this.$store.getters.$lang.messages.errorDeploy
            );
            this.loading = false;
          });
      } else {
        this.$message.error(
          this.$store.getters.$lang.titles.client +
            " " +
            id +
            " " +
            this.$store.getters.$lang.messages.errorDeploy
        );
        this.loading = false;
      }
    },
    getProjectVersion(id) {
      this.loading = true;
      this.$http
        .get(
          this.formatString(this.$store.state.url.client.projectVersion, {
            id: id,
            name: this.projectName,
          })
        )
        .then(({ data: version }) => {
          this.$set(this.projectDescriptions, id, version["description"]);
          this.$set(this.projectDateTimes, id, version["deployed_at"]);
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    onBatchDeploy() {
      this.$confirm(
        this.$store.getters.$lang.messages.confirm,
        this.$store.getters.$lang.buttons.confirm,
        {
          confirmButtonText: this.$store.getters.$lang.buttons.yes,
          cancelButtonText: this.$store.getters.$lang.buttons.no,
          type: "warning",
        }
      )
        .then(() => {
          this.loading = true;
          console.log(this.batchSelect);
          this.batchSelect.forEach(({ pk: id }) => {
            this.deploy(id);
          });
        })
        .catch(() => {
          this.$message.error(this.$store.getters.$lang.messages.errorDeploy);
        });
    },
    onDeploy(id) {
      if (this.buildInfo.egg) {
        this.deploy(id);
      } else {
        this.$message.error(this.$store.getters.$lang.messages.buildFirst);
      }
    },
    onBuild() {
      this.$refs.form.validate((valid) => {
        if (!valid) return false;
        this.$http
          .post(
            this.formatString(this.$store.state.url.project.build, {
              name: this.projectName,
            }),
            {
              description: this.buildInfo["description"],
              egg: this.buildInfo["egg"],
              built_at: this.buildInfo["built_at"],
            }
          )
          .then(({ data: data }) => {
            this.buildInfo = data;
            console.log(data);
            this.loading = false;
            this.$message.success(
              this.$store.getters.$lang.messages.successBuild
            );
          })
          .catch(() => {
            this.loading = false;
            this.$message.error(this.$store.getters.$lang.messages.errorBuild);
          });
      });
    },
  },
};
</script>

<style>
.description input {
  max-width: 200px;
}
</style>
