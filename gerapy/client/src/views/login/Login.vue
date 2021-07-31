<template>
  <div id="login">
    <el-form
      :rules="rules"
      label-width="100px"
      class="form"
      :model="form"
      ref="form"
    >
      <div class="title">
        <img src="../../assets/images/logo.png" alt="Gerapy" />
      </div>
      <el-form-item
        :label="$lang.columns.username"
        prop="username"
        class="item"
      >
        <el-input v-model="form.username" ref="username" autocomplete="off">
        </el-input>
      </el-form-item>
      <el-form-item
        :label="$lang.columns.password"
        prop="password"
        class="item"
      >
        <el-input
          :type="type.password"
          v-model="form.password"
          autocomplete="off"
          ref="password"
        >
        </el-input>
        <span class="display" @click="onShowPassword"
          ><span class="el-icon-view"></span
        ></span>
      </el-form-item>
      <el-form-item :label="null" class="submit">
        <el-button
          type="primary"
          class="btn btn-login"
          :loading="loading"
          @click.native.prevent="onLogin"
          >{{ $lang.buttons.login }}
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
export default {
  name: "Login",
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!value || value.length === 0) {
        callback(
          new Error(this.$store.getters.$lang.messages.pleaseInputUsername)
        );
      } else {
        callback();
      }
    };
    const validatePassword = (rule, value, callback) => {
      if (!value || value.length === 0) {
        callback(
          new Error(this.$store.getters.$lang.messages.pleaseInputPassword)
        );
      } else {
        callback();
      }
    };
    return {
      form: {
        username: null,
        password: null,
      },
      rules: {
        username: [
          { required: true, trigger: "blur", validator: validateUsername },
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword },
        ],
      },
      type: {
        password: "password",
      },
      loading: false,
    };
  },
  methods: {
    onShowPassword() {
      if (this.type.password === "password") {
        this.$set(this.type, "password", "");
      } else {
        this.$set(this.type, "password", "password");
      }
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    onLogin() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true;
          this.$http
            .post(this.$store.state.url.user.auth, this.form)
            .then(({ data: data }) => {
              let token = data.token;
              this.$store.commit("setToken", token);
              this.$store.commit("setUser", this.form.username);
              this.$router.push({ path: "/home" });
              this.loading = false;
            })
            .catch(() => {
              this.loading = false;
              this.$message.error(
                this.$store.getters.$lang.messages.loginError
              );
            });
        } else {
          return false;
        }
      });
    },
  },
};
</script>

<style lang="scss">
$background-color: #283443;
$width-form: 400px;
$width-label: 100px;
#login {
  height: 100%;
  width: 100%;
  background-color: $background-color;
  .form {
    width: $width-form;
    margin: auto;
    padding-top: 200px;
    .title {
      width: 100%;
      margin-bottom: 20px;
      text-align: center;
      image {
        width: 80%;
      }
    }
    .item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      .el-form-item__label::before {
        content: "";
      }
      .el-form-item__label {
        text-align: left;
        padding-left: 20px;
      }
      input {
        background: transparent;
        border: 0;
        -webkit-appearance: none;
        border-radius: 0;
        color: #eee;
        caret-color: #fff;
      }
      .el-form-item__error {
        left: -$width-label;
      }
      .display {
        position: absolute;
        right: 10px;
        color: #606266;
        cursor: pointer;
      }
    }
    .submit {
      margin-top: 5px;
      .el-form-item__content {
        margin-left: 0 !important;
      }
      .btn {
        &.btn-login {
          width: 100%;
        }
      }
    }
  }
}
</style>
