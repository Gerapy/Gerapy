<template>
  <div class="panel">
    <panel-title :title="$lang.objects.clients">
      <el-button @click="onRefresh" size="mini">
        <i class="fa fa-refresh"></i>
        {{ $lang.buttons.refresh }}
      </el-button>
      <router-link :to="{ name: 'clientCreate' }" tag="span">
        <el-button type="success" size="mini">
          <i class="fa fa-plus"></i>
          {{ $lang.buttons.create }}
        </el-button>
      </router-link>
    </panel-title>
    <div class="panel-body">
      <el-table
        :empty-text="$lang.messages.noData"
        :data="clients"
        v-loading="loading"
        :element-loading-text="$lang.messages.loading"
      >
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
          width="200"
        >
        </el-table-column>
        <el-table-column
          align="center"
          prop="fields.ip"
          :label="$lang.columns.ip"
          width="200"
        >
        </el-table-column>
        <el-table-column
          align="center"
          prop="fields.port"
          :label="$lang.columns.port"
        >
        </el-table-column>
        <el-table-column
          align="center"
          prop="fields.auth"
          width="80"
          :label="$lang.columns.auth"
        >
          <template slot-scope="props">
            <span v-if="props.row.fields.auth">
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
        <el-table-column align="center" :label="$lang.columns.operations">
          <template slot-scope="props">
            <router-link
              :to="{ name: 'clientEdit', params: { id: props.row.pk } }"
              tag="span"
            >
              <el-button type="info" size="mini">
                <i class="fa fa-edit"></i>
                {{ $lang.buttons.edit }}
              </el-button>
            </router-link>
            <router-link
              :to="{ name: 'clientSchedule', params: { id: props.row.pk } }"
              tag="span"
            >
              <el-button type="success" size="mini">
                <i class="fa fa-sitemap"></i>
                {{ $lang.buttons.schedule }}
              </el-button>
            </router-link>
            <el-button
              type="danger"
              size="mini"
              @click="onSingleDelete(props.row.pk)"
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
  name: "ClientIndex",
  props: {},
  data() {
    return {
      clients: null,
      loading: true,
      // to store batch selected id of client
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
    };
  },
  components: {
    PanelTitle,
  },
  created() {
    this.onGetClientData();
  },
  methods: {
    onRefresh() {
      this.onGetClientData();
    },
    onGetClientsStatus() {
      this.clients.forEach((client) => {
        this.onGetClientStatus(client.pk);
      });
    },
    onGetClientStatus(id) {
      this.$set(this.clientsStatus, id, 0);
      this.$http
        .get(
          this.formatString(this.$store.state.url.client.status, {
            id: id,
          })
        )
        .then(({ data: { result: result } }) => {
          this.$set(this.clientsStatus, id, result);
        })
        .catch(() => {
          this.$set(this.clientsStatus, id, -1);
        });
    },
    onGetClientData() {
      this.loading = true;
      this.$http
        .get(this.$store.state.url.client.index)
        .then(({ data: clients }) => {
          this.clients = clients;
          this.loading = false;
          this.onGetClientsStatus();
        })
        .catch(() => {
          this.loading = false;
        });
    },
    onDeleteClient(id) {
      this.$http
        .post(
          this.formatString(this.$store.state.url.client.remove, {
            id: id,
          })
        )
        .then(() => {
          this.$message.success(
            this.$store.getters.$lang.messages.successDelete
          );
          this.loading = false;
          this.onGetClientData();
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
        this.onDeleteClient(id);
      });
    },
  },
};
</script>
