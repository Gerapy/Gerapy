<template>
  <div class="panel">
    <panel-title :title="$lang.titles.createTask"></panel-title>
    <div
      class="panel-body"
      v-loading="loadData"
      :element-loading-text="$lang.messages.loading"
    >
      <el-row>
        <el-col :span="10">
          <substance ref="substance">
            <template slot="submit">
              <el-button
                type="primary"
                size="small"
                @click="onSubmitForm"
                :loading="onSubmitLoading"
              >
                <i class="fa fa-check"></i>
                {{ $lang.buttons.create }}
              </el-button>
            </template>
          </substance>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script type="text/javascript">
import PanelTitle from "../../components/PanelTitle";
import Substance from "./Substance";

export default {
  data() {
    return {
      onSubmitLoading: false,
      loadData: false,
      routeId: this.$route.params.id,
    };
  },
  methods: {
    onSubmitForm() {
      this.$refs.substance.$refs.form.validate((valid) => {
        if (!valid) return false;
        let formData = this.$refs.substance.formData;
        this.onSubmitLoading = true;
        this.$http
          .post(this.$store.state.url.task.create, formData)
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.messages.successSave
            );
            this.onSubmitLoading = false;
            this.$router.push({
              name: "taskIndex",
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
    Substance,
  },
};
</script>
