<template>
  <div class="panel-title">
    <span v-if="title" v-text="title"></span>
    <div class="fr">
      <slot></slot>
    </div>
  </div>
</template>
<script>
export default {
  name: "PanelTitle",
  props: {
    title: {
      type: String,
    },
  },
};
</script>
