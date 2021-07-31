<template>
  <div class="panel">
    <panel-title :title="$lang.objects.tasks">
      <router-link :to="{ name: 'taskCreate' }" tag="span">
        <el-button type="success" size="mini">
          <i class="fa fa-plus"></i>
          {{ $lang.buttons.create }}
        </el-button>
      </router-link>
    </panel-title>
    <div class="panel-body">
      <el-table
        :empty-text="$lang.messages.noData"
        :data="tasks"
        v-loading="loading"
        :element-loading-text="$lang.messages.loading"
      >
        <el-table-column
          align="center"
          prop="id"
          :label="$lang.columns.id"
          width="60"
        >
        </el-table-column>
        <el-table-column
          align="center"
          prop="name"
          :label="$lang.columns.name"
          width="200"
        >
        </el-table-column>
        <el-table-column
          align="center"
          prop="project"
          :label="$lang.columns.project"
          width="200"
        >
        </el-table-column>
        <el-table-column
          align="center"
          prop="spider"
          width="200"
          :label="$lang.columns.spider"
        >
        </el-table-column>
        <el-table-column align="center" :label="$lang.columns.operations">
          <template slot-scope="props">
            <router-link
              :to="{ name: 'taskStatus', params: { id: props.row.id } }"
              tag="span"
            >
              <el-button type="success" size="mini">
                <i class="fa fa-sitemap"></i>
                {{ $lang.buttons.status }}
              </el-button>
            </router-link>
            <router-link
              :to="{ name: 'taskEdit', params: { id: props.row.id } }"
              tag="span"
            >
              <el-button type="info" size="mini">
                <i class="fa fa-edit"></i>
                {{ $lang.buttons.edit }}
              </el-button>
            </router-link>
            <el-button
              type="danger"
              size="mini"
              @click="onSingleDelete(props.row.id)"
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
<script type="text/javascript">
import PanelTitle from "../../components/PanelTitle";

export default {
  data() {
    return {
      tasks: null,
      loading: true,
      statusText: {
        "1": this.$store.getters.$lang.buttons.normal,
        "0": this.$store.getters.$lang.buttons.connecting,
        "-1": this.$store.getters.$lang.buttons.error,
      },
    };
  },
  components: {
    PanelTitle,
  },
  created() {
    this.getTaskData();
  },
  methods: {
    onRefresh() {
      this.getTaskData();
    },
    changeFilter() {
      this.lastIds = {};
      this.getTaskData();
    },
    //获取数据
    getTaskData() {
      this.loading = true;
      this.$http
        .get(this.$store.state.url.task.index)
        .then(({ data: { data: tasks } }) => {
          this.tasks = tasks;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    deleteTask(id) {
      this.$http
        .post(
          this.formatString(this.$store.state.url.task.remove, {
            id: id,
          })
        )
        .then(() => {
          this.$message.success(
            this.$store.getters.$lang.messages.successDelete
          );
          this.loading = false;
          this.getTaskData();
        })
        .catch(() => {
          this.$message.error(this.$store.getters.$lang.messages.errorDelete);
          this.loading = false;
        });
    },
    onSingleDelete(id) {
      this.$confirm(
        this.$store.getters.$lang.messages.confirm,
        this.$store.getters.$lang.buttons.confirm,
        {
          confirmButtonText: this.$store.getters.$lang.buttons.yes,
          cancelButtonText: this.$store.getters.$lang.buttons.no,
          type: "warning",
        }
      ).then(() => {
        this.deleteTask(id);
      });
    },
  },
};
</script>
