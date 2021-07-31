<template>
  <div class="header-section">
    <div class="pull-right">
      <lang-switch></lang-switch>
      <user></user>
    </div>
  </div>
</template>
<script>
import User from "./User";
import LangSwitch from "./LangSwitch";

export default {
  components: {
    User,
    LangSwitch,
  },
};
</script>
