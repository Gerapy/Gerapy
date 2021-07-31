<template>
  <div class="panel" id="project-index">
    <el-dialog
      :visible.sync="createProjectDialog"
      size="tiny"
      width="400px"
      class="dialog"
    >
      <el-tabs v-model="activeDialogTab">
        <el-tab-pane :label="$lang.columns.create" name="create">
          <el-form>
            <el-form-item :label="$lang.columns.name" label-width="65px">
              <el-input
                v-model="projectName"
                class="inline"
                :placeholder="$lang.columns.name"
                size="small"
              >
              </el-input>
              <p>
                <small>{{ $lang.messages.createConfigurableProject }}</small>
              </p>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane :label="$lang.columns.upload" name="upload">
          <el-upload
            class="upload"
            drag
            accept=".zip"
            :action="$store.state.url.project.upload"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              {{ $lang.messages.dragOrSelect }}
            </div>
            <div class="el-upload__tip" slot="tip">
              {{ $lang.messages.supportZip }}
            </div>
          </el-upload>
        </el-tab-pane>
        <el-tab-pane :label="$lang.columns.clone" name="clone">
          <el-form>
            <el-form-item :label="$lang.columns.address" label-width="65px">
              <el-input
                v-model="gitAddress"
                class="inline"
                :placeholder="$lang.columns.address"
                size="small"
              >
              </el-input>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>

      <div slot="footer">
        <el-button @click="createProjectDialog = false" size="small"
          >{{ $lang.buttons.cancel }}
        </el-button>
        <el-button
          @click="onCreateProject()"
          v-if="activeDialogTab === 'create'"
          type="primary"
          size="small"
          >{{ $lang.buttons.create }}
        </el-button>
        <el-button
          @click="onUploadedProject()"
          v-if="activeDialogTab === 'upload'"
          type="primary"
          size="small"
          >{{ $lang.buttons.finish }}
        </el-button>
        <el-button
          @click="onCloneProject()"
          v-if="activeDialogTab === 'clone'"
          type="primary"
          size="small"
          >{{ $lang.buttons.clone }}
        </el-button>
      </div>
    </el-dialog>
    <panel-title :title="$lang.objects.project">
      <el-button @click.stop="onRefresh" size="mini">
        <i class="fa fa-refresh"></i>
        {{ $lang.buttons.refresh }}
      </el-button>
      <el-button type="primary" size="mini" @click="createProjectDialog = true">
        <i class="fa fa-plus"></i>
        {{ $lang.buttons.create }}
      </el-button>
    </panel-title>
    <div class="panel-body">
      <el-table
        :data="projects"
        :empty-text="$lang.messages.noData"
        v-loading="loading"
        :element-loading-text="$lang.messages.loading"
        :style="{ width: '100%;' }"
      >
        <el-table-column
          align="center"
          prop="name"
          :label="$lang.columns.name"
          width="150"
        >
        </el-table-column>
        <el-table-column
          align="center"
          :label="$lang.columns.configurable"
          width="150"
        >
          <template slot-scope="props" v-if="buildInfos[props.row.name]">
            <span v-if="buildInfos[props.row.name]['configurable']">
              <el-button
                type="primary"
                icon="el-icon-check"
                size="mini"
                round
              ></el-button>
            </span>
            <span v-else>
              <el-button
                type="primary"
                icon="el-icon-close"
                size="mini"
                round
              ></el-button>
            </span>
          </template>
        </el-table-column>
        <el-table-column align="center" :label="$lang.columns.built" width="80">
          <template slot-scope="props" v-if="buildInfos[props.row.name]">
            <span v-if="buildInfos[props.row.name]['egg']">
              <el-button
                type="primary"
                icon="el-icon-check"
                size="mini"
                round
              ></el-button>
            </span>
            <span v-else>
              <el-button
                type="primary"
                icon="el-icon-close"
                size="mini"
                round
              ></el-button>
            </span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          :label="$lang.columns.builtAt"
          width="200"
        >
          <template slot-scope="props">
            <span v-if="buildInfos[props.row.name]">
              {{ buildInfos[props.row.name]["built_at"] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          :label="$lang.columns.description"
          width="200"
        >
          <template slot-scope="props">
            <span v-if="buildInfos[props.row.name]">
              {{ buildInfos[props.row.name]["description"] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column align="center" :label="$lang.columns.operations">
          <template slot-scope="props">
            <router-link
              :to="{
                name: 'projectConfigure',
                params: { name: props.row.name },
              }"
              tag="span"
              v-if="
                buildInfos[props.row.name] &&
                  buildInfos[props.row.name]['configurable']
              "
            >
              <el-button type="warning" size="mini">
                <i class="fa fa-edit"></i>
                {{ $lang.buttons.configure }}
              </el-button>
            </router-link>
            <router-link
              :to="{ name: 'projectEdit', params: { name: props.row.name } }"
              tag="span"
              v-else
            >
              <el-button type="warning" size="mini">
                <i class="fa fa-edit"></i>
                {{ $lang.buttons.edit }}
              </el-button>
            </router-link>
            <router-link
              :to="{ name: 'projectDeploy', params: { name: props.row.name } }"
              tag="span"
            >
              <el-button type="success" size="mini">
                <i class="fa fa-cloud-upload"></i>
                {{ $lang.buttons.deploy }}
              </el-button>
            </router-link>
            <!--<router-link :to="{name: 'projectMonitor', params: {name: props.row.name}}" tag="span">-->
            <!--<el-button type="info" size="mini">-->
            <!--<i class="fa fa-podcast"></i>-->
            <!--监控-->
            <!--</el-button>-->
            <!--</router-link>-->
            <el-button
              type="danger"
              size="mini"
              @click="onSingleDelete(props.row.name)"
            >
              <i class="fa fa-remove"></i>
              {{ $lang.buttons.delete }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
import PanelTitle from "../../components/PanelTitle";

export default {
  name: "ProjectIndex",
  data() {
    return {
      activeDialogTab: "create",
      createProjectDialog: false,
      projectName: null,
      gitAddress: null,
      projects: [],
      loading: false,
      buildInfos: {},
    };
  },
  components: {
    PanelTitle,
  },
  created() {
    this.getProjectData();
  },
  methods: {
    getBuildInfo(name) {
      this.$http
        .get(
          this.formatString(this.$store.state.url.project.build, {
            name: name,
          })
        )
        .then(({ data: data }) => {
          this.$set(this.buildInfos, name, data);
        });
    },
    getProjectData() {
      this.loading = true;
      this.$http
        .get(this.$store.state.url.project.index)
        .then(({ data: projects }) => {
          this.projects = projects;
          this.loading = false;
          this.projects.forEach((project) => {
            this.getBuildInfo(project.name);
          });
        })
        .catch(() => {
          this.loading = false;
        });
    },
    onRefresh() {
      //this.$message.info(this.$store.getters.$lang.messages.loading)
      this.getProjectData();
    },
    onDeleteProject(name) {
      this.loading = true;
      this.$http
        .post(
          this.formatString(this.$store.state.url.project.remove, {
            name: name,
          })
        )
        .then(() => {
          this.$message.success(
            this.$store.getters.$lang.messages.successDelete
          );
          this.loading = false;
          this.getProjectData();
        })
        .catch(() => {
          this.loading = false;
          this.$message.error(this.$store.getters.$lang.messages.errorDelete);
        });
    },
    onSingleDelete(name) {
      this.$confirm(
        this.$store.getters.$lang.messages.confirm,
        this.$store.getters.$lang.buttons.confirm,
        {
          confirmButtonText: this.$store.getters.$lang.buttons.yes,
          cancelButtonText: this.$store.getters.$lang.buttons.no,
          type: "warning",
        }
      ).then(() => {
        this.onDeleteProject(name);
      });
    },
    onCloneProject() {
      this.$message.success(this.$store.getters.$lang.messages.cloning);
      this.$http
        .post(this.$store.state.url.project.clone, {
          address: this.gitAddress,
        })
        .then(() => {
          this.$message.success(
            this.$store.getters.$lang.messages.successClone
          );
          this.loading = false;
          this.createProjectDialog = false;
          this.onRefresh();
        })
        .catch(() => {
          this.loading = false;
          this.$message.error(this.$store.getters.$lang.messages.errorClone);
        });
    },
    onCreateProject() {
      this.$http
        .post(this.$store.state.url.project.create, {
          name: this.projectName,
        })
        .then(() => {
          this.$message.success(this.$store.getters.$lang.messages.successSave);
          this.loading = false;
          this.$router.push({
            name: "projectConfigure",
            params: { name: this.projectName },
          });
        })
        .catch(() => {
          this.loading = false;
          this.$message.error(this.$store.getters.$lang.messages.errorSave);
        });
    },
    onUploadedProject() {
      this.createProjectDialog = false;
      this.onRefresh();
    },
  },
};
</script>

<style lang="scss">
#project-index {
  .dialog {
    .el-dialog__body {
      padding-bottom: 0;
      padding-left: 40px;
      padding-right: 40px;
    }
  }
  .upload {
    width: 100%;
    .el-upload {
      width: 100%;
      .el-upload-dragger {
        width: 100%;
      }
    }
  }
}
</style>
