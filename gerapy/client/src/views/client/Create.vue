<template>
  <div class="panel">
    <panel-title :title="$lang.titles.createClient"></panel-title>
    <div
      class="panel-body"
      v-loading="loadData"
      :element-loading-text="$lang.messages.loading"
    >
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <el-form-item :label="$lang.columns.name" prop="name">
              <el-input
                v-model="form.name"
                :placeholder="$lang.messages.enter + ' ' + $lang.columns.name"
                size="small"
              ></el-input>
            </el-form-item>

            <el-form-item :label="$lang.columns.ip" prop="ip">
              <el-input
                v-model="form.ip"
                :placeholder="$lang.messages.enter + ' ' + $lang.columns.ip"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item :label="$lang.columns.port" prop="port">
              <el-input
                v-model="form.port"
                :placeholder="$lang.messages.enter + ' ' + $lang.columns.port"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item :label="$lang.columns.auth" prop="auth">
              <el-switch v-model="form.auth"> </el-switch>
            </el-form-item>
            <el-form-item
              :label="$lang.columns.username"
              prop="username"
              v-if="form.auth"
            >
              <el-input
                v-model="form.username"
                :placeholder="
                  $lang.messages.enter + ' ' + $lang.columns.username
                "
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item
              :label="$lang.columns.password"
              prop="password"
              v-if="form.auth"
            >
              <el-input
                v-model="form.password"
                type="password"
                :placeholder="
                  $lang.messages.enter + ' ' + $lang.columns.password
                "
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                size="small"
                @click="onSubmitForm"
                :loading="onSubmitLoading"
              >
                <i class="fa fa-check"></i>
                {{ $lang.buttons.create }}
              </el-button>
              <el-button @click="$router.back()" size="small">
                <i class="fa fa-reply"></i>
                {{ $lang.buttons.return }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
import PanelTitle from "../../components/PanelTitle";
import { ip, port } from "../../utils/regex";

export default {
  data() {
    return {
      form: {
        name: "",
        ip: "",
        port: "",
        description: "",
        auth: false,
        username: "",
        password: "",
      },
      loadData: false,
      onSubmitLoading: false,
      rules: {
        name: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.name +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        ip: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.ip +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        port: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.port +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
          {
            pattern: port,
            message:
              this.$store.getters.$lang.columns.port +
              " " +
              this.$store.getters.$lang.messages.notValid,
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    onSubmitForm() {
      this.$refs.form.validate((valid) => {
        if (!valid) return false;
        this.onSubmitLoading = true;
        this.$http
          .post(this.$store.state.url.client.create, this.form)
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.messages.successSave
            );
            this.onSubmitLoading = false;
            this.$router.push({
              name: "clientIndex",
            });
          })
          .catch(() => {
            this.onSubmitLoading = false;
          });
      });
    },
  },
  components: {
    PanelTitle,
  },
};
</script>
