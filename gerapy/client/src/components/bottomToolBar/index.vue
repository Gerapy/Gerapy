<template>
  <div class="bottom-toolbar ofh">
    <el-row>
      <el-col :span="24">
        <div class="fl">
          <slot name="handler"></slot>
        </div>
        <div class="fr">
          <slot name="page"></slot>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
