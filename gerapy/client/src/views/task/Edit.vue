<template>
  <div class="panel">
    <panel-title :title="$lang.titles.editTask">
      <router-link
        :to="{ name: 'taskStatus', params: { id: routeId } }"
        tag="span"
      >
        <el-button type="success" size="mini">
          <i class="fa fa-sitemap"></i>
          {{ $lang.buttons.status }}
        </el-button>
      </router-link>
    </panel-title>
    <div
      class="panel-body"
      v-loading="loadData"
      :element-loading-text="$lang.messages.loading"
    >
      <el-row>
        <el-col :span="10">
          <substance ref="substance" :id="routeId">
            <template slot="submit">
              <el-button
                type="primary"
                size="small"
                @click="onSubmitForm"
                :loading="onSubmitLoading"
              >
                <i class="fa fa-check"></i>
                {{ $lang.buttons.update }}
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
        this.onSubmitLoading = true;
        let formData = this.$refs.substance.formData;
        this.$http
          .post(
            this.formatString(this.$store.state.url.task.update, {
              id: this.routeId,
            }),
            formData
          )
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.messages.successSave
            );
            this.onSubmitLoading = false;
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
