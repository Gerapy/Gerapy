<template>
  <div id="user">
    <el-dropdown size="mini" split-button type="primary">
      <span>{{ $store.getters.user }}</span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item
          ><span @click="onLogout">{{
            $lang.buttons.logout
          }}</span></el-dropdown-item
        >
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
export default {
  components: {},
  name: "User",
  methods: {
    onLogout() {
      this.$store.commit("clearToken");
      this.$router.push({ path: "/login" });
    },
  },
};
</script>

<style lang="scss">
#user {
  /*float: right;*/
  display: inline-block;
  margin-top: 15px;
  margin-right: 240px;
  cursor: pointer;
  .el-button {
    margin: 0 !important;
    border-right: none;
  }
}
</style>
